import json
import os
#from typing import Literal
from openai import OpenAI
#from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from pydantic import BaseModel
#import re
from routes import chat
from routes import rapports



# Charger la cle API
#load_dotenv()

# Initialisation de l'applicaiton Web Backend FastAPI et du client Gemini
app = FastAPI(title="LabGen Backend", description="Backend pour LabGen utilisant FastAPI et Groq", version="1.0.0")

# Autoriser REACT a communiquer avec FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Le proxy système Windows ferme la connexion vers Groq; on bypass uniquement cet hôte.
no_proxy_hosts = {
    host.strip().lower()
    for variable in ("NO_PROXY", "no_proxy")
    for host in os.environ.get(variable, "").split(",")
    if host.strip()
}
no_proxy_hosts.add("api.groq.com")
no_proxy = ",".join(sorted(no_proxy_hosts))
os.environ["NO_PROXY"] = no_proxy
os.environ["no_proxy"] = no_proxy

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

app.include_router(chat.router)
app.include_router(rapports.router)


# Route principale appelee par le frontend
@app.get("/")
async def root():
    return {"status": "API operationnelle"}    