from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from neo_queries import Queries
from models_validate import NodeAndRelationships
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_API_TOKEN")

# Инициализация приложения FastAPI
app = FastAPI()

# Механизм авторизации
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

@app.get("/nodes")
async def get_all_nodes():
    return Queries.get_all_nodes()

@app.get("/nodes/{node_id}")
async def get_node_and_relations(node_id: int):
    return Queries.get_node_and_relations(node_id)

@app.post("/graph/insert")
async def insert_node_and_relationships(data: NodeAndRelationships, token: str = Depends(verify_token)):
    # Добавление узла и связей
    response = Queries.insert_node_and_relationships(data.node, data.relationships)
    return {"status": "Узел и связи добавлены.", "response": response}

@app.delete("/nodes/{node_id}")
async def delete_node_and_relationship(node_id: str, token: str = Depends(verify_token)):
    response =  Queries.delete_node_and_relationships(node_id)
    return {"status": "Узел удален.", "response": response}