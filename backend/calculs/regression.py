import os
import sys
from scipy.stats import linregress
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from services.extract  import extraction_tab
from config import OUTPUT_DIR

# This function defines the linear regression model, which takes an input x and returns the corresponding y value based on the slope and intercept of the regression line.
def regress(x, slope, intercept):
    return slope * x + intercept

# This function takes the extracted data from the Word document, performs linear regression on the x and y data, and returns the slope, intercept, x and y data, and their corresponding keys.
def calcul_regression(tab):

    if len(tab) < 3:
        raise ValueError("Le tableau doit avoir au moins 3 lignes.")

    x_key = list(tab.keys())[2]
    y_key = list(tab.keys())[1]
    x = np.array(tab[x_key], dtype=float)
    y = np.array(tab[y_key], dtype=float)

    linear_regression = linregress(x, y)
    slope, intercept, r, p, std = linear_regression

    return slope, intercept, x, y, x_key, y_key, std, r


def clean_key(key):
    return key.replace("(", "_").replace(")", "_").replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
def name_file(i, x_key, y_key):
    return f"Graphe_{i + 1}_{clean_key(x_key)}_{clean_key(y_key)}.png"


# This function takes the x and y data, along with the slope and intercept of the regression line, and plots the data points and the regression line. It saves the plot as a PNG file with a name that includes the x and y keys.
def tracer_regression(x, y, x_key, y_key, i, slope, intercept):

    model = np.linspace(min(x), max(x), 1000)
    chemin = OUTPUT_DIR / name_file(i, x_key, y_key)

    plt.figure(figsize=(10, 6))
    plt.title(f"Régression linéaire entre {x_key} et {y_key}")
    plt.scatter(x, y, label="Données expérimentales", color="blue")
    plt.plot(model, regress(model, slope, intercept), label="Modèle de régression", color="red")
    plt.ylabel(f"{y_key}")
    plt.xlabel(f"{x_key}")
    plt.legend()
    plt.grid(True)
    plt.savefig(chemin, dpi=300, bbox_inches="tight")
    plt.close()

    return chemin



# This function iterates through the extracted data tables, performs linear regression on each table, and plots the regression line along with the data points for each table.
def get_results(extraction_tab=extraction_tab):

    resultats = []
    for i, table in enumerate(extraction_tab):
        slope, intercept, x, y, x_key, y_key, std, r = calcul_regression(table)
        chemin = tracer_regression(x, y, x_key, y_key, i, slope, intercept)

        resultat = {
            "type": "lineaire",
            "x_key": x_key,
            "y_key": y_key,
            "points_x": x.tolist(),
            "points_y": y.tolist(),
            "pente": slope,
            "ordonnee": intercept,
            "r2": r ** 2,
            "incertitude_pente": std,
            "n": len(x),
            "graphe": str(chemin)
        }
        resultats.append(resultat)

    return resultats

if __name__=="__main__":
    get_results()