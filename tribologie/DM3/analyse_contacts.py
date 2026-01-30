# -*- coding: utf-8 -*-
"""Analyse complète des contacts non-adhesifs elastique, elasto-plastique et plastique"""

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

Materiau1 = Materiau.iloc[[2, 4], :4].copy()
Materiau1.loc["acier alle", "v"] = 0.3

rayons = np.array([5e-3, 50e-3])

def E_contact(E1, v1, E2, v2):
    return 1 / ((1 - v1**2) / E1 + (1 - v2**2) / E2)

def calcul_regime_elastique(delta, R, E_star):
    F = (4/3) * E_star * np.sqrt(R) * delta**1.5
    A = np.pi * R * delta
    P = (4 * E_star) / (3 * np.pi) * np.sqrt(delta / R)
    return F, A, P

def calcul_regime_elastoplastique(delta, delta1, delta2, R, H, E_star):
    if np.all(delta > delta1) and np.all(delta <= delta2):
        terme_log = (np.log(delta2) - np.log(delta)) / (np.log(delta2) - np.log(delta1))
        P = H * (1 - 0.6 * terme_log)
    else:
        P = np.zeros_like(delta)
    
    x = (delta - delta1) / (delta2 - delta1)
    A = np.pi * R * delta * (1 - 2*x**3 + 3*x**2)
    
    F = P * A
    
    return F, A, P

def calcul_regime_plastique(delta, R, H):
    A = 2 * np.pi * R * delta
    P = H * np.ones_like(delta)
    F = A * P
    return F, A, P

for i, mat in enumerate(Materiau1.index):
    E_star = E_contact(
        Materiau1.loc[mat, "E"], Materiau1.loc[mat, "v"],
        Materiau1.loc["acier alle", "E"], Materiau1.loc["acier alle", "v"]
    )
    Materiau1.loc[mat, "E_contact"] = E_star

for R in rayons:
    for mat in Materiau1.index:
        H = Materiau1.loc[mat, "H"]
        E_star = Materiau1.loc[mat, "E_contact"]
        delta1 = 0.9 * R * (H / E_star)**2
        delta2 = 54 * delta1
        
        Materiau1.loc[mat, f"delta1_R{R:.3f}"] = delta1
        Materiau1.loc[mat, f"delta2_R{R:.3f}"] = delta2

print("Parametres des materiaux:")
print(Materiau1)
print("\n" + "="*80 + "\n")

n_points = 500
couleurs = ['blue', 'red', 'green', 'orange']

for idx_mat, mat in enumerate(Materiau1.index):
    for idx_R, R in enumerate(rayons):
        H = Materiau1.loc[mat, "H"]
        E_star = Materiau1.loc[mat, "E_contact"]
        delta1 = Materiau1.loc[mat, f"delta1_R{R:.3f}"]
        delta2 = Materiau1.loc[mat, f"delta2_R{R:.3f}"]
        
        delta_elastique = np.linspace(1e-9, delta1, n_points//3)
        F_el, A_el, P_el = calcul_regime_elastique(delta_elastique, R, E_star)
        
        delta_elastoplastique = np.linspace(delta1*1.001, delta2, n_points//3)
        F_ep, A_ep, P_ep = calcul_regime_elastoplastique(delta_elastoplastique, delta1, delta2, R, H, E_star)
        
        delta_plastique = np.linspace(delta2*1.001, delta2*2, n_points//3)
        F_pl, A_pl, P_pl = calcul_regime_plastique(delta_plastique, R, H)
        
        delta_complet = np.concatenate([delta_elastique, delta_elastoplastique, delta_plastique])
        F_complet = np.concatenate([F_el, F_ep, F_pl])
        A_complet = np.concatenate([A_el, A_ep, A_pl])
        P_complet = np.concatenate([P_el, P_ep, P_pl])
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        axes[0].plot(delta_elastique*1e6, F_el, 'b-', linewidth=2, label='Elastique')
        axes[0].plot(delta_elastoplastique*1e6, F_ep, 'r-', linewidth=2, label='Elasto-plastique')
        axes[0].plot(delta_plastique*1e6, F_pl, 'g-', linewidth=2, label='Plastique')
        axes[0].axvline(delta1*1e6, color='k', linestyle='--', alpha=0.5, label=f'delta1 = {delta1*1e6:.2f} um')
        axes[0].axvline(delta2*1e6, color='k', linestyle=':', alpha=0.5, label=f'delta2 = {delta2*1e6:.2f} um')
        axes[0].set_xlabel('Deplacement delta (um)')
        axes[0].set_ylabel('Force F (N)')
        axes[0].set_title(f'Force - {mat} - R = {R*1000:.0f} mm')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(delta_elastique*1e6, P_el/1e6, 'b-', linewidth=2, label='Elastique')
        axes[1].plot(delta_elastoplastique*1e6, P_ep/1e6, 'r-', linewidth=2, label='Elasto-plastique')
        axes[1].plot(delta_plastique*1e6, P_pl/1e6, 'g-', linewidth=2, label='Plastique')
        axes[1].axhline(H/1e6, color='k', linestyle='--', alpha=0.3, label=f'H = {H/1e6:.0f} MPa')
        axes[1].axvline(delta1*1e6, color='k', linestyle='--', alpha=0.5)
        axes[1].axvline(delta2*1e6, color='k', linestyle=':', alpha=0.5)
        axes[1].set_xlabel('Deplacement delta (um)')
        axes[1].set_ylabel('Pression P (MPa)')
        axes[1].set_title(f'Pression - {mat} - R = {R*1000:.0f} mm')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(delta_elastique*1e6, A_el*1e6, 'b-', linewidth=2, label='Elastique')
        axes[2].plot(delta_elastoplastique*1e6, A_ep*1e6, 'r-', linewidth=2, label='Elasto-plastique')
        axes[2].plot(delta_plastique*1e6, A_pl*1e6, 'g-', linewidth=2, label='Plastique')
        axes[2].axvline(delta1*1e6, color='k', linestyle='--', alpha=0.5)
        axes[2].axvline(delta2*1e6, color='k', linestyle=':', alpha=0.5)
        axes[2].set_xlabel('Deplacement delta (um)')
        axes[2].set_ylabel('Aire A (mm2)')
        axes[2].set_title(f'Aire - {mat} - R = {R*1000:.0f} mm')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/contact_{mat}_R{int(R*1000)}_par_regime.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        axes[0].plot(delta_complet*1e6, F_complet, 'b-', linewidth=2)
        axes[0].axvline(delta1*1e6, color='r', linestyle='--', alpha=0.7, label='Transition elastique')
        axes[0].axvline(delta2*1e6, color='g', linestyle='--', alpha=0.7, label='Transition plastique')
        axes[0].set_xlabel('Deplacement delta (um)')
        axes[0].set_ylabel('Force F (N)')
        axes[0].set_title(f'Force complete - {mat} - R = {R*1000:.0f} mm')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(delta_complet*1e6, P_complet/1e6, 'b-', linewidth=2)
        axes[1].axhline(H/1e6, color='k', linestyle='--', alpha=0.5, label=f'H = {H/1e6:.0f} MPa')
        axes[1].axvline(delta1*1e6, color='r', linestyle='--', alpha=0.7)
        axes[1].axvline(delta2*1e6, color='g', linestyle='--', alpha=0.7)
        axes[1].set_xlabel('Deplacement delta (um)')
        axes[1].set_ylabel('Pression P (MPa)')
        axes[1].set_title(f'Pression complete - {mat} - R = {R*1000:.0f} mm')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(delta_complet*1e6, A_complet*1e6, 'b-', linewidth=2)
        axes[2].axvline(delta1*1e6, color='r', linestyle='--', alpha=0.7)
        axes[2].axvline(delta2*1e6, color='g', linestyle='--', alpha=0.7)
        axes[2].set_xlabel('Deplacement delta (um)')
        axes[2].set_ylabel('Aire A (mm2)')
        axes[2].set_title(f'Aire complete - {mat} - R = {R*1000:.0f} mm')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/contact_{mat}_R{int(R*1000)}_complet.png', dpi=300, bbox_inches='tight')
        plt.close()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

for idx_mat, mat in enumerate(Materiau1.index):
    for idx_R, R in enumerate(rayons):
        H = Materiau1.loc[mat, "H"]
        E_star = Materiau1.loc[mat, "E_contact"]
        delta1 = Materiau1.loc[mat, f"delta1_R{R:.3f}"]
        delta2 = Materiau1.loc[mat, f"delta2_R{R:.3f}"]
        
        delta_el = np.linspace(1e-9, delta1, 100)
        delta_ep = np.linspace(delta1*1.001, delta2, 100)
        delta_pl = np.linspace(delta2*1.001, delta2*2, 100)
        
        delta_all = np.concatenate([delta_el, delta_ep, delta_pl])
        
        F_el, _, _ = calcul_regime_elastique(delta_el, R, E_star)
        F_ep, _, _ = calcul_regime_elastoplastique(delta_ep, delta1, delta2, R, H, E_star)
        F_pl, _, _ = calcul_regime_plastique(delta_pl, R, H)
        
        F_all = np.concatenate([F_el, F_ep, F_pl])
        
        axes[0, 0].plot(delta_el*1e6, F_el, color=couleurs[idx_mat*2 + idx_R], 
                       linestyle='-', linewidth=2, 
                       label=f'{mat} - R={R*1000:.0f}mm (Elastique)')
        axes[0, 1].plot(delta_ep*1e6, F_ep, color=couleurs[idx_mat*2 + idx_R], 
                       linestyle='-', linewidth=2,
                       label=f'{mat} - R={R*1000:.0f}mm (Elasto-plastique)')
        axes[1, 0].plot(delta_pl*1e6, F_pl, color=couleurs[idx_mat*2 + idx_R], 
                       linestyle='-', linewidth=2,
                       label=f'{mat} - R={R*1000:.0f}mm (Plastique)')
        axes[1, 1].plot(delta_all*1e6, F_all, color=couleurs[idx_mat*2 + idx_R], 
                       linestyle='-', linewidth=2,
                       label=f'{mat} - R={R*1000:.0f}mm (Complet)')

axes[0, 0].set_xlabel('delta (um)')
axes[0, 0].set_ylabel('Force F (N)')
axes[0, 0].set_title('Regime Elastique - Tous les contacts')
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].set_xlabel('delta (um)')
axes[0, 1].set_ylabel('Force F (N)')
axes[0, 1].set_title('Regime Elasto-plastique - Tous les contacts')
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].set_xlabel('delta (um)')
axes[1, 0].set_ylabel('Force F (N)')
axes[1, 0].set_title('Regime Plastique - Tous les contacts')
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].set_xlabel('delta (um)')
axes[1, 1].set_ylabel('Force F (N)')
axes[1, 1].set_title('Domaine Complet - Tous les contacts')
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/comparaison_forces_tous_contacts.png', dpi=300, bbox_inches='tight')
plt.close()

print("="*80)
print("ANALYSE DES RESULTATS")
print("="*80)

print("\n1. COMPARAISON DES PARAMETRES DE TRANSITION:")
print("-"*50)

for mat in Materiau1.index:
    for R in rayons:
        delta1 = Materiau1.loc[mat, f"delta1_R{R:.3f}"]
        delta2 = Materiau1.loc[mat, f"delta2_R{R:.3f}"]
        print(f"{mat:15s} - R={R*1000:4.0f} mm: delta1 = {delta1*1e6:6.2f} um, delta2 = {delta2*1e6:6.2f} um")

print("\n2. INFLUENCE DU RAYON:")
print("-"*50)
print("Pour un meme materiau, un rayon plus grand:")
print("- Augmente delta1 et delta2 proportionnellement")
print("- Reduit la pression pour un meme deplacement")
print("- Augmente l'aire de contact")
print("- Augmente la force necessaire pour atteindre un meme delta")

print("\n3. INFLUENCE DU MATERIAU:")
print("-"*50)
print("Cuivre ecroui vs Acier alle:")
print("- Acier alle: H plus eleve -> transitions a plus faible delta")
print("- Acier alle: module E plus eleve -> rigidite plus grande")
print("- Acier alle: necessite plus de force pour meme penetration")

print("\n4. COMPORTEMENT PAR REGIME:")
print("-"*50)
print("Regime elastique: F ∝ delta^(3/2), P ∝ √delta")
print("Regime elasto-plastique: transition progressive, P → H")
print("Regime plastique: F ∝ delta, P = H (constant)")
print("L'aire augmente lineairement avec delta en regime plastique")

print("\n5. IMPLICATIONS POUR LA CONCEPTION:")
print("-"*50)
print("- Pour eviter la deformation plastique: maintenir delta < delta1")
print("- Pour les contacts repetes: eviter l'accumulation de deformation plastique")
print("- Choix du rayon selon l'application: grand rayon pour repartirl la charge")
print("- Importance du rapport H/E pour la resistance a l'indentation")

print("\n" + "="*80)
print("Toutes les figures ont ete sauvegardees dans le dossier 'images/'")
print("="*80)
