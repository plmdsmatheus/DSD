from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Roteador para a API Sorte
sorte_api_router = APIRouter()
sorte_api_router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Redireciona a documentação para a nova rota
@app.get("/api/sorte/docs", response_class=HTMLResponse)
async def sorte_docs():
    # Obtém o HTML da documentação gerada automaticamente
    swagger_ui_html = get_swagger_ui_html(openapi_url="http://localhost:8002/docs", title="API Sorte")

    # Retorna o HTML com a nova URL do OpenAPI
    return HTMLResponse(content=swagger_ui_html.body)


# Roteador para a API Social
social_api_router = APIRouter()
social_api_router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Rota de redirecionamento para a documentação da API FastAPI
@app.get("/api/social/docs", response_class=HTMLResponse)
async def redirect_to_docs():
    # URL da documentação da API FastAPI
    fastapi_docs_url = 'https://bug-free-broccoli-p6xx46x7jgrc6v7j-8000.app.github.dev/docs'

    # Redireciona para a rota de documentação da API FastAPI
    return RedirectResponse(url=fastapi_docs_url, status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
