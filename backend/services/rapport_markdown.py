import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.ai import normilization, client
from calculs.regression import get_results

resultats = get_results()

def tableau_markdown(r):

    header = f"{r["x_key"]} | {r["y_key"]}"
    separator = "| --- | --- |"
    body_lines = [header, separator]

    for x, y in zip(r["points_x"], r["points_y"]):
       body_lines.append(f"| {x:.2f} | {y:.2f} |")

    return "\n".join(body_lines)


def get_dict(resultats):

    blocs = []
    for i, r in enumerate(resultats):

        texte = f"""
            - marqueur du tableau = [[TABLEAU_{i + 1}]]
            - marqueur du graphe = [[Graphe_{i + 1}]]
            - variable en abscisse = {r['x_key']}
            - variable en ordonnee = {r['y_key']}
            - points en abscisse = {r['points_x']}
            - points en ordonnee = {r['points_y']}
            - Pente = {r['pente']:.3f}
            - ordonnee a l'origine = {r['ordonnee']:.3f}
            - incertitude sur la pente = {r['incertitude_pente']:.3f}
            - Coefficient de correlation au carré (r2) = {r['r2']:.3f}
            - nombre de points = {r['n']}
        """
        blocs.append(texte)
    
    return "\n\n".join(blocs)


PROMPT_RAPPORT = r"""
    Tu es un assistant de redaction de TP, reponds en texte normal et en Markdown.

    Style de redaction exige : Redige le corps du rapport sous forme de paragraphes argumentes, fluides et tres denses. Interdiction absolue de faire de simples listes de formules mathematiques isolees. Chaque formule doit etre introduite par une phrase d'explication physique et suivie d'un paragraphe d'interpretation critiques des resultats.

    Regles:
    - Chaque section du developpement doit etre placee de maniere intelligente, logique et fluide.
    - Si le TP comporte plusieurs graphiques, l'analyse doit se faire a tour de role (graphe1 -> interpretation physique, puis Graph2 -> interpretation physique, etc.).
    - Le Developpement doit etre tres bien detaille, explicatif et argumente. Il doit obligatoirement integrer tableaux et les graphiques a leur place exacte.
    - Sa structure interne doit etre logique, bien organisee et flexibles c'est a dire que tu peux ajouter des sous-sections si necessaire. 
    - La bibliographie utilisee doit respecter strictement le style HARVARD.
    - N'ecris jamais de tableau toi meme et ne recopie pas les listes des mesures: le tableau est insere automatiquement a l'endroit du marqueur [[TABLEAU_n]].
    - N'utilise Jamais de bloc de code (pas de ``, pas de texte indente de 4 espaces) pour representer les resultats.
    - utilise uniquement les informations fournies. N'invente aucune mesure ni aucun resultat.
    - Recopie les valeurs de la section 'Resultats calcules' exactement telles qu'elles sont. Ne recalcule rien et ne change pas les arrondis.
    - Avant chaque graphe, ecris son marqueur [[TABLEAU_n]] seul sur sa ligne avec le meme numero que le graphe, suivi d'une courte description de ce que le graphe represente.
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

    Consignes specifiques pour la section "Evaluation des incertitudes":
    - Expose clairement les methodes de calcul d'incertitudes applicables selon le contexte experimental en utilisant les formules standardisees:
      1. Incertitude de Type A (statistique) basee sur la moyenne, la variance $s^2$, l'ecart-type $s = \sqrt{s^2}$ et l'incertitude type $u_A = \frac{s}{\sqrt{n}}$.
      2. Incertitude de Type B (instrumentale / non statistique) en distinguant la distribution rectangulaire ($u = \frac{a}{2\sqrt{3}}$ pour les lectures a echelle graduee et la construction de certaines balances) et les specificites des appareils :
         - Appareils analogiques (ex: amperemetres/voltmetres a aiguilles) : $u_B = \frac{\text{class} \times \text{calibre}}{100 \times \sqrt{3}}$
         - Appareils numeriques (ex: multimetre numerique) : $u_B = \fract{(\text{valeur mesuree} \times \text{precision} + \text{nombre de digits})}{\sqrt{3}}
      3. Incertitude composee (Type C) combinant les sources par la racine carree de la somme des carres ($u_C = \sqrt{u_A^2 + U_B^2}$) ou la propagation des incertitudes.
    -Respecte et integre les choix ou les resultats numeriques fournis par l'etudiant sans les modifier, en les inserant proprement dans le formalisme mathematique approprie.

    Structure imposee (avec des titres de taille adaptee):
    - Le rapport est redige entierement en francais, a l'exception du resume.
    - Resume (10 a 15 lignes sur format A4) redige en anglais (rappelle sur le principe experimental et des resultats cles de l'experience)
    - Introduction
    - Principe
    - Materiel
    - Mode operatoire / Methode
    - Corps du rapport (Developpement, exploitation des donnees, analyse physique approfondie)
    - Evaluation des incertitudes (Exposition des formules theoriques applicables et traitement des donnees.)
    - Ecritures scientifiques (Presentation normalisees sous la forme : $\text{Grandeur} = (\text{Valeur} \pm \text{Incertitude}) \, \text{Unite}$.). 
    - Conclusion (Bilan factuel de l'experience et perspectives.)
    - Bibliographie (au moins 4 references differentes rigoureusement au format Harvard.)

    === CONSIGNES SPECIFICES POUR LE CORPS DU RAPPORT (DEVELOPPEMENT & EXPLOITATION) ===
    Le corps du rapport constitue la partie centrale et la plus riche du document. Il doit s'adapter rigoureusement a la thematique du TP (mecanique, electronique, electromagnetisme, thermodynamique, .... etc) en suivant une demarche scientifique explicite:
      
      1. Adaptation thematique et structuration:
         - Si le TP traite des circuits ou signaux (ex: electricite/elctronique) : decris qualitativement l'allure des signaux, l'influence des composants (diodes, condensateurs, spires, ...) te exploite les relstions de proportionnalite ou d'induction.
         - Si le TP traite de mecanique ou de fluides (ex: plan incline, viscosimetrie) : pose explicitement le bilan des forces (ex: PFD de Newton, loi des Stokes), etablis les equations differentielles ou d'equilibre menant aux grandeurs recherchees (accceleration, viscosite, ...), et discute des limites du modele (ex: frottements, correction de Ladenburg, nombre de Reynolds).

      2. Integration stricte des donnees et des graphiques :
         - Insere les tableaux de mesures (via le marqueur [[TABLEAU_n]]) et les graphiques correspondants (via [[Graphe_n]]) au moment opportun dans l'analyse.
         - Commente l'allure des courbes obtenues (lineaire, hyperbolique, etc.) et explique comment l'exploitation graphique (calcul de pente a = \Delta y / \Delta x, ordonnee a l'origine) permet de valider la theorie ou une grandeur physique ($N_1$, $i_c$, $\mu$, etc.).

      3. Integrite des resultats de l'etudiant :
         - Utilise strictement et exclusivement les valeurs numeriques et les resultats fournis par l'etudiant. N'interprete pas les ecarts comme des erreurs l'eleve et ne modifie  en aucun cas  ses chiffres.
         - Explicitement les formules mathematiques et physiques associees en LaTeX pour justifier les calculs presents dans les tableaux ou les applications numeriques.
         - Interdiction formelle de laisser le corps du rapport vide, succinct ou de sauter directement a la concluison : Chaque serie de mesure ou chaque graphique doit faire l'objet d'un paragraphe d'analyse detaille, argumennte et redige dans un style academique. 
"""


def insert_graphs(texte, resultats):
    for i, r in enumerate(resultats):
        marqueur_graphe = f"[[Graphe_{i + 1}]]"
        marqueur_tableau = f"[[TABLEAU_{i + 1}]]"
        tableau = tableau_markdown(r)
        image = f"![Graphe {i + 1} : {r["y_key"]} en fonction de {r["x_key"]}]({r["graphe"]})"
        texte = texte.replace(marqueur_tableau, tableau)
        texte = texte.replace(marqueur_graphe, image)
    return texte

tp = { 
        "titre": "Pendule Simple", 
        "matiere": "Physique", 
        "principe_mode_operatoire": "Determination experimentale de la constante gravitationnelle. materiel: fil inextensible d .." }

def generate_markdown_report(tp, resultats):
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

