from api.routes import users, cards, login, menus, suggests, dinings, qr_codes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI

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
def get_route():
    return {"Success": "True"}


app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(cards.router, prefix="/cards", tags=["cards"])
app.include_router(menus.router, prefix="/menus", tags=["menus"])
app.include_router(dinings.router, prefix="/dinings", tags=["dinings"])
app.include_router(suggests.router, prefix="/suggests", tags=["suggests"])
app.include_router(qr_codes.router, prefix="/qr_codes", tags=["qr_codes"])
