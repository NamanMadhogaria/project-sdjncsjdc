from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.seed import seed_demo_data
from app.db.session import Base, SessionLocal, engine
from app.services.mqtt_consumer import start_mqtt_consumer

app = FastAPI(title="GPS Vehicle Tracking API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()
    start_mqtt_consumer()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
