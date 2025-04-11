from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

AnalisadorParametro = (
    "Você é um analisador de perfil do github. "
    "Você vai fazer um relatório sobre o perfil com base nas informações fornecidas. "
    "Diga ao usuário os pontos fortes e fracos, o que está bom e o que precisa melhorar nos repositórios. "
    "Não invente nada. Use apenas os dados fornecidos."
)

app = FastAPI()

@app.get("/{username}")
def getGithubUser(username: str):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"erro": "Usuário não encontrado."}

    respostaFiltrada = {
        "nome": response.json().get("name"),
        "imagem": response.json().get("avatar_url"),
        "localizacao": response.json().get("location"),
        "seguidores": response.json().get("followers"),
        "repositorios": response.json().get("public_repos"),
        "data_criacao": response.json().get("created_at"),
        "bio": response.json().get("bio"),
    }

    prompt = f"""
    Nome: {respostaFiltrada['nome']}
    Localização: {respostaFiltrada['localizacao']}
    Seguidores: {respostaFiltrada['seguidores']}
    Repositórios Públicos: {respostaFiltrada['repositorios']}
    Data de Criação: {respostaFiltrada['data_criacao']}
    Bio: {respostaFiltrada['bio']}
    """

    gemini_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=AnalisadorParametro + "\n\n" + prompt,
    )

    respostaFiltrada["resposta"] = gemini_response.text
    return respostaFiltrada
