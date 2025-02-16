from api.endpoints import chat, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer is used to extract the token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "http://localhost",  # Add other origins as needed
    "http://localhost:3000",  # Example for a React frontend
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)  # Include the chat router
app.include_router(auth.router)  # Include the chat router
