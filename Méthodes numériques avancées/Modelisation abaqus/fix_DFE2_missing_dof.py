#!/usr/bin/env python3
"""
Script pour corriger le problème des DDL manquants dans DFE2_final.inp

Problème: Les nœuds 1076-1219 dans la Part BEAM sont orphelins (non connectés
à des éléments) ce qui cause l'erreur "nodes are missing degree of freedoms"

Solution: Ajouter des éléments MASS à ces nœuds pour leur donner des DDL

Usage:
    python fix_DFE2_missing_dof.py

Input: DFE2_final.inp
Output: DFE2_final_corrected.inp
"""

import os
import re

def fix_dfe2_file(input_file, output_file):
    """
    Corrige le fichier DFE2 en ajoutant des éléments MASS aux nœuds orphelins
    """
    
    print(f"Lecture de {input_file}...")
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Trouver la position de *End Part pour la Part beam
    # Pattern: chercher *End Part après *Part, name=beam
    
    # On va chercher la section des éléments C3D8R dans la Part beam
    # et ajouter les éléments MASS juste après
    
    # Pattern pour trouver la fin des éléments dans Part beam
    # Chercher après "*Element, type=C3D8R" et les lignes d'éléments
    
    lines = content.split('\n')
    output_lines = []
    in_beam_part = False
    found_elements = False
    elements_section_ended = False
    mass_elements_added = False
    
    for i, line in enumerate(lines):
        output_lines.append(line)
        
        # Détecter le début de la Part beam
        if '*Part, name=beam' in line.lower():
            in_beam_part = True
            print("  Trouvé: Part beam")
        
        # Détecter la fin de la Part beam
        if in_beam_part and '*End Part' in line:
            in_beam_part = False
            print("  Fin de Part beam")
        
        # Détecter la section des éléments
        if in_beam_part and '*Element, type=C3D8R' in line:
            found_elements = True
            print("  Trouvé: Éléments C3D8R")
        
        # Détecter la fin de la section éléments (ligne commençant par *)
        if in_beam_part and found_elements and not elements_section_ended:
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Si la prochaine ligne commence par * (nouvelle section) et n'est pas un élément
                if next_line.startswith('*') and not mass_elements_added:
                    elements_section_ended = True
                    print("  Fin de section éléments détectée")
                    
                    # Ajouter les éléments MASS
                    mass_section = generate_mass_elements()
                    output_lines.append(mass_section)
                    mass_elements_added = True
                    print("  Éléments MASS ajoutés (2001-2144)")
    
    # Vérifier si les corrections ont été appliquées
    if not mass_elements_added:
        print("\n[ATTENTION] Les éléments MASS n'ont pas pu être ajoutés automatiquement.")
        print("Tentative d'ajout manuel après la section *Nset, nset=RP_E18_GP1...")
        
        # Méthode alternative: ajouter après *Nset, nset=RP_E18_GP1
        output_content = '\n'.join(output_lines)
        
        # Trouver la position après les Node sets de la Part beam
        pattern = r'(\*Nset, nset=RP_E18_GP1\n[^\*]+)'
        match = re.search(pattern, output_content)
        
        if match:
            insert_pos = match.end()
            mass_section = generate_mass_elements()
            output_content = output_content[:insert_pos] + '\n' + mass_section + output_content[insert_pos:]
            output_lines = output_content.split('\n')
            mass_elements_added = True
            print("  Éléments MASS ajoutés après RP_E18_GP1")
    
    # Écrire le fichier corrigé
    print(f"\nÉcriture de {output_file}...")
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\nTerminé! Fichier corrigé: {output_file}")
    
    if mass_elements_added:
        print("\nModifications apportées:")
        print("  - Ajout de 144 éléments MASS (numéros 2001-2144)")
        print("  - Ces éléments donnent des DDL aux nœuds 1076-1219")
        print("  - Masse utilisée: 1e-12 (négligeable)")
    
    return mass_elements_added


def generate_mass_elements():
    """
    Génère la section des éléments MASS pour les nœuds 1076-1219
    """
    lines = []
    lines.append('**')
    lines.append('** =============================================================')
    lines.append('** MASS ELEMENTS pour nœuds de référence (CORRECTION DDL)')
    lines.append('** Résout: "nodes are missing degree of freedoms"')
    lines.append('** =============================================================')
    lines.append('*Element, type=MASS')
    
    # Générer 144 éléments MASS (nœuds 1076-1219)
    for i, node in enumerate(range(1076, 1220)):
        elem_id = 2001 + i
        lines.append(f'  {elem_id}, {node}')
    
    lines.append('**')
    lines.append('** Element set for MASS elements')
    lines.append('*Elset, elset=ELSET_MASS_RP, generate')
    lines.append('  2001, 2144, 1')
    lines.append('**')
    lines.append('** Mass property (très petite masse, juste pour DDL)')
    lines.append('*Mass, elset=ELSET_MASS_RP')
    lines.append('1.0e-12,')
    lines.append('**')
    
    return '\n'.join(lines)


def main():
    # Chemins des fichiers
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'DFE2_final.inp')
    output_file = os.path.join(script_dir, 'DFE2_final_corrected.inp')
    
    if not os.path.exists(input_file):
        print(f"Erreur: Fichier non trouvé: {input_file}")
        return False
    
    print("=" * 60)
    print("Correction du problème DDL manquants dans DFE2")
    print("=" * 60)
    
    success = fix_dfe2_file(input_file, output_file)
    
    if success:
        print("\n" + "=" * 60)
        print("Pour tester le fichier corrigé:")
        print(f"  abaqus job=DFE2_final_corrected interactive")
        print("=" * 60)
    
    return success


if __name__ == '__main__':
    main()
