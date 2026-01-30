import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# ============================================
# CONSTANTES ET DONNEES
# ============================================

E_ACIER = 210e9  # Pa
NU_ACIER = 0.3

R_VALUES = [5e-3, 100e-3]  # Rayons en m
F_VALUES = [50, 500]       # Forces en N

E_MOU = 10e9  # Pa
NU_MOU = 0.3

E1_V2013 = 20e9   # Pa
E2_V2013 = 100e9  # Pa
NU_V2013 = 0.145
F3 = 10e6         # Pression en Pa

# ============================================
# FONCTIONS DE CALCUL
# ============================================

def calcul_module_effectif(E1, nu1, E2, nu2):
    return 1 / ((1 - nu1**2)/E1 + (1 - nu2**2)/E2)

def calcul_rayon_contact_hertz(P, R, E_star):
    return (3 * P * R / (4 * E_star)) ** (1/3)

def calcul_enfoncement(a, R):
    return a**2 / R

def calcul_pression_maximale(P, a):
    return (3 * P) / (2 * np.pi * a**2)

def calcul_pression_moyenne(P, a):
    return P / (np.pi * a**2)

def calcul_raideur_contact(a, E_star):
    return 2 * a * E_star

def calcul_hauteur_bourlet(delta, R):
    return 0.42 * np.sqrt(delta / R)

def profil_pression_hertz(r, p0, a):
    return p0 * np.sqrt(np.maximum(0, 1 - (r / a)**2))

# ============================================
# CALCULS
# ============================================

E_star_mou = calcul_module_effectif(E_ACIER, NU_ACIER, E_MOU, NU_MOU)

resultats_mou = []

for R in R_VALUES:
    for F in F_VALUES:
        a = calcul_rayon_contact_hertz(F, R, E_star_mou)
        delta = calcul_enfoncement(a, R)
        p0 = calcul_pression_maximale(F, a)
        p_moy = calcul_pression_moyenne(F, a)
        K = calcul_raideur_contact(a, E_star_mou)
        h = calcul_hauteur_bourlet(delta, R)
        
        resultats_mou.append({
            'R': R,
            'F': F,
            'a': a,
            'delta': delta,
            'p0': p0,
            'p_moy': p_moy,
            'K': K,
            'h': h
        })

# v2013
R_sphere = 5e-3
R_equiv = R_sphere / 2
E_star_v2013 = calcul_module_effectif(E1_V2013, NU_V2013, E2_V2013, NU_V2013)

a0 = 1e-3
F3_calcul = F3 * np.pi * a0**2

a_v2013 = calcul_rayon_contact_hertz(F3_calcul, R_equiv, E_star_v2013)
delta_v2013 = calcul_enfoncement(a_v2013, R_equiv)
p0_v2013 = calcul_pression_maximale(F3_calcul, a_v2013)
K_v2013 = calcul_raideur_contact(a_v2013, E_star_v2013)

# ============================================
# TRACAGE DES GRAPHIQUES
# ============================================

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Analyses des Contacts Hertzien', fontsize=16, fontweight='bold')

# 1. Profil de pression pour R=5mm, F=50N
ax1 = axes[0, 0]
res = resultats_mou[0]
r = np.linspace(0, res['a']*2, 100)
p = profil_pression_hertz(r, res['p0'], res['a'])

ax1.plot(r*1000, p/1e6, 'b-', linewidth=2)
ax1.fill_between(r*1000, 0, p/1e6, alpha=0.3, color='blue')
ax1.axvline(res['a']*1000, color='red', linestyle='--', 
           label=f'a = {res["a"]*1000:.3f} mm')
ax1.set_xlabel('Distance radiale r [mm]')
ax1.set_ylabel('Pression p(r) [MPa]')
ax1.set_title(f'Profil de pression\nR={res["R"]*1000:.0f}mm, F={res["F"]}N')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_ylim(0, res['p0']/1e6*1.1)

# 2. Courbe force-enfoncement
ax2 = axes[0, 1]
delta_range = np.linspace(1e-6, 100e-6, 100)
F_range = (4/3) * E_star_mou * np.sqrt(R_VALUES[0]) * delta_range**(3/2)

ax2.plot(delta_range*1e6, F_range, 'g-', linewidth=2)
ax2.set_xlabel('Enfoncement delta [um]')
ax2.set_ylabel('Force F [N]')
ax2.set_title('Relation force-enfoncement (Hertz)')
ax2.grid(True, alpha=0.3)

for res in resultats_mou:
    if res['R'] == R_VALUES[0]:
        ax2.plot(res['delta']*1e6, res['F'], 'ro', markersize=8)

# 3. Evolution du rayon de contact avec la force
ax3 = axes[0, 2]
F_test_range = np.linspace(10, 600, 50)
a_test_range = [(3*F*R_VALUES[0]/(4*E_star_mou))**(1/3) for F in F_test_range]

ax3.plot(F_test_range, np.array(a_test_range)*1000, 'r-', linewidth=2)
ax3.set_xlabel('Force F [N]')
ax3.set_ylabel('Rayon de contact a [mm]')
ax3.set_title('Evolution de a avec F (R=5mm)')
ax3.grid(True, alpha=0.3)

# 4. Comparaison des pressions pour differents rayons
ax4 = axes[1, 0]
F_test = 100
for R_test in R_VALUES:
    a_test = calcul_rayon_contact_hertz(F_test, R_test, E_star_mou)
    p0_test = calcul_pression_maximale(F_test, a_test)
    r_test = np.linspace(0, a_test, 100)
    p_test = profil_pression_hertz(r_test, p0_test, a_test)
    
    ax4.plot(r_test*1000, p_test/1e6, 
            label=f'R={R_test*1000:.0f}mm, p0={p0_test/1e6:.1f}MPa')

ax4.set_xlabel('Distance radiale r [mm]')
ax4.set_ylabel('Pression p(r) [MPa]')
ax4.set_title('Profils de pression (F=100N, materiau mou)')
ax4.legend(loc='upper right')
ax4.grid(True, alpha=0.3)

# 5. Hauteur du bourlet en fonction de l'enfoncement
ax5 = axes[1, 1]
delta_h = np.linspace(1e-6, 100e-6, 50)
h_R5 = calcul_hauteur_bourlet(delta_h, R_VALUES[0])
h_R100 = calcul_hauteur_bourlet(delta_h, R_VALUES[1])

ax5.plot(delta_h*1e6, h_R5*1e6, 'b-', label=f'R={R_VALUES[0]*1000:.0f}mm', linewidth=2)
ax5.plot(delta_h*1e6, h_R100*1e6, 'r--', label=f'R={R_VALUES[1]*1000:.0f}mm', linewidth=2)
ax5.set_xlabel('Enfoncement delta [um]')
ax5.set_ylabel('Taille du bourlet h [um]')
ax5.set_title('Taille du bourlet en fonction de delta')
ax5.legend()
ax5.grid(True, alpha=0.3)

# 6. Cisaillement maximal
ax6 = axes[1, 2]
z = np.linspace(0, 2*resultats_mou[0]['a'], 100)
tau_max = np.zeros_like(z)
for i, zi in enumerate(z):
    if zi <= resultats_mou[0]['a']:
        tau_max[i] = 0.31 * resultats_mou[0]['p0']
    else:
        tau_max[i] = 0.31 * resultats_mou[0]['p0'] * (resultats_mou[0]['a']/zi)**2

ax6.plot(z*1000, tau_max/1e6, 'purple', linewidth=2)
ax6.set_xlabel('Profondeur z [mm]')
ax6.set_ylabel('tau_max [MPa]')
ax6.set_title('Cisaillement maximal (R=5mm, F=50N)')
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/DM1/hertz_complete_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print("Graphique principal cree: hertz_complete_analysis.png")

# ============================================
# GRAPHIQUE 2: PROFILS DE PRESSION COMPARES
# ============================================

fig2, ax = plt.subplots(figsize=(10, 6))

colors = ['blue', 'green', 'red', 'orange']
labels = ['R=5mm, F=50N', 'R=5mm, F=500N', 'R=100mm, F=50N', 'R=100mm, F=500N']

for idx, res in enumerate(resultats_mou):
    r = np.linspace(0, res['a']*1.5, 100)
    p = profil_pression_hertz(r, res['p0'], res['a'])
    ax.plot(r*1000, p/1e6, color=colors[idx], linewidth=2, label=labels[idx])
    ax.fill_between(r*1000, 0, p/1e6, alpha=0.1, color=colors[idx])
    ax.axvline(res['a']*1000, color=colors[idx], linestyle='--', alpha=0.5)

ax.set_xlabel('Distance radiale r [mm]', fontsize=12)
ax.set_ylabel('Pression p(r) [MPa]', fontsize=12)
ax.set_title('Profils de pression hertziens pour toutes les configurations', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 3)
ax.set_ylim(0, 1600)

plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/DM1/pressure_profiles.png', dpi=150, bbox_inches='tight')
plt.close()

print("Graphique des profils de pression: pressure_profiles.png")

# ============================================
# GRAPHIQUE 3: EVOLUTION AVEC LA FORCE
# ============================================

fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Rayon de contact
F_range = np.linspace(10, 600, 100)
for R in R_VALUES:
    a_range = [(3*F*R/(4*E_star_mou))**(1/3) for F in F_range]
    ax1.plot(F_range, np.array(a_range)*1000, linewidth=2, label=f'R={R*1000:.0f}mm')

ax1.set_xlabel('Force F [N]', fontsize=12)
ax1.set_ylabel('Rayon de contact a [mm]', fontsize=12)
ax1.set_title('Evolution du rayon de contact avec la force', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Enfoncement
for R in R_VALUES:
    a_range = [(3*F*R/(4*E_star_mou))**(1/3) for F in F_range]
    delta_range = [a**2/R for a in a_range]
    ax2.plot(F_range, np.array(delta_range)*1e6, linewidth=2, label=f'R={R*1000:.0f}mm')

ax2.set_xlabel('Force F [N]', fontsize=12)
ax2.set_ylabel('Enfoncement delta [um]', fontsize=12)
ax2.set_title('Evolution de l\'enfoncement avec la force', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/DM1/evolution_with_force.png', dpi=150, bbox_inches='tight')
plt.close()

print("Graphique evolution avec la force: evolution_with_force.png")

# ============================================
# GRAPHIQUE 4: HAUTEUR DU BOURLET
# ============================================

fig4, ax = plt.subplots(figsize=(10, 6))

for res in resultats_mou:
    delta_plot = np.linspace(res['delta']*0.1, res['delta']*2, 50)
    h_plot = calcul_hauteur_bourlet(delta_plot, res['R'])
    ax.plot(delta_plot*1e6, h_plot*1e6, linewidth=2, 
           label=f'R={res["R"]*1000:.0f}mm, F={res["F"]}N')
    ax.scatter(res['delta']*1e6, res['h']*1e6, s=100, zorder=5)

ax.set_xlabel('Enfoncement delta [um]', fontsize=12)
ax.set_ylabel('Taille du bourlet h [um]', fontsize=12)
ax.set_title('Taille du bourlet en fonction de l\'enfoncement', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/DM1/bourlet_height.png', dpi=150, bbox_inches='tight')
plt.close()

print("Graphique du bourlet: bourlet_height.png")

print("\nTous les graphiques ont ete generes avec succes!")
