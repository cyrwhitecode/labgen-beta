import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.ai import normilization, client
from calculs.regression import get_results

resultats = get_results()

def get_dict(resultats):

    blocs = []
    for i, r in enumerate(resultats):

        texte = f"""
            - variable en abscisse = {r['x_key']}
            - variable en ordonnee = {r['y_key']}
            - points en abscisse = {r['points_x']}
            - points en ordonnee = {r['points_y']}
            - Pente = {r['pente']:.3f}
            - ordonnee a l'origine = {r['ordonnee']:.3f}
            - incertitude sur la pente = {r['ecart_type']:.3f}
            - Coefficient de correlation au carré (r2) = {r['r2']:.3f}
            - nombre de points = {r['n']}
            - graphe = {r['graphe']}
        """
        blocs.append(texte)
    
    return "\n\n".join(blocs)


PROMPT_RAPPORT = r"""
    Reponds en texte normal et en Markdown.

    Regles:
    - La bibliographie utilisee doit etre selon le style HARVARD.
    - utilise uniquement les informations fournies. N'invente aucune mesure ni aucun resultat.
    - Recopie les valeurs de la section 'Resultats calcules' exactement telles qu'elles sont. Ne recalcule rien et ne change pas les arrondis.
    - Pour chaque graphe, ecris son nom seul sur sa ligne, dans la section 'Resultats et analyse', suivi d'une courte description de ce que le graphe represente.
    - Si un resultat est accompagne d'un avertissement, mentionne cet avertissement dans l'analyse.
    - Utilise du LaTeX uniquement pour une vraie formule mathematique ou physique, jamais pour du texte ordinaire.
    - Formule dans une phrase: $...$ . 
    - Formule seule sur sa ligne: mets $$ seul sur sa propre ligne, puis la formule, puis $$ seul sur sa propre ligne, avec une ligne vide avant et après: $$...$$
    - N'utilise jamais \[\], \(\), \text{} ni \quad pour du texte.
            
    Exemple de mise en forme attendue:

    La vitesse vaut $v = \frac{d}{t}$ dans ce cas.

    $$
    v = \frac{d}{t}
    $$
            
    Voila, tu es prêt à répondre aux questions de l'utilisateur en respectant ces règles de mise en forme.


    Structure imposee, avec des titres de taille adaptee
    - Rapport se fait en francais sauf le resume
    - bref Resume en anglais du rapport (pas long, ni court mais rappelle sur le principe experimental et donne les grande lignes du rapport et resultats principaux(grandeurs) et la finalite de l'experience)
    - Introduction
    - Principe
    - Materiel
    - Mode operatoire / Methode
    - Corps du rapport (Developpement, Exploitation des donnees (tableaux de donnees necessaires au trace), resultats, graphique, interpretation et analyse, discussion)
        chaque section doit etre placee de maniere intelligente (bien elaborer le contenu avant de placer un tableau ou un graphe n'importe ou.)
        Si on a plusieurs graphiques, l'analyse de fera a tour de role (graphe1 -> interpretation et analyse, puis Graph2, .....).
        Le corps du rapport doit etre assez detaille et explicatif. Il doit contenir les graphiques et les resultats calcules, ainsi que l'analyse de ces resultats.
        Sa structure interne doit etre logique, bien organisee et flexibles c'est a dire que tu peux ajouter des sous-sections si necessaire. 
    - Evaluation des incertitudes
    - Ecritures scientifiques (sous la forme: grandeur = (sa_valeur_normale plus ou moins son incertitude)unite. Pour chacune des grandeurs calculees dans le rapport.) Uniquement dans la section 'Ecriture scientifique'
    - Conclusion
    - Bibliographie (au moins 4 references differentes)
"""


def insert_graphs(texte, resultats):
    for i, r in enumerate(resultats):
        marqueur = f"[[Graphe_{i + 1}]]"
        image = f"![Graphe {i + 1} : {r["y_key"]} en fonction de {r["x_key"]}]"
        texte = texte.replace(marqueur, image)
    return texte

tp = { 
        "titre": "Pendule Simple", 
        "matiere": "Physique", 
        "principe_mode_operatoire": "Determination experimentale de la constante gravitationnelle. materiel: fil inextensible d .." }

def generate_markdown_report(tp=tp, resultats=resultats):
    donnees = (
        f"Titre: {tp['titre']}\n"
        f"Matiere: {tp['matiere']}\n"
        f"Principe et Mode operatoire: {tp['principe_mode_operatoire']}\n"
        "\nResultats calcules:\n"
        + get_dict(resultats)
    )

    response = client.responses.create(
        input=[
            { "role": "system", "content": PROMPT_RAPPORT },
            { "role": "user", "content": donnees }
        ],
        model="openai/gpt-oss-20b",
        max_output_tokens=8000,
        reasoning={"effort": "low"}
    )
    texte = response.output_text
    texte = normilization(texte)
    texte = insert_graphs(texte, resultats) 
    return texte

