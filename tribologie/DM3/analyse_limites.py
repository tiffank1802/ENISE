# -*- coding: utf-8 -*-
"""Analyse des effets des efforts et pressions sur les limites élastiques"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from scipy.optimize import fsolve

# Créer le répertoire pour les images
if not os.path.exists('images'):
    os.makedirs('images')

# =============================================================================
# 1. DONNÉES INITIALES - REPRISE DU CODE PRÉCÉDENT
# =============================================================================

Materiau = pd.DataFrame(
    data={
        "H": [6, 60, 93, 200, 600, 10],
        "Y": [2, 20, 31, 65, 220, 5],
        "E": [1600, 12000, 12000, 20000, 20000, 100]
    },
    index=["Plomb", "cuivre", "cuivre ecroui", "acier doux", "acier allié", "polymère"]
)

Materiau[["H", "Y", "E"]] *= 1e7  # Conversion en Pa
Materiau["v"] = [0.3, 0.3, 0.3, 0.3, 0.45, 0.3]
Materiau.loc["acier allié", "v"] = 0.45  # Spécifique pour acier allié

print("Tableau des propriétés des matériaux:")
print(Materiau[["H", "Y", "E", "v"]])
print("\n" + "="*80 + "\n")

# =============================================================================
# 2. CALCUL DES PRESSIONS DE LIMITE ÉLASTIQUE SELON DIFFÉRENTS MODÈLES
# =============================================================================

# Calcul des pressions de limite élastique selon différents critères
Materiau["P_0y_Tresca"] = 1.6 * Materiau["Y"]
Materiau["P_0y_VonMises"] = 1.67 * Materiau["Y"]
Materiau["P_0y_Tabor"] = 1.1 * Materiau["Y"]

print("Pressions de limite élastique selon différents modèles (en MPa):")
print(Materiau[["P_0y_Tresca", "P_0y_VonMises", "P_0y_Tabor"]] / 1e6)
print("\n" + "="*80 + "\n")

# =============================================================================
# 3. CALCUL DES FORCES DE LIMITE ÉLASTIQUE POUR DIFFÉRENTS RAYONS
# =============================================================================

# Rayons à étudier (en mètres)
R = np.array([1e-6, 100e-6, 1e-3])  # 1 µm, 100 µm, 1 mm

# Fonction pour calculer le module effectif de contact
def E_contact(E1, v1, E2, v2):
    """Calcul du module effectif de contact"""
    return 1 / ((1 - v1**2) / E1 + (1 - v2**2) / E2)

# Calcul du module effectif de contact (contact avec acier allié)
for i in range(len(Materiau)):
    E_star = E_contact(Materiau["E"].iloc[i], Materiau["v"].iloc[i],
                      Materiau.loc["acier allié", "E"], Materiau.loc["acier allié", "v"])
    Materiau.loc[Materiau.index[i], "E_contact"] = E_star

print("Module effectif de contact E* (en GPa):")
print(Materiau["E_contact"] / 1e9)
print("\n" + "="*80 + "\n")

# Calcul des forces de limite élastique pour chaque rayon et chaque critère
for r in R:
    for p in ["P_0y_Tresca", "P_0y_VonMises", "P_0y_Tabor"]:
        Materiau[f"F_0y_{p}_{r:.0e}"] = [
            ((np.pi**3) * (r**2) * Materiau[p].iloc[i]**3) / (6 * Materiau["E_contact"].iloc[i])
            for i in range(len(Materiau))
        ]

print("Forces de limite élastique (en N) pour différents rayons:")
print(Materiau.iloc[:, -9:])
print("\n" + "="*80 + "\n")

# =============================================================================
# 4. VISUALISATION DES RÉSULTATS
# =============================================================================

# 4.1 Comparaison des pressions de limite élastique
fig, ax = plt.subplots(figsize=(12, 8))
x_pos = np.arange(len(Materiau))
width = 0.25

bars1 = ax.bar(x_pos - width, Materiau["P_0y_Tresca"]/1e6, width, 
               label='Tresca (1.6Y)', color='blue', alpha=0.7)
bars2 = ax.bar(x_pos, Materiau["P_0y_VonMises"]/1e6, width, 
               label='Von Mises (1.67Y)', color='red', alpha=0.7)
bars3 = ax.bar(x_pos + width, Materiau["P_0y_Tabor"]/1e6, width, 
               label='Tabor (1.1Y)', color='green', alpha=0.7)

ax.set_xlabel('Matériaux')
ax.set_ylabel('Pression de limite élastique (MPa)')
ax.set_title('Comparaison des pressions de limite élastique selon différents critères')
ax.set_xticks(x_pos)
ax.set_xticklabels(Materiau.index, rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3)

# Ajout des valeurs sur les barres
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('images/comparaison_pressions_limite.png', dpi=300, bbox_inches='tight')
plt.close()

# 4.2 Forces de limite élastique pour R = 1 mm
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (name, r) in enumerate(zip(['1 µm', '100 µm', '1 mm'], R)):
    ax = axes[idx]
    x_pos = np.arange(len(Materiau))
    
    data_tresca = Materiau[f"F_0y_P_0y_Tresca_{r:.0e}"]
    data_vonmises = Materiau[f"F_0y_P_0y_VonMises_{r:.0e}"]
    data_tabor = Materiau[f"F_0y_P_0y_Tabor_{r:.0e}"]
    
    ax.bar(x_pos - 0.25, data_tresca, 0.25, label='Tresca', color='blue', alpha=0.7)
    ax.bar(x_pos, data_vonmises, 0.25, label='Von Mises', color='red', alpha=0.7)
    ax.bar(x_pos + 0.25, data_tabor, 0.25, label='Tabor', color='green', alpha=0.7)
    
    ax.set_xlabel('Matériaux')
    ax.set_ylabel('Force de limite élastique (N)')
    ax.set_title(f'Forces de limite élastique - R = {name}')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(Materiau.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

plt.tight_layout()
plt.savefig('images/comparaison_forces_limite.png', dpi=300, bbox_inches='tight')
plt.close()

# 4.3 Évolution des forces avec le rayon pour chaque matériau
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, mat in enumerate(Materiau.index):
    ax = axes[idx]
    
    rayons_plot = R
    forces_tresca = []
    forces_vonmises = []
    forces_tabor = []
    
    for r in rayons_plot:
        forces_tresca.append(Materiau.loc[mat, f"F_0y_P_0y_Tresca_{r:.0e}"])
        forces_vonmises.append(Materiau.loc[mat, f"F_0y_P_0y_VonMises_{r:.0e}"])
        forces_tabor.append(Materiau.loc[mat, f"F_0y_P_0y_Tabor_{r:.0e}"])
    
    ax.loglog(rayons_plot*1000, forces_tresca, 'o-', label='Tresca', color='blue', linewidth=2)
    ax.loglog(rayons_plot*1000, forces_vonmises, 's-', label='Von Mises', color='red', linewidth=2)
    ax.loglog(rayons_plot*1000, forces_tabor, '^-', label='Tabor', color='green', linewidth=2)
    
    ax.set_xlabel('Rayon (mm)')
    ax.set_ylabel('Force de limite élastique (N)')
    ax.set_title(f'{mat}')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xscale('log')

# Masquer les axes inutilisés
for i in range(len(Materiau), len(axes)):
    axes[i].axis('off')

plt.tight_layout()
plt.savefig('images/evolution_forces_rayon.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 5. CALCUL DES DÉPLACEMENTS DE LIMITE ÉLASTIQUE
# =============================================================================

# Calcul de δ₁ pour chaque matériau et chaque rayon
for r in R:
    Materiau[f"delta1_R{r:.0e}"] = [
        0.9 * r * (Materiau["H"].iloc[i] / Materiau["E_contact"].iloc[i])**2
        for i in range(len(Materiau))
    ]
    Materiau[f"delta2_R{r:.0e}"] = 54 * Materiau[f"delta1_R{r:.0e}"]

print("Déplacements de transition δ₁ et δ₂ (en µm):")
for r in R:
    print(f"\nRayon R = {r*1000:.3f} mm:")
    for mat in Materiau.index:
        delta1 = Materiau.loc[mat, f"delta1_R{r:.0e}"] * 1e6
        delta2 = Materiau.loc[mat, f"delta2_R{r:.0e}"] * 1e6
        print(f"  {mat:15s}: δ₁ = {delta1:.3f} µm, δ₂ = {delta2:.2f} µm")

print("\n" + "="*80 + "\n")

# =============================================================================
# 6. ANALYSE DE LA SENSIBILITÉ AUX DIFFÉRENTS CRITÈRES
# =============================================================================

# Calcul des ratios entre différents critères
Materiau["Ratio_VonMises_Tresca"] = Materiau["P_0y_VonMises"] / Materiau["P_0y_Tresca"]
Materiau["Ratio_Tabor_Tresca"] = Materiau["P_0y_Tabor"] / Materiau["P_0y_Tresca"]
Materiau["Ratio_Tabor_VonMises"] = Materiau["P_0y_Tabor"] / Materiau["P_0y_VonMises"]

print("Ratios entre les différents critères de limite élastique:")
print(Materiau[["Ratio_VonMises_Tresca", "Ratio_Tabor_Tresca", "Ratio_Tabor_VonMises"]])
print("\n" + "="*80 + "\n")

# 6.1 Visualisation des ratios
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Ratio Von Mises / Tresca
axes[0].bar(Materiau.index, Materiau["Ratio_VonMises_Tresca"], color='blue', alpha=0.7)
axes[0].axhline(y=1.67/1.6, color='red', linestyle='--', label='Valeur théorique (1.67/1.6)')
axes[0].set_xlabel('Matériaux')
axes[0].set_ylabel('Ratio')
axes[0].set_title('Ratio Von Mises / Tresca')
axes[0].set_xticklabels(Materiau.index, rotation=45, ha='right')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Ratio Tabor / Tresca
axes[1].bar(Materiau.index, Materiau["Ratio_Tabor_Tresca"], color='green', alpha=0.7)
axes[1].axhline(y=1.1/1.6, color='red', linestyle='--', label='Valeur théorique (1.1/1.6)')
axes[1].set_xlabel('Matériaux')
axes[0].set_ylabel('Ratio')
axes[1].set_title('Ratio Tabor / Tresca')
axes[1].set_xticklabels(Materiau.index, rotation=45, ha='right')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Ratio Tabor / Von Mises
axes[2].bar(Materiau.index, Materiau["Ratio_Tabor_VonMises"], color='orange', alpha=0.7)
axes[2].axhline(y=1.1/1.67, color='red', linestyle='--', label='Valeur théorique (1.1/1.67)')
axes[2].set_xlabel('Matériaux')
axes[2].set_ylabel('Ratio')
axes[2].set_title('Ratio Tabor / Von Mises')
axes[2].set_xticklabels(Materiau.index, rotation=45, ha='right')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('images/ratios_criteres_limite.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 7. ANALYSE STATISTIQUE ET CONCLUSIONS
# =============================================================================

print("ANALYSE STATISTIQUE DES RÉSULTATS")
print("="*80)

print("\n1. STATISTIQUES DES PRESSIONS DE LIMITE ÉLASTIQUE (en MPa):")
print("-"*50)
for critere in ["P_0y_Tresca", "P_0y_VonMises", "P_0y_Tabor"]:
    pressions = Materiau[critere] / 1e6
    print(f"\n{critere}:")
    print(f"  Min: {pressions.min():.1f} MPa")
    print(f"  Max: {pressions.max():.1f} MPa")
    print(f"  Moyenne: {pressions.mean():.1f} MPa")
    print(f"  Écart-type: {pressions.std():.1f} MPa")

print("\n\n2. VARIATION DES FORCES AVEC LE RAYON:")
print("-"*50)
print("La force de limite élastique varie avec R²:")
print("F ∝ R² × P_y³ / E*")
print("\nPour un matériau donné, quand R augmente:")
for factor in [10, 100, 1000]:
    print(f"  R × {factor} → F × {factor**2:.0e} (si les autres paramètres restent constants)")

print("\n\n3. SENSIBILITÉ AU CHOIX DU CRITÈRE:")
print("-"*50)
print("Différence maximale entre critères:")
print(f"  Von Mises / Tresca: {Materiau['Ratio_VonMises_Tresca'].max():.3f} (matériau: {Materiau.index[Materiau['Ratio_VonMises_Tresca'].argmax()]})")
print(f"  Tabor / Tresca: {Materiau['Ratio_Tabor_Tresca'].min():.3f} (matériau: {Materiau.index[Materiau['Ratio_Tabor_Tresca'].argmin()]})")
print(f"  Écart relatif moyen Tresca→Von Mises: {(Materiau['Ratio_VonMises_Tresca'].mean() - 1)*100:.1f}%")
print(f"  Écart relatif moyen Tresca→Tabor: {(Materiau['Ratio_Tabor_Tresca'].mean() - 1)*100:.1f}%")

print("\n\n4. CLASSEMENT DES MATÉRIAUX PAR RAPPORT À LA LIMITE ÉLASTIQUE:")
print("-"*50)
print("Par pression de limite élastique (critère de Tresca):")
sorted_materials = Materiau.sort_values("P_0y_Tresca", ascending=False)
for i, (mat, row) in enumerate(sorted_materials.iterrows(), 1):
    print(f"  {i:2d}. {mat:15s}: {row['P_0y_Tresca']/1e6:6.1f} MPa")

print("\n\n5. DÉPLACEMENTS CRITIQUES (pour R = 1 mm):")
print("-"*50)
r_ref = 1e-3
for mat in Materiau.index:
    delta1 = Materiau.loc[mat, f"delta1_R{r_ref:.0e}"] * 1e6
    delta2 = Materiau.loc[mat, f"delta2_R{r_ref:.0e}"] * 1e6
    print(f"  {mat:15s}: δ₁ = {delta1:6.3f} µm, δ₂ = {delta2:6.1f} µm")

print("\n\n6. IMPLICATIONS POUR LA CONCEPTION:")
print("-"*50)
print("a) Pour éviter la déformation plastique:")
print("   - Maintenir la pression de contact < P_y selon le critère choisi")
print("   - Considérer le critère le plus conservateur (Tabor) pour la sécurité")
print("   - Tenir compte de l'influence du rayon sur la force critique")
print("\nb) Choix du critère:")
print("   - Tresca: plus simple, conservative pour certains matériaux")
print("   - Von Mises: plus précis pour les matériaux isotropes")
print("   - Tabor: basé sur des mesures expérimentales d'indentation")
print("\nc) Influence des paramètres matériaux:")
print("   - H (dureté): détermine la pression en régime plastique")
print("   - Y (limite élastique): base des critères de limite élastique")
print("   - E (module d'Young): influence la raideur et δ₁")
print("   - ν (coefficient de Poisson): influence légèrement E*")

print("\n\n7. MATÉRIAUX EXTRÊMES:")
print("-"*50)
print("Plus haute limite élastique (Tresca):")
max_mat = Materiau["P_0y_Tresca"].idxmax()
print(f"  {max_mat}: {Materiau.loc[max_mat, 'P_0y_Tresca']/1e6:.1f} MPa")
print("\nPlus faible limite élastique (Tresca):")
min_mat = Materiau["P_0y_Tresca"].idxmin()
print(f"  {min_mat}: {Materiau.loc[min_mat, 'P_0y_Tresca']/1e6:.1f} MPa")
print("\nPlus grand écart entre critères:")
max_diff_mat = Materiau["Ratio_VonMises_Tresca"].idxmax()
print(f"  {max_diff_mat}: Von Mises/Tresca = {Materiau.loc[max_diff_mat, 'Ratio_VonMises_Tresca']:.3f}")

print("\n" + "="*80)
print("FIN DE L'ANALYSE")
print("="*80)

# =============================================================================
# 8. SAUVEGARDE DES RÉSULTATS
# =============================================================================

# Sauvegarde des résultats dans un fichier CSV
Materiau.to_csv('resultats_limites_elastiques.csv')
print("\nRésultats sauvegardés dans 'resultats_limites_elastiques.csv'")

# Création d'un rapport synthétique
with open('rapport_synthese.txt', 'w', encoding='utf-8') as f:
    f.write("RAPPORT SYNTHÈSE - ANALYSE DES LIMITES ÉLASTIQUES\n")
    f.write("="*60 + "\n\n")
    
    f.write("1. PRESSIONS DE LIMITE ÉLASTIQUE (MPa)\n")
    f.write("-"*40 + "\n")
    for mat in Materiau.index:
        f.write(f"{mat:15s}: Tresca={Materiau.loc[mat, 'P_0y_Tresca']/1e6:6.1f}, "
                f"VonMises={Materiau.loc[mat, 'P_0y_VonMises']/1e6:6.1f}, "
                f"Tabor={Materiau.loc[mat, 'P_0y_Tabor']/1e6:6.1f}\n")
    
    f.write("\n\n2. FORCES DE LIMITE ÉLASTIQUE POUR R=1mm (N)\n")
    f.write("-"*40 + "\n")
    for mat in Materiau.index:
        f.write(f"{mat:15s}: Tresca={Materiau.loc[mat, 'F_0y_P_0y_Tresca_1e-03']:.2e}, "
                f"VonMises={Materiau.loc[mat, 'F_0y_P_0y_VonMises_1e-03']:.2e}, "
                f"Tabor={Materiau.loc[mat, 'F_0y_P_0y_Tabor_1e-03']:.2e}\n")
    
    f.write("\n\n3. RECOMMANDATIONS POUR LA CONCEPTION\n")
    f.write("-"*40 + "\n")
    f.write("- Utiliser le critère de Tabor pour des applications critiques\n")
    f.write("- Considérer l'influence significative du rayon sur la force\n")
    f.write("- Vérifier que δ < δ₁ pour éviter toute déformation plastique\n")
    f.write("- Pour les polymères, considérer le comportement viscoélastique\n")

print("Rapport synthèse généré dans 'rapport_synthese.txt'")