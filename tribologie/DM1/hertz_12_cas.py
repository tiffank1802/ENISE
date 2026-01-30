import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

R_VALUES = [5e-3, 100e-3]
F_VALUES = [50, 500]

PLAN_MATERIALS = {
    'Acier': {'E': 210e9, 'nu': 0.3, 'couleur': 'blue'},
    'Fonte': {'E': 100e9, 'nu': 0.3, 'couleur': 'green'},
    'Alu': {'E': 10e9, 'nu': 0.45, 'couleur': 'red'}
}

E_SPHERE = 210e9
NU_SPHERE = 0.3

def calcul_module_effectif(E1, nu1, E2, nu2):
    return 1 / ((1 - nu1**2)/E1 + (1 - nu2**2)/E2)

def calcul_rayon_contact_hertz(P, R, E_star):
    return (3 * P * R / (4 * E_star)) ** (1/3)

def calcul_enfoncement(a, R):
    return a**2 / R

def calcul_pression_maximale(P, a):
    return (3 * P) / (2 * np.pi * a**2)

def profil_pression_hertz(r, p0, a):
    return p0 * np.sqrt(np.maximum(0, 1 - (r / a)**2))

def calcul_raideur_contact(a, E_star):
    return 2 * a * E_star

def calcul_hauteur_bourlet(delta, R):
    return 0.42 * np.sqrt(delta / R)

def calculer_tous_les_cas():
    resultats = []
    
    for R in R_VALUES:
        for F in F_VALUES:
            for plan_name, plan_props in PLAN_MATERIALS.items():
                E_star = calcul_module_effectif(
                    E_SPHERE, NU_SPHERE, 
                    plan_props['E'], plan_props['nu']
                )
                
                a = calcul_rayon_contact_hertz(F, R, E_star)
                delta = calcul_enfoncement(a, R)
                p0 = calcul_pression_maximale(F, a)
                K = calcul_raideur_contact(a, E_star)
                h = calcul_hauteur_bourlet(delta, R)
                
                r = np.linspace(0, a * 1.5, 100)
                p = profil_pression_hertz(r, p0, a)
                
                resultats.append({
                    'R_mm': R * 1000,
                    'F_N': F,
                    'plan': plan_name,
                    'couleur': plan_props['couleur'],
                    'E_star_GPa': E_star / 1e9,
                    'a_mm': a * 1000,
                    'delta_um': delta * 1e6,
                    'p0_MPa': p0 / 1e6,
                    'K_MN_m': K / 1e6,
                    'h_um': h * 1e6,
                    'r_mm': r * 1000,
                    'p_MPa': p / 1e6
                })
    
    return resultats

def tracer_profils_pression(resultats):
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('PROFILS DE PRESSION HERTZIEN - 12 CAS', fontsize=16, fontweight='bold')
    
    gs = gridspec.GridSpec(3, 4, hspace=0.35, wspace=0.25)
    
    for idx, res in enumerate(resultats):
        row = idx // 4
        col = idx % 4
        
        ax = plt.subplot(gs[row, col])
        
        ax.plot(res['r_mm'], res['p_MPa'], color=res['couleur'], linewidth=2)
        ax.fill_between(res['r_mm'], 0, res['p_MPa'], alpha=0.2, color=res['couleur'])
        ax.axvline(res['a_mm'], color='red', linestyle='--', linewidth=1, alpha=0.7)
        
        ax.text(0.05, 0.95, f"R={res['R_mm']:.0f}mm\nF={res['F_N']}N", 
                transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.8))
        
        ax.text(0.05, 0.72, f"p0={res['p0_MPa']:.1f}MPa\na={res['a_mm']:.3f}mm", 
                transform=ax.transAxes, fontsize=8,
                verticalalignment='top', bbox=dict(boxstyle='round', alpha=0.6))
        
        ax.set_xlabel('r (mm)', fontsize=9)
        ax.set_ylabel('p(r) (MPa)', fontsize=9)
        ax.set_xlim([0, res['a_mm'] * 1.5])
        ax.set_ylim([0, res['p0_MPa'] * 1.1])
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_title(f"{res['plan']}", fontsize=10)
    
    plt.savefig('/root/ENISE/tribologie/DM1/profils_pression_12_cas.png', dpi=150, bbox_inches='tight')
    plt.close()

def tracer_raideurs_contact(resultats):
    fig = plt.figure(figsize=(14, 8))
    
    labels_R = [f'R={R*1000:.0f}mm' for R in R_VALUES]
    labels_F = [f'F={F}N' for F in F_VALUES]
    plans = list(PLAN_MATERIALS.keys())
    
    K_data = np.zeros((len(R_VALUES), len(F_VALUES), len(plans)))
    
    for res in resultats:
        i = R_VALUES.index(res['R_mm']/1000)
        j = F_VALUES.index(res['F_N'])
        k = plans.index(res['plan'])
        K_data[i, j, k] = res['K_MN_m']
    
    ax = fig.add_subplot(121, projection='3d')
    
    x_pos = []
    y_pos = []
    z_pos = []
    dx = []
    dy = []
    dz = []
    colors = []
    
    for i in range(len(R_VALUES)):
        for j in range(len(F_VALUES)):
            for k in range(len(plans)):
                x_pos.append(i)
                y_pos.append(j)
                z_pos.append(0)
                dx.append(0.8)
                dy.append(0.8)
                dz.append(K_data[i, j, k])
                colors.append(PLAN_MATERIALS[plans[k]]['couleur'])
    
    ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colors, alpha=0.7, shade=True)
    
    ax.set_xlabel('Rayon')
    ax.set_ylabel('Force')
    ax.set_zlabel('Raideur (MN/m)')
    ax.set_xticks(range(len(R_VALUES)))
    ax.set_xticklabels(labels_R)
    ax.set_yticks(range(len(F_VALUES)))
    ax.set_yticklabels(labels_F)
    ax.set_title('Raideurs de contact - Vue 3D', fontweight='bold')
    
    ax2 = fig.add_subplot(122)
    
    x = np.arange(len(plans))
    width = 0.35
    
    for i in range(len(R_VALUES)):
        for j in range(len(F_VALUES)):
            K_values = []
            for plan in plans:
                for res in resultats:
                    if res['R_mm'] == R_VALUES[i]*1000 and res['F_N'] == F_VALUES[j] and res['plan'] == plan:
                        K_values.append(res['K_MN_m'])
                        break
            
            offset = (i * len(F_VALUES) + j) * 0.1 - 0.15
            bars = ax2.bar(x + offset, K_values, width/3, 
                          label=f'R={R_VALUES[i]*1000:.0f}mm, F={F_VALUES[j]}N',
                          color=PLAN_MATERIALS[plans[0]]['couleur'], alpha=0.6)
            
            for bar, val in zip(bars, K_values):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                        f'{val:.1f}', ha='center', va='bottom', fontsize=8)
    
    ax2.set_xlabel('Type de plan')
    ax2.set_ylabel('Raideur (MN/m)')
    ax2.set_title('Raideurs de contact - Comparaison', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([p for p in plans], rotation=45, ha='right')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/root/ENISE/tribologie/DM1/raideurs_contact_12_cas.png', dpi=150, bbox_inches='tight')
    plt.close()

def tracer_hauteurs_bourlets(resultats):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('HAUTEURS DES BOURLETS - 12 CAS', fontsize=16, fontweight='bold')
    
    data_R5 = np.zeros((len(F_VALUES), len(PLAN_MATERIALS)))
    data_R100 = np.zeros((len(F_VALUES), len(PLAN_MATERIALS)))
    
    plans_list = list(PLAN_MATERIALS.keys())
    
    for res in resultats:
        i = F_VALUES.index(res['F_N'])
        j = plans_list.index(res['plan'])
        
        if res['R_mm'] == 5:
            data_R5[i, j] = res['h_um']
        else:
            data_R100[i, j] = res['h_um']
    
    ax1 = axes[0, 0]
    im1 = ax1.imshow(data_R5, cmap='YlOrRd', aspect='auto')
    ax1.set_title('R = 5 mm', fontweight='bold')
    ax1.set_xlabel('Type de plan')
    ax1.set_ylabel('Force (N)')
    ax1.set_xticks(range(len(plans_list)))
    ax1.set_xticklabels([p for p in plans_list], rotation=45, ha='right')
    ax1.set_yticks(range(len(F_VALUES)))
    ax1.set_yticklabels([f'{F}' for F in F_VALUES])
    
    for i in range(len(F_VALUES)):
        for j in range(len(plans_list)):
            text = ax1.text(j, i, f'{data_R5[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=9,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
    
    ax2 = axes[0, 1]
    im2 = ax2.imshow(data_R100, cmap='YlOrRd', aspect='auto')
    ax2.set_title('R = 100 mm', fontweight='bold')
    ax2.set_xlabel('Type de plan')
    ax2.set_ylabel('Force (N)')
    ax2.set_xticks(range(len(plans_list)))
    ax2.set_xticklabels([p for p in plans_list], rotation=45, ha='right')
    ax2.set_yticks(range(len(F_VALUES)))
    ax2.set_yticklabels([f'{F}' for F in F_VALUES])
    
    for i in range(len(F_VALUES)):
        for j in range(len(plans_list)):
            text = ax2.text(j, i, f'{data_R100[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=9,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
    
    ax3 = axes[1, 0]
    x = np.arange(len(plans_list))
    width = 0.35
    
    h_R5_F50 = [res['h_um'] for res in resultats if res['R_mm'] == 5 and res['F_N'] == 50]
    h_R100_F50 = [res['h_um'] for res in resultats if res['R_mm'] == 100 and res['F_N'] == 50]
    
    bars1 = ax3.bar(x - width/2, h_R5_F50, width, label='R=5mm', color='skyblue', alpha=0.8)
    bars2 = ax3.bar(x + width/2, h_R100_F50, width, label='R=100mm', color='lightcoral', alpha=0.8)
    
    ax3.set_xlabel('Type de plan')
    ax3.set_ylabel('Taille du bourlet (um)')
    ax3.set_title('Comparaison pour F = 50 N', fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels([p for p in plans_list], rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    ax4 = axes[1, 1]
    
    h_R5_F500 = [res['h_um'] for res in resultats if res['R_mm'] == 5 and res['F_N'] == 500]
    h_R100_F500 = [res['h_um'] for res in resultats if res['R_mm'] == 100 and res['F_N'] == 500]
    
    bars3 = ax4.bar(x - width/2, h_R5_F500, width, label='R=5mm', color='skyblue', alpha=0.8)
    bars4 = ax4.bar(x + width/2, h_R100_F500, width, label='R=100mm', color='lightcoral', alpha=0.8)
    
    ax4.set_xlabel('Type de plan')
    ax4.set_ylabel('Taille du bourlet (um)')
    ax4.set_title('Comparaison pour F = 500 N', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels([p for p in plans_list], rotation=45, ha='right')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/root/ENISE/tribologie/DM1/hauteurs_bourlets_12_cas.png', dpi=150, bbox_inches='tight')
    plt.close()

def tracer_synthese_comparative(resultats):
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(3, 4, hspace=0.4, wspace=0.3)
    
    ax1 = plt.subplot(gs[0, 0:2])
    x = np.arange(len(PLAN_MATERIALS))
    width = 0.35
    
    for i, R in enumerate(R_VALUES):
        a_values_R = []
        for plan in PLAN_MATERIALS.keys():
            for res in resultats:
                if res['R_mm'] == R*1000 and res['F_N'] == 50 and res['plan'] == plan:
                    a_values_R.append(res['a_mm'])
                    break
        
        ax1.bar(x + (i-0.5)*width, a_values_R, width, 
                label=f'R={R*1000:.0f}mm, F=50N', alpha=0.7)
    
    ax1.set_xlabel('Type de plan')
    ax1.set_ylabel('Rayon de contact (mm)')
    ax1.set_title('Rayons de contact (F=50N)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([p for p in PLAN_MATERIALS.keys()], rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax2 = plt.subplot(gs[0, 2:])
    
    for i, R in enumerate(R_VALUES):
        p0_values_R = []
        for plan in PLAN_MATERIALS.keys():
            for res in resultats:
                if res['R_mm'] == R*1000 and res['F_N'] == 500 and res['plan'] == plan:
                    p0_values_R.append(res['p0_MPa'])
                    break
        
        ax2.bar(x + (i-0.5)*width, p0_values_R, width, 
                label=f'R={R*1000:.0f}mm, F=500N', alpha=0.7)
    
    ax2.set_xlabel('Type de plan')
    ax2.set_ylabel('Pression maximale (MPa)')
    ax2.set_title('Pressions maximales (F=500N)', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([p for p in PLAN_MATERIALS.keys()], rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    ax3 = plt.subplot(gs[1, :])
    
    for plan_name, plan_props in PLAN_MATERIALS.items():
        delta_values = []
        
        for res in resultats:
            if res['R_mm'] == 5 and res['plan'] == plan_name:
                delta_values.append((res['F_N'], res['delta_um']))
        
        delta_values.sort(key=lambda x: x[0])
        F_sorted = [d[0] for d in delta_values]
        delta_sorted = [d[1] for d in delta_values]
        
        ax3.plot(F_sorted, delta_sorted, 'o-', 
                label=plan_name,
                color=plan_props['couleur'], linewidth=2, markersize=8)
    
    ax3.set_xlabel('Force (N)')
    ax3.set_ylabel('Enfoncement (um)')
    ax3.set_title('Relation Force-Enfoncement (R=5mm)', fontweight='bold')
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)
    
    ax4 = plt.subplot(gs[2, 0:2])
    
    param_names = ['a_mm', 'delta_um', 'p0_MPa', 'K_MN_m', 'h_um']
    n_params = len(param_names)
    
    corr_matrix = np.zeros((n_params, n_params))
    
    data_dict = {name: [] for name in param_names}
    for res in resultats:
        for name in param_names:
            data_dict[name].append(res[name])
    
    for i in range(n_params):
        for j in range(n_params):
            corr = np.corrcoef(data_dict[param_names[i]], data_dict[param_names[j]])[0, 1]
            corr_matrix[i, j] = corr
    
    im = ax4.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
    
    ax4.set_xticks(range(n_params))
    ax4.set_yticks(range(n_params))
    ax4.set_xticklabels(['a', 'd', 'p0', 'K', 'h'], fontsize=10)
    ax4.set_yticklabels(['a', 'd', 'p0', 'K', 'h'], fontsize=10)
    ax4.set_title('Matrice de Correlations', fontweight='bold')
    
    for i in range(n_params):
        for j in range(n_params):
            text = ax4.text(j, i, f'{corr_matrix[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=9)
    
    plt.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)
    
    ax5 = plt.subplot(gs[2, 2:], projection='polar')
    
    cas_F50_R5 = [res for res in resultats if res['R_mm'] == 5 and res['F_N'] == 50]
    
    radar_params = ['a_mm', 'delta_um', 'p0_MPa', 'K_MN_m', 'h_um']
    n_radar = len(radar_params)
    
    angles = np.linspace(0, 2 * np.pi, n_radar, endpoint=False).tolist()
    angles += angles[:1]
    
    for cas in cas_F50_R5:
        values = [cas[param] for param in radar_params]
        
        values_norm = []
        for val, param in zip(values, radar_params):
            all_vals = [res[param] for res in resultats]
            min_val = min(all_vals)
            max_val = max(all_vals)
            if max_val > min_val:
                norm_val = (val - min_val) / (max_val - min_val)
            else:
                norm_val = 0.5
            values_norm.append(norm_val)
        
        values_norm += values_norm[:1]
        ax5.plot(angles, values_norm, 'o-', linewidth=2, 
                label=cas['plan'])
        ax5.fill(angles, values_norm, alpha=0.1)
    
    ax5.set_xticks(angles[:-1])
    ax5.set_xticklabels(['a', 'd', 'p0', 'K', 'h'])
    ax5.set_title('Diagramme Radar (R=5mm, F=50N)', fontweight='bold', y=1.1)
    ax5.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    plt.tight_layout()
    plt.savefig('/root/ENISE/tribologie/DM1/synthese_comparative.png', dpi=150, bbox_inches='tight')
    plt.close()

def generer_tableau_resultats(resultats):
    df = pd.DataFrame(resultats)
    
    cols_order = ['R_mm', 'F_N', 'plan', 'E_star_GPa', 'a_mm', 'delta_um', 
                  'p0_MPa', 'K_MN_m', 'h_um']
    df = df[cols_order]
    
    df['E_star_GPa'] = df['E_star_GPa'].round(2)
    df['a_mm'] = df['a_mm'].round(3)
    df['delta_um'] = df['delta_um'].round(2)
    df['p0_MPa'] = df['p0_MPa'].round(1)
    df['K_MN_m'] = df['K_MN_m'].round(3)
    df['h_um'] = df['h_um'].round(2)
    
    df.to_csv('/root/ENISE/tribologie/DM1/resultats_12_cas.csv', index=False, encoding='utf-8')
    
    return df

def main():
    print("="*80)
    print("ANALYSE DE CONTACT HERTZIEN - 12 CAS")
    print("="*80)
    
    print("\n1. Calcul des 12 cas en cours...")
    resultats = calculer_tous_les_cas()
    print(f"   OK: {len(resultats)} cas calcules avec succes")
    
    print("\n2. Generation du tableau recapitulatif...")
    df = generer_tableau_resultats(resultats)
    print("   OK: Tableau genere et sauvegarde dans 'resultats_12_cas.csv'")
    
    print("\n3. Generation des visualisations...")
    
    print("   a) Profils de pression...")
    tracer_profils_pression(resultats)
    print("     OK: profils_pression_12_cas.png")
    
    print("   b) Raideurs de contact...")
    tracer_raideurs_contact(resultats)
    print("     OK: raideurs_contact_12_cas.png")
    
    print("   c) Hauteurs des bourlets...")
    tracer_hauteurs_bourlets(resultats)
    print("     OK: hauteurs_bourlets_12_cas.png")
    
    print("   d) Synthese comparative...")
    tracer_synthese_comparative(resultats)
    print("     OK: synthese_comparative.png")
    
    print("\n" + "="*80)
    print("ANALYSE TERMINEE AVEC SUCCES")
    print("="*80)

if __name__ == "__main__":
    main()
