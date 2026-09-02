from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GITHUB_API_KEY = os.getenv("GITHUB_KEY")
VERCEL_URL = os.getenv("VERCEL_URL")
client = genai.Client(api_key=GEMINI_API_KEY)


AnalisadorParametro = (
    """
    Você é uma inteligência artificial especializada em desenvolvimento de software, análise de perfis técnicos e boas práticas de programação. 

    Receberá os dados públicos do GitHub de um usuário, incluindo:
    - Informações do perfil (nome, bio, localização, etc.)
    - Lista de repositórios públicos
    - Linguagens utilizadas
    - Descrições dos projetos
    - Estrutura e conteúdo relevante dos arquivos

    Sua tarefa é analisar esse perfil e gerar um texto que contenha:
    1. Uma visão geral do perfil
    2. Pontos fortes observados
    3. Pontos que podem ser melhorados
    4. Sugestões de tecnologias novas ou complementares para aprender, com base no que o usuário já utiliza
    5. Outras dicas relevantes e realistas para ajudar no desenvolvimento da carreira ou projetos
    6. Análise de repositórios de destaque (opcional, se houver)

    Regras importantes:
    - NÃO invente informações. Baseie-se apenas nos dados fornecidos.
    - NÃO gere projetos, repositórios ou fatos que não existem.
    - NÃO crie listas genéricas que não tenham relação com o perfil analisado.
    - Faça sugestões coerentes e personalizadas, com base nas tecnologias já utilizadas e no contexto dos repositórios.
    - Mantenha um tom amigável e construtivo.
    - Foque em ajudar o usuário a evoluir, destacando boas práticas e incentivando melhorias reais.
    """
)

app = FastAPI()

# VERCEL_URL pode nao estar definida em dev; None quebra a validacao do CORS.
origins = [
    origin
    for origin in ["http://localhost:3000", "http://127.0.0.1:3000", VERCEL_URL]
    if origin
]

# Regra de nomes de usuario do GitHub: alfanumericos e hifens (nao no inicio/fim),
# ate 39 caracteres. Impede que o path seja usado para montar outra URL da API.
USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")

REQUEST_TIMEOUT = 10

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{username}")
def getGithubUser(username: str):

    if not USERNAME_RE.match(username):
        return JSONResponse(
            content={"erro": "Usuario invalido."},
            status_code=400,
        )

    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_API_KEY:
        headers["Authorization"] = f"Bearer {GITHUB_API_KEY}"

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

    url_repos = f"https://api.github.com/users/{username}/repos"
    response_repos = requests.get(url_repos, headers=headers, timeout=REQUEST_TIMEOUT)


    if response.status_code != 200:
        return JSONResponse(
            content={"erro": "Usuário não encontrado."},
            status_code=404,
        )
    

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
    Repositórios: {response_repos.json()}
    """

    gemini_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=AnalisadorParametro + "\n\n" + prompt,
    )

    respostaFiltrada["resposta"] = gemini_response.text
    return respostaFiltrada
