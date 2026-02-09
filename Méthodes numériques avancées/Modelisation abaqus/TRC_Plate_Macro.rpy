# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2025.HF3 replay file
# Script de Modélisation Macroscopique de Plaque TRC
# Basé sur les résultats d'homogénéisation du VER
#
# Dimensions de la plaque: 550 x 99 x 7.5 mm
# Matériau homogénéisé: E = 25 MPa, nu = 0.18
#

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=326.873443603516, 
    height=208.144454956055)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

# ============================================================================
# PARAMETRES DE MODELISATION
# ============================================================================
LONGUEUR = 550.0    # mm (direction x - traction)
LARGEUR = 99.0      # mm (direction y)
EPAISSEUR = 7.5     # mm (direction z)
E_HOMOGENISE = 25.0 # MPa
NU_HOMOGENISE = 0.18
SEED_SIZE = 10.0    # mm
DEPLACEMENT = 5.0   # mm (déplacement imposé)

# ============================================================================
# CREATION DU MODELE
# ============================================================================
mdb.Model(name='TRC_Plate_Macro', modelType=STANDARD_EXPLICIT)
myModel = mdb.models['TRC_Plate_Macro']

# ============================================================================
# CREATION DE LA GEOMETRIE - PLAQUE 3D SOLIDE
# ============================================================================
session.viewports['Viewport: 1'].setValues(displayedObject=None)

# Créer l'esquisse de la plaque
s = myModel.ConstrainedSketch(name='__profile__', sheetSize=1000.0)
s.rectangle(point1=(0.0, 0.0), point2=(LONGUEUR, LARGEUR))

# Créer la pièce 3D par extrusion
p = myModel.Part(name='TRC_Plate', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=EPAISSEUR)
del myModel.sketches['__profile__']

session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)

# ============================================================================
# DEFINITION DU MATERIAU HOMOGENEISE TRC
# ============================================================================
# Matériau isotrope basé sur l'homogénéisation du VER
# E_homogénéisé ≈ 25 MPa (directions 1 et 3)
# nu ≈ 0.18 (coefficient de Poisson de la matrice)

myModel.Material(name='TRC_Homogenise')
myModel.materials['TRC_Homogenise'].Elastic(table=((E_HOMOGENISE, NU_HOMOGENISE), ))

# ============================================================================
# CREATION DE LA SECTION SOLIDE ET ASSIGNATION
# ============================================================================
myModel.HomogeneousSolidSection(name='Section_TRC', material='TRC_Homogenise', 
    thickness=None)

# Sélectionner toutes les cellules de la pièce
p = myModel.parts['TRC_Plate']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='All_Cells')
p.SectionAssignment(region=region, sectionName='Section_TRC', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

# ============================================================================
# CREATION DE L'ASSEMBLAGE
# ============================================================================
a = myModel.rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a.DatumCsysByDefault(CARTESIAN)
p = myModel.parts['TRC_Plate']
a.Instance(name='TRC_Plate-1', part=p, dependent=ON)

# ============================================================================
# CREATION DES SETS POUR LES CONDITIONS AUX LIMITES
# ============================================================================
a = myModel.rootAssembly

# Face gauche (x=0) - pour encastrement
f = a.instances['TRC_Plate-1'].faces
faces_left = f.getByBoundingBox(xMin=-0.1, xMax=0.1, 
    yMin=-0.1, yMax=LARGEUR+0.1, 
    zMin=-0.1, zMax=EPAISSEUR+0.1)
a.Set(faces=faces_left, name='Face_Gauche')

# Face droite (x=LONGUEUR) - pour déplacement imposé
faces_right = f.getByBoundingBox(xMin=LONGUEUR-0.1, xMax=LONGUEUR+0.1, 
    yMin=-0.1, yMax=LARGEUR+0.1, 
    zMin=-0.1, zMax=EPAISSEUR+0.1)
a.Set(faces=faces_right, name='Face_Droite')

# Face inférieure (z=0) - symétrie optionnelle
faces_bottom = f.getByBoundingBox(xMin=-0.1, xMax=LONGUEUR+0.1, 
    yMin=-0.1, yMax=LARGEUR+0.1, 
    zMin=-0.1, zMax=0.1)
a.Set(faces=faces_bottom, name='Face_Inferieure')

# Face supérieure (z=EPAISSEUR)
faces_top = f.getByBoundingBox(xMin=-0.1, xMax=LONGUEUR+0.1, 
    yMin=-0.1, yMax=LARGEUR+0.1, 
    zMin=EPAISSEUR-0.1, zMax=EPAISSEUR+0.1)
a.Set(faces=faces_top, name='Face_Superieure')

# ============================================================================
# ETAPE D'ANALYSE STATIQUE
# ============================================================================
myModel.StaticStep(name='Step-1', previous='Initial', 
    description='Essai de traction sur plaque TRC homogeneisee',
    nlgeom=OFF, maxNumInc=100, initialInc=0.1, minInc=1e-08, maxInc=1.0)

session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

# ============================================================================
# CONDITIONS AUX LIMITES
# ============================================================================
# Encastrement sur la face gauche (x=0)
region = a.sets['Face_Gauche']
myModel.EncastreBC(name='BC_Encastrement', createStepName='Initial', 
    region=region, localCsys=None)

# Déplacement imposé sur la face droite (x=LONGUEUR)
# Condition initiale: bloquer u2 et u3, libérer u1
region = a.sets['Face_Droite']
myModel.DisplacementBC(name='BC_Deplacement', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

# Appliquer le déplacement de traction dans Step-1
myModel.boundaryConditions['BC_Deplacement'].setValuesInStep(
    stepName='Step-1', u1=DEPLACEMENT, u2=0.0, u3=0.0)

# ============================================================================
# CONFIGURATION DES SORTIES
# ============================================================================
myModel.fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
    'E', 'EVOL', 'IVOL', 'COORD'))

# ============================================================================
# MAILLAGE
# ============================================================================
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)

p = myModel.parts['TRC_Plate']
session.viewports['Viewport: 1'].setValues(displayedObject=p)

# Semer les arêtes
p.seedPart(size=SEED_SIZE, deviationFactor=0.1, minSizeFactor=0.1)

# Définir le type d'élément (C3D8R - hexaèdres à intégration réduite)
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=STRUCTURED)

elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)

p.setElementType(regions=(pickedRegions, ), elemTypes=(elemType1, elemType2, 
    elemType3))

# Générer le maillage
p.generateMesh()

# Régénérer l'assemblage
a = myModel.rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)

# ============================================================================
# CREATION DU JOB
# ============================================================================
mdb.Job(name='TRC_Plate_Macro_Job', model='TRC_Plate_Macro', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numCpus=1, numGPUs=0)

# ============================================================================
# AFFICHAGE FINAL
# ============================================================================
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)

# Vue isométrique
session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])

#: ============================================================================
#: MODELISATION TERMINEE
#: ============================================================================
#: Modele: TRC_Plate_Macro
#: Dimensions: 550 x 99 x 7.5 mm
#: Materiau: TRC Homogeneise (E=25 MPa, nu=0.18)
#: Chargement: Traction avec deplacement impose de 5 mm
#: 
#: Pour soumettre le job:
#:   mdb.jobs['TRC_Plate_Macro_Job'].submit(consistencyChecking=OFF)
#: ============================================================================
