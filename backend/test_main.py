from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

# Cliente de teste do FastAPI (simula um navegador/frontend)
client = TestClient(app)

# --- TESTES BÁSICOS ---

def test_read_root():
    """Testa se a rota raiz responde 200 OK"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API do Marlon está ON e SEGURA! 🛡️"}

# --- TESTES DE VALIDAÇÃO (PYDANTIC) ---

def test_feedback_muito_curto():
    """Deve falhar se o texto tiver menos de 5 caracteres"""
    payload = {"text": "Oi"}
    response = client.post("/analyze", json=payload)
    
    # Esperamos erro 422 (Unprocessable Entity)
    assert response.status_code == 422
    # Verificamos se a mensagem de erro é a que definimos
    assert "O feedback é muito curto" in response.json()["detail"][0]["msg"]

def test_feedback_vazio():
    """Deve falhar se o texto for apenas espaços"""
    payload = {"text": "   "}
    response = client.post("/analyze", json=payload)
    
    assert response.status_code == 422
    assert "não pode estar vazio" in response.json()["detail"][0]["msg"]

# --- TESTES DE INTEGRAÇÃO COM MOCK (O MAIS IMPORTANTE) ---

@patch("google.generativeai.GenerativeModel")
def test_analise_com_sucesso(mock_model_class):
    """
    Simula uma análise bem-sucedida SEM chamar o Google de verdade.
    Usamos MOCK para fingir que a IA respondeu.
    """
    # 1. PREPARAÇÃO DO MOCK
    # Criamos uma resposta falsa que o Gemini "devolveria"
    mock_response = MagicMock()
    mock_response.text = '{"sentimento": "Positivo", "resumo": "Teste OK", "tags": ["teste"]}'
    
    # Ensinamos o Mock: "Quando chamarem generate_content, retorne isso aqui"
    mock_instance = mock_model_class.return_value
    mock_instance.generate_content.return_value = mock_response

    # 2. AÇÃO
    payload = {"text": "O sistema de testes automatizados é incrível e muito rápido."}
    response = client.post("/analyze", json=payload)

    # 3. VERIFICAÇÃO
    assert response.status_code == 200
    resultado = response.json()
    
    # Verifica se o backend repassou o que o "Gemini Falso" disse
    assert "Positivo" in resultado["result"]
    
    # BÔNUS: Verifica se o código realmente tentou limpar a tag XML antes de enviar
    # Isso prova que sua sanitização está sendo chamada
    args, _ = mock_instance.generate_content.call_args
    prompt_enviado = args[0]
    assert "<feedback_cliente>" in prompt_enviado