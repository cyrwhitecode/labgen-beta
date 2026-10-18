import numpy as np
import numbers
import matplotlib.pyplot as plt
from config import OUTPUT_DIR
from services.extract  import extraction_tab

x = np.arange(0, 10, 2)
y = np.array([0, 1, 4, 9, 16])
#x = np.array(tab[x_key], dtype=float)
#y = np.array(tab[y_key], dtype=float)

def polynomial_regress(x, y, degre):

    if len(x) != len(y):
        raise ValueError("X et Y n'ont pas la meme longueur.")
    
    if (not all(isinstance(m, numbers.Number) for m in x)) or (not all(isinstance(n, numbers.Number) for n in y)):
        raise ValueError("Des caracteres non numeriques apparaissent dans les tableaux. Veillez ajuster les valeurs des tableaux.")

    if len(x) < (degre + 2) or len(y) < (degre + 2):
        raise ValueError(f"Il faut au moins {degre + 2} points pour un degre {degre}.")
    else:
        coeffs = np.polyfit(x, y, degre)
    poly_func = np.poly1d(coeffs)

    y_predict = poly_func(x)

    ss_res = np.sum((y - y_predict) ** 2)
    ss_tot =  np.sum((y - np.mean(y)) ** 2)
    if ss_tot==0:
        raise ValueError("Division par 0 impossible. au ss_tot")
    else:
        r2 = 1 - (ss_res / ss_tot)

    return {
        "type": "polynomial",
        "function": poly_func,
        "degre": degre,
        "coeffs": coeffs,
        "score": r2
    }

chemin = OUTPUT_DIR / "Poly_graph.png"
def plot_polynomial_regress(x, y, degre):

    funct, degre, coeffs, score = polynomial_regress(x, y, degre).values()
    xs = np.linspace(min(x), max(x), 200)
    ys = polynomial_regress(x, y, degre)["function"](xs)

    plt.plot(xs, ys, label=f"{coeffs[1]:.2f}")
    plt.scatter(x, y)
    plt.xlabel("xs")
    plt.ylabel("ys")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chemin, dpi=300)
    plt.close()
    

if __name__=="__main__":
    print(polynomial_regress(x, y, 2))
    

