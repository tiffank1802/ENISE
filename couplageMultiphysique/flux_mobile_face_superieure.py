"""
Simulation de flux thermique mobile sur la face supérieure uniquement.
Le flux est appliqué au centre de la face supérieure (Z=H) et se déplace le long de X.
"""

from ansys.mapdl.core import launch_mapdl
import numpy as np
import matplotlib.pyplot as plt

# =========================
# LANCEMENT MAPDL
# =========================
mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
mapdl.title('Flux mobile sur face superieure uniquement')

# =========================
# GÉOMÉTRIE ET MAILLAGE 3D
# =========================
L = 0.1      # 10 cm de long (X)
W = 0.02     # 2 cm de large (Y)
H = 0.01     # 1 cm d'épaisseur (Z)

print(f"Creation geometrie: {L*1000}x{W*1000}x{H*1000} mm")

mapdl.block(0, L, 0, W, 0, H)

# Élément thermique 3D
mapdl.et(1, 'SOLID70')

# Maillage
mapdl.esize(0.002)
mapdl.vmesh('ALL')

num_elem = mapdl.mesh.n_elem
num_nodes = mapdl.mesh.n_node
print(f"Maillage: {num_elem} elements, {num_nodes} noeuds")

# =========================
# CRÉER UN COMPONENT POUR LA FACE SUPÉRIEURE UNIQUEMENT
# =========================
# Sélectionner UNIQUEMENT les nœuds sur Z = H (face supérieure)
mapdl.nsel('S', 'LOC', 'Z', H - 1e-6, H + 1e-6)
top_nodes = mapdl.mesh.nnum.copy()
mapdl.cm('TOP_FACE', 'NODE')
print(f"Nombre de noeuds sur la face superieure: {len(top_nodes)}")

mapdl.allsel()

# =========================
# MATÉRIAU - ACIER
# =========================
mapdl.mp('KXX', 1, 50.0)      # Conductivité thermique (W/m·K)
mapdl.mp('KYY', 1, 50.0)
mapdl.mp('KZZ', 1, 50.0)
mapdl.mp('DENS', 1, 7850)     # Densité (kg/m³)
mapdl.mp('C', 1, 460)         # Capacité calorifique (J/kg·K)

print("\nProprietes materiau (Acier):")
print(f"  Conductivite: 50 W/m.K")
print(f"  Densite: 7850 kg/m3")
print(f"  Capacite thermique: 460 J/kg.K")

# =========================
# CONDITIONS INITIALES
# =========================
mapdl.ic('ALL', 'TEMP', 20.0)

# Convection sur face inférieure seulement (contact avec support)
mapdl.nsel('S', 'LOC', 'Z', -1e-6, 1e-6)
mapdl.sf('ALL', 'CONV', 100.0, 20.0)
mapdl.allsel()

# =========================
# PARAMÈTRES DU FLUX MOBILE
# =========================
total_time = 30.0       # Durée totale (s)
dt = 0.2                # Pas de temps (s)
num_steps = int(total_time / dt)

flux_value = 2e5        # 200 kW/m²
x_start = 0.01          # Position initiale X (m)
velocity = 0.003        # Vitesse de déplacement 3 mm/s
spot_radius = 0.006     # Rayon du spot 6 mm
y_center = W / 2.0      # Centre en Y (milieu de la largeur)

print(f"\n=== PARAMETRES FLUX MOBILE ===")
print(f"Intensite flux: {flux_value/1000:.0f} kW/m2")
print(f"Vitesse: {velocity*1000:.1f} mm/s")
print(f"Rayon spot: {spot_radius*1000:.0f} mm")
print(f"Position Y du centre: {y_center*1000:.1f} mm (centre de la piece)")
print(f"Temps total: {total_time} s")
print(f"Nombre de pas: {num_steps}")

# =========================
# SOLUTION TRANSITOIRE
# =========================
mapdl.slashsolu()
mapdl.antype('TRANS')
mapdl.trnopt('FULL')

mapdl.time(0)
mapdl.autots('ON')
mapdl.deltim(dt, dt/10, dt*2)
mapdl.kbc(0)
mapdl.tref(20)
mapdl.outres('ALL', 'ALL')

# =========================
# BOUCLE PRINCIPALE - FLUX MOBILE
# =========================
print("\n=== DEBUT SIMULATION ===")
print("Temps(s) | Position(mm) | Noeuds spot | Tmax(C)")
print("-" * 55)

results = {'time': [], 'x_pos': [], 'T_max': [], 'T_min': [], 'n_nodes': []}

for step in range(num_steps + 1):
    current_time = step * dt
    
    # Position actuelle du spot
    x_center = x_start + velocity * current_time
    
    # Arrêter si le spot sort de la pièce
    if x_center > L - spot_radius:
        print(f"Spot sort de la piece a t={current_time:.1f}s")
        break
    
    # 1. SUPPRIMER TOUS LES FLUX PRÉCÉDENTS
    mapdl.allsel()
    mapdl.sfdele('ALL', 'HFLUX')
    
    # 2. SÉLECTIONNER LES NŒUDS DU SPOT SUR LA FACE SUPÉRIEURE UNIQUEMENT
    
    # D'abord sélectionner UNIQUEMENT la face supérieure (Z = H)
    mapdl.nsel('S', 'LOC', 'Z', H - 1e-6, H + 1e-6)
    
    # Puis restreindre à la zone du spot (rectangle englobant)
    x_min = max(0, x_center - spot_radius)
    x_max = min(L, x_center + spot_radius)
    y_min = max(0, y_center - spot_radius)
    y_max = min(W, y_center + spot_radius)
    
    mapdl.nsel('R', 'LOC', 'X', x_min, x_max)
    mapdl.nsel('R', 'LOC', 'Y', y_min, y_max)
    
    # Récupérer les nœuds sélectionnés
    selected_nodes = mapdl.mesh.nnum
    
    # Filtrer pour garder uniquement les nœuds dans le cercle du spot
    spot_nodes = []
    for node in selected_nodes:
        x = mapdl.queries.nx(node)
        y = mapdl.queries.ny(node)
        distance = np.sqrt((x - x_center)**2 + (y - y_center)**2)
        if distance <= spot_radius:
            spot_nodes.append(node)
    
    # 3. APPLIQUER LE FLUX UNIQUEMENT SUR CES NŒUDS
    if len(spot_nodes) > 0:
        # Sélectionner uniquement les nœuds du spot
        mapdl.nsel('NONE')
        for node in spot_nodes:
            mapdl.nsel('A', 'NODE', '', node)
        
        # Appliquer le flux thermique
        mapdl.sf('ALL', 'HFLUX', flux_value)
        n_nodes_flux = len(spot_nodes)
    else:
        n_nodes_flux = 0
        print(f"Attention: aucun noeud dans le spot a t={current_time:.1f}s")
    
    # 4. RÉSOUDRE
    mapdl.allsel()  # Important: resélectionner tout pour la résolution
    mapdl.time(current_time + dt)
    mapdl.solve()
    
    # 5. SUIVI DES RÉSULTATS (tous les 5 pas)
    if step % 5 == 0:
        mapdl.post1()
        mapdl.set('LAST')
        all_temps = mapdl.post_processing.nodal_temperature()
        T_max = np.max(all_temps)
        T_min = np.min(all_temps)
        
        results['time'].append(current_time)
        results['x_pos'].append(x_center * 1000)
        results['T_max'].append(T_max)
        results['T_min'].append(T_min)
        results['n_nodes'].append(n_nodes_flux)
        
        print(f"{current_time:6.1f}   | {x_center*1000:9.1f}    | {n_nodes_flux:11d} | {T_max:8.1f}")
        
        mapdl.slashsolu()

mapdl.finish()
print("\n=== SIMULATION TERMINEE ===")

# =========================
# POST-TRAITEMENT
# =========================
mapdl.post1()
mapdl.set('LAST')

# Vérification: température sur chaque face
print("\n=== VERIFICATION DES TEMPERATURES PAR FACE ===")

# Face supérieure (Z = H) - où le flux a été appliqué
mapdl.nsel('S', 'LOC', 'Z', H - 1e-6, H + 1e-6)
temps_top = mapdl.post_processing.nodal_temperature()
print(f"Face SUPERIEURE (Z={H*1000}mm) - FLUX APPLIQUE ICI:")
print(f"    Tmin={temps_top.min():.1f}C, Tmax={temps_top.max():.1f}C")

# Face inférieure (Z = 0)
mapdl.nsel('S', 'LOC', 'Z', -1e-6, 1e-6)
temps_bottom = mapdl.post_processing.nodal_temperature()
print(f"Face inferieure (Z=0mm):")
print(f"    Tmin={temps_bottom.min():.1f}C, Tmax={temps_bottom.max():.1f}C")

# Faces latérales X
mapdl.nsel('S', 'LOC', 'X', -1e-6, 1e-6)
temps_x0 = mapdl.post_processing.nodal_temperature()
print(f"Face laterale X=0:")
print(f"    Tmin={temps_x0.min():.1f}C, Tmax={temps_x0.max():.1f}C")

mapdl.nsel('S', 'LOC', 'X', L - 1e-6, L + 1e-6)
temps_xL = mapdl.post_processing.nodal_temperature()
print(f"Face laterale X={L*1000}mm:")
print(f"    Tmin={temps_xL.min():.1f}C, Tmax={temps_xL.max():.1f}C")

# Faces latérales Y
mapdl.nsel('S', 'LOC', 'Y', -1e-6, 1e-6)
temps_y0 = mapdl.post_processing.nodal_temperature()
print(f"Face laterale Y=0:")
print(f"    Tmin={temps_y0.min():.1f}C, Tmax={temps_y0.max():.1f}C")

mapdl.nsel('S', 'LOC', 'Y', W - 1e-6, W + 1e-6)
temps_yW = mapdl.post_processing.nodal_temperature()
print(f"Face laterale Y={W*1000}mm:")
print(f"    Tmin={temps_yW.min():.1f}C, Tmax={temps_yW.max():.1f}C")

mapdl.allsel()

# =========================
# VISUALISATIONS
# =========================
print("\n=== GENERATION DES VISUALISATIONS ===")

# Vue 3D isométrique
mapdl.post_processing.plot_nodal_temperature(
    cmap='jet',
    show_edges=True,
    background='white',
    title='Distribution de temperature - Flux sur face superieure uniquement',
    cpos='iso'
)

# Coupe longitudinale (plan Y = y_center)
mapdl.nsel('S', 'LOC', 'Y', y_center - 0.002, y_center + 0.002)
mapdl.post_processing.plot_nodal_temperature(
    cmap='jet',
    show_edges=True,
    background='white',
    title=f'Coupe longitudinale Y={y_center*1000:.0f}mm - Propagation en profondeur',
    cpos='xz'
)

mapdl.allsel()

# =========================
# GRAPHIQUES MATPLOTLIB
# =========================
print("\nGeneration des graphiques...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Graphique 1: Évolution température max
ax1 = axes[0, 0]
ax1.plot(results['time'], results['T_max'], 'r-o', linewidth=2, markersize=4, label='Tmax')
ax1.plot(results['time'], results['T_min'], 'b-s', linewidth=2, markersize=4, label='Tmin')
ax1.set_xlabel('Temps (s)')
ax1.set_ylabel('Temperature (C)')
ax1.set_title('Evolution des temperatures')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Graphique 2: Position du spot vs Tmax
ax2 = axes[0, 1]
ax2.plot(results['x_pos'], results['T_max'], 'r-o', linewidth=2, markersize=4)
ax2.set_xlabel('Position X du spot (mm)')
ax2.set_ylabel('Temperature max (C)')
ax2.set_title('Temperature max vs position du spot')
ax2.grid(True, alpha=0.3)

# Graphique 3: Nombre de nœuds dans le spot
ax3 = axes[1, 0]
ax3.plot(results['time'], results['n_nodes'], 'g-o', linewidth=2, markersize=4)
ax3.set_xlabel('Temps (s)')
ax3.set_ylabel('Nombre de noeuds')
ax3.set_title('Noeuds dans la zone du spot (face superieure)')
ax3.grid(True, alpha=0.3)

# Graphique 4: Gradient thermique
ax4 = axes[1, 1]
gradient = np.array(results['T_max']) - np.array(results['T_min'])
ax4.plot(results['time'], gradient, 'm-o', linewidth=2, markersize=4)
ax4.set_xlabel('Temps (s)')
ax4.set_ylabel('Gradient (C)')
ax4.set_title('Gradient thermique (Tmax - Tmin)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('flux_mobile_resultats.png', dpi=150)
print("Graphique sauvegarde: flux_mobile_resultats.png")
plt.show()

# =========================
# RÉSUMÉ FINAL
# =========================
print("\n" + "=" * 60)
print("RESUME DE LA SIMULATION")
print("=" * 60)
print(f"Temperature maximale atteinte: {max(results['T_max']):.1f} C")
print(f"Temperature minimale finale: {min(results['T_min']):.1f} C")
print(f"Gradient max: {max(results['T_max']) - min(results['T_min']):.1f} C")
print(f"Face superieure - Tmax: {temps_top.max():.1f} C (flux applique ici)")
print(f"Face inferieure - Tmax: {temps_bottom.max():.1f} C (propagation par conduction)")
print("=" * 60)

# Export des résultats
try:
    import pandas as pd
    df = pd.DataFrame(results)
    df.to_csv('flux_mobile_donnees.csv', index=False)
    print("Donnees exportees: flux_mobile_donnees.csv")
except ImportError:
    print("pandas non disponible - export CSV ignore")

# Fermeture propre
mapdl.exit()
print("\nSimulation terminee avec succes!")
