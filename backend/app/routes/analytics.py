from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.auth import require_admin
from app.config import get_db
from app.models.analytics import AnalyticsEvent, AnalyticsEventList

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/event", status_code=204)
async def ingest(body: AnalyticsEventList):
    """Recibe lotes de eventos del frontend y los persiste en MongoDB."""
    if not body.events:
        return
    db = get_db()
    docs = []
    for event in body.events:
        d = event.model_dump()
        # Convertir datetime a objeto Python para Motor
        if isinstance(d.get("timestamp"), datetime):
            pass  # Motor lo serializa correctamente
        docs.append(d)
    await db.analytics_events.insert_many(docs)


@router.get("/summary", dependencies=[Depends(require_admin)])
async def summary(days: Optional[int] = Query(30, ge=1, le=365)):
    """Resumen de métricas para el panel de admin."""
    db = get_db()
    since = datetime.now(timezone.utc) - timedelta(days=days)

    # Visitas por página
    page_views_pipeline = [
        {"$match": {"type": "page_view", "timestamp": {"$gte": since}}},
        {"$group": {"_id": "$page", "visits": {"$sum": 1}}},
        {"$sort": {"visits": -1}},
        {"$limit": 20},
    ]

    # Sesiones únicas
    unique_sessions_pipeline = [
        {"$match": {"type": "page_view", "timestamp": {"$gte": since}}},
        {"$group": {"_id": "$session_id"}},
        {"$count": "total"},
    ]

    # Clics más frecuentes
    top_clicks_pipeline = [
        {"$match": {"type": "click", "timestamp": {"$gte": since}}},
        {
            "$group": {
                "_id": {
                    "page": "$page",
                    "label": "$element_label",
                    "tag": "$element_tag",
                    "section": "$section",
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 20},
    ]

    # Tiempo promedio en cada página (en segundos)
    avg_time_pipeline = [
        {"$match": {"type": "time_on_page", "timestamp": {"$gte": since}}},
        {
            "$group": {
                "_id": "$page",
                "avg_ms": {"$avg": "$duration_ms"},
                "sessions": {"$sum": 1},
            }
        },
        {"$sort": {"sessions": -1}},
        {"$limit": 20},
    ]

    # Profundidad de scroll promedio
    scroll_pipeline = [
        {"$match": {"type": "scroll_depth", "timestamp": {"$gte": since}}},
        {
            "$group": {
                "_id": "$page",
                "avg_scroll": {"$avg": "$max_percent"},
                "sessions": {"$sum": 1},
            }
        },
        {"$sort": {"sessions": -1}},
        {"$limit": 20},
    ]

    # Visitas por día (últimos N días)
    daily_pipeline = [
        {"$match": {"type": "page_view", "timestamp": {"$gte": since}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}
                },
                "visits": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    page_views = await db.analytics_events.aggregate(page_views_pipeline).to_list(20)
    unique_sessions_result = await db.analytics_events.aggregate(unique_sessions_pipeline).to_list(1)
    top_clicks = await db.analytics_events.aggregate(top_clicks_pipeline).to_list(20)
    avg_time = await db.analytics_events.aggregate(avg_time_pipeline).to_list(20)
    scroll_depth = await db.analytics_events.aggregate(scroll_pipeline).to_list(20)
    daily = await db.analytics_events.aggregate(daily_pipeline).to_list(365)

    return {
        "period_days": days,
        "unique_sessions": unique_sessions_result[0]["total"] if unique_sessions_result else 0,
        "page_views": [{"page": r["_id"], "visits": r["visits"]} for r in page_views],
        "top_clicks": [
            {
                "page": r["_id"]["page"],
                "label": r["_id"].get("label"),
                "tag": r["_id"].get("tag"),
                "section": r["_id"].get("section"),
                "count": r["count"],
            }
            for r in top_clicks
        ],
        "avg_time_on_page": [
            {
                "page": r["_id"],
                "avg_seconds": round(r["avg_ms"] / 1000, 1),
                "sessions": r["sessions"],
            }
            for r in avg_time
        ],
        "scroll_depth": [
            {
                "page": r["_id"],
                "avg_scroll_percent": round(r["avg_scroll"], 1),
                "sessions": r["sessions"],
            }
            for r in scroll_depth
        ],
        "daily_visits": [{"date": r["_id"], "visits": r["visits"]} for r in daily],
    }
