# -*- coding: utf-8 -*-
"""Calcul et tracé des raideurs de contact pour différents régimes"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Créer le répertoire pour les images
if not os.path.exists('images'):
    os.makedirs('images')

# =============================================================================
# 1. DONNÉES INITIALES
# =============================================================================

Materiau = pd.DataFrame(
    data={
        "H": [6, 60, 93, 200, 600, 10],
        "Y": [2, 20, 31, 65, 220, 5],
        "E": [1600, 12000, 12000, 20000, 20000, 100]
    },
    index=["Plomb", "cuivre", "cuivre ecroui", "acier doux", "acier allié", "polymère"]
)

Materiau[["H", "Y", "E"]] *= 1e7
Materiau["v"] = [0.3, 0.3, 0.3, 0.3, 0.45, 0.3]
Materiau.loc["acier allié", "v"] = 0.45

# Sélection des matériaux d'intérêt
Materiau1 = Materiau.iloc[[2, 4], :4].copy()  # cuivre ecroui et acier allié
Materiau1.loc["acier allié", "v"] = 0.3

# Rayons des sphères (en mètres)
rayons = np.array([5e-3, 50e-3])  # 5 mm et 50 mm

# =============================================================================
# 2. FONCTIONS DE CALCUL
# =============================================================================

def E_contact(E1, v1, E2, v2):
    """Calcul du module effectif de contact"""
    return 1 / ((1 - v1**2) / E1 + (1 - v2**2) / E2)

def rayon_contact_elastique(delta, R):
    """Rayon de contact en régime élastique : a = sqrt(R * delta)"""
    return np.sqrt(R * delta)

def rayon_contact_elastoplastique(delta, delta1, delta2, R):
    """Rayon de contact en régime élasto-plastique"""
    # Calcul selon la formule de l'aire
    x = (delta - delta1) / (delta2 - delta1)
    A = np.pi * R * delta * (1 - 2*x**3 + 3*x**2)
    # a = sqrt(A/π)
    return np.sqrt(A / np.pi)

def rayon_contact_plastique(delta, R):
    """Rayon de contact en régime plastique : a = sqrt(2Rδ)"""
    return np.sqrt(2 * R * delta)

def raideur_elastique(delta, R, E_star):
    """Raideur en régime élastique : k = 2aE*"""
    a = rayon_contact_elastique(delta, R)
    return 2 * a * E_star

def raideur_elastoplastique(delta, delta1, delta2, R, E_star):
    """Raideur en régime élasto-plastique"""
    a = rayon_contact_elastoplastique(delta, delta1, delta2, R)
    return 2 * a * E_star

def raideur_plastique(delta, R, E_star):
    """Raideur en régime plastique"""
    a = rayon_contact_plastique(delta, R)
    return 2 * a * E_star

# =============================================================================
# 3. CALCUL DES PARAMÈTRES
# =============================================================================

# Calcul du module effectif
for i, mat in enumerate(Materiau1.index):
    E_star = E_contact(
        Materiau1.loc[mat, "E"], Materiau1.loc[mat, "v"],
        Materiau1.loc["acier allié", "E"], Materiau1.loc["acier allié", "v"]
    )
    Materiau1.loc[mat, "E_contact"] = E_star

# Calcul des delta1 et delta2
for R in rayons:
    for mat in Materiau1.index:
        H = Materiau1.loc[mat, "H"]
        E_star = Materiau1.loc[mat, "E_contact"]
        delta1 = 0.9 * R * (H / E_star)**2
        delta2 = 54 * delta1
        
        Materiau1.loc[mat, f"delta1_R{R:.3f}"] = delta1
        Materiau1.loc[mat, f"delta2_R{R:.3f}"] = delta2

print("Paramètres des matériaux:")
print(f"Module effectif E* (GPa):")
print(Materiau1["E_contact"] / 1e9)
print("\n" + "="*80 + "\n")

# =============================================================================
# 4. CALCUL DES RAIDEURS POUR CHAQUE RÉGIME ET CHAQUE CONTACT
# =============================================================================

# Stockage des résultats
resultats_raideurs = {}

for idx_mat, mat in enumerate(Materiau1.index):
    for idx_R, R in enumerate(rayons):
        H = Materiau1.loc[mat, "H"]
        E_star = Materiau1.loc[mat, "E_contact"]
        delta1 = Materiau1.loc[mat, f"delta1_R{R:.3f}"]
        delta2 = Materiau1.loc[mat, f"delta2_R{R:.3f}"]
        
        # Points pour chaque régime
        n_points = 100
        
        # Régime élastique
        delta_el = np.linspace(1e-9, delta1, n_points)
        k_el = raideur_elastique(delta_el, R, E_star)
        a_el = rayon_contact_elastique(delta_el, R)
        
        # Régime élasto-plastique
        delta_ep = np.linspace(delta1*1.001, delta2, n_points)
        k_ep = raideur_elastoplastique(delta_ep, delta1, delta2, R, E_star)
        a_ep = rayon_contact_elastoplastique(delta_ep, delta1, delta2, R)
        
        # Régime plastique
        delta_pl = np.linspace(delta2*1.001, delta2*2, n_points)
        k_pl = raideur_plastique(delta_pl, R, E_star)
        a_pl = rayon_contact_plastique(delta_pl, R)
        
        # Stockage
        key = f"{mat}_R{R*1000:.0f}mm"
        resultats_raideurs[key] = {
            'delta_el': delta_el, 'k_el': k_el, 'a_el': a_el,
            'delta_ep': delta_ep, 'k_ep': k_ep, 'a_ep': a_ep,
            'delta_pl': delta_pl, 'k_pl': k_pl, 'a_pl': a_pl,
            'delta1': delta1, 'delta2': delta2, 'E_star': E_star, 'R': R
        }

# =============================================================================
# 5. TRACÉS DES RAIDEURS
# =============================================================================

# 5.1 Raideurs par régime pour chaque contact individuel
for key, data in resultats_raideurs.items():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Tracé de la raideur
    axes[0].plot(data['delta_el']*1e6, data['k_el']/1e6, 'b-', linewidth=2, label='Élastique')
    axes[0].plot(data['delta_ep']*1e6, data['k_ep']/1e6, 'r-', linewidth=2, label='Élasto-plastique')
    axes[0].plot(data['delta_pl']*1e6, data['k_pl']/1e6, 'g-', linewidth=2, label='Plastique')
    axes[0].axvline(data['delta1']*1e6, color='k', linestyle='--', alpha=0.5, label=f'δ₁ = {data["delta1"]*1e6:.2f} µm')
    axes[0].axvline(data['delta2']*1e6, color='k', linestyle=':', alpha=0.5, label=f'δ₂ = {data["delta2"]*1e6:.2f} µm')
    axes[0].set_xlabel('Déplacement δ (µm)')
    axes[0].set_ylabel('Raideur k (MN/m)')
    axes[0].set_title(f'Raideur de contact - {key}')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Tracé du rayon de contact
    axes[1].plot(data['delta_el']*1e6, data['a_el']*1e3, 'b-', linewidth=2, label='Élastique')
    axes[1].plot(data['delta_ep']*1e6, data['a_ep']*1e3, 'r-', linewidth=2, label='Élasto-plastique')
    axes[1].plot(data['delta_pl']*1e6, data['a_pl']*1e3, 'g-', linewidth=2, label='Plastique')
    axes[1].axvline(data['delta1']*1e6, color='k', linestyle='--', alpha=0.5)
    axes[1].axvline(data['delta2']*1e6, color='k', linestyle=':', alpha=0.5)
    axes[1].set_xlabel('Déplacement δ (µm)')
    axes[1].set_ylabel('Rayon de contact a (mm)')
    axes[1].set_title(f'Rayon de contact - {key}')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Tracé en échelle log-log
    delta_complet = np.concatenate([data['delta_el'], data['delta_ep'], data['delta_pl']])
    k_complet = np.concatenate([data['k_el'], data['k_ep'], data['k_pl']])
    a_complet = np.concatenate([data['a_el'], data['a_ep'], data['a_pl']])
    
    axes[2].loglog(delta_complet*1e6, k_complet/1e6, 'b-', linewidth=2)
    axes[2].axvline(data['delta1']*1e6, color='r', linestyle='--', alpha=0.7, label='Transition élastique')
    axes[2].axvline(data['delta2']*1e6, color='g', linestyle='--', alpha=0.7, label='Transition plastique')
    axes[2].set_xlabel('Déplacement δ (µm)')
    axes[2].set_ylabel('Raideur k (MN/m)')
    axes[2].set_title(f'Raideur (log-log) - {key}')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig(f'images/raideur_{key}.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5.2 Comparaison des raideurs pour tous les contacts
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
couleurs = ['blue', 'red', 'green', 'orange']

for idx, (key, data) in enumerate(resultats_raideurs.items()):
    row = idx // 2
    col = idx % 2
    
    # Régime élastique
    axes[0, 0].plot(data['delta_el']*1e6, data['k_el']/1e6, 
                   color=couleurs[idx], linewidth=2, label=key)
    
    # Régime élasto-plastique
    axes[0, 1].plot(data['delta_ep']*1e6, data['k_ep']/1e6,
                   color=couleurs[idx], linewidth=2, label=key)
    
    # Régime plastique
    axes[1, 0].plot(data['delta_pl']*1e6, data['k_pl']/1e6,
                   color=couleurs[idx], linewidth=2, label=key)
    
    # Complet
    delta_complet = np.concatenate([data['delta_el'], data['delta_ep'], data['delta_pl']])
    k_complet = np.concatenate([data['k_el'], data['k_ep'], data['k_pl']])
    axes[1, 1].plot(delta_complet*1e6, k_complet/1e6,
                   color=couleurs[idx], linewidth=2, label=key)

# Configuration des sous-graphiques
axes[0, 0].set_xlabel('δ (µm)')
axes[0, 0].set_ylabel('k (MN/m)')
axes[0, 0].set_title('Régime Élastique - Raideurs')
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].set_xlabel('δ (µm)')
axes[0, 1].set_ylabel('k (MN/m)')
axes[0, 1].set_title('Régime Élasto-plastique - Raideurs')
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].set_xlabel('δ (µm)')
axes[1, 0].set_ylabel('k (MN/m)')
axes[1, 0].set_title('Régime Plastique - Raideurs')
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].set_xlabel('δ (µm)')
axes[1, 1].set_ylabel('k (MN/m)')
axes[1, 1].set_title('Domaine Complet - Raideurs')
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('images/comparaison_raideurs_tous_contacts.png', dpi=300, bbox_inches='tight')
plt.close()

# 5.3 Tracé en 3D : Raideur en fonction de δ et R
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 10))

# Pour chaque matériau
for idx_mat, mat in enumerate(Materiau1.index):
    ax = fig.add_subplot(2, 2, idx_mat + 1, projection='3d')
    
    # Création d'une grille pour δ et R
    delta_range = np.logspace(-9, -5, 50)  # 1 nm à 10 µm
    R_range = np.logspace(-4, -2, 20)      # 0.1 mm à 10 mm
    
    Delta, R_grid = np.meshgrid(delta_range, R_range)
    K = np.zeros_like(Delta)
    
    for i in range(len(delta_range)):
        for j in range(len(R_range)):
            delta = delta_range[i]
            R_val = R_range[j]
            
            # Calcul de δ1 pour ce rayon
            H = Materiau1.loc[mat, "H"]
            E_star = Materiau1.loc[mat, "E_contact"]
            delta1 = 0.9 * R_val * (H / E_star)**2
            
            # Détermination du régime et calcul de la raideur
            if delta <= delta1:
                a = np.sqrt(R_val * delta)
                K[j, i] = 2 * a * E_star
            else:
                # Approximation pour régime non-élastique
                a = np.sqrt(2 * R_val * delta)  # Approximation plastique
                K[j, i] = 2 * a * E_star
    
    # Tracé 3D
    surf = ax.plot_surface(np.log10(Delta*1e6), np.log10(R_grid*1000), np.log10(K/1e6),
                          cmap='viridis', alpha=0.8)
    
    ax.set_xlabel('log(δ) (log µm)')
    ax.set_ylabel('log(R) (log mm)')
    ax.set_zlabel('log(k) (log MN/m)')
    ax.set_title(f'Raideur 3D - {mat}')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='log(k)')

plt.tight_layout()
plt.savefig('images/raideur_3D.png', dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# 6. ANALYSE DÉTAILLÉE DES RAIDEURS
# =============================================================================

print("ANALYSE DÉTAILLÉE DES RAIDEURS DE CONTACT")
print("="*80)

print("\n1. COMPORTEMENT THÉORIQUE PAR RÉGIME:")
print("-"*50)
print("Régime élastique:")
print("  a = √(Rδ) → k = 2E*√(Rδ)")
print("  ⇒ k ∝ √δ (augmentation en racine carrée)")
print("\nRégime élasto-plastique:")
print("  a = fonction complexe de δ")
print("  ⇒ k augmente moins rapidement")
print("\nRégime plastique:")
print("  a = √(2Rδ) → k = 2E*√(2Rδ)")
print("  ⇒ k ∝ √δ (augmentation en racine carrée, pente √2 plus forte)")

print("\n\n2. VALEURS CARACTÉRISTIQUES (pour δ = δ₁):")
print("-"*50)
for key, data in resultats_raideurs.items():
    mat, R_str = key.split('_')
    R_val = float(R_str.replace('mm', '').replace('R', ''))
    
    # Trouver l'indice le plus proche de δ₁
    idx = np.argmin(np.abs(data['delta_el'] - data['delta1']))
    k_at_delta1 = data['k_el'][idx] if idx < len(data['k_el']) else data['k_el'][-1]
    a_at_delta1 = data['a_el'][idx] if idx < len(data['a_el']) else data['a_el'][-1]
    
    print(f"\n{key}:")
    print(f"  δ₁ = {data['delta1']*1e6:.2f} µm")
    print(f"  a(δ₁) = {a_at_delta1*1e3:.3f} mm")
    print(f"  k(δ₁) = {k_at_delta1/1e6:.2f} MN/m")
    print(f"  E* = {data['E_star']/1e9:.1f} GPa")

print("\n\n3. PENTES CARACTÉRISTIQUES:")
print("-"*50)
print("Pente de la raideur en régime élastique:")
print("  dk/dδ = E*√(R/δ)")
print("  ⇒ La pente diminue lorsque δ augmente")
print("\nComparaison des pentes à δ = δ₁:")
for key, data in resultats_raideurs.items():
    # Calcul numérique de la dérivée
    if len(data['delta_el']) > 1:
        dk = np.diff(data['k_el'])
        dd = np.diff(data['delta_el'])
        pente = dk[-1] / dd[-1] if len(dk) > 0 else 0
        print(f"  {key}: dk/dδ ≈ {pente/1e9:.1e} GN/m²")

print("\n\n4. INFLUENCE DU RAYON:")
print("-"*50)
print("Pour un même matériau et un même δ:")
print("  k ∝ √R  (en régime élastique)")
print("  ⇒ R × 10 → k × √10 ≈ 3.16")
print("\nVérification numérique:")
for mat in Materiau1.index:
    keys = [k for k in resultats_raideurs.keys() if mat in k]
    if len(keys) == 2:
        key_small = keys[0] if '5' in keys[0] else keys[1]
        key_large = keys[1] if key_small == keys[0] else keys[0]
        
        # Comparaison à δ = 1 µm
        delta_ref = 1e-6
        for key in [key_small, key_large]:
            data = resultats_raideurs[key]
            # Interpolation pour δ_ref
            if delta_ref < data['delta_el'][-1]:
                k_ref = np.interp(delta_ref, data['delta_el'], data['k_el'])
                print(f"  {key}: k(δ=1µm) = {k_ref/1e6:.2f} MN/m")

print("\n\n5. INFLUENCE DU MODULE EFFECTIF:")
print("-"*50)
print("k ∝ E* (linéairement pour un même a)")
print("\nComparaison cuivre écroui / acier allié:")
for R in rayons:
    k_cuivre = None
    k_acier = None
    
    for key, data in resultats_raideurs.items():
        if f'R{R*1000:.0f}mm' in key:
            # Valeur à δ = 0.5 µm
            delta_ref = 0.5e-6
            if delta_ref < data['delta_el'][-1]:
                k_ref = np.interp(delta_ref, data['delta_el'], data['k_el'])
                if 'cuivre' in key:
                    k_cuivre = k_ref
                elif 'acier' in key:
                    k_acier = k_ref
    
    if k_cuivre and k_acier:
        ratio = k_acier / k_cuivre
        print(f"  R={R*1000:.0f}mm: k_acier/k_cuivre = {ratio:.2f}")
        print(f"    (E*_acier/E*_cuivre = {Materiau1.loc['acier allié', 'E_contact']/Materiau1.loc['cuivre ecroui', 'E_contact']:.2f})")

print("\n\n6. LIMITES DU MODÈLE:")
print("-"*50)
print("a) Hypothèses du modèle:")
print("   - Contact non-adhésif")
print("   - Matériaux isotropes")
print("   - Petites déformations")
print("   - État de contraintes axisymétrique")
print("\nb) Validité de k = 2aE*:")
print("   - Exact en régime élastique pour contact sphère-plan")
print("   - Approximatif en régime élasto-plastique")
print("   - Nécessite une définition cohérente de a")
print("\nc) Transition entre régimes:")
print("   - Continuité C¹ généralement assurée")
print("   - La raideur augmente continûment")
print("   - La pente peut présenter des discontinuités")

print("\n\n7. APPLICATIONS PRATIQUES:")
print("-"*50)
print("a) Micro-indentation:")
print("   - La raideur mesure la réponse élastique")
print("   - Permet de déterminer E*")
print("   - Information sur l'endommagement")
print("\nb) Conception de mécanismes:")
print("   - Prédiction de la rigidité des contacts")
print("   - Optimisation pour éviter le fluage")
print("   - Dimensionnement des butées")
print("\nc) Caractérisation des matériaux:")
print("   - Détermination des propriétés élasto-plastiques")
print("   - Évaluation de la résistance à l'indentation")
print("   - Étude de l'écrouissage")

print("\n" + "="*80)
print("Toutes les figures ont été sauvegardées dans le dossier 'images/'")
print("="*80)

# =============================================================================
# 7. SAUVEGARDE DES RÉSULTATS NUMÉRIQUES
# =============================================================================

# Création d'un DataFrame avec les résultats principaux
resultats_df = pd.DataFrame()

for key, data in resultats_raideurs.items():
    # Points caractéristiques
    row = {
        'Contact': key,
        'Rayon_R_mm': data['R']*1000,
        'E_star_GPa': data['E_star']/1e9,
        'delta1_µm': data['delta1']*1e6,
        'delta2_µm': data['delta2']*1e6,
    }
    
    # Valeurs à δ = δ₁
    idx = np.argmin(np.abs(data['delta_el'] - data['delta1']))
    if idx < len(data['delta_el']):
        row.update({
            'k_delta1_MN/m': data['k_el'][idx]/1e6,
            'a_delta1_mm': data['a_el'][idx]*1e3,
        })
    
    # Valeurs à δ = δ₂
    if len(data['delta_ep']) > 0:
        idx2 = len(data['delta_ep']) // 2
        row.update({
            'k_delta2_MN/m': data['k_ep'][idx2]/1e6 if idx2 < len(data['k_ep']) else np.nan,
            'a_delta2_mm': data['a_ep'][idx2]*1e3 if idx2 < len(data['a_ep']) else np.nan,
        })
    
    resultats_df = pd.concat([resultats_df, pd.DataFrame([row])], ignore_index=True)

print("\nTableau récapitulatif des résultats:")
print(resultats_df.to_string(index=False))

# Sauvegarde en CSV
resultats_df.to_csv('resultats_raideurs.csv', index=False)
print("\nRésultats sauvegardés dans 'resultats_raideurs.csv'")