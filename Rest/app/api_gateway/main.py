from fastapi import FastAPI, HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Roteador para a API Social
social_api_router = APIRouter()

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

# Rota de redirecionamento para a documentação da API FastAPI
@app.get("/api/social/docs", response_class=JSONResponse)
async def redirect_to_docs():
    # Redireciona para a rota de documentação da API FastAPI
    return {"message": "Redirecting to FastAPI docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
