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

'''class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: dict | None = None
'''
# Route principale appelee par le frontend
@app.get("/")
async def root():
    return {"status": "API operationnelle"}    

'''def normilization(texte: str) -> str:
    texte = re.sub(
       r"\\\[(.*?)\\\]",
       lambda m: "$$" + m.group(1) + "$$", 
       texte,
       flags=re.DOTALL,
    )

    texte = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: "$" + m.group(1).strip() + "$", 
        texte,
        flags=re.DOTALL,
    )
    return texte

@app.post("/chat") 
async def chat_with_groq(payload: ChatRequest):
    try:
        system_prompt = r"""Tu es LabGen, un assistant IA spécialisé dans la conception de rapports de TP et l'exploration scientifique. 
            Ton créateur est White Cyr, un étudiant camerounais.
            Tu as un bon sens de la conversation, tu ecoute et tu reponds poliment  

            Reponds en texte normal et en Markdown.

            Regles pour la mise en forme des formules mathematiques et physiques:
            - Utilise du LaTeX uniquement pour une vraie formule mathematique ou physique, jamais pour du texte ordinaire.
            - Formule dans une phrase: $...$ . 
            - Formule seule sur sa ligne: mets $$ seul sur sa propre ligne, puis la formule, puis $$ seul sur sa propre ligne, avec une ligne vide avant et après: $$...$$
            - N'utilise jamais \[\], \(\), \text{} ni \quad pour du texte.
            
            Exemple de mise en forme attendue:

            La vitesse vaut $v = \frac{d}{t}$ dans ce cas.

            $$
            v = \frac{d}{t}
            $$
            
            Voila, tu es prêt à répondre aux questions de l'utilisateur en respectant ces règles de mise en forme."""
        
        if payload.context:
            system_prompt += f"\n\nContexte fourni par l'utilisateur: {json.dumps(payload.context, ensure_ascii=False)}"
            print("payload.context:", payload.context)

        response = client.responses.create(
                input=[
                    {"role": "system", "content": system_prompt},
                    *[message.model_dump() for message in payload.messages[-20:]]
                ],
                model="openai/gpt-oss-20b",
                #stream=True,
            )
        texte_brute = response.output_text
        texte_normalized = normilization(texte_brute)
        #print("Réponse de Groq:", texte_normalized.count("$$"))
        return {"reply": texte_normalized}
    
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code=500, detail=str(e))'''
