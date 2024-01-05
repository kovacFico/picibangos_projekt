from core.config import settings
from db.database import Base
from db.database import engine
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from routers import account
from routers import event
from routers import home
from routers import login
from routers import register
from routers import team
from starlette.exceptions import HTTPException as StarletteHTTPException


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


app.include_router(account.router)
app.include_router(event.router)
app.include_router(home.router)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(team.router)


# zasada je ovo neki ofrlji exception handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


@app.get("/")
async def pocetna():
    return {"message": "Picibangos projekt by 2Ficcos"}
