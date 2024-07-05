from api.routes import (
    recoverys,
    users,
    cards,
    login,
    menus,
    suggests,
    dinings,
    qr_codes,
)
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import JSONResponse, HTMLResponse
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from api.schemas import sch_tokens as sch_token
from api.utils.auth import get_current_user
from starlette.requests import Request


app = FastAPI(
    title="Comtex",
    version="1.0.0",
)
""" 
docs_url=None,
redoc_url=None,
openapi_url=None, 
"""


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def get_route(current_user: sch_token.UserToken = Depends(get_current_user)):
    if current_user.id_user_type == 0:
        return {"Success": "True"}
    else:
        return {"WAIT!": "You should'nt be here"}


@app.get("/docs", response_class=HTMLResponse)
async def get_docs(
    current_user: sch_token.UserToken = Depends(get_current_user),
):
    if current_user.id_user_type == 0:
        return get_swagger_ui_html(openapi_url="api/openapi.json", title="docs")
    else:
        return {"WAIT!": "You should'nt be here"}


@app.get("/redoc", response_class=HTMLResponse)
async def get_redoc(
    current_user: sch_token.UserToken = Depends(get_current_user),
):
    if current_user.id_user_type == 0:
        return get_redoc_html(openapi_url="api/openapi.json", title="redoc")
    else:
        return {"WAIT!": "You should'nt be here"}


app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cards.router, prefix="/cards", tags=["cards"])
app.include_router(menus.router, prefix="/menus", tags=["menus"])
app.include_router(dinings.router, prefix="/dinings", tags=["dinings"])
app.include_router(suggests.router, prefix="/suggests", tags=["suggests"])
app.include_router(qr_codes.router, prefix="/qr_codes", tags=["qr_codes"])
app.include_router(recoverys.router, prefix="/recoverys", tags=["recoverys"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"Hey hey!": "We're calling FBI"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
