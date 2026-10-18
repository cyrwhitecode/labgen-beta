from io import BytesIO

from docx import Document
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from services.extract import extraction

from uuid import uuid4
from calculs.regression import get_results
from config import OUTPUT_DIR
from schemas.models import GenerateRequest, RapportValidationRequest
from services.rapport_markdown import generate_markdown_report
from services.word import markdown_to_docx


router = APIRouter(prefix="/rapport")

@router.post("/importer")
async def importer(fichier: UploadFile = File(...)):

    # On verifie que le nom de termine par .docx sinon on retourne une HTTPException
    contenu = await fichier.read()

    try:
        doc = Document(BytesIO(contenu))
    except Exception:
        raise HTTPException(status_code=400, detail="Fichier word illisible.")

    # Verifier si la liste est vide. 
    tableaux = extraction(doc)
    if not tableaux:
        raise HTTPException(status_code=400, detail="Aucun tableau retrouvedans le document.")

    for t in tableaux:
        for nom, valeur in t.items():
            print(nom, type(valeur), [type(v) for v in valeur][:3])

    return { "tableau": tableaux } 


@router.post("/generer_texte")
async def generer_texte_rapport(payload: GenerateRequest):
    try:
        results = get_results(payload.tableaux)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    markdown = generate_markdown_report(payload.tp.model_dump(), results)

    return { "markdown": markdown }


@router.post("/generer")
async def generate(payload: GenerateRequest):
    try:
        results = get_results(payload.tableaux)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    markdown = generate_markdown_report(payload.tp.model_dump(), results)
    (OUTPUT_DIR / "debug.md").write_text(markdown, encoding="utf-8")

    chemin = OUTPUT_DIR / f"rapport_{uuid4().hex[:8]}.docx"
    markdown_to_docx(markdown, chemin)

    return FileResponse(
        chemin,
        media_type="application/vdn.openxmlformats-officedocument.wordprocessingml.document",
        filename="rapport.docx"
    )

