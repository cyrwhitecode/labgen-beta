import pypandoc
import os
from docx import Document
import numpy as np

texte = r"""# Compte Rendu de TP

## Objectif
L'objectif de ce TP est de maitriser la loi d'Ohm aux bornes d'une resistance

## Formation requise
La relation est $$R = \frac{U}{I}$$
"""

#pypandoc.convert_text(texte, "docx", format="md", outputfile="mesures.docx")
doc = Document("mesures.docx")

def nombre(texte):
    try:
        return float(texte.strip().replace(",", "."))
    except ValueError:
        return texte

result = []

def extraction(doc):
    for i, tableau in enumerate(doc.tables):
        tab = {}
        for line in tableau.rows:
            nom = line.cells[0].text.strip()
            valeur = np.array([nombre(cellule.text) for cellule in line.cells[1:]])
            tab[nom] = valeur
        result.append(tab)
    return result

extraction_tab = extraction(doc)
