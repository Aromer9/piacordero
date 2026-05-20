from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class PageViewEvent(BaseModel):
    type: Literal["page_view"]
    session_id: str
    page: str
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime


class ClickEvent(BaseModel):
    type: Literal["click"]
    session_id: str
    page: str
    element_label: Optional[str] = None
    element_tag: Optional[str] = None
    section: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    timestamp: datetime


class TimeOnPageEvent(BaseModel):
    type: Literal["time_on_page"]
    session_id: str
    page: str
    duration_ms: int
    timestamp: datetime


class ScrollDepthEvent(BaseModel):
    type: Literal["scroll_depth"]
    session_id: str
    page: str
    max_percent: float
    timestamp: datetime


from typing import Union
from pydantic import RootModel

AnalyticsEvent = Union[PageViewEvent, ClickEvent, TimeOnPageEvent, ScrollDepthEvent]


class AnalyticsEventList(BaseModel):
    events: list[AnalyticsEvent] = Field(default_factory=list)
