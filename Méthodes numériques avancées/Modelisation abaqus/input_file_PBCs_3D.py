#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
input_file_PBCs_3D.py

Script pour ajouter les equations MPC (Multi-Point Constraints) au fichier
genere par micro_RVE_placement_3D.py pour la methode Direct FE² en 3D.

Ce script ajoute:
1. Equations de couplage macro-micro (liant les coins RVE aux noeuds macro)
2. Conditions aux limites periodiques (PBC) sur les faces du RVE

Base sur la methodologie du repository DirectFE2:
https://github.com/rkarthikayen89/DirectFE2-sample-codes

Auteur: Projet ENISE - Methodes numeriques avancees
Date: 2024
"""

import numpy as np
import re
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

# Fichier d'entree (genere par micro_RVE_placement_3D.py)
INPUT_FILE = "DFE2_placed.inp"

# Fichier de sortie final
OUTPUT_FILE = "DFE2_final.inp"

# Fichier d'informations de couplage
COUPLING_INFO_FILE = "coupling_info.txt"

# Dimensions du RVE (mm)
RVE_L = 5.5   # Longueur en X
RVE_H = 5.5   # Hauteur en Y  
RVE_T = 6.69  # Epaisseur en Z

# Tolerance pour la detection des noeuds sur les faces/coins
TOLERANCE = 0.01

# Type d'element (pour les points de Gauss)
ELEMENT_TYPE = "C3D8R"

# Points de Gauss
if ELEMENT_TYPE == "C3D8R":
    NUM_GAUSS = 1
    GAUSS_POINTS = [(0.0, 0.0, 0.0)]
else:
    NUM_GAUSS = 8
    g = 1.0 / np.sqrt(3.0)
    GAUSS_POINTS = [
        (-g, -g, -g), (g, -g, -g), (g, g, -g), (-g, g, -g),
        (-g, -g, g), (g, -g, g), (g, g, g), (-g, g, g)
    ]


# =============================================================================
# FONCTIONS DE FORME C3D8
# =============================================================================

def shape_functions_C3D8(xi, eta, zeta):
    """
    Fonctions de forme pour un hexaedre a 8 noeuds.
    
    Convention Abaqus pour C3D8:
        1: (x-,y-,z-)  2: (x+,y-,z-)  3: (x+,y+,z-)  4: (x-,y+,z-)
        5: (x-,y-,z+)  6: (x+,y-,z+)  7: (x+,y+,z+)  8: (x-,y+,z+)
    """
    N = np.zeros(8)
    N[0] = 0.125 * (1 - xi) * (1 - eta) * (1 - zeta)
    N[1] = 0.125 * (1 + xi) * (1 - eta) * (1 - zeta)
    N[2] = 0.125 * (1 + xi) * (1 + eta) * (1 - zeta)
    N[3] = 0.125 * (1 - xi) * (1 + eta) * (1 - zeta)
    N[4] = 0.125 * (1 - xi) * (1 - eta) * (1 + zeta)
    N[5] = 0.125 * (1 + xi) * (1 - eta) * (1 + zeta)
    N[6] = 0.125 * (1 + xi) * (1 + eta) * (1 + zeta)
    N[7] = 0.125 * (1 - xi) * (1 + eta) * (1 + zeta)
    return N


# =============================================================================
# PARSEURS
# =============================================================================

def load_coupling_info(filename):
    """
    Charge les informations de couplage depuis le fichier genere par
    micro_RVE_placement_3D.py
    """
    info = {
        'rp_nodes_map': {},
        'macro_elements': {},
        'num_elements': 0,
        'num_gauss': 1
    }
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('NUM_ELEMENTS='):
                info['num_elements'] = int(line.split('=')[1])
            elif line.startswith('NUM_GAUSS='):
                info['num_gauss'] = int(line.split('=')[1])
            elif line.startswith('RVE_L='):
                pass  # Deja configure
            elif line.startswith('RP_NODE,'):
                parts = line.split(',')
                elem_id = int(parts[1])
                gp_idx = int(parts[2])
                local_node = int(parts[3])
                rp_node_id = int(parts[4])
                info['rp_nodes_map'][(elem_id, gp_idx, local_node)] = rp_node_id
            elif line.startswith('ELEMENT,'):
                parts = line.split(',')
                elem_id = int(parts[1])
                nodes = [int(p) for p in parts[2:]]
                info['macro_elements'][elem_id] = nodes
    
    return info


def parse_rve_nodes_from_inp(filename, part_name):
    """
    Parse les noeuds d'une part specifique depuis le fichier .inp
    """
    nodes = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_part = False
    in_nodes = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        if line_stripped.upper().startswith('*PART'):
            match = re.search(r'NAME\s*=\s*(\S+)', line_stripped, re.IGNORECASE)
            if match and match.group(1).lower() == part_name.lower():
                in_part = True
        
        elif line_stripped.upper().startswith('*END PART'):
            if in_part:
                in_part = False
                break
        
        elif in_part and line_stripped.upper().startswith('*NODE') and 'OUTPUT' not in line_stripped.upper():
            in_nodes = True
            continue
        
        elif in_part and in_nodes:
            if line_stripped.startswith('*'):
                in_nodes = False
            elif line_stripped and not line_stripped.startswith('**'):
                parts = line_stripped.split(',')
                if len(parts) >= 4:
                    node_id = int(parts[0].strip())
                    x = float(parts[1].strip())
                    y = float(parts[2].strip())
                    z = float(parts[3].strip())
                    nodes[node_id] = (x, y, z)
    
    return nodes


def identify_rve_corners_and_faces(nodes, L, H, T, tol):
    """
    Identifie les coins et faces du RVE a partir des coordonnees des noeuds.
    
    Retourne:
        corners: dict {corner_name: node_id}
        faces: dict {face_name: [node_ids]}
        edges: dict {edge_name: [node_ids]}
    """
    corners = {}
    faces = {}
    edges = {}
    
    # Definition des coins
    corner_coords = {
        'V1': (0, 0, 0),
        'V2': (L, 0, 0),
        'V3': (L, H, 0),
        'V4': (0, H, 0),
        'V5': (0, 0, T),
        'V6': (L, 0, T),
        'V7': (L, H, T),
        'V8': (0, H, T),
    }
    
    # Identifier les coins
    for corner_name, (cx, cy, cz) in corner_coords.items():
        for node_id, (x, y, z) in nodes.items():
            if abs(x - cx) < tol and abs(y - cy) < tol and abs(z - cz) < tol:
                corners[corner_name] = node_id
                break
    
    # Initialiser les faces et aretes
    face_names = ['FACE_XN', 'FACE_XP', 'FACE_YN', 'FACE_YP', 'FACE_ZN', 'FACE_ZP']
    for name in face_names:
        faces[name] = []
    
    # Aretes (12 aretes d'un cube)
    edge_names = [
        'EDGE_X_Y0_Z0', 'EDGE_X_YH_Z0', 'EDGE_X_Y0_ZT', 'EDGE_X_YH_ZT',  # Aretes // X
        'EDGE_Y_X0_Z0', 'EDGE_Y_XL_Z0', 'EDGE_Y_X0_ZT', 'EDGE_Y_XL_ZT',  # Aretes // Y
        'EDGE_Z_X0_Y0', 'EDGE_Z_XL_Y0', 'EDGE_Z_X0_YH', 'EDGE_Z_XL_YH',  # Aretes // Z
    ]
    for name in edge_names:
        edges[name] = []
    
    # Classifier chaque noeud
    for node_id, (x, y, z) in nodes.items():
        on_xn = abs(x - 0) < tol
        on_xp = abs(x - L) < tol
        on_yn = abs(y - 0) < tol
        on_yp = abs(y - H) < tol
        on_zn = abs(z - 0) < tol
        on_zp = abs(z - T) < tol
        
        num_faces = sum([on_xn, on_xp, on_yn, on_yp, on_zn, on_zp])
        
        if num_faces == 3:
            # Coin - deja traite
            pass
        
        elif num_faces == 2:
            # Arete
            if on_yn and on_zn:
                edges['EDGE_X_Y0_Z0'].append(node_id)
            elif on_yp and on_zn:
                edges['EDGE_X_YH_Z0'].append(node_id)
            elif on_yn and on_zp:
                edges['EDGE_X_Y0_ZT'].append(node_id)
            elif on_yp and on_zp:
                edges['EDGE_X_YH_ZT'].append(node_id)
            elif on_xn and on_zn:
                edges['EDGE_Y_X0_Z0'].append(node_id)
            elif on_xp and on_zn:
                edges['EDGE_Y_XL_Z0'].append(node_id)
            elif on_xn and on_zp:
                edges['EDGE_Y_X0_ZT'].append(node_id)
            elif on_xp and on_zp:
                edges['EDGE_Y_XL_ZT'].append(node_id)
            elif on_xn and on_yn:
                edges['EDGE_Z_X0_Y0'].append(node_id)
            elif on_xp and on_yn:
                edges['EDGE_Z_XL_Y0'].append(node_id)
            elif on_xn and on_yp:
                edges['EDGE_Z_X0_YH'].append(node_id)
            elif on_xp and on_yp:
                edges['EDGE_Z_XL_YH'].append(node_id)
        
        elif num_faces == 1:
            # Face interieure (pas sur les aretes)
            if on_xn:
                faces['FACE_XN'].append(node_id)
            elif on_xp:
                faces['FACE_XP'].append(node_id)
            elif on_yn:
                faces['FACE_YN'].append(node_id)
            elif on_yp:
                faces['FACE_YP'].append(node_id)
            elif on_zn:
                faces['FACE_ZN'].append(node_id)
            elif on_zp:
                faces['FACE_ZP'].append(node_id)
    
    # Trier les listes
    for name in faces:
        faces[name].sort()
    for name in edges:
        edges[name].sort()
    
    return corners, faces, edges


def find_paired_nodes(nodes_minus, nodes_plus, coord_indices, nodes_coords, tol):
    """
    Trouve les paires de noeuds sur les faces opposees.
    
    nodes_minus: liste des noeuds sur la face negative
    nodes_plus: liste des noeuds sur la face positive
    coord_indices: indices des coordonnees a comparer (ex: [1,2] pour YZ)
    
    Retourne: liste de tuples (node_minus, node_plus)
    """
    pairs = []
    
    for n_minus in nodes_minus:
        coords_minus = [nodes_coords[n_minus][i] for i in coord_indices]
        
        for n_plus in nodes_plus:
            coords_plus = [nodes_coords[n_plus][i] for i in coord_indices]
            
            # Verifier si les coordonnees correspondent
            match = True
            for c1, c2 in zip(coords_minus, coords_plus):
                if abs(c1 - c2) > tol:
                    match = False
                    break
            
            if match:
                pairs.append((n_minus, n_plus))
                break
    
    return pairs


# =============================================================================
# GENERATION DES EQUATIONS MPC
# =============================================================================

def generate_coupling_equations(coupling_info, nodes_matrice, output_file):
    """
    Genere les equations de couplage macro-micro.
    
    Pour la methode DFE2, les 8 coins du RVE sont lies aux 8 noeuds de 
    l'element macro. Comme le RVE est place au centre (point de Gauss 0,0,0),
    et que le RVE occupe exactement le volume de l'element macro,
    chaque coin du RVE correspond directement a un noeud de l'element macro.
    
    Convention de correspondance:
    - Coin RVE V1 (0,0,0) -> Noeud macro 1 (x-,y-,z-)
    - Coin RVE V2 (L,0,0) -> Noeud macro 2 (x+,y-,z-)
    - Coin RVE V3 (L,H,0) -> Noeud macro 3 (x+,y+,z-)
    - Coin RVE V4 (0,H,0) -> Noeud macro 4 (x-,y+,z-)
    - Coin RVE V5 (0,0,T) -> Noeud macro 5 (x-,y-,z+)
    - Coin RVE V6 (L,0,T) -> Noeud macro 6 (x+,y-,z+)
    - Coin RVE V7 (L,H,T) -> Noeud macro 7 (x+,y+,z+)
    - Coin RVE V8 (0,H,T) -> Noeud macro 8 (x-,y+,z+)
    
    Equation simple: u_RVE_corner_i = u_macro_i
    En format Abaqus: u_RVE - u_macro = 0
    """
    equations = []
    
    # Correspondance coin RVE -> indice noeud macro (dans la liste macro_nodes)
    # V1 -> indice 0, V2 -> indice 1, etc.
    corner_to_macro_idx = {
        1: 0,  # V1 -> noeud macro 1 (indice 0)
        2: 1,  # V2 -> noeud macro 2 (indice 1)
        3: 2,  # V3 -> noeud macro 3 (indice 2)
        4: 3,  # V4 -> noeud macro 4 (indice 3)
        5: 4,  # V5 -> noeud macro 5 (indice 4)
        6: 5,  # V6 -> noeud macro 6 (indice 5)
        7: 6,  # V7 -> noeud macro 7 (indice 6)
        8: 7,  # V8 -> noeud macro 8 (indice 7)
    }
    
    # Identifier les coins du RVE dans la Matrice
    corners_matrice, _, _ = identify_rve_corners_and_faces(
        nodes_matrice, RVE_L, RVE_H, RVE_T, TOLERANCE
    )
    
    print(f"Coins identifies dans la Matrice: {corners_matrice}")
    
    for elem_id in sorted(coupling_info['macro_elements'].keys()):
        macro_nodes = coupling_info['macro_elements'][elem_id]
        
        for gp_idx in range(coupling_info['num_gauss']):
            # Pour chaque coin du RVE
            for corner_local in range(1, 9):
                corner_name = f'V{corner_local}'
                
                if corner_name not in corners_matrice:
                    print(f"  ATTENTION: Coin {corner_name} non trouve dans la Matrice")
                    continue
                
                rve_corner_node = corners_matrice[corner_name]
                macro_idx = corner_to_macro_idx[corner_local]
                macro_node = macro_nodes[macro_idx]
                
                # Pour chaque degre de liberte (1, 2, 3)
                for dof in [1, 2, 3]:
                    # Generer l'equation: u_RVE_corner - u_macro = 0
                    instance_name = f"Matrice_E{elem_id}_GP{gp_idx+1}"
                    terms = [
                        (f"{instance_name}.{rve_corner_node}", dof, 1.0),
                        (f"MACRO-1.{macro_node}", dof, -1.0),
                    ]
                    equations.append(terms)
    
    return equations


def generate_pbc_equations(nodes_matrice, elem_id, gp_idx):
    """
    Genere les equations PBC (Periodic Boundary Conditions) pour un RVE.
    
    PBC sur faces opposees:
    u(x+) - u(x-) = u(V2) - u(V1)  (face X)
    u(y+) - u(y-) = u(V4) - u(V1)  (face Y)
    u(z+) - u(z-) = u(V5) - u(V1)  (face Z)
    
    En format equation:
    u(x+) - u(x-) - u(V2) + u(V1) = 0
    """
    equations = []
    instance_name = f"Matrice_E{elem_id}_GP{gp_idx+1}"
    
    # Identifier les coins, faces et aretes
    corners, faces, edges = identify_rve_corners_and_faces(
        nodes_matrice, RVE_L, RVE_H, RVE_T, TOLERANCE
    )
    
    # Verifier que les coins sont trouves
    required_corners = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8']
    for c in required_corners:
        if c not in corners:
            print(f"  ATTENTION: Coin {c} manquant, PBC incompletes")
            return equations
    
    # =========================================================================
    # PBC sur les faces (noeuds interieurs aux faces)
    # =========================================================================
    
    # Face X: FACE_XN (x=0) <-> FACE_XP (x=L), reference V2-V1
    pairs_x = find_paired_nodes(
        faces['FACE_XN'], faces['FACE_XP'],
        [1, 2],  # Comparer y et z
        nodes_matrice, TOLERANCE
    )
    
    for n_minus, n_plus in pairs_x:
        for dof in [1, 2, 3]:
            # u(x+) - u(x-) - u(V2) + u(V1) = 0
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V2']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # Face Y: FACE_YN (y=0) <-> FACE_YP (y=H), reference V4-V1
    pairs_y = find_paired_nodes(
        faces['FACE_YN'], faces['FACE_YP'],
        [0, 2],  # Comparer x et z
        nodes_matrice, TOLERANCE
    )
    
    for n_minus, n_plus in pairs_y:
        for dof in [1, 2, 3]:
            # u(y+) - u(y-) - u(V4) + u(V1) = 0
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V4']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # Face Z: FACE_ZN (z=0) <-> FACE_ZP (z=T), reference V5-V1
    pairs_z = find_paired_nodes(
        faces['FACE_ZN'], faces['FACE_ZP'],
        [0, 1],  # Comparer x et y
        nodes_matrice, TOLERANCE
    )
    
    for n_minus, n_plus in pairs_z:
        for dof in [1, 2, 3]:
            # u(z+) - u(z-) - u(V5) + u(V1) = 0
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V5']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # =========================================================================
    # PBC sur les aretes
    # =========================================================================
    
    # Aretes paralleles a X
    # EDGE_X_Y0_Z0 <-> EDGE_X_YH_Z0 (reference V4-V1)
    pairs = find_paired_nodes(
        edges['EDGE_X_Y0_Z0'], edges['EDGE_X_YH_Z0'],
        [0],  # Comparer x
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V4']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # EDGE_X_Y0_Z0 <-> EDGE_X_Y0_ZT (reference V5-V1)
    pairs = find_paired_nodes(
        edges['EDGE_X_Y0_Z0'], edges['EDGE_X_Y0_ZT'],
        [0],  # Comparer x
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V5']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # EDGE_X_Y0_Z0 <-> EDGE_X_YH_ZT (reference V8-V1)
    pairs = find_paired_nodes(
        edges['EDGE_X_Y0_Z0'], edges['EDGE_X_YH_ZT'],
        [0],  # Comparer x
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V8']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # Aretes paralleles a Y
    # EDGE_Y_X0_Z0 <-> EDGE_Y_XL_Z0 (reference V2-V1)
    pairs = find_paired_nodes(
        edges['EDGE_Y_X0_Z0'], edges['EDGE_Y_XL_Z0'],
        [1],  # Comparer y
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V2']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # EDGE_Y_X0_Z0 <-> EDGE_Y_X0_ZT (reference V5-V1)
    pairs = find_paired_nodes(
        edges['EDGE_Y_X0_Z0'], edges['EDGE_Y_X0_ZT'],
        [1],  # Comparer y
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V5']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # EDGE_Y_X0_Z0 <-> EDGE_Y_XL_ZT (reference V6-V1)
    pairs = find_paired_nodes(
        edges['EDGE_Y_X0_Z0'], edges['EDGE_Y_XL_ZT'],
        [1],  # Comparer y
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V6']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # Aretes paralleles a Z
    # EDGE_Z_X0_Y0 <-> EDGE_Z_XL_Y0 (reference V2-V1)
    pairs = find_paired_nodes(
        edges['EDGE_Z_X0_Y0'], edges['EDGE_Z_XL_Y0'],
        [2],  # Comparer z
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V2']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # EDGE_Z_X0_Y0 <-> EDGE_Z_X0_YH (reference V4-V1)
    pairs = find_paired_nodes(
        edges['EDGE_Z_X0_Y0'], edges['EDGE_Z_X0_YH'],
        [2],  # Comparer z
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V4']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # EDGE_Z_X0_Y0 <-> EDGE_Z_XL_YH (reference V3-V1)
    pairs = find_paired_nodes(
        edges['EDGE_Z_X0_Y0'], edges['EDGE_Z_XL_YH'],
        [2],  # Comparer z
        nodes_matrice, TOLERANCE
    )
    for n_minus, n_plus in pairs:
        for dof in [1, 2, 3]:
            terms = [
                (f"{instance_name}.{n_plus}", dof, 1.0),
                (f"{instance_name}.{n_minus}", dof, -1.0),
                (f"{instance_name}.{corners['V3']}", dof, -1.0),
                (f"{instance_name}.{corners['V1']}", dof, 1.0),
            ]
            equations.append(terms)
    
    # =========================================================================
    # PBC pour les coins (lier les 7 autres coins a V1)
    # =========================================================================
    
    # V3 = V1 + (V2-V1) + (V4-V1) = V2 + V4 - V1
    # => V3 - V2 - V4 + V1 = 0
    for dof in [1, 2, 3]:
        terms = [
            (f"{instance_name}.{corners['V3']}", dof, 1.0),
            (f"{instance_name}.{corners['V2']}", dof, -1.0),
            (f"{instance_name}.{corners['V4']}", dof, -1.0),
            (f"{instance_name}.{corners['V1']}", dof, 1.0),
        ]
        equations.append(terms)
    
    # V6 = V1 + (V2-V1) + (V5-V1) = V2 + V5 - V1
    for dof in [1, 2, 3]:
        terms = [
            (f"{instance_name}.{corners['V6']}", dof, 1.0),
            (f"{instance_name}.{corners['V2']}", dof, -1.0),
            (f"{instance_name}.{corners['V5']}", dof, -1.0),
            (f"{instance_name}.{corners['V1']}", dof, 1.0),
        ]
        equations.append(terms)
    
    # V7 = V1 + (V2-V1) + (V4-V1) + (V5-V1) = V2 + V4 + V5 - 2*V1
    for dof in [1, 2, 3]:
        terms = [
            (f"{instance_name}.{corners['V7']}", dof, 1.0),
            (f"{instance_name}.{corners['V2']}", dof, -1.0),
            (f"{instance_name}.{corners['V4']}", dof, -1.0),
            (f"{instance_name}.{corners['V5']}", dof, -1.0),
            (f"{instance_name}.{corners['V1']}", dof, 2.0),
        ]
        equations.append(terms)
    
    # V8 = V1 + (V4-V1) + (V5-V1) = V4 + V5 - V1
    for dof in [1, 2, 3]:
        terms = [
            (f"{instance_name}.{corners['V8']}", dof, 1.0),
            (f"{instance_name}.{corners['V4']}", dof, -1.0),
            (f"{instance_name}.{corners['V5']}", dof, -1.0),
            (f"{instance_name}.{corners['V1']}", dof, 1.0),
        ]
        equations.append(terms)
    
    return equations


def write_equations_to_file(equations, output_file):
    """
    Ecrit les equations MPC dans le fichier de sortie.
    
    Format Abaqus:
    *Equation
    n_terms
    node1, dof1, coef1, node2, dof2, coef2, ...
    """
    with open(output_file, 'a') as f:
        f.write("** =============================================================\n")
        f.write("** MPC EQUATIONS - MACRO-MICRO COUPLING AND PBC\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        for eq_idx, terms in enumerate(equations):
            f.write(f"*Equation\n")
            f.write(f"{len(terms)}\n")
            
            # Ecrire les termes (max 4 par ligne pour lisibilite)
            term_strs = []
            for node_ref, dof, coef in terms:
                term_strs.append(f"{node_ref}, {dof}, {coef:.10f}")
            
            # Ecrire par lignes de 2 termes max
            for i in range(0, len(term_strs), 2):
                chunk = term_strs[i:i+2]
                f.write(", ".join(chunk) + "\n")
        
        f.write("**\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Programme principal.
    """
    print("=" * 60)
    print("input_file_PBCs_3D.py")
    print("Ajout des equations MPC pour DFE2")
    print("=" * 60)
    print()
    
    # Verifier que les fichiers existent
    if not os.path.exists(INPUT_FILE):
        print(f"ERREUR: Fichier d'entree non trouve: {INPUT_FILE}")
        print("Executez d'abord micro_RVE_placement_3D.py")
        return
    
    if not os.path.exists(COUPLING_INFO_FILE):
        print(f"ERREUR: Fichier d'info couplage non trouve: {COUPLING_INFO_FILE}")
        print("Executez d'abord micro_RVE_placement_3D.py")
        return
    
    # Charger les informations de couplage
    print(f"Chargement des informations de couplage: {COUPLING_INFO_FILE}")
    coupling_info = load_coupling_info(COUPLING_INFO_FILE)
    print(f"  - {coupling_info['num_elements']} elements macro")
    print(f"  - {coupling_info['num_gauss']} point(s) de Gauss")
    print()
    
    # Charger les noeuds du RVE (Matrice)
    print(f"Lecture des noeuds RVE depuis: {INPUT_FILE}")
    nodes_matrice = parse_rve_nodes_from_inp(INPUT_FILE, "Matrice")
    print(f"  - {len(nodes_matrice)} noeuds dans la Matrice")
    print()
    
    # Copier le fichier d'entree vers le fichier de sortie
    print(f"Copie du fichier vers: {OUTPUT_FILE}")
    with open(INPUT_FILE, 'r') as f_in:
        content = f_in.read()
    
    # Trouver la position pour inserer les equations (avant *End Assembly ou a la fin)
    insert_pos = content.find("*End Assembly")
    if insert_pos == -1:
        insert_pos = len(content)
    
    # Ecrire le debut du fichier
    with open(OUTPUT_FILE, 'w') as f_out:
        f_out.write(content[:insert_pos])
    
    # Generer et ecrire les equations de couplage macro-micro
    print("Generation des equations de couplage macro-micro...")
    coupling_equations = generate_coupling_equations(coupling_info, nodes_matrice, OUTPUT_FILE)
    print(f"  - {len(coupling_equations)} equations de couplage")
    
    # Generer les equations PBC pour chaque RVE
    print("Generation des equations PBC...")
    all_pbc_equations = []
    
    for elem_id in sorted(coupling_info['macro_elements'].keys()):
        for gp_idx in range(coupling_info['num_gauss']):
            pbc_equations = generate_pbc_equations(nodes_matrice, elem_id, gp_idx)
            all_pbc_equations.extend(pbc_equations)
    
    print(f"  - {len(all_pbc_equations)} equations PBC")
    
    # Combiner toutes les equations
    all_equations = coupling_equations + all_pbc_equations
    print(f"Total: {len(all_equations)} equations MPC")
    print()
    
    # Ecrire les equations dans le fichier
    write_equations_to_file(all_equations, OUTPUT_FILE)
    
    # Ecrire la fin du fichier
    with open(OUTPUT_FILE, 'a') as f_out:
        f_out.write(content[insert_pos:])
    
    print(f"Fichier {OUTPUT_FILE} genere avec succes!")
    print()
    
    print("=" * 60)
    print("Generation terminee!")
    print(f"Fichier final: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
