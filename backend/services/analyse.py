from calculs.regression import get_results

def analyse(tableaux, choix):
    resultats = []

    for i, tab in enumerate(tableaux):
        modele = choix[i] if i < len(choix) else "lineaire"

        if modele == "lineaire":
            resultat = get_results()
        else:
            raise ValueError(f"Modele inconnu: {modele}")

        