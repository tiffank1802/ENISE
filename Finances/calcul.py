import numpy as np
import pandas as pd

# -----------------------------
# 1. Paramètres de base
# -----------------------------

# Données de l'année de base (N = dernier exercice connu, ex: 2024)
CA_N = 500_000_000      # Chiffre d'affaires 2024 (exemple, à remplacer)
EBE_N = 40_000_000      # EBE 2024
EBIT_N = 30_000_000     # Résultat d'exploitation 2024
BFR_N = 50_000_000      # BFR 2024
Capex_N = 12_000_000    # Capex 2024 (investissements de maintien/développement)
Dette_financiere_N = 80_000_000  # Dettes financières totales
Tresorerie_N = 10_000_000        # Trésorerie
taux_IS = 0.25
taux_actualisation = 0.08  # 8%
taux_croissance_volume = 0.05
taux_inflation_prix = 0.05
taux_inflation_couts = 0.05
horizon = 5  # 5 ans de projection

# Hypothèse : marge EBE et marge EBIT constantes (à partir de l'année N)
marge_EBE = EBE_N / CA_N
marge_EBIT = EBIT_N / CA_N

# Hypothèse simple : Capex proportionnel au CA
capex_ratio = Capex_N / CA_N

# Hypothèse BFR normatif : BFR en % du CA (à partir de l'année N)
bfr_ratio = BFR_N / CA_N

# -----------------------------
# 2. Projection des flux sur 5 ans
# -----------------------------

annees = [f"N+{t}" for t in range(1, horizon + 1)]
resultats = []

CA_t = CA_N

for t in range(1, horizon + 1):
    # Croissance nominale du CA : volume * prix
    croissance_CA = (1 + taux_croissance_volume) * (1 + taux_inflation_prix) - 1
    CA_t = CA_t * (1 + croissance_CA)

    # EBE et EBIT en gardant les marges constantes
    EBE_t = marge_EBE * CA_t
    EBIT_t = marge_EBIT * CA_t

    # Impôt sur le résultat d'exploitation
    impot_t = max(0, EBIT_t) * taux_IS  # pas d'impôt si EBIT négatif

    # Capex proportionnel au CA
    Capex_t = capex_ratio * CA_t

    # BFR normatif : % du CA
    BFR_t = bfr_ratio * CA_t
    if t == 1:
        delta_BFR_t = BFR_t - BFR_N
    else:
        # variation par rapport à l'année précédente
        BFR_prev = resultats[-1]["BFR"]
        delta_BFR_t = BFR_t - BFR_prev

    # Free Cash Flow (FCF)
    FCF_t = EBE_t - impot_t - delta_BFR_t - Capex_t

    resultats.append({
        "Annee": f"N+{t}",
        "CA": CA_t,
        "EBE": EBE_t,
        "EBIT": EBIT_t,
        "Impots": impot_t,
        "Capex": Capex_t,
        "BFR": BFR_t,
        "Delta_BFR": delta_BFR_t,
        "FCF": FCF_t
    })

df = pd.DataFrame(resultats)

# -----------------------------
# 3. VAN des FCF et valeur terminale
# -----------------------------

# Actualisation des FCF
df["Facteur_actualisation"] = [(1 / (1 + taux_actualisation) ** t) for t in range(1, horizon + 1)]
df["FCF_actualise"] = df["FCF"] * df["Facteur_actualisation"]

VAN_FCF = df["FCF_actualise"].sum()

# Valeur terminale (hypothèse de croissance à long terme g_inf)
g_inf = 0.02  # 2% de croissance à long terme, à adapter
FCF_T = df.iloc[-1]["FCF"]
FCF_T_plus_1 = FCF_T * (1 + g_inf)
Valeur_terminal = FCF_T_plus_1 / (taux_actualisation - g_inf)

Valeur_terminal_actualisee = Valeur_terminal / ((1 + taux_actualisation) ** horizon)

Valeur_entreprise = VAN_FCF + Valeur_terminal_actualisee

# -----------------------------
# 4. Dette nette et valeur des titres
# -----------------------------

Dette_nette = Dette_financiere_N - Tresorerie_N
Valeur_titres = Valeur_entreprise - Dette_nette

# -----------------------------
# 5. Capacité d'endettement et apport en capital
# -----------------------------

# Règle empirique : Dette max ≈ multiple * EBE moyen prévisionnel
multiple_EBE = 3.5
EBE_moyen = df["EBE"].mean()
Dette_max = multiple_EBE * EBE_moyen

Apport_min = max(0, Valeur_titres - Dette_max)

# -----------------------------
# 6. Budget de trésorerie de la holding
# -----------------------------

taux_dette_senior = 0.05
duree_dette = horizon  # 5 ans
Dette_senior = min(Dette_max, Valeur_titres)  # par prudence

# Hypothèse : amortissement linéaire du principal
remboursement_principal_annuel = Dette_senior / duree_dette

treasury = []
tresorerie_debut = Apport_min  # la holding commence avec l'apport en capital

for t in range(1, horizon + 1):
    interets = Dette_senior * taux_dette_senior
    # On suppose que la holding remonte chaque année la totalité du FCF de la cible
    FCF_remonte = df.iloc[t-1]["FCF"]

    tresorerie_fin = tresorerie_debut + FCF_remonte - interets - remboursement_principal_annuel

    treasury.append({
        "Annee": f"N+{t}",
        "Tresorerie_debut": tresorerie_debut,
        "FCF_remonte": FCF_remonte,
        "Interets": interets,
        "Remboursement_principal": remboursement_principal_annuel,
        "Tresorerie_fin": tresorerie_fin
    })

    tresorerie_debut = tresorerie_fin
    Dette_senior -= remboursement_principal_annuel

df_tresorerie = pd.DataFrame(treasury)

# -----------------------------
# 7. Affichage des résultats
# -----------------------------

pd.set_option("display.float_format", lambda x: f"{x:,.0f}")

print("=== Projection des flux (FCF) ===")
print(df[["Annee", "CA", "EBE", "EBIT", "Impots", "Capex", "Delta_BFR", "FCF"]])

print("\n=== VAN des FCF et valeur d'entreprise ===")
print(f"VAN des FCF sur {horizon} ans : {VAN_FCF:,.0f} €")
print(f"Valeur terminale actualisée : {Valeur_terminal_actualisee:,.0f} €")
print(f"Valeur d'entreprise (VE) : {Valeur_entreprise:,.0f} €")

print("\n=== Dette nette et valeur des titres ===")
print(f"Dette nette : {Dette_nette:,.0f} €")
print(f"Valeur des titres : {Valeur_titres:,.0f} €")

print("\n=== Capacité d'endettement et apport en capital ===")
print(f"EBE moyen prévisionnel : {EBE_moyen:,.0f} €")
print(f"Dette max (≈ {multiple_EBE} x EBE moyen) : {Dette_max:,.0f} €")
print(f"Apport en capital minimum : {Apport_min:,.0f} €")

print("\n=== Budget de trésorerie de la holding ===")
print(df_tresorerie)
