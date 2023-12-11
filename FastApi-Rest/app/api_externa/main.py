from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/conselho")
async def get_advice():
    # URL da API externa
    api_url = "https://api.adviceslip.com/advice"

    # Fazendo a requisição à API externa usando httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)

    # Verifica se a requisição foi bem-sucedida (status code 200)
    if response.status_code == 200:
        # Extrai o conselho da resposta JSON
        advice = response.json()["slip"]["advice"]
        return {"advice": advice}
    else:
        # Se a requisição falhar, retorna uma mensagem de erro
        return {"error": "Failed to fetch advice from the external API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)