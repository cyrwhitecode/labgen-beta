import numpy as np
import numbers

values = np.arange(1, 13, 0.4)

# ELEMENTARY COMPUTATIONS -- TYPE A
def get_mean(values):
    return np.mean(values)

def get_std(values):
    return np.std(values, ddof=1)

def get_uncertainty_a(values):
    return get_std(values)/np.sqrt(len(values))

def not_a_number(values):
    for i, elt in enumerate(values):
        if not isinstance(elt, numbers.Number):
            raise TypeError(f"L'element {elt} position {i} n'est pas un nombres. c'est un {type(elt).__name__}")


# ELEMENTARY COMPUTATIONS -- TYPE B
def get_uncertainty_b(a_const, a_lect):
    u_const = a_const/(2*np.sqrt(3))
    u_lect = a_lect/(2*np.sqrt(3))

    u_b = np.sqrt((u_const ** 2) + (u_lect ** 2))
    return u_b


# COMPOUND UNCERTAINTY -- TYPE C
def get_uncertainty_c(a_const, a_lect, values, k=2):
    return k * np.sqrt((get_uncertainty_a(values) ** 2) + (get_uncertainty_b(a_const, a_lect) ** 2))


# UNCERTAINTY PROPAGATION
def relative(value, uncertainty):
    if value==0:
        raise ValueError(f"Division par 0 impossible!")
    else:
        return uncertainty/abs(value)

def accuracy(value, uncertainty):
    return relative(value, uncertainty) * 100

def combi_relatives(relative):
    return np.sqrt(np.sum(relative**2))

## CONSTANTE GRAVITATIONNELLE --> CAS Particulier
def g_from_slope(a, u_a):
    g = 4*(np.pi ** 2)/(a)
    return {
        "g": round(g, 2),
        "u_g": round(g * relative(a, u_a), 2)
    }


# FINAL RESULTS
def stats_serie(values, a_const, a_lect):
    if len(values) < 2:
        raise ValueError("Il faut au moins 2 mesures.")
    not_a_number(values)

    resultats = {
        "type": "Resultats de Calculs d'incertitudes",
        "n": len(values),
        "moyenne": get_mean(values),
        "ecart_type": get_std(values),
        "incertitude type A": get_uncertainty_a(values),
        "incertitude type B": get_uncertainty_b(a_const, a_lect),
        "incertitude type C": get_uncertainty_c(),
        "incertitude relative de la serie": combi_relatives(),
        "precision en (%)": accuracy(),
    }

    return resultats