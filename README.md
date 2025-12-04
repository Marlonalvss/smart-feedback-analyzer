# 🧠 Smart Feedback Analyzer (Microsserviços + IA)

Aplicação Full-Stack desenvolvida para modernizar a análise de feedbacks de clientes utilizando Inteligência Artificial. O projeto demonstra uma arquitetura desacoplada, segura e pronta para escalar.

## 🚀 Diferenciais Técnicos (Highlights)

Além da integração básica, este projeto implementa práticas avançadas de engenharia de software:

- 🛡️ Prompt Injection Defense: Camada de segurança que blinda a IA contra tentativas de manipulação (Jailbreak) usando delimitadores XML e reforço de instruções.  
- 🧹 Sanitização de Dados: Pipeline de limpeza automática (Regex) para remover tags HTML maliciosas (XSS) e formatação inválida antes de processar.  
- ✅ Validação Robusta: Uso de Pydantic para garantir integridade dos dados (limites de caracteres, verificação de conteúdo vazio) com feedback visual imediato no Frontend.  
- 🧪 Testes Automatizados: Cobertura de testes unitários e de integração utilizando pytest e unittest.mock para garantir a estabilidade do sistema sem custos de API.  
- 👁️ Observabilidade: Sistema de logs detalhado no Backend para rastreabilidade de requisições.  
- 🔒 Segurança: Gestão de segredos via variáveis de ambiente (.env).

## 🛠️ Stack Tecnológico

- Backend: Python 3.11+, FastAPI, Pydantic (Validation), Google Generative AI SDK.  
- Frontend: Vue.js 3 (Composition API), Vite, CSS Scoped.  
- IA: Google Gemini 2.5 Flash (Modelo otimizado para latência baixa).  
- Arquitetura: REST API desacoplada, preparada para containerização (Docker).

## 💡 O Problema e a Solução

Desafio: Migrar um fluxo de análise de dados manual/monolítico para um microsserviço inteligente e seguro.

Minha abordagem:
- Serviço de Ingestão: Criei uma API Python isolada para receber e normalizar dados.  
- Inteligência: Integrei com LLM (Gemini) para classificar sentimento (Positivo/Neutro/Negativo) e extrair tags automaticamente.  
- Interface: Desenvolvi um Frontend reativo com feedback visual de erros e contagem de caracteres em tempo real.

## 📦 Como Rodar Localmente

### Pré-requisitos
- Python 3.9+  
- Node.js 18+  
- Uma API Key do Google Gemini (colocar em .env)

### 1. Backend (Python)
```bash
cd backend
# Crie e ative seu ambiente virtual (opcional, mas recomendado)
python -m venv venv
# Windows:
.\venv\Scripts\Activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Crie um arquivo .env na pasta backend e adicione sua chave:
# GEMINI_API_KEY=sua_chave_aqui

uvicorn main:app --reload
```

### 2. Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Como Rodar os Testes

O projeto inclui testes automatizados que verificam a validação de dados e simulam a integração com a IA (Mocking), permitindo rodar a suíte de testes offline e sem custos.

```bash
cd backend
pip install pytest httpx

# Rodar todos os testes
pytest -v
```

Projeto desenvolvido por Marlon Alves como prova de conceito para arquiteturas modernas e seguras.