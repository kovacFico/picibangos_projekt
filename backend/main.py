import logging

from core.config import settings
from db.database import Base
from db.database import engine
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import account
from routers import event
from routers import friends
from routers import home
from routers import login
from routers import register
from routers import team


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

logger = logging.getLogger(__name__)

app.include_router(account.router)
app.include_router(event.router)
app.include_router(home.router)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(team.router)
app.include_router(friends.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: Exception):
    exception_msg = f"Unsuccessful request due to error: {exc}".replace(
        "\n", " "
    ).replace("  ", " ")
    logging.error(exception_msg)
    content = {"message": exception_msg}

    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
