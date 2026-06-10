"""Service `feedback` — collecte des annotations métier (SOLUTION M6-B2).

POST /feedback : un conseiller renvoie la **vraie** classe d'un dossier déjà
scoré (`request_id`). On valide que le `request_id` existe (jointure avec
`prod_scored.csv`), on stocke dans SQLite. Quand le volume atteint le seuil,
le job `retrain.py` (cron) réentraîne.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DATA = Path(__file__).parent.parent.parent.parent / "data"
DB_PATH = Path(os.environ.get("FEEDBACK_DB", DATA / "feedbacks.db"))


class Feedback(BaseModel):
    """Annotation métier sur un dossier déjà scoré."""

    request_id: str = Field(..., examples=["REQ-00042"])
    true_label: int = Field(..., ge=0, le=1, description="0 = remboursé, 1 = défaut")
    comments: str | None = None


def _init_db() -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS feedbacks (
                request_id TEXT PRIMARY KEY,
                true_label INTEGER NOT NULL,
                comments   TEXT,
                created_at TEXT NOT NULL
            )"""
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge les request_id valides + initialise la base au démarrage."""
    DB_PATH.parent.mkdir(exist_ok=True)
    _init_db()
    app.state.valid_ids = set(pd.read_csv(DATA / "prod_scored.csv")["request_id"])
    yield


app = FastAPI(title="Pyrenex Feedback Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/feedback/count")
async def count() -> dict[str, int]:
    """Nombre de feedbacks stockés (sert au trigger de réentraînement)."""
    with sqlite3.connect(DB_PATH) as con:
        n = con.execute("SELECT COUNT(*) FROM feedbacks").fetchone()[0]
    return {"count": int(n)}


@app.post("/feedback", status_code=status.HTTP_201_CREATED)
async def post_feedback(fb: Feedback) -> dict[str, str]:
    """Enregistre une annotation. Rejette un `request_id` inconnu (404)."""
    if fb.request_id not in app.state.valid_ids:
        raise HTTPException(status_code=404, detail=f"request_id inconnu : {fb.request_id}")
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT OR REPLACE INTO feedbacks VALUES (?, ?, ?, ?)",
            (fb.request_id, fb.true_label, fb.comments, datetime.now(timezone.utc).isoformat()),
        )
    return {"status": "stored", "request_id": fb.request_id}
