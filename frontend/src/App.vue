<script setup>
import { ref } from 'vue'

const feedback = ref('')
const analysis = ref(null)
const loading = ref(false)
const errorMessage = ref('') // Variável reativa para o erro visual

const analyzeFeedback = async () => {
  // Limpa estados anteriores
  loading.value = true
  analysis.value = null
  errorMessage.value = '' 

  try {
    const response = await fetch('http://127.0.0.1:8000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: feedback.value })
    })

    // --- A MÁGICA ACONTECE AQUI ---
    if (!response.ok) {
      const errorData = await response.json()
      
      // 1. Erros de Validação do FastAPI (HTTP 422)
      // O FastAPI devolve: { "detail": [ { "msg": "Value error, texto do erro..." } ] }
      if (response.status === 422 && errorData.detail) {
        // Pegamos a primeira mensagem de erro da lista
        let msg = errorData.detail[0].msg
        
        // Removemos o prefixo técnico "Value error, " que o Pydantic coloca
        msg = msg.replace('Value error, ', '') 
        
        throw new Error(msg)
      } 
      
      // 2. Erros genéricos do nosso código (HTTP 500 etc)
      if (errorData.error) {
        throw new Error(errorData.error)
      }

      throw new Error('Erro desconhecido ao comunicar com o servidor.')
    }

    const data = await response.json()
    analysis.value = JSON.parse(data.result)
    
  } catch (error) {
    console.error(error)
    // Se o backend estiver desligado, o fetch falha com "Failed to fetch"
    if (error.message.includes('Failed to fetch')) {
      errorMessage.value = "O servidor parece estar offline. Verifique se o terminal do Python está rodando."
    } else {
      errorMessage.value = error.message
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <header>
      <h1>🧠 Smart Feedback Analyzer</h1>
      <p>Powered by Gemini 2.5 & Python</p>
    </header>

    <main>
      <div class="input-area">
        <textarea 
          v-model="feedback" 
          placeholder="Cole aqui o feedback do cliente..."
          :class="{ 'has-error': errorMessage }"
          maxlength="5000"
        ></textarea>
        
        <!-- ✨ CONTADOR DE CARACTERES ✨ -->
        <!-- Fica vermelho se tiver texto mas for menor que 5 caracteres -->
        <div class="char-counter" :class="{ 'invalid': feedback.length > 0 && feedback.length < 5 }">
          {{ feedback.length }} / 5000 caracteres
        </div>
        
        <div v-if="errorMessage" class="error-alert">
          🚫 {{ errorMessage }}
        </div>

        <button @click="analyzeFeedback" :disabled="loading">
          {{ loading ? 'Analisando...' : '🔍 Analisar com IA' }}
        </button>
      </div>

      <div v-if="analysis" class="result-card">
        <div class="sentiment-badge" :class="analysis.sentimento.toLowerCase()">
          {{ analysis.sentimento }}
        </div>
        
        <h3>Resumo</h3>
        <p>{{ analysis.resumo }}</p>

        <div class="tags">
          <span v-for="tag in analysis.tags" :key="tag" class="tag">#{{ tag }}</span>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Container Principal */
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

header { text-align: center; margin-bottom: 2rem; }
header h1 { color: #2c3e50; margin-bottom: 0.5rem; }
header p { color: #7f8c8d; font-size: 0.9rem; }

/* Área de Input */
textarea {
  width: 100%;
  height: 120px;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  margin-bottom: 0.5rem; /* Espaço para o erro */
  transition: all 0.3s;
  outline: none;
}

textarea:focus { border-color: #42b983; }

/* Estilo quando dá erro no textarea */
textarea.has-error {
  border-color: #e74c3c;
  background-color: #fff5f5;
}

/* --- ESTILO DO CONTADOR --- */
.char-counter {
  text-align: right;
  font-size: 0.8rem;
  color: #7f8c8d;
  margin-top: -5px;
  margin-bottom: 1rem;
  transition: color 0.3s;
}

.char-counter.invalid {
  color: #e74c3c; /* Vermelho alerta */
  font-weight: bold;
}

/* O NOVO ALERTA VISUAL */
.error-alert {
  color: #e74c3c;
  background-color: #fdecea;
  padding: 0.8rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  border-left: 4px solid #e74c3c;
  animation: shake 0.3s ease-in-out;
}

/* Animação de "tremida" para chamar atenção no erro */
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
}

button {
  width: 100%;
  padding: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}
button:disabled { background-color: #a8d5c2; cursor: not-allowed; }
button:hover:not(:disabled) { background-color: #3aa876; }

/* Card de Resultado */
.result-card {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  border: 1px solid #e9ecef;
}

.sentiment-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  color: white;
  font-weight: bold;
  margin-bottom: 1rem;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.sentiment-badge.positivo { background-color: #27ae60; }
.sentiment-badge.negativo { background-color: #e74c3c; }
.sentiment-badge.neutro { background-color: #f39c12; }

.tags { margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.tag { background: #e9ecef; color: #495057; padding: 0.3rem 0.8rem; border-radius: 4px; font-size: 0.85rem; }
</style>