#!/usr/bin/env python3
"""
DFE2_TRC.py - Direct FE² Multi-scale Coupling for TRC Composites

This script implements the Direct FE² method to couple:
- Macro model: TRC_Macro_3D.inp (3D solid plate with C3D8R elements)
- Micro model: TRC_RVE.inp (RVE with Matrice + Fibre parts)

The method places RVE instances at each integration point of the 
macro elements and creates Multi-Point Constraints (MPC) to link the scales.

For 18 macro elements (1x18x1), this creates 18 RVE instances.

Author: Generated for ENISE Advanced Numerical Methods course
"""

import numpy as np
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import os

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Node:
    """Node data structure"""
    id: int
    x: float
    y: float
    z: float

@dataclass  
class Element:
    """Element data structure"""
    id: int
    nodes: List[int]
    elem_type: str

@dataclass
class Material:
    """Material properties"""
    name: str
    E: float
    nu: float

@dataclass
class Part:
    """Part data structure"""
    name: str
    nodes: Dict[int, Node]
    elements: Dict[int, Element]

# =============================================================================
# GAUSS INTEGRATION POINTS FOR C3D8R
# =============================================================================

# C3D8R has 1 integration point at center (reduced integration)
GAUSS_C3D8R = {
    'points': [(0.0, 0.0, 0.0)],
    'weights': [8.0]
}

# =============================================================================
# PARSER FUNCTIONS
# =============================================================================

def parse_inp_file_multipart(filepath: str) -> Tuple[Dict[str, Part], List[Material]]:
    """
    Parse an Abaqus .inp file with multiple parts.
    
    Returns:
        parts: Dictionary of Part objects keyed by part name
        materials: List of Material objects
    """
    parts = {}
    materials = []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all parts
    part_pattern = r'\*Part, name=(\w+)\n(.*?)\*End Part'
    part_matches = re.findall(part_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for part_name, part_content in part_matches:
        nodes = {}
        elements = {}
        
        lines = part_content.split('\n')
        i = 0
        current_elem_type = None
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Parse nodes
            if line.upper().startswith('*NODE') and 'NSET' not in line.upper():
                i += 1
                while i < len(lines):
                    current_line = lines[i].strip()
                    if current_line.startswith('*') and not current_line.startswith('**'):
                        break
                    if current_line.startswith('**') or not current_line:
                        i += 1
                        continue
                    parts_list = current_line.split(',')
                    if len(parts_list) >= 3:
                        try:
                            nid = int(parts_list[0])
                            x = float(parts_list[1])
                            y = float(parts_list[2])
                            z = float(parts_list[3]) if len(parts_list) > 3 else 0.0
                            nodes[nid] = Node(nid, x, y, z)
                        except (ValueError, IndexError):
                            pass
                    i += 1
                continue
            
            # Parse elements
            if line.upper().startswith('*ELEMENT'):
                match = re.search(r'TYPE\s*=\s*(\w+)', line, re.IGNORECASE)
                if match:
                    current_elem_type = match.group(1).upper()
                i += 1
                while i < len(lines):
                    current_line = lines[i].strip()
                    if current_line.startswith('*') and not current_line.startswith('**'):
                        break
                    if current_line.startswith('**') or not current_line:
                        i += 1
                        continue
                    parts_list = current_line.replace(' ', '').split(',')
                    parts_list = [p for p in parts_list if p]
                    if len(parts_list) >= 2 and current_elem_type:
                        try:
                            eid = int(parts_list[0])
                            node_ids = [int(p) for p in parts_list[1:]]
                            elements[eid] = Element(eid, node_ids, current_elem_type)
                        except (ValueError, IndexError):
                            pass
                    i += 1
                continue
            
            i += 1
        
        parts[part_name] = Part(part_name, nodes, elements)
    
    # Parse materials
    mat_pattern = r'\*Material, name=(\w+).*?\*Elastic\n\s*([\d.]+),\s*([\d.]+)'
    mat_matches = re.findall(mat_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for mat_name, E_str, nu_str in mat_matches:
        try:
            materials.append(Material(mat_name, float(E_str), float(nu_str)))
        except ValueError:
            pass
    
    return parts, materials


def parse_inp_file_simple(filepath: str) -> Tuple[Dict[int, Node], Dict[int, Element], List[Material]]:
    """Parse a simple .inp file (single part or macro model)."""
    nodes = {}
    elements = {}
    materials = []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    i = 0
    current_elem_type = None
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Parse nodes
        if line.upper().startswith('*NODE') and 'NSET' not in line.upper():
            i += 1
            while i < len(lines):
                current_line = lines[i].strip()
                if current_line.startswith('*') and not current_line.startswith('**'):
                    break
                if current_line.startswith('**') or not current_line:
                    i += 1
                    continue
                parts = current_line.split(',')
                if len(parts) >= 3:
                    try:
                        nid = int(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3]) if len(parts) > 3 else 0.0
                        nodes[nid] = Node(nid, x, y, z)
                    except (ValueError, IndexError):
                        pass
                i += 1
            continue
        
        # Parse elements
        if line.upper().startswith('*ELEMENT'):
            match = re.search(r'TYPE\s*=\s*(\w+)', line, re.IGNORECASE)
            if match:
                current_elem_type = match.group(1).upper()
            i += 1
            while i < len(lines):
                current_line = lines[i].strip()
                if current_line.startswith('*') and not current_line.startswith('**'):
                    break
                if current_line.startswith('**') or not current_line:
                    i += 1
                    continue
                parts = current_line.replace(' ', '').split(',')
                parts = [p for p in parts if p]
                if len(parts) >= 2 and current_elem_type:
                    try:
                        eid = int(parts[0])
                        node_ids = [int(p) for p in parts[1:]]
                        elements[eid] = Element(eid, node_ids, current_elem_type)
                    except (ValueError, IndexError):
                        pass
                i += 1
            continue
        
        # Parse materials
        if line.upper().startswith('*MATERIAL'):
            match = re.search(r'NAME\s*=\s*(\w+)', line, re.IGNORECASE)
            if match:
                mat_name = match.group(1)
                i += 1
                while i < len(lines):
                    if lines[i].strip().upper().startswith('*ELASTIC'):
                        i += 1
                        if i < len(lines):
                            parts = lines[i].strip().split(',')
                            if len(parts) >= 2:
                                try:
                                    E = float(parts[0])
                                    nu = float(parts[1])
                                    materials.append(Material(mat_name, E, nu))
                                except ValueError:
                                    pass
                        break
                    elif lines[i].strip().startswith('*') and not lines[i].strip().startswith('**'):
                        break
                    i += 1
            continue
        
        i += 1
    
    return nodes, elements, materials


# =============================================================================
# SHAPE FUNCTIONS FOR C3D8 (8-node hexahedron)
# =============================================================================

def shape_functions_C3D8(xi: float, eta: float, zeta: float) -> np.ndarray:
    """Shape functions for 8-node hexahedron."""
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
# RVE UTILITIES
# =============================================================================

def get_rve_dimensions_from_part(part: Part) -> Tuple[float, float, float]:
    """Calculate RVE bounding box dimensions from a part."""
    xs = [n.x for n in part.nodes.values()]
    ys = [n.y for n in part.nodes.values()]
    zs = [n.z for n in part.nodes.values()]
    return max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)


def identify_corner_nodes_in_part(part: Part, dims: Tuple[float, float, float], 
                                   tol: float = 1e-4) -> Dict[str, int]:
    """Identify the 8 corner nodes of the RVE (assuming origin at 0,0,0)."""
    B, H, T = dims
    
    corners = {
        'V1': (0, 0, 0),
        'V2': (B, 0, 0),
        'V3': (B, H, 0),
        'V4': (0, H, 0),
        'V5': (0, 0, T),
        'V6': (B, 0, T),
        'V7': (B, H, T),
        'V8': (0, H, T),
    }
    
    corner_nodes = {}
    for name, (cx, cy, cz) in corners.items():
        for nid, node in part.nodes.items():
            if (abs(node.x - cx) < tol and 
                abs(node.y - cy) < tol and 
                abs(node.z - cz) < tol):
                corner_nodes[name] = nid
                break
    
    return corner_nodes


def identify_face_nodes_in_part(part: Part, dims: Tuple[float, float, float],
                                 tol: float = 1e-4) -> Dict[str, List[int]]:
    """Identify nodes on each face of the RVE."""
    B, H, T = dims
    
    faces = {'XN': [], 'XP': [], 'YN': [], 'YP': [], 'ZN': [], 'ZP': []}
    
    for nid, node in part.nodes.items():
        if abs(node.x - 0) < tol:
            faces['XN'].append(nid)
        if abs(node.x - B) < tol:
            faces['XP'].append(nid)
        if abs(node.y - 0) < tol:
            faces['YN'].append(nid)
        if abs(node.y - H) < tol:
            faces['YP'].append(nid)
        if abs(node.z - 0) < tol:
            faces['ZN'].append(nid)
        if abs(node.z - T) < tol:
            faces['ZP'].append(nid)
    
    return faces


def pair_face_nodes(part: Part, face_n: List[int], face_p: List[int],
                    direction: int, dims: Tuple[float, float, float], 
                    tol: float = 1e-4) -> List[Tuple[int, int]]:
    """Pair nodes on opposite faces for PBC."""
    pairs = []
    dim_offset = dims[direction]
    
    for n_minus in face_n:
        node_m = part.nodes[n_minus]
        pos_m = [node_m.x, node_m.y, node_m.z]
        pos_p_expected = pos_m.copy()
        pos_p_expected[direction] += dim_offset
        
        for n_plus in face_p:
            node_p = part.nodes[n_plus]
            pos_p = [node_p.x, node_p.y, node_p.z]
            
            if (abs(pos_p[0] - pos_p_expected[0]) < tol and
                abs(pos_p[1] - pos_p_expected[1]) < tol and
                abs(pos_p[2] - pos_p_expected[2]) < tol):
                pairs.append((n_minus, n_plus))
                break
    
    return pairs


# =============================================================================
# DFE² MODEL GENERATION
# =============================================================================

def generate_dfe2_inp(macro_file: str, rve_file: str, output_file: str):
    """
    Generate the combined DFE² input file.
    
    This creates a single Abaqus input file that contains:
    1. All macro nodes (control nodes)
    2. RVE instances (Matrice + Fibre) at each integration point
    3. MPC equations linking macro nodes to RVE corner nodes
    4. PBC equations on each RVE
    """
    
    print("=" * 70)
    print("DFE² Multi-scale Model Generator for TRC")
    print("=" * 70)
    
    # Parse macro model
    print("\n[1] Parsing macro model...")
    macro_nodes, macro_elements, macro_materials = parse_inp_file_simple(macro_file)
    print(f"    Macro: {len(macro_nodes)} nodes, {len(macro_elements)} elements")
    
    # Parse RVE model (multi-part)
    print("\n[2] Parsing RVE model...")
    rve_parts, rve_materials = parse_inp_file_multipart(rve_file)
    
    for part_name, part in rve_parts.items():
        print(f"    Part '{part_name}': {len(part.nodes)} nodes, {len(part.elements)} elements")
    
    # The Matrice part defines the RVE geometry
    if 'Matrice' not in rve_parts:
        print("ERROR: Part 'Matrice' not found in RVE file")
        return
    
    matrice_part = rve_parts['Matrice']
    rve_dims = get_rve_dimensions_from_part(matrice_part)
    V_RVE = rve_dims[0] * rve_dims[1] * rve_dims[2]
    
    print(f"\n    RVE dimensions: {rve_dims[0]:.4f} x {rve_dims[1]:.4f} x {rve_dims[2]:.4f} mm")
    print(f"    RVE volume: {V_RVE:.6f} mm³")
    
    # Identify corner nodes on the Matrice (they define the PBC)
    corner_nodes = identify_corner_nodes_in_part(matrice_part, rve_dims)
    print(f"    RVE corners identified: {len(corner_nodes)}/8")
    
    # Identify face nodes for PBC
    face_nodes = identify_face_nodes_in_part(matrice_part, rve_dims)
    print(f"    Face nodes: XN={len(face_nodes['XN'])}, XP={len(face_nodes['XP'])}, " + 
          f"YN={len(face_nodes['YN'])}, YP={len(face_nodes['YP'])}, " +
          f"ZN={len(face_nodes['ZN'])}, ZP={len(face_nodes['ZP'])}")
    
    # Gauss integration
    gauss = GAUSS_C3D8R
    n_gauss = len(gauss['points'])
    n_macro_elem = len(macro_elements)
    n_rve_instances = n_macro_elem * n_gauss
    
    print(f"\n[3] Configuration:")
    print(f"    Integration points per element: {n_gauss}")
    print(f"    Total RVE instances: {n_rve_instances}")
    
    # Start writing output file
    print(f"\n[4] Generating output file: {output_file}")
    
    with open(output_file, 'w') as f:
        # Header
        f.write("*Heading\n")
        f.write("** DFE² Multi-scale Model for TRC Composite\n")
        f.write(f"** Macro: {os.path.basename(macro_file)}\n")
        f.write(f"** RVE: {os.path.basename(rve_file)}\n")
        f.write(f"** Macro elements: {n_macro_elem}\n")
        f.write(f"** RVE instances: {n_rve_instances}\n")
        f.write(f"** RVE dimensions: {rve_dims[0]} x {rve_dims[1]} x {rve_dims[2]} mm\n")
        f.write("**\n")
        f.write("*Preprint, echo=NO, model=NO, history=NO, contact=NO\n")
        f.write("**\n")
        
        # =====================================================================
        # PART DEFINITIONS
        # =====================================================================
        
        # Macro control nodes (no elements - they use RVE stiffness)
        f.write("** =============================================================\n")
        f.write("** MACRO PART (Control nodes only)\n")
        f.write("** =============================================================\n")
        f.write("*Part, name=MACRO\n")
        f.write("*Node\n")
        for nid in sorted(macro_nodes.keys()):
            n = macro_nodes[nid]
            f.write(f"{nid}, {n.x:.10f}, {n.y:.10f}, {n.z:.10f}\n")
        f.write("*End Part\n")
        f.write("**\n")
        
        # RVE parts (Matrice and Fibre)
        for part_name, part in rve_parts.items():
            f.write(f"** =============================================================\n")
            f.write(f"** RVE PART: {part_name}\n")
            f.write(f"** =============================================================\n")
            f.write(f"*Part, name={part_name}\n")
            f.write("*Node\n")
            for nid in sorted(part.nodes.keys()):
                n = part.nodes[nid]
                f.write(f"{nid}, {n.x:.10f}, {n.y:.10f}, {n.z:.10f}\n")
            
            # Elements
            f.write("**\n")
            current_type = None
            for eid in sorted(part.elements.keys()):
                elem = part.elements[eid]
                if elem.elem_type != current_type:
                    f.write(f"*Element, type={elem.elem_type}\n")
                    current_type = elem.elem_type
                node_str = ', '.join(str(n) for n in elem.nodes)
                f.write(f"{eid}, {node_str}\n")
            
            # Node sets for corners (only for Matrice)
            if part_name == 'Matrice':
                f.write("**\n")
                f.write("** Corner node sets\n")
                for vname, vnid in corner_nodes.items():
                    f.write(f"*Nset, nset={vname}\n")
                    f.write(f" {vnid}\n")
            
            # All nodes and elements sets
            f.write(f"*Nset, nset=ALL_NODES, generate\n")
            f.write(f" 1, {max(part.nodes.keys())}, 1\n")
            f.write(f"*Elset, elset=ALL_ELEMENTS, generate\n")
            f.write(f" 1, {max(part.elements.keys())}, 1\n")
            
            f.write("*End Part\n")
            f.write("**\n")
        
        # =====================================================================
        # ASSEMBLY
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** ASSEMBLY\n")
        f.write("** =============================================================\n")
        f.write("*Assembly, name=Assembly\n")
        f.write("**\n")
        
        # Macro instance
        f.write("** Macro control nodes\n")
        f.write("*Instance, name=MACRO-1, part=MACRO\n")
        f.write("*End Instance\n")
        f.write("**\n")
        
        # RVE instances at each integration point
        f.write("** RVE instances at integration points\n")
        f.write("** Each RVE = Matrice + Fibre instances\n")
        f.write("**\n")
        
        rve_instance_data = []
        
        for eid in sorted(macro_elements.keys()):
            elem = macro_elements[eid]
            
            # Get element node coordinates
            node_coords = np.array([[macro_nodes[nid].x, 
                                     macro_nodes[nid].y, 
                                     macro_nodes[nid].z] for nid in elem.nodes])
            
            # For each integration point
            for gp_idx, (xi, eta, zeta) in enumerate(gauss['points']):
                # Compute physical position of integration point
                N = shape_functions_C3D8(xi, eta, zeta)
                gp_pos = N @ node_coords
                
                # RVE is placed with its corner at the integration point position
                # (actually offset so it's centered at the GP)
                translation = gp_pos - np.array([rve_dims[0]/2, rve_dims[1]/2, rve_dims[2]/2])
                
                # Create instances for each RVE part
                for part_name in rve_parts.keys():
                    instance_name = f"RVE-E{eid}-GP{gp_idx+1}-{part_name}"
                    
                    f.write(f"*Instance, name={instance_name}, part={part_name}\n")
                    f.write(f" {translation[0]:.10f}, {translation[1]:.10f}, {translation[2]:.10f}\n")
                    f.write("*End Instance\n")
                
                # Store data for MPC
                matrice_instance_name = f"RVE-E{eid}-GP{gp_idx+1}-Matrice"
                rve_instance_data.append({
                    'matrice_instance': matrice_instance_name,
                    'macro_elem_id': eid,
                    'macro_nodes': elem.nodes,
                    'shape_functions': N,
                })
        
        f.write("**\n")
        
        # =====================================================================
        # MULTI-POINT CONSTRAINTS (MPC)
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** MULTI-POINT CONSTRAINTS - Macro-Micro coupling\n")
        f.write("** Links RVE corner nodes (Matrice) to macro element nodes\n")
        f.write("** u_RVE_corner = sum(N_i * u_macro_i)\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        for rve_data in rve_instance_data:
            instance_name = rve_data['matrice_instance']
            macro_node_ids = rve_data['macro_nodes']
            N = rve_data['shape_functions']
            
            f.write(f"** MPC for {instance_name}\n")
            
            # For each corner of the RVE
            for corner_name, corner_nid in corner_nodes.items():
                # Create equation for each DOF (1=X, 2=Y, 3=Z)
                for dof in [1, 2, 3]:
                    f.write("*Equation\n")
                    f.write("9\n")  # 1 RVE corner + 8 macro nodes
                    f.write(f"{instance_name}.{corner_nid}, {dof}, 1.0\n")
                    for i, macro_nid in enumerate(macro_node_ids):
                        coef = -N[i]
                        f.write(f"MACRO-1.{macro_nid}, {dof}, {coef:.10f}\n")
        
        f.write("**\n")
        
        # =====================================================================
        # PERIODIC BOUNDARY CONDITIONS ON RVEs
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** PERIODIC BOUNDARY CONDITIONS on RVE faces (Matrice only)\n")
        f.write("** u(+) - u(-) = u(V+) - u(V-)\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        # Create face node pairs
        x_pairs = pair_face_nodes(matrice_part, face_nodes['XN'], face_nodes['XP'], 0, rve_dims)
        y_pairs = pair_face_nodes(matrice_part, face_nodes['YN'], face_nodes['YP'], 1, rve_dims)
        z_pairs = pair_face_nodes(matrice_part, face_nodes['ZN'], face_nodes['ZP'], 2, rve_dims)
        
        print(f"    PBC pairs: X={len(x_pairs)}, Y={len(y_pairs)}, Z={len(z_pairs)}")
        
        corner_nids = set(corner_nodes.values())
        
        for rve_data in rve_instance_data:
            instance_name = rve_data['matrice_instance']
            
            # X-direction PBC
            for (n_minus, n_plus) in x_pairs:
                if n_minus in corner_nids or n_plus in corner_nids:
                    continue
                for dof in [1, 2, 3]:
                    f.write("*Equation\n")
                    f.write("4\n")
                    f.write(f"{instance_name}.{n_plus}, {dof}, 1.0\n")
                    f.write(f"{instance_name}.{n_minus}, {dof}, -1.0\n")
                    f.write(f"{instance_name}.{corner_nodes['V2']}, {dof}, -1.0\n")
                    f.write(f"{instance_name}.{corner_nodes['V1']}, {dof}, 1.0\n")
            
            # Y-direction PBC
            for (n_minus, n_plus) in y_pairs:
                if n_minus in corner_nids or n_plus in corner_nids:
                    continue
                for dof in [1, 2, 3]:
                    f.write("*Equation\n")
                    f.write("4\n")
                    f.write(f"{instance_name}.{n_plus}, {dof}, 1.0\n")
                    f.write(f"{instance_name}.{n_minus}, {dof}, -1.0\n")
                    f.write(f"{instance_name}.{corner_nodes['V4']}, {dof}, -1.0\n")
                    f.write(f"{instance_name}.{corner_nodes['V1']}, {dof}, 1.0\n")
            
            # Z-direction PBC
            for (n_minus, n_plus) in z_pairs:
                if n_minus in corner_nids or n_plus in corner_nids:
                    continue
                for dof in [1, 2, 3]:
                    f.write("*Equation\n")
                    f.write("4\n")
                    f.write(f"{instance_name}.{n_plus}, {dof}, 1.0\n")
                    f.write(f"{instance_name}.{n_minus}, {dof}, -1.0\n")
                    f.write(f"{instance_name}.{corner_nodes['V5']}, {dof}, -1.0\n")
                    f.write(f"{instance_name}.{corner_nodes['V1']}, {dof}, 1.0\n")
        
        f.write("**\n")
        f.write("*End Assembly\n")
        f.write("**\n")
        
        # =====================================================================
        # MATERIALS
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** MATERIALS\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        for mat in rve_materials:
            f.write(f"*Material, name={mat.name}\n")
            f.write("*Elastic\n")
            f.write(f" {mat.E}, {mat.nu}\n")
        
        f.write("**\n")
        
        # =====================================================================
        # SECTION ASSIGNMENTS
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** SECTION ASSIGNMENTS\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        # Assign sections to all RVE instances
        for eid in sorted(macro_elements.keys()):
            for gp_idx in range(n_gauss):
                matrice_inst = f"RVE-E{eid}-GP{gp_idx+1}-Matrice"
                fibre_inst = f"RVE-E{eid}-GP{gp_idx+1}-Fibre"
                
                f.write(f"*Solid Section, elset={matrice_inst}.ALL_ELEMENTS, material=Matrice\n")
                f.write(" 1.,\n")
                f.write(f"*Solid Section, elset={fibre_inst}.ALL_ELEMENTS, material=Fibre\n")
                f.write(" 1.,\n")
        
        f.write("**\n")
        
        # =====================================================================
        # BOUNDARY CONDITIONS
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** BOUNDARY CONDITIONS\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        
        # Determine beam orientation (longest dimension)
        x_range = max(n.x for n in macro_nodes.values()) - min(n.x for n in macro_nodes.values())
        y_range = max(n.y for n in macro_nodes.values()) - min(n.y for n in macro_nodes.values())
        z_range = max(n.z for n in macro_nodes.values()) - min(n.z for n in macro_nodes.values())
        
        y_min = min(n.y for n in macro_nodes.values())
        y_max = max(n.y for n in macro_nodes.values())
        
        # Fixed face (Y=0) - encastrement at one end of the beam
        f.write(f"** Fixed face (Y={y_min} mm) - Encastrement\n")
        f.write(f"** Beam dimensions: {x_range:.1f} x {y_range:.1f} x {z_range:.1f} mm\n")
        f.write("*Boundary\n")
        for nid, node in macro_nodes.items():
            if abs(node.y - y_min) < 1e-6:
                f.write(f"MACRO-1.{nid}, ENCASTRE\n")
        
        f.write("**\n")
        
        # =====================================================================
        # STEP
        # =====================================================================
        f.write("** =============================================================\n")
        f.write("** STEP\n")
        f.write("** =============================================================\n")
        f.write("**\n")
        f.write("*Step, name=Step-1, nlgeom=NO\n")
        f.write("*Static\n")
        f.write("1., 1., 1e-05, 1.\n")
        f.write("**\n")
        
        # Applied displacement at Y=L (traction along beam length)
        # Displacement = 0.5 mm in Y direction (DOF 2)
        f.write(f"** Applied displacement at Y={y_max} mm (traction along Y)\n")
        f.write("*Boundary\n")
        for nid, node in macro_nodes.items():
            if abs(node.y - y_max) < 1e-6:
                f.write(f"MACRO-1.{nid}, 2, 2, 0.5\n")
        
        f.write("**\n")
        f.write("** OUTPUT REQUESTS\n")
        f.write("**\n")
        f.write("*Restart, write, frequency=0\n")
        f.write("**\n")
        f.write("*Output, field\n")
        f.write("*Node Output\n")
        f.write("U, RF\n")
        f.write("*Element Output\n")
        f.write("S, E\n")
        f.write("**\n")
        f.write("*End Step\n")
    
    # Summary
    total_rve_nodes = sum(len(p.nodes) for p in rve_parts.values())
    total_rve_elements = sum(len(p.elements) for p in rve_parts.values())
    
    print(f"\n[5] Output file generated successfully!")
    print(f"    File: {output_file}")
    print(f"\n    Model statistics:")
    print(f"    - Macro nodes: {len(macro_nodes)}")
    print(f"    - RVE instances: {n_rve_instances}")
    print(f"    - Total nodes (approx): {len(macro_nodes) + n_rve_instances * total_rve_nodes:,}")
    print(f"    - Total elements (approx): {n_rve_instances * total_rve_elements:,}")
    
    return output_file


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    macro_file = os.path.join(base_dir, "TRC_Macro_3D.inp")
    rve_file = os.path.join(base_dir, "TRC_RVE.inp")
    output_file = os.path.join(base_dir, "TRC_DFE2_Combined.inp")
    
    if not os.path.exists(macro_file):
        print(f"ERROR: Macro file not found: {macro_file}")
        sys.exit(1)
    
    if not os.path.exists(rve_file):
        print(f"ERROR: RVE file not found: {rve_file}")
        sys.exit(1)
    
    generate_dfe2_inp(macro_file, rve_file, output_file)
