from api.routes import users, cards, login, menus, suggests, dinings, qr_codes
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from api.schemas import sch_tokens as sch_token
from starlette.responses import JSONResponse
from api.utils.auth import get_current_user
from starlette.requests import Request


app = FastAPI(title="Comtex", version="1.0.0")

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


app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cards.router, prefix="/cards", tags=["cards"])
app.include_router(menus.router, prefix="/menus", tags=["menus"])
app.include_router(dinings.router, prefix="/dinings", tags=["dinings"])
app.include_router(suggests.router, prefix="/suggests", tags=["suggests"])
app.include_router(qr_codes.router, prefix="/qr_codes", tags=["qr_codes"])


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
