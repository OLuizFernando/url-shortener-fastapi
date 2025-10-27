from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import Union
from pydantic import BaseModel
from datetime import datetime, timedelta

import infra.database as db

app = FastAPI()


class Link(BaseModel):
    url: str
    slug: Union[str, None] = None


@app.get("/")
def read_root():
    return RedirectResponse("/docs")


@app.post("/", status_code=201)
def insert_link(link: Link):
    expires_at = datetime.now() + timedelta(days=30)

    results = db.execute("""
        INSERT INTO links (url, slug, expires_at)
        VALUES (%s, %s, %s)
        RETURNING *
    """, link.url, link.slug, expires_at, fetch=True)

    return results[0]


@app.get("/{link_slug}")
def read_item(link_slug: str):
    results = db.execute("""
        SELECT id, url
        FROM links
        WHERE slug = %s
        AND (
            expires_at > NOW()
            OR expires_at IS NULL
        )
    """, link_slug, fetch=True)

    db.execute("""
        UPDATE links
        SET clicks = clicks + 1
        WHERE id = %s
    """, results[0]["id"])

    return RedirectResponse(results[0]["url"])