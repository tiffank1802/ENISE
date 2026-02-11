#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
micro_RVE_placement_3D.py

Script de placement des RVE aux points de Gauss des elements macro
pour la methode Direct FE² en 3D.

Base sur la methodologie du repository DirectFE2:
https://github.com/rkarthikayen89/DirectFE2-sample-codes

Adapte pour le cas 3D avec elements hexaedriques C3D8R/C3D8.

Auteur: Projet ENISE - Methodes numeriques avancees
Date: 2024
"""

import numpy as np
import re
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

# Fichiers d'entree
MACRO_FILE = "TRC_Macro_3D.inp"
RVE_FILE = "TRC_RVE.inp"

# Fichier de sortie
OUTPUT_FILE = "DFE2_placed.inp"

# Dimensions du RVE (mm)
RVE_L = 5.5   # Longueur en X
RVE_H = 5.5   # Hauteur en Y  
RVE_T = 6.69  # Epaisseur en Z

# Type d'element macro (pour determiner le nombre de points de Gauss)
# C3D8R: 1 point de Gauss (integration reduite)
# C3D8: 8 points de Gauss (integration complete)
ELEMENT_TYPE = "C3D8R"

# Position des points de Gauss en coordonnees naturelles [-1, 1]
if ELEMENT_TYPE == "C3D8R":
    # Integration reduite: 1 point au centre
    GAUSS_POINTS = [(0.0, 0.0, 0.0)]
elif ELEMENT_TYPE == "C3D8":
    # Integration complete: 8 points
    g = 1.0 / np.sqrt(3.0)
    GAUSS_POINTS = [
        (-g, -g, -g), (g, -g, -g), (g, g, -g), (-g, g, -g),
        (-g, -g, g), (g, -g, g), (g, g, g), (-g, g, g)
    ]
else:
    raise ValueError(f"Type d'element non supporte: {ELEMENT_TYPE}")


# =============================================================================
# FONCTIONS DE FORME C3D8 (Hexaedre 8 noeuds)
# =============================================================================

def shape_functions_C3D8(xi, eta, zeta):
    """
    Fonctions de forme pour un hexaedre a 8 noeuds.
    
    Convention de numerotation (Abaqus):
        5-------8
       /|      /|
      / |     / |
     6-------7  |
     |  1----|--4
     | /     | /
     |/      |/
     2-------3
    
    En coordonnees naturelles:
        N1: (-1,-1,-1)  N2: (+1,-1,-1)  N3: (+1,+1,-1)  N4: (-1,+1,-1)
        N5: (-1,-1,+1)  N6: (+1,-1,+1)  N7: (+1,+1,+1)  N8: (-1,+1,+1)
    
    ATTENTION: Convention Abaqus pour C3D8:
        1: (x-,y-,z-)  2: (x+,y-,z-)  3: (x+,y+,z-)  4: (x-,y+,z-)
        5: (x-,y-,z+)  6: (x+,y-,z+)  7: (x+,y+,z+)  8: (x-,y+,z+)
    """
    N = np.zeros(8)
    
    # Fonctions de forme
    N[0] = 0.125 * (1 - xi) * (1 - eta) * (1 - zeta)  # N1
    N[1] = 0.125 * (1 + xi) * (1 - eta) * (1 - zeta)  # N2
    N[2] = 0.125 * (1 + xi) * (1 + eta) * (1 - zeta)  # N3
    N[3] = 0.125 * (1 - xi) * (1 + eta) * (1 - zeta)  # N4
    N[4] = 0.125 * (1 - xi) * (1 - eta) * (1 + zeta)  # N5
    N[5] = 0.125 * (1 + xi) * (1 - eta) * (1 + zeta)  # N6
    N[6] = 0.125 * (1 + xi) * (1 + eta) * (1 + zeta)  # N7
    N[7] = 0.125 * (1 - xi) * (1 + eta) * (1 + zeta)  # N8
    
    return N


def gauss_point_coordinates(node_coords, xi, eta, zeta):
    """
    Calcule les coordonnees physiques d'un point de Gauss
    a partir des coordonnees des 8 noeuds de l'element.
    
    node_coords: array (8, 3) des coordonnees des noeuds
    xi, eta, zeta: coordonnees naturelles du point de Gauss
    
    Retourne: (x, y, z) coordonnees physiques
    """
    N = shape_functions_C3D8(xi, eta, zeta)
    
    x = np.dot(N, node_coords[:, 0])
    y = np.dot(N, node_coords[:, 1])
    z = np.dot(N, node_coords[:, 2])
    
    return x, y, z


# =============================================================================
# PARSEUR DE FICHIER .inp
# =============================================================================

def parse_macro_inp(filename):
    """
    Parse le fichier macro .inp pour extraire les noeuds et elements.
    
    Retourne:
        nodes: dict {node_id: (x, y, z)}
        elements: dict {elem_id: [n1, n2, n3, n4, n5, n6, n7, n8]}
        part_name: nom de la part
    """
    nodes = {}
    elements = {}
    part_name = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detecter le nom de la part
        if line.upper().startswith('*PART'):
            match = re.search(r'NAME\s*=\s*(\S+)', line, re.IGNORECASE)
            if match:
                part_name = match.group(1)
        
        # Lire les noeuds
        elif line.upper().startswith('*NODE') and 'OUTPUT' not in line.upper():
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('*'):
                node_line = lines[i].strip()
                if node_line and not node_line.startswith('**'):
                    parts = node_line.split(',')
                    if len(parts) >= 4:
                        node_id = int(parts[0].strip())
                        x = float(parts[1].strip())
                        y = float(parts[2].strip())
                        z = float(parts[3].strip())
                        nodes[node_id] = (x, y, z)
                i += 1
            continue
        
        # Lire les elements
        elif line.upper().startswith('*ELEMENT'):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('*'):
                elem_line = lines[i].strip()
                if elem_line and not elem_line.startswith('**'):
                    parts = elem_line.split(',')
                    if len(parts) >= 9:  # elem_id + 8 noeuds
                        elem_id = int(parts[0].strip())
                        node_ids = [int(p.strip()) for p in parts[1:9]]
                        elements[elem_id] = node_ids
                i += 1
            continue
        
        i += 1
    
    return nodes, elements, part_name


def parse_rve_inp(filename):
    """
    Parse le fichier RVE .inp pour extraire la geometrie complete.
    Le fichier peut contenir plusieurs parts (Matrice, Fibre).
    
    Retourne:
        parts: dict {part_name: {'nodes': {id: (x,y,z)}, 'elements': {id: [nodes]}, 'elem_type': type}}
        full_content: contenu complet du fichier
    """
    parts = {}
    
    with open(filename, 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    current_part = None
    current_section = None
    elem_type = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detecter une nouvelle part
        if line.upper().startswith('*PART'):
            match = re.search(r'NAME\s*=\s*(\S+)', line, re.IGNORECASE)
            if match:
                current_part = match.group(1)
                parts[current_part] = {'nodes': {}, 'elements': {}, 'elem_type': None}
            i += 1
            continue
        
        # Fin de part
        elif line.upper().startswith('*END PART'):
            current_part = None
            i += 1
            continue
        
        # Lire les noeuds de la part courante
        elif line.upper().startswith('*NODE') and current_part and 'OUTPUT' not in line.upper():
            current_section = 'nodes'
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('*'):
                node_line = lines[i].strip()
                if node_line and not node_line.startswith('**'):
                    parts_data = node_line.split(',')
                    if len(parts_data) >= 4:
                        node_id = int(parts_data[0].strip())
                        x = float(parts_data[1].strip())
                        y = float(parts_data[2].strip())
                        z = float(parts_data[3].strip())
                        parts[current_part]['nodes'][node_id] = (x, y, z)
                i += 1
            continue
        
        # Lire les elements de la part courante
        elif line.upper().startswith('*ELEMENT') and current_part:
            # Extraire le type d'element
            match = re.search(r'TYPE\s*=\s*(\S+)', line, re.IGNORECASE)
            if match:
                parts[current_part]['elem_type'] = match.group(1).rstrip(',')
            
            current_section = 'elements'
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('*'):
                elem_line = lines[i].strip()
                if elem_line and not elem_line.startswith('**'):
                    parts_data = elem_line.split(',')
                    if len(parts_data) >= 2:
                        elem_id = int(parts_data[0].strip())
                        node_ids = [int(p.strip()) for p in parts_data[1:] if p.strip()]
                        parts[current_part]['elements'][elem_id] = node_ids
                i += 1
            continue
        
        i += 1
    
    return parts, content


# =============================================================================
# GENERATION DU FICHIER DE SORTIE
# =============================================================================

def generate_output_file(macro_nodes, macro_elements, macro_part_name, 
                         rve_parts, output_filename):
    """
    Genere le fichier .inp avec les RVE places aux points de Gauss.
    
    Structure du fichier:
    1. En-tete
    2. Part macro (avec noeuds de reference)
    3. Parts RVE (Matrice, Fibre)
    4. Assembly avec instances placees
    5. Materials et Sections
    """
    
    num_elements = len(macro_elements)
    num_gauss = len(GAUSS_POINTS)
    total_rve = num_elements * num_gauss
    
    print(f"Generation du fichier {output_filename}...")
    print(f"  - {num_elements} elements macro")
    print(f"  - {num_gauss} point(s) de Gauss par element")
    print(f"  - {total_rve} RVE au total")
    
    with open(output_filename, 'w') as f:
        # =================================================================
        # EN-TETE
        # =================================================================
        f.write("*Heading\n")
        f.write("** DFE2 Multi-scale Model - Generated by micro_RVE_placement_3D.py\n")
        f.write(f"** Macro model: {MACRO_FILE}\n")
        f.write(f"** RVE model: {RVE_FILE}\n")
        f.write(f"** Number of macro elements: {num_elements}\n")
        f.write(f"** Number of Gauss points per element: {num_gauss}\n")
        f.write(f"** Total RVE instances: {total_rve}\n")
        f.write(f"** RVE dimensions: {RVE_L} x {RVE_H} x {RVE_T} mm\n")
        f.write("**\n")
        f.write("*Preprint, echo=NO, model=NO, history=NO, contact=NO\n")
        f.write("**\n")
        
        # =================================================================
        # PART MACRO (beam) avec noeuds de reference pour couplage
        # =================================================================
        f.write("** =============================================================\n")
        f.write("** PART: MACRO MODEL (beam)\n")
        f.write("** =============================================================\n")
        f.write("*Part, name=beam\n")
        f.write("*Node\n")
        
        # Ecrire les noeuds macro
        for node_id in sorted(macro_nodes.keys()):
            x, y, z = macro_nodes[node_id]
            f.write(f"{node_id:6d}, {x:14.10f}, {y:14.10f}, {z:14.10f}\n")
        
        # Creer des noeuds de reference (RP) pour chaque noeud macro
        # Ces noeuds serviront au couplage avec les coins des RVE
        # Format: pour chaque element, 8 noeuds de reference N1-RP_elemX a N8-RP_elemX
        f.write("**\n")
        f.write("** Reference nodes for macro-micro coupling\n")
        
        # Offset pour les noeuds de reference
        max_macro_node = max(macro_nodes.keys())
        rp_node_offset = max_macro_node + 1000
        
        rp_node_id = rp_node_offset
        rp_nodes_map = {}  # {(elem_id, local_node): rp_node_id}
        
        for elem_id in sorted(macro_elements.keys()):
            elem_nodes = macro_elements[elem_id]
            for gp_idx, (xi, eta, zeta) in enumerate(GAUSS_POINTS):
                # Calculer les coordonnees du point de Gauss
                node_coords = np.array([macro_nodes[n] for n in elem_nodes])
                gp_x, gp_y, gp_z = gauss_point_coordinates(node_coords, xi, eta, zeta)
                
                # Creer 8 noeuds de reference a la position du point de Gauss
                # (ils seront deplaces par les equations MPC)
                for local_node in range(1, 9):
                    key = (elem_id, gp_idx, local_node)
                    rp_nodes_map[key] = rp_node_id
                    f.write(f"{rp_node_id:6d}, {gp_x:14.10f}, {gp_y:14.10f}, {gp_z:14.10f}\n")
                    rp_node_id += 1
        
        # Elements macro (pas necessaires pour DFE2, mais on les garde pour reference)
        f.write("**\n")
        f.write(f"*Element, type={ELEMENT_TYPE}\n")
        for elem_id in sorted(macro_elements.keys()):
            nodes = macro_elements[elem_id]
            f.write(f"{elem_id:6d}, " + ", ".join([f"{n:6d}" for n in nodes]) + "\n")
        
        # Node sets pour les noeuds de reference
        f.write("**\n")
        f.write("** Node sets for reference points\n")
        for elem_id in sorted(macro_elements.keys()):
            for gp_idx in range(num_gauss):
                f.write(f"*Nset, nset=RP_E{elem_id}_GP{gp_idx+1}\n")
                rp_ids = [rp_nodes_map[(elem_id, gp_idx, i)] for i in range(1, 9)]
                f.write(", ".join([str(n) for n in rp_ids]) + "\n")
        
        # Sets individuels pour chaque noeud de reference (N1-RP, N2-RP, etc.)
        for elem_id in sorted(macro_elements.keys()):
            for gp_idx in range(num_gauss):
                for local_node in range(1, 9):
                    rp_id = rp_nodes_map[(elem_id, gp_idx, local_node)]
                    f.write(f"*Nset, nset=N{local_node}-RP_E{elem_id}_GP{gp_idx+1}\n")
                    f.write(f"{rp_id}\n")
        
        f.write("*End Part\n")
        f.write("**\n")
        
        # =================================================================
        # PARTS RVE (Matrice et Fibre)
        # =================================================================
        f.write("** =============================================================\n")
        f.write("** PARTS: RVE COMPONENTS\n")
        f.write("** =============================================================\n")
        
        for part_name, part_data in rve_parts.items():
            f.write(f"*Part, name={part_name}\n")
            f.write("*Node\n")
            
            for node_id in sorted(part_data['nodes'].keys()):
                x, y, z = part_data['nodes'][node_id]
                f.write(f"{node_id:6d}, {x:14.10f}, {y:14.10f}, {z:14.10f}\n")
            
            elem_type = part_data['elem_type'] or 'C3D8R'
            f.write(f"*Element, type={elem_type}\n")
            
            for elem_id in sorted(part_data['elements'].keys()):
                nodes = part_data['elements'][elem_id]
                node_str = ", ".join([str(n) for n in nodes])
                f.write(f"{elem_id:6d}, {node_str}\n")
            
            # Node sets pour les coins du RVE (pour les PBC)
            # Identifier les coins du RVE
            corner_tolerance = 0.01
            corners = identify_rve_corners(part_data['nodes'], RVE_L, RVE_H, RVE_T, corner_tolerance)
            
            if corners:
                f.write("**\n")
                f.write("** Corner node sets for PBC\n")
                corner_names = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8']
                for i, (corner_name, node_id) in enumerate(zip(corner_names, corners)):
                    if node_id:
                        f.write(f"*Nset, nset={corner_name}\n")
                        f.write(f"{node_id}\n")
            
            # Node sets pour les faces du RVE
            faces = identify_rve_faces(part_data['nodes'], RVE_L, RVE_H, RVE_T, corner_tolerance)
            if faces:
                f.write("**\n")
                f.write("** Face node sets for PBC\n")
                for face_name, node_ids in faces.items():
                    if node_ids:
                        f.write(f"*Nset, nset={face_name}\n")
                        # Ecrire les noeuds par lignes de 16 max
                        for j in range(0, len(node_ids), 16):
                            chunk = node_ids[j:j+16]
                            f.write(", ".join([str(n) for n in chunk]) + "\n")
            
            f.write("*End Part\n")
            f.write("**\n")
        
        # =================================================================
        # ASSEMBLY
        # =================================================================
        f.write("** =============================================================\n")
        f.write("** ASSEMBLY\n")
        f.write("** =============================================================\n")
        f.write("*Assembly, name=Assembly\n")
        f.write("**\n")
        
        # Instance macro
        f.write("*Instance, name=MACRO-1, part=beam\n")
        f.write("*End Instance\n")
        f.write("**\n")
        
        # Instances RVE aux points de Gauss
        f.write("** RVE instances at Gauss points\n")
        
        for elem_id in sorted(macro_elements.keys()):
            elem_nodes = macro_elements[elem_id]
            node_coords = np.array([macro_nodes[n] for n in elem_nodes])
            
            for gp_idx, (xi, eta, zeta) in enumerate(GAUSS_POINTS):
                # Calculer la position du point de Gauss
                gp_x, gp_y, gp_z = gauss_point_coordinates(node_coords, xi, eta, zeta)
                
                # Translation pour centrer le RVE sur le point de Gauss
                # Le RVE a son origine en (0,0,0), donc on translate de:
                # (gp_x - RVE_L/2, gp_y - RVE_H/2, gp_z - RVE_T/2)
                # Note: le RVE_FILE a deja son origine en (0,0,0)
                tx = gp_x - RVE_L / 2.0
                ty = gp_y - RVE_H / 2.0
                tz = gp_z - RVE_T / 2.0
                
                # Creer une instance pour chaque part du RVE
                for part_name in rve_parts.keys():
                    instance_name = f"{part_name}_E{elem_id}_GP{gp_idx+1}"
                    f.write(f"*Instance, name={instance_name}, part={part_name}\n")
                    f.write(f"  {tx:14.10f}, {ty:14.10f}, {tz:14.10f}\n")
                    f.write("*End Instance\n")
        
        f.write("**\n")
        
        # Node sets pour le couplage (referencer les noeuds de l'instance macro)
        f.write("** Node sets for macro-micro coupling (assembly level)\n")
        for elem_id in sorted(macro_elements.keys()):
            elem_nodes = macro_elements[elem_id]
            for gp_idx in range(num_gauss):
                # Set pour les 8 noeuds macro de l'element
                f.write(f"*Nset, nset=MACRO_E{elem_id}_GP{gp_idx+1}, instance=MACRO-1\n")
                f.write(", ".join([str(n) for n in elem_nodes]) + "\n")
                
                # Sets individuels pour chaque noeud macro
                for local_node, global_node in enumerate(elem_nodes, start=1):
                    f.write(f"*Nset, nset=N{local_node}_E{elem_id}_GP{gp_idx+1}, instance=MACRO-1\n")
                    f.write(f"{global_node}\n")
        
        f.write("**\n")
        f.write("*End Assembly\n")
        f.write("**\n")
        
        # =================================================================
        # MATERIALS
        # =================================================================
        f.write("** =============================================================\n")
        f.write("** MATERIALS\n")
        f.write("** =============================================================\n")
        f.write("*Material, name=Fibre\n")
        f.write("*Elastic\n")
        f.write("200000., 0.2\n")
        f.write("**\n")
        f.write("*Material, name=Matrice\n")
        f.write("*Elastic\n")
        f.write("25000., 0.18\n")
        f.write("**\n")
        
        # =================================================================
        # SECTIONS (a completer apres les PBC)
        # =================================================================
        f.write("** =============================================================\n")
        f.write("** SECTION ASSIGNMENTS\n")
        f.write("** (To be completed in input_file_PBCs_3D.py)\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        # =================================================================
        # PLACEHOLDER POUR LES EQUATIONS MPC
        # =================================================================
        f.write("** =============================================================\n")
        f.write("** MPC EQUATIONS (To be added by input_file_PBCs_3D.py)\n")
        f.write("** =============================================================\n")
        f.write("**\n")
    
    print(f"Fichier {output_filename} genere avec succes!")
    
    # Retourner les informations pour le script suivant
    return {
        'rp_nodes_map': rp_nodes_map,
        'macro_elements': macro_elements,
        'macro_nodes': macro_nodes,
        'num_gauss': num_gauss,
        'rve_parts': rve_parts
    }


def identify_rve_corners(nodes, L, H, T, tol=0.01):
    """
    Identifie les 8 coins du RVE.
    
    Convention (origine 0,0,0):
        V1: (0,0,0)     V2: (L,0,0)     V3: (L,H,0)     V4: (0,H,0)
        V5: (0,0,T)     V6: (L,0,T)     V7: (L,H,T)     V8: (0,H,T)
    
    Retourne: liste de 8 node_ids ou None si non trouve
    """
    corner_coords = [
        (0, 0, 0),      # V1
        (L, 0, 0),      # V2
        (L, H, 0),      # V3
        (0, H, 0),      # V4
        (0, 0, T),      # V5
        (L, 0, T),      # V6
        (L, H, T),      # V7
        (0, H, T),      # V8
    ]
    
    corners = []
    for cx, cy, cz in corner_coords:
        found = None
        for node_id, (x, y, z) in nodes.items():
            if abs(x - cx) < tol and abs(y - cy) < tol and abs(z - cz) < tol:
                found = node_id
                break
        corners.append(found)
    
    return corners


def identify_rve_faces(nodes, L, H, T, tol=0.01):
    """
    Identifie les noeuds sur chaque face du RVE (sans les coins ni aretes).
    
    Faces:
        XN (x=0), XP (x=L)
        YN (y=0), YP (y=H)
        ZN (z=0), ZP (z=T)
    
    Retourne: dict {face_name: [node_ids]}
    """
    faces = {
        'FACE_XN': [],  # x = 0
        'FACE_XP': [],  # x = L
        'FACE_YN': [],  # y = 0
        'FACE_YP': [],  # y = H
        'FACE_ZN': [],  # z = 0
        'FACE_ZP': [],  # z = T
    }
    
    for node_id, (x, y, z) in nodes.items():
        on_xn = abs(x - 0) < tol
        on_xp = abs(x - L) < tol
        on_yn = abs(y - 0) < tol
        on_yp = abs(y - H) < tol
        on_zn = abs(z - 0) < tol
        on_zp = abs(z - T) < tol
        
        # Compter le nombre de faces sur lesquelles se trouve le noeud
        num_faces = sum([on_xn, on_xp, on_yn, on_yp, on_zn, on_zp])
        
        # Noeuds interieurs aux faces (pas sur les aretes ou coins)
        if num_faces == 1:
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
    for face_name in faces:
        faces[face_name].sort()
    
    return faces


def save_coupling_info(info, filename="coupling_info.txt"):
    """
    Sauvegarde les informations de couplage pour le script PBC.
    """
    with open(filename, 'w') as f:
        f.write("# Coupling information for DFE2\n")
        f.write(f"# Generated by micro_RVE_placement_3D.py\n\n")
        
        f.write(f"NUM_ELEMENTS={len(info['macro_elements'])}\n")
        f.write(f"NUM_GAUSS={info['num_gauss']}\n")
        f.write(f"RVE_L={RVE_L}\n")
        f.write(f"RVE_H={RVE_H}\n")
        f.write(f"RVE_T={RVE_T}\n\n")
        
        f.write("# Reference point nodes map: (elem_id, gp_idx, local_node) -> rp_node_id\n")
        for key, value in sorted(info['rp_nodes_map'].items()):
            f.write(f"RP_NODE,{key[0]},{key[1]},{key[2]},{value}\n")
        
        f.write("\n# Macro elements: elem_id -> [n1, n2, n3, n4, n5, n6, n7, n8]\n")
        for elem_id, nodes in sorted(info['macro_elements'].items()):
            f.write(f"ELEMENT,{elem_id}," + ",".join(map(str, nodes)) + "\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Programme principal.
    """
    print("=" * 60)
    print("micro_RVE_placement_3D.py")
    print("Placement des RVE aux points de Gauss - Methode DFE2")
    print("=" * 60)
    print()
    
    # Verifier que les fichiers existent
    if not os.path.exists(MACRO_FILE):
        print(f"ERREUR: Fichier macro non trouve: {MACRO_FILE}")
        return
    
    if not os.path.exists(RVE_FILE):
        print(f"ERREUR: Fichier RVE non trouve: {RVE_FILE}")
        return
    
    # Parser le fichier macro
    print(f"Lecture du fichier macro: {MACRO_FILE}")
    macro_nodes, macro_elements, macro_part_name = parse_macro_inp(MACRO_FILE)
    print(f"  - {len(macro_nodes)} noeuds")
    print(f"  - {len(macro_elements)} elements")
    print(f"  - Part: {macro_part_name}")
    print()
    
    # Parser le fichier RVE
    print(f"Lecture du fichier RVE: {RVE_FILE}")
    rve_parts, rve_content = parse_rve_inp(RVE_FILE)
    for part_name, part_data in rve_parts.items():
        print(f"  - Part '{part_name}': {len(part_data['nodes'])} noeuds, "
              f"{len(part_data['elements'])} elements, type={part_data['elem_type']}")
    print()
    
    # Generer le fichier de sortie
    print(f"Generation du fichier de sortie: {OUTPUT_FILE}")
    coupling_info = generate_output_file(
        macro_nodes, macro_elements, macro_part_name,
        rve_parts, OUTPUT_FILE
    )
    print()
    
    # Sauvegarder les informations de couplage
    save_coupling_info(coupling_info, "coupling_info.txt")
    print("Informations de couplage sauvegardees dans: coupling_info.txt")
    print()
    
    print("=" * 60)
    print("Placement termine!")
    print(f"Prochaine etape: executer input_file_PBCs_3D.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
