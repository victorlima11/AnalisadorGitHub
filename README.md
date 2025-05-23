# Analisador de GitHub

![Demonstração da aplicação](assets/image.png)

O **Analisador de GitHub** é uma aplicação que utiliza inteligência artificial para analisar perfis do GitHub e fornecer insights personalizados sobre o perfil do usuário. Ele destaca pontos fortes, áreas de melhoria e sugere tecnologias e boas práticas para o desenvolvimento de carreira.

## Tecnologias Utilizadas

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construção de APIs rápidas e eficientes.
- **[Google Gemini AI](https://cloud.google.com/genai/)**: Para geração de análises detalhadas com inteligência artificial.
- **[Python](https://www.python.org/)**: Linguagem de programação principal.

### Frontend
- **[Next.js](https://nextjs.org/)**: Framework React para renderização do lado do servidor.
- **[Tailwind CSS](https://tailwindcss.com/)**: Para estilização rápida e responsiva.
- **[Framer Motion](https://www.framer.com/motion/)**: Para animações suaves.

### Outras Bibliotecas
- **Lucide Icons**: Para ícones modernos e personalizáveis.
- **Highlight.js**: Para destacar trechos de código no conteúdo gerado.

## Como Rodar o Projeto

### Pré-requisitos
- **Node.js** (v16 ou superior)
- **Python** (v3.10 ou superior)
- **Gerenciador de Pacotes**: `npm` ou `yarn`
- **Variáveis de Ambiente**: Configure um arquivo `.env` com as seguintes chaves:
  - `GEMINI_KEY`: Chave da API do Google Gemini.
  - `GITHUB_KEY`: Chave da API do GitHub.
  - `VERCEL_URL`: URL do frontend hospedado (opcional para CORS).

### Backend
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
3. Entre na pasta web:
    ```bash
    cd web
    npm install
    npm run dev
    ```

A aplicação permite que você insira o nome de usuário do GitHub e receba uma análise detalhada do perfil, incluindo:

Informações gerais (nome, localização, seguidores, etc.).
Pontos fortes e áreas de melhoria.
Sugestões de tecnologias e boas práticas.