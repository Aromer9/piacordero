"""
Script de seed para poblar la base de datos con datos iniciales.
Ejecutar con: python -m app.seed
"""
import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings


PRODUCTS = [
    {
        "name": "Torta Frambuesas",
        "description": "Bizcocho de vainilla con crema diplomática, frambuesas frescas y merengue suizo",
        "category": "tortas",
        "image_url": "/images/torta-frambuesas.jpg",
        "featured": True,
        "order": 1,
        "price": 32000,
        "price_15p": 32000,
        "price_20p": 42000,
        "price_30p": 56000,
        "badge": "Favorita",
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Torta Naranja & Lavanda",
        "description": "Naked cake de especias con crema de naranja, merengues y naranjas deshidratadas",
        "category": "tortas",
        "image_url": "/images/torta-naranja-lavanda.jpg",
        "featured": True,
        "order": 2,
        "price": 36000,
        "price_15p": 36000,
        "price_20p": 48000,
        "price_30p": 62000,
        "badge": None,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Torta Frutos Rojos",
        "description": "Crema chantilly con frutillas, moras, arándanos y frambuesas frescas de temporada",
        "category": "tortas",
        "image_url": "/images/torta-frutos-rojos.jpg",
        "featured": True,
        "order": 3,
        "price": 32000,
        "badge": None,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Pavlova de Frambuesas",
        "description": "Merengue crujiente por fuera y suave por dentro, cubierto con frambuesas frescas y menta",
        "category": "temporada",
        "image_url": "/images/pavlova-frambuesas.jpg",
        "featured": True,
        "order": 4,
        "price": 28000,
        "badge": "Temporada",
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Torta Limón & Arándanos",
        "description": "Crema de limón con decoración en espiral, arándanos frescos y flores comestibles",
        "category": "tartas",
        "image_url": "/images/torta-limon-top.jpg",
        "featured": False,
        "order": 5,
        "price": 18000,
        "price_2_3p": 18000,
        "price_8_10p": 24000,
        "price_15p": 30000,
        "badge": None,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Torta Espiral de Limón",
        "description": "Crema de vainilla con espiral artesanal, arándanos, limón y flores silvestres",
        "category": "tartas",
        "image_url": "/images/torta-espiral-top.jpg",
        "featured": False,
        "order": 6,
        "price": 16000,
        "price_2_3p": 16000,
        "price_8_10p": 22000,
        "price_15p": 28000,
        "badge": None,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Naked Cake Naranja",
        "description": "Naked cake de especias con naranjas deshidratadas, almendras y flores de lavanda",
        "category": "tortas",
        "image_url": "/images/naked-cake-naranja.jpg",
        "featured": False,
        "order": 7,
        "price": 36000,
        "badge": None,
        "created_at": datetime.now(timezone.utc),
    },
    {
        "name": "Torta Naranja desde Arriba",
        "description": "Torta festiva con merengues, naranjas caramelizadas, lavanda y almendras tostadas",
        "category": "tortas",
        "image_url": "/images/torta-naranja-top.jpg",
        "featured": False,
        "order": 8,
        "price": 34000,
        "badge": None,
        "created_at": datetime.now(timezone.utc),
    },
]

SITE_CONTENT = [
    {
        "section": "hero",
        "content": {
            "tagline": "Pasteles que cuentan una historia",
            "tagline_italic": "historia",
            "subtitle": "Tortas artesanales, pasteles y dulces únicos hechos con los mejores ingredientes. Cada creación es diseñada especialmente para ti.",
            "image_main": "/images/torta-frambuesas.jpg",
            "image_2": "/images/torta-frutos-rojos.jpg",
            "image_3": "/images/torta-naranja-top.jpg",
            "featured_label": "Torta del mes",
            "featured_desc": "Frambuesa & vainilla",
            "eyebrow": "Hecho con amor en Chile",
        },
    },
    {
        "section": "about",
        "content": {
            "title": "Hola, soy Pía",
            "paragraphs": [
                "Creadora de los pasteles que hago con tanto amor. Hace ya varios años estudié Gastronomía y, después de practicar en restaurantes y hacer cursos de muchas cosas diferentes, me di cuenta que lo mío era hacer pasteles, cosas dulces y hacer felices a mi familia y mis amigos.",
                "En todo este tiempo conocí gente hermosa, profesores que admiro muchísimo y colegas que son talentosísimas.",
                "Ahora que decidí emprender, estoy feliz de hacer lo que amo y que se vea reflejado en cada detalle que hago para ustedes.",
            ],
            "signature": "Pía",
            "since_year": "2015",
            "image_main": "/images/naked-cake-naranja.jpg",
            "image_2": "/images/torta-espiral-top.jpg",
        },
    },
    {
        "section": "process",
        "content": {
            "steps": [
                {
                    "title": "Conversamos",
                    "description": "Me contás tu idea, la ocasión especial y tus sabores favoritos. Juntas diseñamos algo único para ti.",
                },
                {
                    "title": "Creamos",
                    "description": "Selecciono los mejores ingredientes de temporada y elaboro tu pedido con todo el cuidado artesanal.",
                },
                {
                    "title": "Celebramos",
                    "description": "Tu creación llega lista para hacer de tu momento algo verdaderamente memorable.",
                },
            ]
        },
    },
    {
        "section": "contact",
        "content": {
            "phone": "+56 9 8964 6783",
            "email": "hola@piacordero.cl",
            "instagram": "@piacordero_pasteleria",
            "whatsapp_number": "56989646783",
            "whatsapp_message": "Hola Pía! Me gustaría encargar un pedido especial 🎂",
            "location": "Santiago, Chile",
        },
    },
]


async def seed():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]

    print("Limpiando colecciones existentes...")
    await db.products.delete_many({})
    await db.site_content.delete_many({})

    print(f"Insertando {len(PRODUCTS)} productos...")
    await db.products.insert_many(PRODUCTS)

    print(f"Insertando {len(SITE_CONTENT)} secciones de contenido...")
    await db.site_content.insert_many(SITE_CONTENT)

    print("Creando índices...")
    await db.products.create_index("category")
    await db.products.create_index("featured")
    await db.products.create_index("order")
    await db.site_content.create_index("section", unique=True)

    client.close()
    print("Seed completado exitosamente.")


if __name__ == "__main__":
    asyncio.run(seed())
