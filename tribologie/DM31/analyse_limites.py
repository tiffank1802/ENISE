# -*- coding: utf-8 -*-
"""Analyse des effets des efforts et pressions sur les limites elastiques"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

output_dir = "images"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

Materiau = pd.DataFrame(
    data={
        "H": [6, 60, 93, 200, 600, 10],
        "Y": [2, 20, 31, 65, 220, 5],
        "E": [1600, 12000, 12000, 20000, 20000, 100]
    },
    index=["Plomb", "cuivre", "cuivre ecroui", "acier doux", "acier alle", "polymere"]
)

Materiau[["H", "Y", "E"]] *= 1e7
Materiau["v"] = [0.3, 0.3, 0.3, 0.3, 0.45, 0.3]
Materiau.loc["acier alle", "v"] = 0.45

print("Tableau des proprietes des materiaux:")
print(Materiau[["H", "Y", "E", "v"]])
print("\n" + "="*80 + "\n")

Materiau["P_0y_Tresca"] = 1.6 * Materiau["Y"]
Materiau["P_0y_VonMises"] = 1.67 * Materiau["Y"]
Materiau["P_0y_Tabor"] = 1.1 * Materiau["Y"]

print("Pressions de limite elastique selon differents modeles (en MPa):")
print(Materiau[["P_0y_Tresca", "P_0y_VonMises", "P_0y_Tabor"]] / 1e6)
print("\n" + "="*80 + "\n")

R = np.array([1e-6, 100e-6, 1e-3])

def E_contact(E1, v1, E2, v2):
    return 1 / ((1 - v1**2) / E1 + (1 - v2**2) / E2)

for i in range(len(Materiau)):
    E_star = E_contact(Materiau["E"].iloc[i], Materiau["v"].iloc[i],
                      Materiau.loc["acier alle", "E"], Materiau.loc["acier alle", "v"])
    Materiau.loc[Materiau.index[i], "E_contact"] = E_star

print("Module effectif de contact E* (en GPa):")
print(Materiau["E_contact"] / 1e9)
print("\n" + "="*80 + "\n")

for r in R:
    for p in ["P_0y_Tresca", "P_0y_VonMises", "P_0y_Tabor"]:
        Materiau[f"F_0y_{p}_{r:.0e}"] = [
            ((np.pi**3) * (r**2) * Materiau[p].iloc[i]**3) / (6 * Materiau["E_contact"].iloc[i])
            for i in range(len(Materiau))
        ]

print("Forces de limite elastique (en N) pour differents rayons:")
print(Materiau.iloc[:, -9:])
print("\n" + "="*80 + "\n")

fig, ax = plt.subplots(figsize=(12, 8))
x_pos = np.arange(len(Materiau))
width = 0.25

bars1 = ax.bar(x_pos - width, Materiau["P_0y_Tresca"]/1e6, width, 
               label='Tresca (1.6Y)', color='blue', alpha=0.7)
bars2 = ax.bar(x_pos, Materiau["P_0y_VonMises"]/1e6, width, 
               label='Von Mises (1.67Y)', color='red', alpha=0.7)
bars3 = ax.bar(x_pos + width, Materiau["P_0y_Tabor"]/1e6, width, 
               label='Tabor (1.1Y)', color='green', alpha=0.7)

ax.set_xlabel('Materiaux')
ax.set_ylabel('Pression de limite elastique (MPa)')
ax.set_title('Comparaison des pressions de limite elastique selon differents criteres')
ax.set_xticks(x_pos)
ax.set_xticklabels(Materiau.index, rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3)

for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(f'{output_dir}/comparaison_pressions_limite.png', dpi=300, bbox_inches='tight')
plt.close()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (name, r) in enumerate(zip(['1 um', '100 um', '1 mm'], R)):
    ax = axes[idx]
    x_pos = np.arange(len(Materiau))
    
    data_tresca = Materiau[f"F_0y_P_0y_Tresca_{r:.0e}"]
    data_vonmises = Materiau[f"F_0y_P_0y_VonMises_{r:.0e}"]
    data_tabor = Materiau[f"F_0y_P_0y_Tabor_{r:.0e}"]
    
    ax.bar(x_pos - 0.25, data_tresca, 0.25, label='Tresca', color='blue', alpha=0.7)
    ax.bar(x_pos, data_vonmises, 0.25, label='Von Mises', color='red', alpha=0.7)
    ax.bar(x_pos + 0.25, data_tabor, 0.25, label='Tabor', color='green', alpha=0.7)
    
    ax.set_xlabel('Materiaux')
    ax.set_ylabel('Force de limite elastique (N)')
    ax.set_title(f'Forces de limite elastique - R = {name}')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(Materiau.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

plt.tight_layout()
plt.savefig(f'{output_dir}/comparaison_forces_limite.png', dpi=300, bbox_inches='tight')
plt.close()

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
    ax.set_ylabel('Force de limite elastique (N)')
    ax.set_title(f'{mat}')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xscale('log')

for i in range(len(Materiau), len(axes)):
    axes[i].axis('off')

plt.tight_layout()
plt.savefig(f'{output_dir}/evolution_forces_rayon.png', dpi=300, bbox_inches='tight')
plt.close()

for r in R:
    Materiau[f"delta1_R{r:.0e}"] = [
        0.9 * r * (Materiau["H"].iloc[i] / Materiau["E_contact"].iloc[i])**2
        for i in range(len(Materiau))
    ]
    Materiau[f"delta2_R{r:.0e}"] = 54 * Materiau[f"delta1_R{r:.0e}"]

print("Deplacements de transition delta1 et delta2 (en um):")
for r in R:
    print(f"\nRayon R = {r*1000:.3f} mm:")
    for mat in Materiau.index:
        delta1 = Materiau.loc[mat, f"delta1_R{r:.0e}"] * 1e6
        delta2 = Materiau.loc[mat, f"delta2_R{r:.0e}"] * 1e6
        print(f"  {mat:15s}: delta1 = {delta1:.3f} um, delta2 = {delta2:.2f} um")

print("\n" + "="*80 + "\n")

Materiau["Ratio_VonMises_Tresca"] = Materiau["P_0y_VonMises"] / Materiau["P_0y_Tresca"]
Materiau["Ratio_Tabor_Tresca"] = Materiau["P_0y_Tabor"] / Materiau["P_0y_Tresca"]
Materiau["Ratio_Tabor_VonMises"] = Materiau["P_0y_Tabor"] / Materiau["P_0y_VonMises"]

print("Ratios entre les differents criteres de limite elastique:")
print(Materiau[["Ratio_VonMises_Tresca", "Ratio_Tabor_Tresca", "Ratio_Tabor_VonMises"]])
print("\n" + "="*80 + "\n")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].bar(Materiau.index, Materiau["Ratio_VonMises_Tresca"], color='blue', alpha=0.7)
axes[0].axhline(y=1.67/1.6, color='red', linestyle='--', label='Valeur theorique (1.67/1.6)')
axes[0].set_xlabel('Materiaux')
axes[0].set_ylabel('Ratio')
axes[0].set_title('Ratio Von Mises / Tresca')
axes[0].set_xticklabels(Materiau.index, rotation=45, ha='right')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].bar(Materiau.index, Materiau["Ratio_Tabor_Tresca"], color='green', alpha=0.7)
axes[1].axhline(y=1.1/1.6, color='red', linestyle='--', label='Valeur theorique (1.1/1.6)')
axes[1].set_xlabel('Materiaux')
axes[1].set_ylabel('Ratio')
axes[1].set_title('Ratio Tabor / Tresca')
axes[1].set_xticklabels(Materiau.index, rotation=45, ha='right')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

axes[2].bar(Materiau.index, Materiau["Ratio_Tabor_VonMises"], color='orange', alpha=0.7)
axes[2].axhline(y=1.1/1.67, color='red', linestyle='--', label='Valeur theorique (1.1/1.67)')
axes[2].set_xlabel('Materiaux')
axes[2].set_ylabel('Ratio')
axes[2].set_title('Ratio Tabor / Von Mises')
axes[2].set_xticklabels(Materiau.index, rotation=45, ha='right')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/ratios_criteres_limite.png', dpi=300, bbox_inches='tight')
plt.close()

Materiau.to_csv('resultats_limites_elastiques.csv')
print("Resultats sauvegardes dans 'resultats_limites_elastiques.csv'")

print("\n" + "="*80)
print("FIN DE L'ANALYSE")
print("="*80)
