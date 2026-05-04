from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import engine
from app.models import user, ingredient, dish, cooking, diet  # noqa: F401
from app.database import Base
from app.routers import auth, ingredients, dishes, diet as diet_router
from app.routers import cooking as cooking_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YaZa — Платформа конструирования блюд",
    description="Расчёт КБЖУ с учётом термической обработки",
    version="2.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(dishes.router)
app.include_router(cooking_router.router)
app.include_router(diet_router.router)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
