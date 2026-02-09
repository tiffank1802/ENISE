import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# =============================================================================
# DONNÉES D'INDENTATION
# =============================================================================

# Noms des colonnes
colonnes = [
    "Echantillon",
    "Rayon_ind_mm",
    "Fmax_mN",
    "Enfmax_um",
    "Fadh_mN",
    "Gamma",
    "Raideur_K_N_m",
    "Module_E_Hz_Pa"
]

# Données du tableau
donnees = [
    # Echantillon, Rayon,   Fmax,     Enfmax,    Fadh,     Gamma,    K,          E_Hz
    ["Jaune",      2.0,   5.1194,   179.1858,  -1.0025,  -0.3342,  53.8335,   44963.0346],
    ["Jaune",      2.0,   5.1360,   179.6499,  -0.9534,  -0.3178,  55.3803,   46195.1840],
    ["Jaune",      2.0,   5.1416,   180.4877,  -0.9263,  -0.3088,  52.7795,   43923.4236],

    ["Rouge",      2.0,   5.2046,   115.9968,  -1.1985,  -0.3995,  81.7079,   84819.5874],
    ["Rouge",      2.0,   5.2377,   115.0264,  -1.1330,  -0.3777,  82.7777,   86291.7986],
    ["Rouge",      2.0,   5.2488,   117.0311,  -1.1219,  -0.3740,  89.7007,   92704.3160],

    ["Vert",       2.0,   5.0738,   296.5754,  -0.6587,  -0.2196,  33.3846,   21673.7160],
    ["Vert",       2.0,   5.1487,   292.9515,  -0.6380,  -0.2127,  31.2176,   20391.8210],
    ["Vert",       2.0,   5.1500,   297.8616,  -0.6258,  -0.2086,  30.9936,   20077.9754],
]

# Conversion en DataFrame
df = pd.DataFrame(donnees, columns=colonnes)


# =============================================================================
# FONCTIONS DE CALCUL
# =============================================================================

def rayon_Hertz():
    """
    Calcule le rayon de contact selon le modèle de Hertz.
    Formule: a = (3*F*R / (4*E*))^(1/3)
    Retourne le rayon en mètres.
    """
    R = df['Rayon_ind_mm'] * 1e-3      # mm -> m
    F = df['Fmax_mN'] * 1e-3           # mN -> N
    E_star = df['Module_E_Hz_Pa']      # déjà en Pa
    
    a_hertz = ((3 * F * R) / (4 * E_star)) ** (1/3)
    return a_hertz  # en mètres


def rayon_JKR():
    """
    Calcule le rayon de contact selon le modèle JKR.
    Formule: a = (3R/(4E*) * (F + 3*pi*gamma*R + sqrt(6*pi*gamma*R*F + (3*pi*gamma*R)^2)))^(1/3)
    Retourne le rayon en mètres.
    """
    R = df['Rayon_ind_mm'] * 1e-3      # mm -> m
    F = df['Fmax_mN'] * 1e-3           # mN -> N
    E_star = df['Module_E_Hz_Pa']      # déjà en Pa
    gamma = np.abs(df['Gamma'])        # énergie de surface (J/m²)
    
    terme_adhesion = 3 * np.pi * gamma * R
    terme_racine = np.sqrt(6 * np.pi * gamma * R * F + terme_adhesion**2)
    
    a_jkr = ((3 * R / (4 * E_star)) * (F + terme_adhesion + terme_racine)) ** (1/3)
    return a_jkr  # en mètres


def coef_frottement_deformation(a):
    """
    Calcule le coefficient de frottement dû à la déformation.
    Formule: mu_def = 4a / (3*pi*R)
    """
    R = df['Rayon_ind_mm'] * 1e-3      # mm -> m
    mu_def = (4 * a) / (3 * np.pi * R)
    return mu_def


# =============================================================================
# CALCULS DES RAYONS ET COEFFICIENTS DE DÉFORMATION
# =============================================================================

# Rayons de contact
df['Rayon_Hertz_m'] = rayon_Hertz()
df['Rayon_JKR_m'] = rayon_JKR()

# Conversion en µm pour lisibilité
df['Rayon_Hertz_um'] = df['Rayon_Hertz_m'] * 1e6
df['Rayon_JKR_um'] = df['Rayon_JKR_m'] * 1e6

# Coefficients de frottement dû à la déformation
df['mu_def_Hertz'] = coef_frottement_deformation(df['Rayon_Hertz_m'])
df['mu_def_JKR'] = coef_frottement_deformation(df['Rayon_JKR_m'])

# Affichage des résultats d'indentation
print("\n=== Rayons de contact calculés ===\n")
print(df[['Echantillon', 'Fmax_mN', 'Rayon_Hertz_um', 'Rayon_JKR_um']].to_string(index=False))

print("\n=== Coefficients de frottement (déformation) ===\n")
print(df[['Echantillon', 'mu_def_Hertz', 'mu_def_JKR']].to_string(index=False))


# =============================================================================
# CHARGEMENT DES DONNÉES DE FROTTEMENT AVEC PANDAS
# =============================================================================

dir1 = "datas1/Frot_J_5mN_5mm_1000µms_1.txt"
dir2 = "datas1/Frot_R_5mN_5mm_1000µms_1.txt"
dir3 = "datas1/Frot_V_5mN_5mm_1000µms_1.txt"

# Noms des colonnes pour les fichiers de frottement
col_frot = ['Deplacement_um', 'Ft_mN', 'Fn_mN', 'Temps_s', 'Fx_Fz']

# Chargement avec pandas
df_jaune_frot = pd.read_csv(dir1, sep='\t', skiprows=11, names=col_frot, 
                            encoding='latin-1', usecols=[0, 1, 2, 3, 4])
df_rouge_frot = pd.read_csv(dir2, sep='\t', skiprows=11, names=col_frot, 
                            encoding='latin-1', usecols=[0, 1, 2, 3, 4])
df_vert_frot = pd.read_csv(dir3, sep='\t', skiprows=11, names=col_frot, 
                           encoding='latin-1', usecols=[0, 1, 2, 3, 4])

# Suppression des lignes vides ou avec des NaN
df_jaune_frot = df_jaune_frot.dropna()
df_rouge_frot = df_rouge_frot.dropna()
df_vert_frot = df_vert_frot.dropna()


# =============================================================================
# CALCUL DU COEFFICIENT DE FROTTEMENT TOTAL (Ft/Fn)
# =============================================================================

# On prend la valeur absolue de Ft car le signe dépend du sens de déplacement
mu_total_jaune = (np.abs(df_jaune_frot['Ft_mN']) / df_jaune_frot['Fn_mN']).mean()
mu_total_rouge = (np.abs(df_rouge_frot['Ft_mN']) / df_rouge_frot['Fn_mN']).mean()
mu_total_vert = (np.abs(df_vert_frot['Ft_mN']) / df_vert_frot['Fn_mN']).mean()

print("\n=== Coefficient de frottement total (moyenne |Ft|/Fn) ===\n")
print(f"Jaune: µ_total = {mu_total_jaune:.6f}")
print(f"Rouge: µ_total = {mu_total_rouge:.6f}")
print(f"Vert:  µ_total = {mu_total_vert:.6f}")


# =============================================================================
# CALCUL DU COEFFICIENT D'ADHÉRENCE
# =============================================================================

# Moyenne du coefficient de déformation par échantillon
mu_def_hertz_jaune = df[df['Echantillon'] == 'Jaune']['mu_def_Hertz'].mean()
mu_def_hertz_rouge = df[df['Echantillon'] == 'Rouge']['mu_def_Hertz'].mean()
mu_def_hertz_vert = df[df['Echantillon'] == 'Vert']['mu_def_Hertz'].mean()

mu_def_jkr_jaune = df[df['Echantillon'] == 'Jaune']['mu_def_JKR'].mean()
mu_def_jkr_rouge = df[df['Echantillon'] == 'Rouge']['mu_def_JKR'].mean()
mu_def_jkr_vert = df[df['Echantillon'] == 'Vert']['mu_def_JKR'].mean()

# Coefficient d'adhérence: µ_adh = µ_total - µ_def
mu_adh_hertz_jaune = mu_total_jaune - mu_def_hertz_jaune
mu_adh_hertz_rouge = mu_total_rouge - mu_def_hertz_rouge
mu_adh_hertz_vert = mu_total_vert - mu_def_hertz_vert

mu_adh_jkr_jaune = mu_total_jaune - mu_def_jkr_jaune
mu_adh_jkr_rouge = mu_total_rouge - mu_def_jkr_rouge
mu_adh_jkr_vert = mu_total_vert - mu_def_jkr_vert

print("\n=== Coefficient d'adhérence (µ_total - µ_def) ===\n")
print("Avec modèle Hertz:")
print(f"  Jaune: µ_adh = {mu_adh_hertz_jaune:.6f}")
print(f"  Rouge: µ_adh = {mu_adh_hertz_rouge:.6f}")
print(f"  Vert:  µ_adh = {mu_adh_hertz_vert:.6f}")
print("\nAvec modèle JKR:")
print(f"  Jaune: µ_adh = {mu_adh_jkr_jaune:.6f}")
print(f"  Rouge: µ_adh = {mu_adh_jkr_rouge:.6f}")
print(f"  Vert:  µ_adh = {mu_adh_jkr_vert:.6f}")


# =============================================================================
# TABLEAU RÉCAPITULATIF
# =============================================================================

df_recap = pd.DataFrame({
    'Echantillon': ['Jaune', 'Rouge', 'Vert'],
    'mu_total': [mu_total_jaune, mu_total_rouge, mu_total_vert],
    'mu_def_Hertz': [mu_def_hertz_jaune, mu_def_hertz_rouge, mu_def_hertz_vert],
    'mu_def_JKR': [mu_def_jkr_jaune, mu_def_jkr_rouge, mu_def_jkr_vert],
    'mu_adh_Hertz': [mu_adh_hertz_jaune, mu_adh_hertz_rouge, mu_adh_hertz_vert],
    'mu_adh_JKR': [mu_adh_jkr_jaune, mu_adh_jkr_rouge, mu_adh_jkr_vert]
})

print("\n=== Tableau récapitulatif ===\n")
print(df_recap.to_string(index=False))


# =============================================================================
# TRACÉ DU GRAPHIQUE
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(df_recap['Echantillon']))  # Position des barres
width = 0.2  # Largeur des barres

# Barres groupées
bars1 = ax.bar(x - 1.5*width, df_recap['mu_total'], width, label='µ total', color='steelblue')
bars2 = ax.bar(x - 0.5*width, df_recap['mu_def_Hertz'], width, label='µ déf (Hertz)', color='orange')
bars3 = ax.bar(x + 0.5*width, df_recap['mu_def_JKR'], width, label='µ déf (JKR)', color='green')
bars4 = ax.bar(x + 1.5*width, df_recap['mu_adh_JKR'], width, label='µ adh (JKR)', color='red')

ax.set_xlabel('Échantillon')
ax.set_ylabel('Coefficient de frottement')
ax.set_title('Décomposition du coefficient de frottement total')
ax.set_xticks(x)
ax.set_xticklabels(df_recap['Echantillon'])
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/coefficients_frottement.png', dpi=150)
plt.show()

print("\n[Graphique sauvegardé: figures/coefficients_frottement.png]")


# =============================================================================
# TRACÉ DES EFFORTS EN FONCTION DU TEMPS
# =============================================================================

# Figure 1: Efforts tangentiels et normaux pour les 3 échantillons
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Échantillon Jaune
axes[0].plot(df_jaune_frot['Temps_s'], df_jaune_frot['Ft_mN'], 'y-', label='Ft (tangentiel)', linewidth=0.8)
axes[0].plot(df_jaune_frot['Temps_s'], df_jaune_frot['Fn_mN'], 'k-', label='Fn (normal)', linewidth=0.8)
axes[0].set_ylabel('Force (mN)')
axes[0].set_title('Échantillon Jaune')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

# Échantillon Rouge
axes[1].plot(df_rouge_frot['Temps_s'], df_rouge_frot['Ft_mN'], 'r-', label='Ft (tangentiel)', linewidth=0.8)
axes[1].plot(df_rouge_frot['Temps_s'], df_rouge_frot['Fn_mN'], 'k-', label='Fn (normal)', linewidth=0.8)
axes[1].set_ylabel('Force (mN)')
axes[1].set_title('Échantillon Rouge')
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)

# Échantillon Vert
axes[2].plot(df_vert_frot['Temps_s'], df_vert_frot['Ft_mN'], 'g-', label='Ft (tangentiel)', linewidth=0.8)
axes[2].plot(df_vert_frot['Temps_s'], df_vert_frot['Fn_mN'], 'k-', label='Fn (normal)', linewidth=0.8)
axes[2].set_ylabel('Force (mN)')
axes[2].set_xlabel('Temps (s)')
axes[2].set_title('Échantillon Vert')
axes[2].legend(loc='upper right')
axes[2].grid(True, alpha=0.3)

plt.suptitle('Évolution des efforts de frottement en fonction du temps', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('figures/efforts_temps.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n[Graphique sauvegardé: figures/efforts_temps.png]")


# Figure 2: Coefficient de frottement instantané en fonction du temps
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Calcul du coefficient de frottement instantané
mu_jaune = np.abs(df_jaune_frot['Ft_mN']) / df_jaune_frot['Fn_mN']
mu_rouge = np.abs(df_rouge_frot['Ft_mN']) / df_rouge_frot['Fn_mN']
mu_vert = np.abs(df_vert_frot['Ft_mN']) / df_vert_frot['Fn_mN']

# Échantillon Jaune
axes[0].plot(df_jaune_frot['Temps_s'], mu_jaune, 'y-', linewidth=0.8)
axes[0].axhline(y=mu_total_jaune, color='k', linestyle='--', label=f'Moyenne = {mu_total_jaune:.2f}')
axes[0].set_ylabel('µ = |Ft|/Fn')
axes[0].set_title('Échantillon Jaune')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim([0, 2.5])

# Échantillon Rouge
axes[1].plot(df_rouge_frot['Temps_s'], mu_rouge, 'r-', linewidth=0.8)
axes[1].axhline(y=mu_total_rouge, color='k', linestyle='--', label=f'Moyenne = {mu_total_rouge:.2f}')
axes[1].set_ylabel('µ = |Ft|/Fn')
axes[1].set_title('Échantillon Rouge')
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim([0, 2.5])

# Échantillon Vert
axes[2].plot(df_vert_frot['Temps_s'], mu_vert, 'g-', linewidth=0.8)
axes[2].axhline(y=mu_total_vert, color='k', linestyle='--', label=f'Moyenne = {mu_total_vert:.2f}')
axes[2].set_ylabel('µ = |Ft|/Fn')
axes[2].set_xlabel('Temps (s)')
axes[2].set_title('Échantillon Vert')
axes[2].legend(loc='upper right')
axes[2].grid(True, alpha=0.3)
axes[2].set_ylim([0, 2.5])

plt.suptitle('Évolution du coefficient de frottement en fonction du temps', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('figures/coefficient_frottement_temps.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n[Graphique sauvegardé: figures/coefficient_frottement_temps.png]")


# Figure 3: Comparaison des 3 échantillons sur un seul graphique
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_jaune_frot['Temps_s'], df_jaune_frot['Ft_mN'], 'y-', label='Jaune', linewidth=0.8, alpha=0.8)
ax.plot(df_rouge_frot['Temps_s'], df_rouge_frot['Ft_mN'], 'r-', label='Rouge', linewidth=0.8, alpha=0.8)
ax.plot(df_vert_frot['Temps_s'], df_vert_frot['Ft_mN'], 'g-', label='Vert', linewidth=0.8, alpha=0.8)

ax.set_xlabel('Temps (s)')
ax.set_ylabel('Effort tangentiel Ft (mN)')
ax.set_title('Comparaison des efforts tangentiels pour les 3 échantillons')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/comparaison_efforts.png', dpi=150)
plt.show()

print("\n[Graphique sauvegardé: figures/comparaison_efforts.png]")
