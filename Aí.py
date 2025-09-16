from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
import json
import uvicorn

# Get API key from environment (will be set via secrets)
# os.environ["GROQ_API_KEY"] should be set via Replit secrets

# Import all the AI agent components from your original code
from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import BaseModel, Field
from groq import Groq
from langchain.agents import Tool
from datetime import datetime
from googlesearch import search
from fpdf import FPDF
import subprocess
import sys
import requests
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

# GroqLLM class from your original code
class GroqLLM(LLM, BaseModel):
    api_key: str = Field(...)
    model_name: str = Field(default="llama-3.3-70b-versatile")
    client: Optional[Groq] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.client = Groq(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager=None, **kwargs) -> str:
        if self.client is None:
            self.client = Groq(api_key=self.api_key)
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name
        )
        return response.choices[0].message.content or ""

# All your tool functions
def calculadora(expr: str) -> str:
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Erro: {e}"

def buscador(query: str) -> str:
    try:
        resultados = list(search(query, num_results=5))
        if resultados:
            return "\n".join([str(r) for r in resultados])
        else:
            return "Nenhum resultado encontrado."
    except Exception as e:
        return f"Erro ao buscar: {e}"

def data_hoje(_: str) -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def criar_arquivo(dados: str) -> str:
    try:
        with open("arquivo_gerado.txt", "w", encoding="utf-8") as f:
            f.write(dados)
        return "Arquivo 'arquivo_gerado.txt' criado com sucesso."
    except Exception as e:
        return f"Erro ao criar arquivo: {e}"

def ler_arquivo(_: str) -> str:
    try:
        with open("arquivo_gerado.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"

def criar_pdf(texto: str) -> str:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, texto)
        pdf.output("arquivo_gerado.pdf")
        return "PDF 'arquivo_gerado.pdf' criado com sucesso."
    except Exception as e:
        return f"Erro ao criar PDF: {e}"

def executar_codigo_proativo(codigo: str) -> str:
    try:
        local_vars = {}
        try:
            exec(codigo, {}, local_vars)
        except ModuleNotFoundError as e:
            lib = str(e).split("'")[1]
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            exec(codigo, {}, local_vars)
        return str(local_vars) if local_vars else "Código executado."
    except Exception as e:
        return f"Erro ao executar código: {e}"

def getProductInSkyVenda(termo="Casa", offset=1, limit=10) -> str:
    base_url = "https://skyvendas-production.up.railway.app/produtos/pesquisa/"
    headers = {"accept": "application/json"}

    def requisitar(query):
        url = f"{base_url}?termo={query}&offset={offset}&limit={limit}"
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    try:
        data = requisitar(termo)

        produtos = None
        if isinstance(data, dict):
            if "results" in data:
                produtos = data["results"]
            elif "items" in data:
                produtos = data["items"]
        elif isinstance(data, list):
            produtos = data

        if not produtos:
            alternativas = [termo.lower(), termo.capitalize(), termo + "s"]
            for alt in alternativas:
                if alt != termo:
                    try:
                        data = requisitar(alt)
                        if isinstance(data, dict):
                            if "results" in data:
                                produtos = data["results"]
                            elif "items" in data:
                                produtos = data["items"]
                        elif isinstance(data, list):
                            produtos = data
                        if produtos:
                            termo = alt
                            break
                    except:
                        continue

        if not produtos:
            try:
                links = list(search(f"comprar {termo}", num_results=5))
                if links:
                    return f"Não encontrei no SkyVenda. Veja opções no Google:\n" + "\n".join([str(link) for link in links])
            except:
                pass
            return f"Nenhum produto encontrado nem no SkyVenda nem no Google para '{termo}'."

        lista_simplificada = []
        for p in produtos:
            lista_simplificada.append(
                f"📌 {p.get('title', 'Sem título')} | 💵 {p.get('price', 'Sem preço')} | 📍 {p.get('province', '')} {p.get('district', '')}".strip()
            )

        texto = "\n".join(lista_simplificada)

        if len(texto) > 800:
            return f"Resultados resumidos:\n- Mostrando {len(produtos)} itens relacionados a '{termo}'."
        return texto

    except Exception as e:
        return f"Erro ao buscar produtos: {e}"

# Create tools
tools = [
    Tool(name="Calculadora", func=calculadora, description="Resolve expressões matemáticas"),
    Tool(name="Buscador", func=buscador, description="Pesquisa algo na web"),
    Tool(name="DataHoje", func=data_hoje, description="Mostra a data e hora atual"),
    Tool(name="ExecutarCodigoProativo", func=executar_codigo_proativo, description="Executa qualquer código Python gerado"),
    Tool(name="CriarArquivo", func=criar_arquivo, description="Cria arquivo de texto"),
    Tool(name="LerArquivo", func=ler_arquivo, description="Lê arquivo de texto"),
    Tool(name="CriarPDF", func=criar_pdf, description="Cria PDF com o conteúdo fornecido"),
    Tool(name="SkyVenda", func=getProductInSkyVenda, description="Busca produtos no SkyVenda por nome (com fallback)")
]

# Initialize the agent
memory = ConversationBufferMemory(memory_key="chat_history")
llm = GroqLLM(api_key=os.environ.get("GROQ_API_KEY"))
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# FastAPI app setup
app = FastAPI(title="Gena AI Agent", description="AI Agent with FastAPI and HTML interface")

# Request model
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Get response from the agent
        response = agent.invoke({"input": request.message})
        
        # Handle different response types
        if isinstance(response, dict):
            response_text = response.get('output', str(response))
        else:
            response_text = str(response)
        
        # Limit response length for web display
        if len(response_text) > 2000:
            response_text = response_text[:1800] + "\n\n[🔽 Resposta resumida: texto muito longo]"
            
        return ChatResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no agente: {str(e)}")

# File download endpoints
@app.get("/download/txt")
async def download_txt():
    try:
        return FileResponse("arquivo_gerado.txt", filename="arquivo_gerado.txt")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

@app.get("/download/pdf")
async def download_pdf():
    try:
        return FileResponse("arquivo_gerado.pdf", filename="arquivo_gerado.pdf")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF não encontrado")

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Gena AI Agent está funcionando!"}

# Root endpoint - serve HTML interface
@app.get("/", response_class=HTMLResponse)
async def serve_interface():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gena AI Agent</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                width: 90%;
                max-width: 800px;
                height: 90vh;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 20px 20px 0 0;
            }
            
            .header h1 {
                font-size: 1.8rem;
                margin-bottom: 5px;
            }
            
            .header p {
                opacity: 0.9;
                font-size: 0.9rem;
            }
            
            .chat-container {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
            }
            
            .message {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 18px;
                max-width: 80%;
                word-wrap: break-word;
            }
            
            .user-message {
                background: #007bff;
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 4px;
            }
            
            .bot-message {
                background: white;
                border: 1px solid #e9ecef;
                margin-right: auto;
                border-bottom-left-radius: 4px;
            }
            
            .input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e9ecef;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .input-container input {
                flex: 1;
                padding: 12px 16px;
                border: 1px solid #ddd;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            
            .input-container input:focus {
                border-color: #007bff;
            }
            
            .send-btn {
                padding: 12px 20px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
                transition: background 0.3s;
            }
            
            .send-btn:hover {
                background: #0056b3;
            }
            
            .send-btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 10px;
                color: #666;
            }
            
            .file-links {
                margin-top: 10px;
            }
            
            .file-links a {
                display: inline-block;
                padding: 5px 10px;
                background: #28a745;
                color: white;
                text-decoration: none;
                border-radius: 15px;
                font-size: 0.8rem;
                margin-right: 5px;
            }
            
            .file-links a:hover {
                background: #1e7e34;
            }
            
            pre {
                background: #f1f1f1;
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0;
                overflow-x: auto;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Gena AI Agent</h1>
                <p>Seu assistente inteligente com múltiplas ferramentas</p>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    <strong>Gena:</strong> Olá! Eu sou a Gena, sua assistente AI! Posso ajudar com:<br>
                    • 🧮 Cálculos matemáticos<br>
                    • 🔍 Pesquisas na web<br>
                    • 📄 Criar arquivos e PDFs<br>
                    • 🛒 Buscar produtos no SkyVenda<br>
                    • 🐍 Executar código Python<br>
                    • ⏰ Informações de data/hora<br><br>
                    Como posso ajudá-lo hoje?
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div>🤖 Gena está pensando...</div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Digite sua mensagem..." />
                <button id="sendBtn" class="send-btn">Enviar</button>
            </div>
        </div>

        <script>
            const chatContainer = document.getElementById('chatContainer');
            const messageInput = document.getElementById('messageInput');
            const sendBtn = document.getElementById('sendBtn');
            const loading = document.getElementById('loading');
            
            function addMessage(content, isUser = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                
                if (isUser) {
                    messageDiv.innerHTML = `<strong>Você:</strong> ${content}`;
                } else {
                    let formattedContent = content.replace(/\\n/g, '<br>');
                    messageDiv.innerHTML = `<strong>Gena:</strong> ${formattedContent}`;
                    
                    // Add download links if files were created
                    if (content.includes('arquivo_gerado.txt') || content.includes('arquivo_gerado.pdf')) {
                        const fileLinks = document.createElement('div');
                        fileLinks.className = 'file-links';
                        
                        if (content.includes('arquivo_gerado.txt')) {
                            fileLinks.innerHTML += '<a href="/download/txt" target="_blank">📄 Baixar TXT</a>';
                        }
                        if (content.includes('arquivo_gerado.pdf')) {
                            fileLinks.innerHTML += '<a href="/download/pdf" target="_blank">📑 Baixar PDF</a>';
                        }
                        
                        messageDiv.appendChild(fileLinks);
                    }
                }
                
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;
                
                // Add user message
                addMessage(message, true);
                messageInput.value = '';
                
                // Show loading
                sendBtn.disabled = true;
                sendBtn.textContent = 'Enviando...';
                loading.style.display = 'block';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        addMessage(data.response);
                    } else {
                        addMessage('Desculpe, ocorreu um erro. Tente novamente.');
                    }
                } catch (error) {
                    addMessage('Erro de conexão. Verifique sua internet e tente novamente.');
                }
                
                // Hide loading
                loading.style.display = 'none';
                sendBtn.disabled = false;
                sendBtn.textContent = 'Enviar';
            }
            
            sendBtn.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // Focus on input when page loads
            messageInput.focus();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
