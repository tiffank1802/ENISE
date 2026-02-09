#!/usr/bin/env python3
"""
Script pour calculer les moyennes volumiques de contraintes et déformations
à partir de fichiers .rpt (Abaqus) et déterminer le module d'élasticité apparent.

Hypothèse: Matériau élastique linéaire => E = <σ> / <ε>

Usage:
    python moyenne_volumique.py <chemin_repertoire> [--plot]
    python moyenne_volumique.py <chemin_fichier.rpt> [--plot]

Options:
    --plot    Affiche les graphiques de répartition

Exemple:
    python moyenne_volumique.py ./datas
    python moyenne_volumique.py ./datas/S11_E11_sym.rpt --plot
"""

import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class DonneesElement:
    """Données extraites pour un élément."""
    deformation: Optional[float]
    volume: float
    contrainte: float


@dataclass
class ResultatsAnalyse:
    """Résultats de l'analyse d'un fichier."""
    fichier: str
    nom_contrainte: str
    nom_deformation: Optional[str]
    nb_elements: int
    volume_total: float
    
    # Contrainte
    contrainte_moyenne_vol: float
    contrainte_min: float
    contrainte_max: float
    
    # Déformation (optionnel)
    deformation_moyenne_vol: Optional[float]
    deformation_min: Optional[float]
    deformation_max: Optional[float]
    
    # Module d'élasticité (si déformation disponible)
    module_elasticite: Optional[float]
    
    # Données brutes pour le tracé
    donnees: list[DonneesElement] = field(default_factory=list)
    
    erreur: Optional[str] = None


def detecter_format_fichier(content: str) -> dict:
    """
    Détecte le format du fichier et les colonnes présentes.
    
    Returns:
        dict avec les indices des colonnes et leurs noms
    """
    info = {
        'has_deformation': False,
        'nom_contrainte': 'S.S11',
        'nom_deformation': None,
        'col_deformation': None,
        'col_volume': None,
        'col_contrainte': None
    }
    
    # Détecter si E.Exx est présent (déformation)
    deform_match = re.search(r'(E\.E\d+)', content)
    if deform_match:
        info['has_deformation'] = True
        info['nom_deformation'] = deform_match.group(1)
    
    # Détecter le nom de la contrainte
    stress_match = re.search(r'(S\.S\d+)', content)
    if stress_match:
        info['nom_contrainte'] = stress_match.group(1)
    
    return info


def lire_fichier_rpt(filepath: str) -> tuple[list[DonneesElement], dict]:
    """
    Lit un fichier .rpt et extrait les données.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    info = detecter_format_fichier(content)
    donnees = []
    
    if info['has_deformation']:
        pattern = r'^\s*\d+\s+\d+\s+([\d.E+-]+)\s+([\d.E+-]+)\s+([\d.E+-]+)\s*$'
        
        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                try:
                    deformation = float(match.group(1))
                    volume = float(match.group(2))
                    contrainte = float(match.group(3))
                    donnees.append(DonneesElement(deformation, volume, contrainte))
                except ValueError:
                    continue
    else:
        pattern = r'^\s*\d+\s+\d+\s+([\d.E+-]+)\s+([\d.E+-]+)\s*$'
        
        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                try:
                    volume = float(match.group(1))
                    contrainte = float(match.group(2))
                    donnees.append(DonneesElement(None, volume, contrainte))
                except ValueError:
                    continue
    
    return donnees, info


def calculer_moyenne_volumique(valeurs: list[float], volumes: list[float]) -> float:
    """
    Calcule la moyenne volumique: <X> = Σ(Vi * Xi) / Σ(Vi)
    """
    volume_total = sum(volumes)
    somme_ponderee = sum(v * x for v, x in zip(volumes, valeurs))
    return somme_ponderee / volume_total


def analyser_fichier(filepath: str) -> ResultatsAnalyse:
    """
    Analyse complète d'un fichier .rpt.
    """
    nom_fichier = os.path.basename(filepath)
    
    try:
        donnees, info = lire_fichier_rpt(filepath)
    except Exception as e:
        return ResultatsAnalyse(
            fichier=nom_fichier,
            nom_contrainte="",
            nom_deformation=None,
            nb_elements=0,
            volume_total=0,
            contrainte_moyenne_vol=0,
            contrainte_min=0,
            contrainte_max=0,
            deformation_moyenne_vol=None,
            deformation_min=None,
            deformation_max=None,
            module_elasticite=None,
            erreur=str(e)
        )
    
    if len(donnees) == 0:
        return ResultatsAnalyse(
            fichier=nom_fichier,
            nom_contrainte=info['nom_contrainte'],
            nom_deformation=info['nom_deformation'],
            nb_elements=0,
            volume_total=0,
            contrainte_moyenne_vol=0,
            contrainte_min=0,
            contrainte_max=0,
            deformation_moyenne_vol=None,
            deformation_min=None,
            deformation_max=None,
            module_elasticite=None,
            erreur="Aucune donnée trouvée dans le fichier"
        )
    
    # Extraire les listes
    volumes = [d.volume for d in donnees]
    contraintes = [d.contrainte for d in donnees]
    
    # Calculs pour la contrainte
    volume_total = sum(volumes)
    contrainte_moyenne_vol = calculer_moyenne_volumique(contraintes, volumes)
    contrainte_min = min(contraintes)
    contrainte_max = max(contraintes)
    
    # Calculs pour la déformation (si disponible)
    deformation_moyenne_vol = None
    deformation_min = None
    deformation_max = None
    module_elasticite = None
    
    if info['has_deformation']:
        deformations = [d.deformation for d in donnees if d.deformation is not None]
        deformation_moyenne_vol = calculer_moyenne_volumique(deformations, volumes)
        deformation_min = min(deformations)
        deformation_max = max(deformations)
        
        if deformation_moyenne_vol != 0:
            module_elasticite = contrainte_moyenne_vol / deformation_moyenne_vol
    
    return ResultatsAnalyse(
        fichier=nom_fichier,
        nom_contrainte=info['nom_contrainte'],
        nom_deformation=info['nom_deformation'],
        nb_elements=len(donnees),
        volume_total=volume_total,
        contrainte_moyenne_vol=contrainte_moyenne_vol,
        contrainte_min=contrainte_min,
        contrainte_max=contrainte_max,
        deformation_moyenne_vol=deformation_moyenne_vol,
        deformation_min=deformation_min,
        deformation_max=deformation_max,
        module_elasticite=module_elasticite,
        donnees=donnees
    )


def tracer_resultats(res: ResultatsAnalyse, save_path: Optional[str] = None, output_dir: str = "figures"):
    """
    Trace les graphiques de répartition de la contrainte et de la déformation
    en fonction du volume d'intégration (IVOL).
    """
    # Créer le dossier de sortie si nécessaire
    os.makedirs(output_dir, exist_ok=True)
    if res.erreur or len(res.donnees) == 0:
        print(f"Impossible de tracer: {res.erreur or 'Pas de données'}")
        return
    
    # Extraire les données
    volumes = np.array([d.volume for d in res.donnees])
    contraintes = np.array([d.contrainte for d in res.donnees])
    
    has_deformation = res.deformation_moyenne_vol is not None
    if has_deformation:
        deformations = np.array([d.deformation for d in res.donnees])
    
    # Configuration de la figure
    if has_deformation:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'Analyse d\'homogénéisation - {res.fichier}', fontsize=14, fontweight='bold')
    else:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        axes = [ax]
        fig.suptitle(f'Analyse d\'homogénéisation - {res.fichier}', fontsize=14, fontweight='bold')
    
    # ==================== Graphique 1: Contrainte ====================
    ax1 = axes[0]
    
    # Scatter plot
    scatter1 = ax1.scatter(volumes, contraintes, c=contraintes, cmap='RdYlBu_r', 
                           alpha=0.6, s=15, edgecolors='none')
    
    # Ligne de la moyenne volumique
    ax1.axhline(y=res.contrainte_moyenne_vol, color='red', linestyle='--', linewidth=2,
                label=f'<{res.nom_contrainte}> = {res.contrainte_moyenne_vol:.4f}')
    
    # Zone min-max
    ax1.fill_between([volumes.min(), volumes.max()], 
                     res.contrainte_min, res.contrainte_max,
                     alpha=0.1, color='blue', label=f'Plage: [{res.contrainte_min:.2f}, {res.contrainte_max:.2f}]')
    
    ax1.set_xlabel('Volume d\'intégration (IVOL)', fontsize=11)
    ax1.set_ylabel(f'Contrainte {res.nom_contrainte}', fontsize=11)
    ax1.set_title(f'Répartition de la Contrainte', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Colorbar
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label(res.nom_contrainte, fontsize=10)
    
    # ==================== Graphique 2: Déformation ====================
    if has_deformation:
        ax2 = axes[1]
        deformations = np.array([d.deformation for d in res.donnees if d.deformation is not None])
        
        # Scatter plot
        scatter2 = ax2.scatter(volumes, deformations, c=deformations, cmap='viridis',
                               alpha=0.6, s=15, edgecolors='none')
        
        # Ligne de la moyenne volumique
        deform_moy = res.deformation_moyenne_vol if res.deformation_moyenne_vol is not None else 0.0
        deform_min = res.deformation_min if res.deformation_min is not None else 0.0
        deform_max = res.deformation_max if res.deformation_max is not None else 0.0
        nom_deform = res.nom_deformation if res.nom_deformation is not None else "E"
        
        ax2.axhline(y=deform_moy, color='green', linestyle='--', linewidth=2,
                    label=f'<{nom_deform}> = {deform_moy:.6f}')
        
        # Zone min-max
        ax2.fill_between([volumes.min(), volumes.max()],
                         deform_min, deform_max,
                         alpha=0.1, color='green', label=f'Plage: [{deform_min:.4f}, {deform_max:.4f}]')
        
        ax2.set_xlabel('Volume d\'intégration (IVOL)', fontsize=11)
        ax2.set_ylabel(f'Déformation {nom_deform}', fontsize=11)
        ax2.set_title(f'Répartition de la Déformation', fontsize=12)
        ax2.legend(loc='upper right', fontsize=9)
        ax2.grid(True, alpha=0.3)
        
        # Colorbar
        cbar2 = plt.colorbar(scatter2, ax=ax2)
        cbar2.set_label(nom_deform, fontsize=10)
    
    # ==================== Encadré avec les résultats ====================
    # Créer un texte récapitulatif
    if has_deformation:
        textstr = '\n'.join([
            'RÉSULTATS',
            '-' * 30,
            f'Nb éléments: {res.nb_elements}',
            f'Volume total: {res.volume_total:.4f}',
            '',
            f'<{res.nom_contrainte}> = {res.contrainte_moyenne_vol:.4f}',
            f'<{res.nom_deformation}> = {res.deformation_moyenne_vol:.6f}',
            '',
            f'E = <σ>/<ε> = {res.module_elasticite:.4f}'
        ])
    else:
        textstr = '\n'.join([
            'RÉSULTATS',
            '-' * 30,
            f'Nb éléments: {res.nb_elements}',
            f'Volume total: {res.volume_total:.4f}',
            '',
            f'<{res.nom_contrainte}> = {res.contrainte_moyenne_vol:.4f}'
        ])
    
    # Ajouter l'encadré
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    fig.text(0.02, 0.02, textstr, transform=fig.transFigure, fontsize=10,
             verticalalignment='bottom', fontfamily='monospace', bbox=props)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    
    # Sauvegarder ou afficher
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure sauvegardée: {save_path}")
    else:
        # Sauvegarder par défaut dans le dossier figures
        default_path = os.path.join(output_dir, res.fichier.replace('.rpt', '_analyse.png'))
        plt.savefig(default_path, dpi=150, bbox_inches='tight')
        print(f"Figure sauvegardée: {default_path}")
    
    plt.close(fig)


def tracer_comparaison_fichiers(resultats: list[ResultatsAnalyse], save_path: Optional[str] = None, output_dir: str = "figures"):
    """
    Trace une comparaison des résultats de plusieurs fichiers.
    """
    # Créer le dossier de sortie si nécessaire
    os.makedirs(output_dir, exist_ok=True)
    
    resultats_valides = [r for r in resultats if r.erreur is None and r.deformation_moyenne_vol is not None]
    
    if len(resultats_valides) == 0:
        print("Aucun fichier avec déformation pour la comparaison")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparaison des analyses d\'homogénéisation', fontsize=14, fontweight='bold')
    
    # Couleurs pour chaque fichier
    colors = plt.colormaps['tab10'](np.linspace(0, 1, len(resultats_valides)))
    
    # ==================== Graphique 1: Contraintes vs IVOL ====================
    ax1 = axes[0, 0]
    for i, res in enumerate(resultats_valides):
        volumes = [d.volume for d in res.donnees]
        contraintes = [d.contrainte for d in res.donnees]
        ax1.scatter(volumes, contraintes, c=[colors[i]], alpha=0.3, s=5, label=res.fichier)
        ax1.axhline(y=res.contrainte_moyenne_vol, color=colors[i], linestyle='--', linewidth=2)
    
    ax1.set_xlabel('IVOL')
    ax1.set_ylabel('Contrainte')
    ax1.set_title('Contrainte vs Volume')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # ==================== Graphique 2: Déformations vs IVOL ====================
    ax2 = axes[0, 1]
    for i, res in enumerate(resultats_valides):
        volumes = [d.volume for d in res.donnees]
        deformations = [d.deformation for d in res.donnees]
        ax2.scatter(volumes, deformations, c=[colors[i]], alpha=0.3, s=5, label=res.fichier)
        ax2.axhline(y=res.deformation_moyenne_vol, color=colors[i], linestyle='--', linewidth=2)
    
    ax2.set_xlabel('IVOL')
    ax2.set_ylabel('Déformation')
    ax2.set_title('Déformation vs Volume')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # ==================== Graphique 3: Barres des moyennes ====================
    ax3 = axes[1, 0]
    fichiers = [r.fichier[:15] + '...' if len(r.fichier) > 15 else r.fichier for r in resultats_valides]
    contraintes_moy = [r.contrainte_moyenne_vol for r in resultats_valides]
    deformations_moy = [r.deformation_moyenne_vol for r in resultats_valides]
    
    x = np.arange(len(fichiers))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, contraintes_moy, width, label='<σ>', color='coral')
    ax3.set_ylabel('Contrainte moyenne <σ>')
    ax3.set_xlabel('Fichier')
    ax3.set_xticks(x)
    ax3.set_xticklabels(fichiers, rotation=45, ha='right')
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Axe secondaire pour déformation
    ax3b = ax3.twinx()
    bars2 = ax3b.bar(x + width/2, deformations_moy, width, label='<ε>', color='steelblue')
    ax3b.set_ylabel('Déformation moyenne <ε>')
    ax3b.legend(loc='upper right')
    
    ax3.set_title('Moyennes volumiques')
    
    # ==================== Graphique 4: Module d'élasticité ====================
    ax4 = axes[1, 1]
    modules = [r.module_elasticite for r in resultats_valides if r.module_elasticite is not None]
    
    bars = ax4.bar(fichiers, modules, color='darkgreen', alpha=0.7, edgecolor='black')
    modules_mean = float(np.mean(modules))
    ax4.axhline(y=modules_mean, color='red', linestyle='--', linewidth=2,
                label=f'Moyenne E = {modules_mean:.4f}')
    
    ax4.set_ylabel('Module d\'élasticité E')
    ax4.set_xlabel('Fichier')
    ax4.set_title('Module d\'élasticité apparent (E = <σ>/<ε>)')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Ajouter les valeurs sur les barres
    for bar, module in zip(bars, modules):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{module:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure de comparaison sauvegardée: {save_path}")
    else:
        default_path = os.path.join(output_dir, "comparaison_homogeneisation.png")
        plt.savefig(default_path, dpi=150, bbox_inches='tight')
        print(f"Figure de comparaison sauvegardée: {default_path}")
    
    plt.close(fig)


def afficher_resultats(res: ResultatsAnalyse):
    """Affiche les résultats de manière formatée."""
    print("\n" + "=" * 70)
    print(f"Fichier: {res.fichier}")
    print("=" * 70)
    
    if res.erreur:
        print(f"ERREUR: {res.erreur}")
        return
    
    print(f"Nombre d'éléments: {res.nb_elements}")
    print(f"Volume total: {res.volume_total:.6f}")
    
    # Section Contrainte
    print("\n" + "-" * 70)
    print(f"CONTRAINTE ({res.nom_contrainte})")
    print("-" * 70)
    print(f"  Min: {res.contrainte_min:.6f}")
    print(f"  Max: {res.contrainte_max:.6f}")
    print(f"  >>> MOYENNE VOLUMIQUE <{res.nom_contrainte}> = {res.contrainte_moyenne_vol:.6f} <<<")
    
    # Section Déformation (si disponible)
    if res.deformation_moyenne_vol is not None:
        print("\n" + "-" * 70)
        print(f"DÉFORMATION ({res.nom_deformation})")
        print("-" * 70)
        print(f"  Min: {res.deformation_min:.6f}")
        print(f"  Max: {res.deformation_max:.6f}")
        print(f"  >>> MOYENNE VOLUMIQUE <{res.nom_deformation}> = {res.deformation_moyenne_vol:.6f} <<<")
        
        # Module d'élasticité
        print("\n" + "-" * 70)
        print("MODULE D'ÉLASTICITÉ APPARENT (Hypothèse: élasticité linéaire)")
        print("-" * 70)
        print(f"  E = <σ> / <ε> = {res.contrainte_moyenne_vol:.6f} / {res.deformation_moyenne_vol:.6f}")
        print(f"  >>> MODULE D'ÉLASTICITÉ E = {res.module_elasticite:.4f} <<<")


def traiter_repertoire(repertoire: str, plot: bool = False) -> list[ResultatsAnalyse]:
    """
    Traite tous les fichiers .rpt d'un répertoire.
    """
    path = Path(repertoire)
    fichiers_rpt = list(path.glob("*.rpt"))
    
    if not fichiers_rpt:
        print(f"Aucun fichier .rpt trouvé dans {repertoire}")
        return []
    
    print(f"\n{'#' * 70}")
    print(f"# ANALYSE DES FICHIERS .rpt - Homogénéisation")
    print(f"# Répertoire: {repertoire}")
    print(f"# Nombre de fichiers: {len(fichiers_rpt)}")
    print(f"{'#' * 70}")
    
    tous_resultats = []
    for fichier in sorted(fichiers_rpt):
        resultats = analyser_fichier(str(fichier))
        tous_resultats.append(resultats)
        afficher_resultats(resultats)
        
        # Tracer si demandé
        if plot and resultats.erreur is None:
            tracer_resultats(resultats)
    
    return tous_resultats


def afficher_resume(resultats: list[ResultatsAnalyse]):
    """Affiche un résumé de tous les résultats."""
    resultats_valides = [r for r in resultats if r.erreur is None]
    
    if len(resultats_valides) == 0:
        return
    
    print("\n" + "=" * 70)
    print("RÉSUMÉ GLOBAL")
    print("=" * 70)
    
    # En-tête du tableau
    print(f"\n{'Fichier':<25} {'<σ>':>12} {'<ε>':>12} {'E':>12}")
    print("-" * 70)
    
    for r in resultats_valides:
        eps_str = f"{r.deformation_moyenne_vol:.6f}" if r.deformation_moyenne_vol else "N/A"
        e_str = f"{r.module_elasticite:.4f}" if r.module_elasticite else "N/A"
        print(f"{r.fichier:<25} {r.contrainte_moyenne_vol:>12.6f} {eps_str:>12} {e_str:>12}")
    
    # Moyenne des modules si plusieurs fichiers avec E
    modules = [r.module_elasticite for r in resultats_valides if r.module_elasticite]
    if len(modules) > 1:
        moyenne_E = sum(modules) / len(modules)
        print("-" * 70)
        print(f"{'Moyenne E':<25} {'':<12} {'':<12} {moyenne_E:>12.4f}")


def main():
    """Point d'entrée principal du script."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExemple d'utilisation:")
        print("  python moyenne_volumique.py ./datas")
        print("  python moyenne_volumique.py ./datas --plot")
        print("  python moyenne_volumique.py ./datas/S11_E11_sym.rpt --plot")
        sys.exit(1)
    
    chemin = sys.argv[1]
    plot = '--plot' in sys.argv
    
    if os.path.isfile(chemin):
        # Traiter un seul fichier
        if not chemin.endswith('.rpt'):
            print("Erreur: Le fichier doit avoir l'extension .rpt")
            sys.exit(1)
        resultats = analyser_fichier(chemin)
        afficher_resultats(resultats)
        
        if plot:
            tracer_resultats(resultats)
        
    elif os.path.isdir(chemin):
        # Traiter tous les fichiers .rpt du répertoire
        tous_resultats = traiter_repertoire(chemin, plot=False)
        afficher_resume(tous_resultats)
        
        # Tracer la comparaison si demandé
        if plot:
            for res in tous_resultats:
                if res.erreur is None:
                    tracer_resultats(res)
            
            # Tracer la comparaison globale
            if len(tous_resultats) > 1:
                tracer_comparaison_fichiers(tous_resultats)
    else:
        print(f"Erreur: '{chemin}' n'est ni un fichier ni un répertoire valide")
        sys.exit(1)


if __name__ == "__main__":
    main()
