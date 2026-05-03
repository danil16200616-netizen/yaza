from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import engine
from app.models import user, ingredient, dish  # noqa: F401 — регистрация моделей
from app.database import Base
from app.routers import auth, ingredients, dishes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Платформа конструирования блюд",
    description="Расчёт калорийности, стоимости и доступности ингредиентов",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(dishes.router)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
