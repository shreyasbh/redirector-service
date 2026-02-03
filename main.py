import sqlite3 

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse 
from datetime import datetime

app = FastAPI(title="Redirector Service")

@app.post("/short-urls")
def create_short_url(payload: dict):
    if not payload:
        raise HTTPException(status_code=400, detail="request body is required")


    source_url = payload.get("source_url")
    shortened_url = payload.get("shortened_url")
    if not source_url or not shortened_url:
        raise HTTPException(status_code=400, detail="source_url and shortened_url are required")
    if not (source_url.startswith("http://") or source_url.startswith("https://")):
        raise HTTPException(status_code=400, detail="invalid url format")
    
    exisiting = fetch_source_url(shortened_url)
    
    if exisiting:
        raise HTTPException(status_code=409, detail="shortened URL already exists")

    try:
        insert_short_url(shortened_url, source_url)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="shortened url already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {
        "shortened_url": shortened_url,
        "source_url": source_url,
        "creation_timestamp": datetime.utcnow().isoformat()
    }

@app.get("/{shortened_url}")
def redirect_short_url(shortened_url: str):
    try:
        source_url = fetch_source_url(shortened_url)
    except Exception:
        raise HTTPException(status=500, detail="Internal Server Error")
    if not source_url:
        raise HTTPException(status=404, detail="shortened url not found")
    return RedirectResponse(url=source_url)

def init_db():
    conn = sqlite3.connect("redirector.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS short_urls (
            shortened_url TEXT PRIMARY KEY,
            source_url TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

def insert_short_url(shortened_url: str, source_url: str):
    conn = sqlite3.connect("redirector.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO short_urls (shortened_url, source_url, created_at) VALUES (?,?,?)",
        (shortened_url, source_url, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()

def fetch_source_url(shortened_url: str):
    conn = sqlite3.connect("redirector.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT source_url FROM short_urls WHERE shortened_url = ?",
        (shortened_url,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None 



