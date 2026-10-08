import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.ai import normilization, client
from fastapi import HTTPException, APIRouter
from schemas.models import ChatRequest

router = APIRouter()

@router.post("/chat") 
async def chat_with_groq(payload: ChatRequest):
    try:
        system_prompt = r"""Tu es LabGen, un assistant IA spécialisé dans la conception de rapports de TP et l'exploration scientifique. 
            Ton créateur est White Cyr, un étudiant camerounais.
            Tu as un bon sens de la conversation, tu ecoute et tu reponds poliment  
            Tout sujet qui s'eloigne de l'education educatif est proscrit (sentiment amoureux, questions desinvoltes, ...) mais repond juste en precisant l'objet de ta presence (sans te representer, fais comme un humain, reponses variables et pleines de vie) et propose un autre assitant IA ouvert a ce genre de conversation(Gemini, Deepseek, chatGPT,..).
            
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
        raise HTTPException(status_code=500, detail=str(e))