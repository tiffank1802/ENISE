#!/usr/bin/env python3
"""
Script de génération des figures pour le rapport de Tribologie - DM2
Contact Hertzien Sphère-Plan
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['legend.fontsize'] = 10

d = 6e-3
R = d / 2
E1 = 210e9
nu1 = 0.3
nu2 = 0.3
F_max = 0.5
delta = 50e-6

a = np.sqrt(R * delta)
E_star = 3 * F_max * R / (4 * a**3)
p0 = 3 * F_max / (2 * np.pi * a**2)
p_moy = F_max / (np.pi * a**2)
K = 2 * a * E_star

E2_num = (1 - nu2**2) / (1/E_star - (1 - nu1**2)/E1)

print(f"Paramètres calculés:")
print(f"Rayon de contact a = {a*1000:.3f} mm")
print(f"Module effectif E* = {E_star/1e9:.1f} GPa")
print(f"Pression max p0 = {p0/1e6:.2f} MPa")
print(f"Pression moy pmoy = {p_moy/1e6:.2f} MPa")
print(f"Raideur K = {K:.1f} N/m")
print(f"Module E2 = {E2_num/1e9:.1f} GPa")

fig1, ax1 = plt.subplots(figsize=(8, 5))
r = np.linspace(0, a, 200)
p = p0 * np.sqrt(1 - (r/a)**2)
ax1.plot(r*1000, p/1e6, 'b-', linewidth=2)
ax1.fill_between(r*1000, p/1e6, alpha=0.3, color='blue')
ax1.axhline(y=p0/1e6, color='r', linestyle='--', alpha=0.7, label=f'$p_0$ = {p0/1e6:.2f} MPa')
ax1.axhline(y=p_moy/1e6, color='g', linestyle='--', alpha=0.7, label=f"$p_{{moy}}$ = {p_moy/1e6:.2f} MPa")
ax1.axvline(x=a*1000, color='k', linestyle=':', alpha=0.5, label=f'$a$ = {a*1000:.3f} mm')
ax1.set_xlabel('Rayon $r$ (mm)')
ax1.set_ylabel('Pression $p$ (MPa)')
ax1.set_title('Profil de pression hertzien')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, a*1000*1.1)
plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/hertz_pressure_profile.png', dpi=150, bbox_inches='tight')
plt.close()

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 5))
delta_range = np.linspace(0, 100e-6, 100)
F = (4/3) * E_star * np.sqrt(R) * delta_range**(3/2)
ax2a.plot(delta_range*1e6, F, 'b-', linewidth=2)
ax2a.set_xlabel('Enfoncement $\\delta$ ($\\mu$m)')
ax2a.set_ylabel('Force $F$ (N)')
ax2a.set_title('Courbe Force-Déplacement')
ax2a.grid(True, alpha=0.3)
ax2a.axvline(x=50, color='r', linestyle='--', alpha=0.7, label='$\\delta$ = 50 $\\mu$m')
ax2a.axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='$F$ = 0.5 N')
ax2a.legend()

contact_strain = delta / (2 * a)
strain_range = delta_range / (2 * a)
p_range = (3 * F / (2 * np.pi * a**2))
ax2b.plot(strain_range*100, p_range/1e6, 'b-', linewidth=2)
ax2b.set_xlabel('Déformation de contact $\\delta/(2a)$ (%)')
ax2b.set_ylabel('Pression de contact $p_0$ (MPa)')
ax2b.set_title('Courbe Contrainte-Déformation')
ax2b.grid(True, alpha=0.3)
ax2b.axvline(x=contact_strain*100, color='r', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/force_displacement_curve.png', dpi=150, bbox_inches='tight')
plt.close()

fig3, ax3 = plt.subplots(figsize=(9, 6))
r_norm = np.linspace(0, 2, 200)
sigma_r = -p0 * ((1 + nu1) * (1 - 2*nu1) / (1 - nu1) - (r_norm**2) / (1 + (r_norm)**2))
sigma_theta = -p0 * ((1 + nu1) * (1 - 2*nu1) / (1 - nu1) + (r_norm**2) / (1 + (r_norm)**2))
sigma_z_vals = np.zeros_like(r_norm)
mask = r_norm <= 1
sigma_z_vals[mask] = -p0 * np.sqrt(1 - r_norm[mask]**2)

ax3.plot(r_norm, sigma_r/p0, 'b-', linewidth=2, label='$\\sigma_r/p_0$')
ax3.plot(r_norm, sigma_theta/p0, 'r-', linewidth=2, label='$\\sigma_\\theta/p_0$')
ax3.plot(r_norm, sigma_z_vals/p0, 'g-', linewidth=2, label='$\\sigma_z/p_0$')
ax3.axvline(x=1, color='k', linestyle='--', alpha=0.5, label='Rayon de contact')
ax3.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax3.set_xlabel('Position normalisée $r/a$')
ax3.set_ylabel('Contrainte normalisée $\\sigma/p_0$')
ax3.set_title('Évolution des contraintes dans le cercle de contact')
ax3.legend()
ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/stress_evolution.png', dpi=150, bbox_inches='tight')
plt.close()

fig4, ax4 = plt.subplots(figsize=(8, 5))
z = np.linspace(0, 3*a, 200)
sigma_z_axis = -p0 / (1 + (z/a)**2)
ax4.plot(z*1000, sigma_z_axis/1e6, 'b-', linewidth=2)
ax4.fill_between(z*1000, sigma_z_axis/1e6, alpha=0.3, color='blue')
ax4.set_xlabel('Profondeur $z$ (mm)')
ax4.set_ylabel('Contrainte $\\sigma_z$ (MPa)')
ax4.set_title('Variation de $\\sigma_z$ avec la profondeur (axe de symétrie)')
ax4.grid(True, alpha=0.3)
ax4.axhline(y=-p0/1e6, color='r', linestyle='--', alpha=0.7, label=f'$\\sigma_{{z, surface}}$ = {p0/1e6:.2f} MPa')
ax4.legend()
plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/sigma_z_depth.png', dpi=150, bbox_inches='tight')
plt.close()

fig5, ax5 = plt.subplots(figsize=(10, 6))
r_range = np.linspace(-2*a, 2*a, 100)
z_range = np.linspace(-a, 3*a, 100)
R_mesh, Z_mesh = np.meshgrid(r_range, z_range)

tau_values = np.zeros_like(R_mesh)
for i in range(Z_mesh.shape[0]):
    for j in range(R_mesh.shape[1]):
        r_val = abs(R_mesh[i, j])
        z_val = Z_mesh[i, j]
        if r_val <= a and z_val >= 0:
            tau_values[i, j] = 0.5 * (p0/2) * (1 - (z_val/a) / np.sqrt(1 + (z_val/a)**2))
        elif z_val >= 0:
            tau_values[i, j] = 0

contour = ax5.contourf(R_mesh*1000, Z_mesh*1000, tau_values/1e6, levels=20, cmap='viridis')
cbar = plt.colorbar(contour, ax=ax5, label='$\\tau$ (MPa)')
ax5.axhline(y=0.24*1000, color='r', linestyle='--', linewidth=2, label=f'$z(\\tau_{{max}})$ = 0.24 mm')
theta = np.linspace(0, 2*np.pi, 100)
ax5.plot(a*1000*np.cos(theta), a*1000*np.sin(theta), 'w-', linewidth=2, label='Cercle de contact')
ax5.set_xlabel('Rayon $r$ (mm)')
ax5.set_ylabel('Profondeur $z$ (mm)')
ax5.set_title('Distribution de la contrainte de cisaillement $\\tau_{max}$')
ax5.legend(loc='upper right')
ax5.set_xlim(-2*a*1000, 2*a*1000)
ax5.set_ylim(-a*1000, 3*a*1000)
plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/shear_stress.png', dpi=150, bbox_inches='tight')
plt.close()

fig6, (ax6a, ax6b) = plt.subplots(1, 2, figsize=(12, 5))

r_surface = np.linspace(0.01*a, 2*a, 200)
u_r = -((1+nu2)*(1-2*nu2))/(2*np.pi*E2_num) * (F_max/r_surface)
u_z_inside = delta - (r_surface[r_surface < a]**2)/(2*R)
u_z_outside = (1-nu2**2)/(np.pi*E2_num) * (F_max/r_surface[r_surface > a])

r_inside = r_surface[r_surface < a]
r_outside = r_surface[r_surface > a]
u_z_inside = delta - (r_inside**2)/(2*R)
u_z_outside = (1-nu2**2)/(np.pi*E2_num) * (F_max/r_outside)

ax6a.plot(r_inside*1000, u_z_inside*1e6, 'b-', linewidth=2, label='r < a')
ax6a.plot(r_outside*1000, u_z_outside*1e6, 'r-', linewidth=2, label='r > a')
ax6a.axvline(x=a*1000, color='k', linestyle='--', alpha=0.5, label='Rayon de contact')
ax6a.set_xlabel('Rayon $r$ (mm)')
ax6a.set_ylabel('Déplacement $u_z$ ($\\mu$m)')
ax6a.set_title('Déplacement vertical à la surface')
ax6a.legend()
ax6a.grid(True, alpha=0.3)

ax6b.plot(r_surface*1000, u_r*1e6, 'g-', linewidth=2)
ax6b.axvline(x=a*1000, color='k', linestyle='--', alpha=0.5, label='Rayon de contact')
ax6b.set_xlabel('Rayon $r$ (mm)')
ax6b.set_ylabel('Déplacement $u_r$ ($\\mu$m)')
ax6b.set_title('Déplacement radial à la surface')
ax6b.legend()
ax6b.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/surface_displacements.png', dpi=150, bbox_inches='tight')
plt.close()

fig7, (ax7a, ax7b) = plt.subplots(1, 2, figsize=(10, 5))

r_points = np.array([1e-3, 2e-3])
u_r_vals = -((1+nu2)*(1-2*nu2))/(2*np.pi*E2_num) * (F_max/r_points)
u_z_vals = (1-nu2**2)/(np.pi*E2_num) * (F_max/r_points)

bars1 = ax7a.bar([1, 2], abs(u_r_vals)*1e6, color=['blue', 'green'], alpha=0.7)
ax7a.set_xlabel('Distance $r$ (mm)')
ax7a.set_ylabel('|$u_r$| ($\\mu$m)')
ax7a.set_title('Déplacement radial à distance')
ax7a.grid(True, alpha=0.3, axis='y')
for i, bar in enumerate(bars1):
    ax7a.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
             f'{abs(u_r_vals[i])*1e6:.3f}', ha='center', va='bottom', fontsize=10)

bars2 = ax7b.bar([1, 2], u_z_vals*1e6, color=['red', 'orange'], alpha=0.7)
ax7b.set_xlabel('Distance $r$ (mm)')
ax7b.set_ylabel('$u_z$ ($\\mu$m)')
ax7b.set_title('Déplacement vertical à distance')
ax7b.grid(True, alpha=0.3, axis='y')
for i, bar in enumerate(bars2):
    ax7b.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
             f'{u_z_vals[i]*1e6:.3f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('/root/ENISE/tribologie/figures/displacements_bars.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nToutes les figures ont été générées avec succès!")
