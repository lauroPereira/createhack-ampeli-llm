from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import json
from datetime import date
from enum import Enum
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from mock_data import MOCK_GROUPS, MOCK_MINISTRIES, MOCK_CELLS, MOCK_MEMBERS
from models import (
    Gender, MaritalStatus, FaithStage, EventPreference,
    User, Member, Group, Ministry, Cell,
    ConnectionRequest, ConnectionResponse, RecommendationItem
)

load_dotenv()

app = FastAPI(
    title="Ampeli",
    description="API para recomendações de conexões em igrejas usando OpenAI LLM",
    version="1.0.0"
)

# Configuração do LangChain OpenAI
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=2000,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Static files - commented for Vercel deployment
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Ampeli - Church Connection Recommendations API"}

@app.get("/form", response_class=HTMLResponse)
async def get_form():
    """
    Endpoint para servir o formulário de cadastro de membro
    """
    try:
        with open("form.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")

@app.post("/recommend-connections", response_model=ConnectionResponse)
async def recommend_connections(request: ConnectionRequest):
    """
    Endpoint para recomendar conexões ideais para um membro da igreja
    """
    try:
        print("Starting recommendation process...")
        
        # Construir os dados para o prompt com serialização de datas
        def serialize_member_data(member_data):
            """Converte objetos date para string para serialização JSON"""
            serialized = member_data.copy()
            if 'data_nascimento' in serialized and serialized['data_nascimento']:
                serialized['data_nascimento'] = serialized['data_nascimento'].isoformat()
            return serialized
        
        data = {
            "member": serialize_member_data(request.member.model_dump()),
            "groups": [group.model_dump() for group in request.groups],
            "ministries": [ministry.model_dump() for ministry in request.ministries],
            "cells": [cell.model_dump() for cell in request.cells]
        }
        
        print("Data prepared successfully")
        
        # Prompt especializado
        prompt = f"""Você é um assistente especializado em recomendar conexões ideais dentro de uma igreja, baseando-se em dados do membro e no perfil de grupos, ministérios e células disponíveis.

Sua tarefa é analisar o perfil completo do membro (interesses, disponibilidade, estágio de fé, etc.) e informações sobre grupos, ministérios e células, e retornar UM ÚNICO JSON válido e bem formatado com 3 listas:

1. "groups": lista de grupos comunitários recomendados (ex: grupo do vôlei), cada item deve conter: 
   - "name" (nome do grupo),
   - "description" (breve descrição do por que é recomendado para este membro),
   - "score" (número decimal entre 0 e 1 representando afinidade, onde 1 é máximo).

2. "ministries": lista de ministérios de voluntários recomendados (ex: Louvor, Recepção), com os mesmos campos do grupo.

3. "cells": lista de células ou pequenos grupos espirituais recomendados, com os mesmos campos.

Critérios a seguir:

- Considere TODOS os dados do membro: áreas de interesse, habilidades, disponibilidade, estágio de fé, preferências de grupo, etc.
- Ordene cada lista do maior para o menor score.
- O score deve refletir sinergia entre o perfil completo do membro e o item recomendado.
- Seja específico nas descrições, explicando por que aquela recomendação faz sentido para este membro.
- Para membros iniciantes, priorize grupos de integração e células de fundamentos.
- Para membros atuantes, considere oportunidades de liderança e serviço.
- Considere compatibilidade de horários e preferências pessoais.
- NÃO inclua texto fora do JSON.
- Garanta que o JSON seja válido para parser JSON em Python ou JavaScript.

Seguem os dados (Membro + Grupos + Ministérios + Células):

{json.dumps(data, ensure_ascii=False, indent=2)}

Retorne somente um JSON com o formato especificado."""

        print("Calling LangChain OpenAI...")
        
        # Chamada para LangChain OpenAI
        try:
            messages = [
                SystemMessage(content="Você é um assistente especializado em recomendações de conexões para igrejas. Analise cuidadosamente o perfil completo do membro e retorne apenas JSON válido com recomendações personalizadas."),
                HumanMessage(content=prompt)
            ]
            response = llm(messages)
            print("LangChain OpenAI call successful")
        except Exception as e:
            print(f"LangChain OpenAI error: {e}")
            raise HTTPException(status_code=500, detail=f"Erro na chamada da API LangChain OpenAI: {str(e)}")
        
        # Extrair e parsear a resposta
        try:
            llm_response = response.content.strip()
            print(f"LLM Response received: {llm_response[:100]}...")
        except Exception as e:
            print(f"Error extracting response: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao extrair resposta: {str(e)}")
        
        try:
            recommendations = json.loads(llm_response)
            print("JSON parsed successfully")
            return ConnectionResponse(**recommendations)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Raw response: {llm_response}")
            raise HTTPException(status_code=500, detail=f"Erro ao parsear resposta do LLM: {str(e)}")
        except Exception as e:
            print(f"Error creating ConnectionResponse: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao criar resposta: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in recommend_connections: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/mock-data")
async def get_mock_data():
    """
    Endpoint para obter dados de exemplo para testes
    """
    return {
        "groups": MOCK_GROUPS,
        "ministries": MOCK_MINISTRIES,
        "cells": MOCK_CELLS,
        "sample_members": MOCK_MEMBERS
    }

@app.get("/test-recommendation/{member_index}")
async def test_recommendation(member_index: int):
    """
    Endpoint para testar recomendações com membros de exemplo
    """
    try:
        if member_index >= len(MOCK_MEMBERS):
            raise HTTPException(status_code=404, detail="Membro não encontrado")
        
        sample_member = MOCK_MEMBERS[member_index]
        print(f"Testing with member: {sample_member['nome_completo']}")
        
        # Criar objetos Pydantic
        try:
            member_obj = Member(**sample_member)
            print("Member object created successfully")
        except Exception as e:
            print(f"Error creating Member object: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating Member: {str(e)}")
        
        try:
            groups_obj = [Group(**group) for group in MOCK_GROUPS]
            ministries_obj = [Ministry(**ministry) for ministry in MOCK_MINISTRIES]
            cells_obj = [Cell(**cell) for cell in MOCK_CELLS]
            print("All objects created successfully")
        except Exception as e:
            print(f"Error creating group/ministry/cell objects: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating objects: {str(e)}")
        
        # Criar request
        try:
            request = ConnectionRequest(
                member=member_obj,
                groups=groups_obj,
                ministries=ministries_obj,
                cells=cells_obj
            )
            print("ConnectionRequest created successfully")
        except Exception as e:
            print(f"Error creating ConnectionRequest: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating request: {str(e)}")
        
        # Chamar o endpoint de recomendações
        try:
            result = await recommend_connections(request)
            print("Recommendations generated successfully")
            return result
        except Exception as e:
            print(f"Error in recommend_connections: {e}")
            raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in test_recommendation: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
