from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def normilization(texte: str) -> str:
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