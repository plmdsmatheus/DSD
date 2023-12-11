from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Configurar o middleware CORS para o aplicativo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Roteador para a API Sorte
sorte_api_router = APIRouter()

async def fetch_advice():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8002/conselho')
        return response.json()

@sorte_api_router.get("/conselho", response_class=JSONResponse)
async def get_advice():
    try:
        advice = await fetch_advice()
        return advice
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Erro ao receber o conselho")

# Inclui o roteador da API Sorte no aplicativo principal
app.include_router(sorte_api_router, prefix="/api/sorte")


# Roteador para a API Social
social_api_router = APIRouter()

# Social ----------------
async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/users')
        return response.json()

@social_api_router.get("/users", response_class=JSONResponse)
async def get_users():
    try:
        users = await fetch_users()
        return users
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error ao receber os usuarios")

app.include_router(social_api_router, prefix="/api/social")

async def fetch_posts():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/posts')
        return response.json()

@social_api_router.get("/posts", response_class=JSONResponse)
async def get_posts():
    try:
        posts = await fetch_posts()
        return posts
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Erro ao receber os posts")
    
app.include_router(social_api_router, prefix="/api/social")

async def fetch_likes():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/likes')
        return response.json()

@social_api_router.get("/likes", response_class=JSONResponse)
async def get_likes():
    try:
        likes = await fetch_likes()
        return likes
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Erro ao receber os likes")
    
app.include_router(social_api_router, prefix="/api/social")

async def fetch_messages():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/api/messages')
        return response.json()

@social_api_router.get("/messages", response_class=JSONResponse)
async def get_messages():
    try:
        messages = await fetch_messages()
        return messages
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Erro ao receber as mensagens")

# Inclui o roteador no aplicativo principal
app.include_router(social_api_router, prefix="/api/social")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)