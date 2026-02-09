"""
Script pour tracer les courbes de frottement des 3 échantillons silicone.
Génère des figures séparées pour chaque type de tracé.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# CHARGEMENT DES DONNÉES
# =============================================================================

dir1 = "datas1/Frot_J_5mN_5mm_1000µms_1.txt"
dir2 = "datas1/Frot_R_5mN_5mm_1000µms_1.txt"
dir3 = "datas1/Frot_V_5mN_5mm_1000µms_1.txt"

col_frot = ['Deplacement_um', 'Ft_mN', 'Fn_mN', 'Temps_s', 'Fx_Fz']

df_jaune = pd.read_csv(dir1, sep='\t', skiprows=11, names=col_frot, 
                       encoding='latin-1', usecols=[0, 1, 2, 3, 4]).dropna()
df_rouge = pd.read_csv(dir2, sep='\t', skiprows=11, names=col_frot, 
                       encoding='latin-1', usecols=[0, 1, 2, 3, 4]).dropna()
df_vert = pd.read_csv(dir3, sep='\t', skiprows=11, names=col_frot, 
                      encoding='latin-1', usecols=[0, 1, 2, 3, 4]).dropna()

# Calcul des coefficients de frottement instantanés
mu_jaune = np.abs(df_jaune['Ft_mN']) / df_jaune['Fn_mN']
mu_rouge = np.abs(df_rouge['Ft_mN']) / df_rouge['Fn_mN']
mu_vert = np.abs(df_vert['Ft_mN']) / df_vert['Fn_mN']

# Moyennes
mu_moy_jaune = mu_jaune.mean()
mu_moy_rouge = mu_rouge.mean()
mu_moy_vert = mu_vert.mean()

print("=== Chargement des données terminé ===")
print(f"Jaune: {len(df_jaune)} points, µ moyen = {mu_moy_jaune:.3f}")
print(f"Rouge: {len(df_rouge)} points, µ moyen = {mu_moy_rouge:.3f}")
print(f"Vert:  {len(df_vert)} points, µ moyen = {mu_moy_vert:.3f}")


# =============================================================================
# FIGURE 1 : ÉCHANTILLON JAUNE - Efforts vs Temps
# =============================================================================

fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(df_jaune['Temps_s'], df_jaune['Ft_mN'], 'gold', label='Ft (tangentiel)', linewidth=1)
ax1.plot(df_jaune['Temps_s'], df_jaune['Fn_mN'], 'k-', label='Fn (normal)', linewidth=1)

ax1.set_xlabel('Temps (s)', fontsize=12)
ax1.set_ylabel('Force (mN)', fontsize=12)
ax1.set_title('Échantillon Jaune - Efforts de frottement vs Temps', fontsize=14)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/jaune_efforts_temps.png', dpi=150)
plt.close()
print("[1/9] Sauvegardé: figures/jaune_efforts_temps.png")


# =============================================================================
# FIGURE 2 : ÉCHANTILLON ROUGE - Efforts vs Temps
# =============================================================================

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.plot(df_rouge['Temps_s'], df_rouge['Ft_mN'], 'r-', label='Ft (tangentiel)', linewidth=1)
ax2.plot(df_rouge['Temps_s'], df_rouge['Fn_mN'], 'k-', label='Fn (normal)', linewidth=1)

ax2.set_xlabel('Temps (s)', fontsize=12)
ax2.set_ylabel('Force (mN)', fontsize=12)
ax2.set_title('Échantillon Rouge - Efforts de frottement vs Temps', fontsize=14)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/rouge_efforts_temps.png', dpi=150)
plt.close()
print("[2/9] Sauvegardé: figures/rouge_efforts_temps.png")


# =============================================================================
# FIGURE 3 : ÉCHANTILLON VERT - Efforts vs Temps
# =============================================================================

fig3, ax3 = plt.subplots(figsize=(10, 5))

ax3.plot(df_vert['Temps_s'], df_vert['Ft_mN'], 'g-', label='Ft (tangentiel)', linewidth=1)
ax3.plot(df_vert['Temps_s'], df_vert['Fn_mN'], 'k-', label='Fn (normal)', linewidth=1)

ax3.set_xlabel('Temps (s)', fontsize=12)
ax3.set_ylabel('Force (mN)', fontsize=12)
ax3.set_title('Échantillon Vert - Efforts de frottement vs Temps', fontsize=14)
ax3.legend(loc='upper right', fontsize=10)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/vert_efforts_temps.png', dpi=150)
plt.close()
print("[3/9] Sauvegardé: figures/vert_efforts_temps.png")


# =============================================================================
# FIGURE 4 : ÉCHANTILLON JAUNE - Coefficient de frottement vs Temps
# =============================================================================

fig4, ax4 = plt.subplots(figsize=(10, 5))

ax4.plot(df_jaune['Temps_s'], mu_jaune, 'gold', linewidth=0.8, alpha=0.8)
ax4.axhline(y=mu_moy_jaune, color='darkgoldenrod', linestyle='--', linewidth=2, 
            label=f'Moyenne µ = {mu_moy_jaune:.2f}')

ax4.set_xlabel('Temps (s)', fontsize=12)
ax4.set_ylabel('Coefficient de frottement µ = |Ft|/Fn', fontsize=12)
ax4.set_title('Échantillon Jaune - Coefficient de frottement vs Temps', fontsize=14)
ax4.legend(loc='upper right', fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.set_ylim([0, 2.5])

plt.tight_layout()
plt.savefig('figures/jaune_mu_temps.png', dpi=150)
plt.close()
print("[4/9] Sauvegardé: figures/jaune_mu_temps.png")


# =============================================================================
# FIGURE 5 : ÉCHANTILLON ROUGE - Coefficient de frottement vs Temps
# =============================================================================

fig5, ax5 = plt.subplots(figsize=(10, 5))

ax5.plot(df_rouge['Temps_s'], mu_rouge, 'r-', linewidth=0.8, alpha=0.8)
ax5.axhline(y=mu_moy_rouge, color='darkred', linestyle='--', linewidth=2, 
            label=f'Moyenne µ = {mu_moy_rouge:.2f}')

ax5.set_xlabel('Temps (s)', fontsize=12)
ax5.set_ylabel('Coefficient de frottement µ = |Ft|/Fn', fontsize=12)
ax5.set_title('Échantillon Rouge - Coefficient de frottement vs Temps', fontsize=14)
ax5.legend(loc='upper right', fontsize=10)
ax5.grid(True, alpha=0.3)
ax5.set_ylim([0, 2.5])

plt.tight_layout()
plt.savefig('figures/rouge_mu_temps.png', dpi=150)
plt.close()
print("[5/9] Sauvegardé: figures/rouge_mu_temps.png")


# =============================================================================
# FIGURE 6 : ÉCHANTILLON VERT - Coefficient de frottement vs Temps
# =============================================================================

fig6, ax6 = plt.subplots(figsize=(10, 5))

ax6.plot(df_vert['Temps_s'], mu_vert, 'g-', linewidth=0.8, alpha=0.8)
ax6.axhline(y=mu_moy_vert, color='darkgreen', linestyle='--', linewidth=2, 
            label=f'Moyenne µ = {mu_moy_vert:.2f}')

ax6.set_xlabel('Temps (s)', fontsize=12)
ax6.set_ylabel('Coefficient de frottement µ = |Ft|/Fn', fontsize=12)
ax6.set_title('Échantillon Vert - Coefficient de frottement vs Temps', fontsize=14)
ax6.legend(loc='upper right', fontsize=10)
ax6.grid(True, alpha=0.3)
ax6.set_ylim([0, 2.5])

plt.tight_layout()
plt.savefig('figures/vert_mu_temps.png', dpi=150)
plt.close()
print("[6/9] Sauvegardé: figures/vert_mu_temps.png")


# =============================================================================
# FIGURE 7 : ÉCHANTILLON JAUNE - Effort tangentiel vs Déplacement
# =============================================================================

fig7, ax7 = plt.subplots(figsize=(10, 5))

ax7.plot(df_jaune['Deplacement_um']/1000, df_jaune['Ft_mN'], 'gold', linewidth=1)

ax7.set_xlabel('Déplacement (mm)', fontsize=12)
ax7.set_ylabel('Effort tangentiel Ft (mN)', fontsize=12)
ax7.set_title('Échantillon Jaune - Effort tangentiel vs Déplacement', fontsize=14)
ax7.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/jaune_Ft_deplacement.png', dpi=150)
plt.close()
print("[7/9] Sauvegardé: figures/jaune_Ft_deplacement.png")


# =============================================================================
# FIGURE 8 : ÉCHANTILLON ROUGE - Effort tangentiel vs Déplacement
# =============================================================================

fig8, ax8 = plt.subplots(figsize=(10, 5))

ax8.plot(df_rouge['Deplacement_um']/1000, df_rouge['Ft_mN'], 'r-', linewidth=1)

ax8.set_xlabel('Déplacement (mm)', fontsize=12)
ax8.set_ylabel('Effort tangentiel Ft (mN)', fontsize=12)
ax8.set_title('Échantillon Rouge - Effort tangentiel vs Déplacement', fontsize=14)
ax8.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/rouge_Ft_deplacement.png', dpi=150)
plt.close()
print("[8/9] Sauvegardé: figures/rouge_Ft_deplacement.png")


# =============================================================================
# FIGURE 9 : ÉCHANTILLON VERT - Effort tangentiel vs Déplacement
# =============================================================================

fig9, ax9 = plt.subplots(figsize=(10, 5))

ax9.plot(df_vert['Deplacement_um']/1000, df_vert['Ft_mN'], 'g-', linewidth=1)

ax9.set_xlabel('Déplacement (mm)', fontsize=12)
ax9.set_ylabel('Effort tangentiel Ft (mN)', fontsize=12)
ax9.set_title('Échantillon Vert - Effort tangentiel vs Déplacement', fontsize=14)
ax9.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/vert_Ft_deplacement.png', dpi=150)
plt.close()
print("[9/9] Sauvegardé: figures/vert_Ft_deplacement.png")


# =============================================================================
# RÉSUMÉ
# =============================================================================

print("\n" + "="*60)
print("GÉNÉRATION TERMINÉE - 9 figures sauvegardées dans figures/")
print("="*60)
print("\nFichiers générés:")
print("  - jaune_efforts_temps.png    : Ft et Fn vs Temps (Jaune)")
print("  - rouge_efforts_temps.png    : Ft et Fn vs Temps (Rouge)")
print("  - vert_efforts_temps.png     : Ft et Fn vs Temps (Vert)")
print("  - jaune_mu_temps.png         : µ vs Temps (Jaune)")
print("  - rouge_mu_temps.png         : µ vs Temps (Rouge)")
print("  - vert_mu_temps.png          : µ vs Temps (Vert)")
print("  - jaune_Ft_deplacement.png   : Ft vs Déplacement (Jaune)")
print("  - rouge_Ft_deplacement.png   : Ft vs Déplacement (Rouge)")
print("  - vert_Ft_deplacement.png    : Ft vs Déplacement (Vert)")
