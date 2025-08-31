# Church Connection Recommendations API

API REST em Python com FastAPI que utiliza OpenAI LLM para recomendar conexões ideais dentro do ambiente eclesiástico.

## 📋 Visão Geral

Esta aplicação analisa o perfil de membros da igreja e recomenda:
- **Grupos/Ministérios** adequados aos interesses e disponibilidade
- **Células** (pequenos grupos espirituais) compatíveis com o perfil
- **Pessoas** relevantes para mentoria, liderança ou companheirismo

## 🚀 Funcionalidades

- **Endpoint `/recommend-connections`**: Recebe dados do membro e retorna recomendações personalizadas
- **Integração OpenAI**: Utiliza GPT-3.5-turbo para análise inteligente
- **Sistema de Scoring**: Pontuação de 0 a 1 para relevância das recomendações
- **Validação Rigorosa**: Entrada e saída de dados estruturados com Pydantic
- **Documentação Automática**: Interface Swagger/OpenAPI integrada

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **OpenAI API**: Modelo de linguagem GPT-3.5-turbo
- **Pydantic**: Validação e serialização de dados
- **Uvicorn**: Servidor ASGI de alta performance
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

## 📦 Instalação

### Pré-requisitos

- Python 3.8+
- Conta OpenAI com API Key

### Passos

1. **Clone o repositório**
```bash
git clone <repository-url>
cd createhack-ampeli-llm
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**
```bash
# Crie arquivo .env na raiz do projeto
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

5. **Execute a aplicação**
```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Endpoint Principal

**POST** `/recommend-connections`

Recebe dados do membro e contexto da igreja, retorna recomendações personalizadas.

#### Exemplo de Requisição

```json
{
  "member": {
    "name": "João Silva",
    "interests": ["música", "jovens", "ensino"],
    "history": "Membro há 2 anos, participou do coral",
    "profile": "Jovem adulto, gosta de liderar",
    "availability": "Domingos manhã, quartas à noite"
  },
  "groups": [
    {
      "name": "Ministério de Louvor",
      "description": "Grupo responsável pela música nos cultos",
      "focus": "música, adoração",
      "schedule": "Domingos 8h, quartas 19h"
    }
  ],
  "cells": [
    {
      "name": "Célula Jovens Centro",
      "description": "Pequeno grupo para jovens adultos",
      "leader": "Pastor Carlos",
      "location": "Centro da cidade",
      "schedule": "Sextas 19h30"
    }
  ],
  "people": [
    {
      "name": "Ana Costa",
      "role": "Líder de Louvor",
      "description": "15 anos de experiência em música",
      "availability": "Domingos e quartas"
    }
  ]
}
```

#### Exemplo de Resposta

```json
{
  "groups": [
    {
      "name": "Ministério de Louvor",
      "description": "Perfeito alinhamento com interesse em música e disponibilidade.",
      "score": 0.95
    }
  ],
  "cells": [
    {
      "name": "Célula Jovens Centro",
      "description": "Grupo ideal para jovens adultos com foco em crescimento.",
      "score": 0.85
    }
  ],
  "people": [
    {
      "name": "Ana Costa",
      "role": "Líder de Louvor",
      "score": 0.90
    }
  ]
}
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-sua_chave_openai_aqui
```

### Parâmetros do OpenAI

No arquivo `main.py`, você pode ajustar:

- **model**: Modelo utilizado (padrão: `gpt-3.5-turbo`)
- **temperature**: Criatividade das respostas (padrão: `0.7`)
- **max_tokens**: Limite de tokens na resposta (padrão: `2000`)

## 📖 Documentação Adicional

- **[GOALS.md](GOALS.md)**: Objetivos detalhados da aplicação
- **[CONTEXT.md](CONTEXT.md)**: Contexto e cenário eclesiástico
- **[AGENT_GUIDE.md](AGENT_GUIDE.md)**: Guia completo do comportamento do agente

## 🧪 Testando a API

### Interface Swagger

Acesse `http://localhost:8000/docs` para interface interativa da API.

### Teste com cURL

```bash
curl -X POST "http://localhost:8000/recommend-connections" \
  -H "Content-Type: application/json" \
  -d @exemplo_request.json
```

## 🔍 Monitoramento

### Logs

A aplicação registra:
- Requisições recebidas
- Chamadas para OpenAI
- Erros de parsing JSON
- Exceções gerais

### Métricas de Qualidade

- **Relevância**: Scores médios > 0.6
- **Performance**: Tempo de resposta < 3s
- **Disponibilidade**: Uptime > 99%

## 🚨 Tratamento de Erros

### Códigos de Status

- **200**: Sucesso
- **422**: Dados de entrada inválidos
- **500**: Erro interno (OpenAI, parsing JSON)

### Erros Comuns

1. **API Key inválida**: Verifique `OPENAI_API_KEY` no `.env`
2. **JSON malformado**: Resposta do LLM não é JSON válido
3. **Timeout**: Chamada para OpenAI excedeu tempo limite

## 🤝 Contribuição

1. Fork o projeto
2. Crie branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abra Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Consulte a documentação em `/docs`
- Verifique os logs da aplicação
