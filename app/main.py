from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword="KEYWORD", publisher="PUBLISHER", price=0, image="IMAGE")
    await mongodb.engine.save(book)
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Book Collector"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    print(q)
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Book Collector", "keyword": q}
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.close()
