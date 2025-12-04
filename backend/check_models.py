import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env (O COFRE)
load_dotenv()

# 2. Pega a chave de forma segura
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERRO: A chave API não foi encontrada no arquivo .env!")
else:
    # 3. Configura usando a variável, NUNCA o texto direto
    genai.configure(api_key=api_key)

    print("🔍 Buscando modelos disponíveis para sua chave...")

    try:
        models_found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Modelo disponível: {m.name}")
                models_found = True
        
        if not models_found:
            print("❌ Nenhum modelo encontrado. Verifique se sua API Key está ativa.")

    except Exception as e:
        print(f"❌ Erro de conexão: {e}")