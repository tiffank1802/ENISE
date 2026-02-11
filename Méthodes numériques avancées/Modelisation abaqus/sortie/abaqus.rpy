# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2025.HF3 replay file
# Internal Version: 2025_05_19-14.22.38 RELr427 199275
# Run by ktongue on Tue Feb 10 17:57:12 2026
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=338.432800292969, 
    height=215.422225952148)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.ModelFromInputFile(name='DFE2_final', 
    inputFileName='C:/Users/ktongue/Documents/DFE2_final.inp/DFE2_final.inp')
#: The model "DFE2_final" has been created.
#: The part "BEAM" has been imported from the input file.
#: The part "MATRICE" has been imported from the input file.
#: The part "FIBRE" has been imported from the input file.
#: WARNING: 16590 unique equation definitions will have to be created in order to import the model. This may take a significant amount of time  ... 
#:     completed equation number 150 
#:     completed equation number 300 
#:     completed equation number 450 
#:     completed equation number 600 
#:     completed equation number 750 
#:     completed equation number 900 
#:     completed equation number 1050 
#:     completed equation number 1200 
#:     completed equation number 1350 
#:     completed equation number 1500 
#:     completed equation number 1650 
#:     completed equation number 1800 
#:     completed equation number 1950 
#:     completed equation number 2100 
#:     completed equation number 2250 
#:     completed equation number 2400 
#:     completed equation number 2550 
#:     completed equation number 2700 
#:     completed equation number 2850 
#:     completed equation number 3000 
#:     completed equation number 3150 
#:     completed equation number 3300 
#:     completed equation number 3450 
#:     completed equation number 3600 
#:     completed equation number 3750 
#:     completed equation number 3900 
#:     completed equation number 4050 
#:     completed equation number 4200 
#:     completed equation number 4350 
#:     completed equation number 4500 
#:     completed equation number 4650 
#:     completed equation number 4800 
#:     completed equation number 4950 
#:     completed equation number 5100 
#:     completed equation number 5250 
#:     completed equation number 5400 
#:     completed equation number 5550 
#:     completed equation number 5700 
#:     completed equation number 5850 
#:     completed equation number 6000 
#:     completed equation number 6150 
#:     completed equation number 6300 
#:     completed equation number 6450 
#:     completed equation number 6600 
#:     completed equation number 6750 
#:     completed equation number 6900 
#:     completed equation number 7050 
#:     completed equation number 7200 
#:     completed equation number 7350 
#:     completed equation number 7500 
#:     completed equation number 7650 
#:     completed equation number 7800 
#:     completed equation number 7950 
#:     completed equation number 8100 
#:     completed equation number 8250 
#:     completed equation number 8400 
#:     completed equation number 8550 
#:     completed equation number 8700 
#:     completed equation number 8850 
#:     completed equation number 9000 
#:     completed equation number 9150 
#:     completed equation number 9300 
#:     completed equation number 9450 
#:     completed equation number 9600 
#:     completed equation number 9750 
#:     completed equation number 9900 
#:     completed equation number 10050 
#:     completed equation number 10200 
#:     completed equation number 10350 
#:     completed equation number 10500 
#:     completed equation number 10650 
#:     completed equation number 10800 
#:     completed equation number 10950 
#:     completed equation number 11100 
#:     completed equation number 11250 
#:     completed equation number 11400 
#:     completed equation number 11550 
#:     completed equation number 11700 
#:     completed equation number 11850 
#:     completed equation number 12000 
#:     completed equation number 12150 
#:     completed equation number 12300 
#:     completed equation number 12450 
#:     completed equation number 12600 
#:     completed equation number 12750 
#:     completed equation number 12900 
#:     completed equation number 13050 
#:     completed equation number 13200 
#:     completed equation number 13350 
#:     completed equation number 13500 
#:     completed equation number 13650 
#:     completed equation number 13800 
#:     completed equation number 13950 
#:     completed equation number 14100 
#:     completed equation number 14250 
#:     completed equation number 14400 
#:     completed equation number 14550 
#:     completed equation number 14700 
#:     completed equation number 14850 
#:     completed equation number 15000 
#:     completed equation number 15150 
#:     completed equation number 15300 
#:     completed equation number 15450 
#:     completed equation number 15600 
#:     completed equation number 15750 
#:     completed equation number 15900 
#:     completed equation number 16050 
#:     completed equation number 16200 
#:     completed equation number 16350 
#:     completed equation number 16500 
#: The model "DFE2_final" has been imported from an input file. 
#: Please scroll up to check for error and warning messages.
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['DFE2_final'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].view.setValues(nearPlane=174.003, 
    farPlane=248.765, width=147.097, height=73.0407, cameraPosition=(23.6245, 
    -38.5827, 194.39), cameraUpVector=(-0.923349, 0.374671, -0.0839521), 
    cameraTarget=(0.862267, 53.2635, 1.4693))
session.viewports['Viewport: 1'].view.setValues(nearPlane=173.29, 
    farPlane=249.831, width=146.495, height=72.7415, cameraPosition=(-13.1199, 
    -45.3459, 191.81), cameraUpVector=(-0.823885, 0.544564, -0.157046), 
    cameraTarget=(1.46939, 53.3752, 1.51192))
session.viewports['Viewport: 1'].view.setValues(nearPlane=172.699, 
    farPlane=250.421, width=145.996, height=72.4937, viewOffsetX=-0.0708485, 
    viewOffsetY=0.244047)
session.viewports['Viewport: 1'].view.setValues(nearPlane=162.428, 
    farPlane=260.115, width=137.312, height=68.182, cameraPosition=(-70.4213, 
    -91.2484, 142.918), cameraUpVector=(-0.749078, 0.603347, -0.273596), 
    cameraTarget=(2.35398, 54.0845, 2.36846), viewOffsetX=-0.0666346, 
    viewOffsetY=0.229532)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['DFE2_final'].parts['BEAM']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.models['DFE2_final'].HomogeneousSolidSection(name='Matrice', 
    material='MATRICE', thickness=None)
p = mdb.models['DFE2_final'].parts['MATRICE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.9564, 
    farPlane=27.6287, width=8.52666, height=4.23389, viewOffsetX=-0.137494, 
    viewOffsetY=0.659884)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.8723, 
    farPlane=27.7128, width=9.64095, height=4.78718, viewOffsetX=-0.136769, 
    viewOffsetY=0.656404)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.1952, 
    farPlane=28.3899, width=17.0101, height=8.44632, viewOffsetX=-0.130934, 
    viewOffsetY=0.628401)
p = mdb.models['DFE2_final'].parts['MATRICE']
e = p.elements
elements = e.getSequenceFromMask(mask=('[#ffffffff:36 #ff ]', ), )
region = p.Set(elements=elements, name='Set-15')
p = mdb.models['DFE2_final'].parts['MATRICE']
p.SectionAssignment(region=region, sectionName='Matrice', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
mdb.models['DFE2_final'].HomogeneousSolidSection(name='Fibre', 
    material='FIBRE', thickness=None)
p = mdb.models['DFE2_final'].parts['FIBRE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12.3893, 
    farPlane=17.331, width=1.1877, height=0.589747, viewOffsetX=-0.432208, 
    viewOffsetY=-0.324166)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12.3712, 
    farPlane=17.3491, width=1.3881, height=0.689257, viewOffsetX=-0.431577, 
    viewOffsetY=-0.323693)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12.3032, 
    farPlane=17.4171, width=2.18839, height=1.08664, viewOffsetX=-0.429206, 
    viewOffsetY=-0.321915)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12.0844, 
    farPlane=17.6359, width=4.72426, height=2.34582, viewOffsetX=-0.421572, 
    viewOffsetY=-0.31619)
session.viewports['Viewport: 1'].view.setValues(nearPlane=11.8082, 
    farPlane=17.9121, width=7.91707, height=3.9312, viewOffsetX=-0.411938, 
    viewOffsetY=-0.308964)
session.viewports['Viewport: 1'].view.setValues(nearPlane=11.6457, 
    farPlane=18.0746, width=9.90223, height=4.91693, viewOffsetX=-0.406268, 
    viewOffsetY=-0.304712)
p = mdb.models['DFE2_final'].parts['FIBRE']
e = p.elements
elements = e.getSequenceFromMask(mask=(
    '[#ffffffff:99 #ffefffff #ffffffff #1 ]', ), )
region = p.Set(elements=elements, name='Set-3')
p = mdb.models['DFE2_final'].parts['FIBRE']
p.SectionAssignment(region=region, sectionName='Fibre', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['DFE2_final'].parts['BEAM']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['DFE2_final'].parts['BEAM']
e = p.elements
elements = e.getSequenceFromMask(mask=('[#3ffff ]', ), )
region = p.Set(elements=elements, name='Set-163')
p = mdb.models['DFE2_final'].parts['BEAM']
p.SectionAssignment(region=region, sectionName='Matrice', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a = mdb.models['DFE2_final'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['DFE2_final'].StaticStep(name='Step-1', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=151.595, 
    farPlane=268.751, width=128.154, height=63.6345, cameraPosition=(-68.3189, 
    -141.85, 53.494), cameraUpVector=(-0.78022, 0.596715, -0.187583), 
    cameraTarget=(2.30427, 54.944, 3.9309), viewOffsetX=-0.0621903, 
    viewOffsetY=0.214223)
session.viewports['Viewport: 1'].view.setValues(nearPlane=150.356, 
    farPlane=267.632, width=127.106, height=63.1142, cameraPosition=(-37.501, 
    -146.378, -57.4585), cameraUpVector=(-0.831738, 0.547073, -0.0944603), 
    cameraTarget=(1.5951, 55.0195, 6.43779), viewOffsetX=-0.0616818, 
    viewOffsetY=0.212472)
session.viewports['Viewport: 1'].view.setValues(nearPlane=159.636, 
    farPlane=258.352, width=16.4636, height=8.17496, viewOffsetX=6.13801, 
    viewOffsetY=-9.27672)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
session.viewports['Viewport: 1'].view.setValues(nearPlane=152.803, 
    farPlane=265.185, width=104.966, height=52.1204, viewOffsetX=14.3887, 
    viewOffsetY=5.07029)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E1_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#fc000c00 #1 #0:2 #c0000 #1fc #0:2 #c000000', 
    ' #1fc00 #0:3 #1fc000c #0:3 #fc000c00 #1 #0:2', 
    ' #c0000 #1fc #0:2 #c000000 #1fc00 #0:3 #1fc000c', 
    ' #0:3 #fc000c00 #1 #0:2 #c0000 #1fc #0:2', ' #c000000 #1fc00 ]', ), )
region = a.Set(nodes=nodes1, name='Set-66121')
mdb.models['DFE2_final'].EncastreBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=155.628, 
    farPlane=262.361, width=69.3261, height=34.4237, viewOffsetX=9.22624, 
    viewOffsetY=-1.19652)
session.viewports['Viewport: 1'].view.setValues(nearPlane=158.542, 
    farPlane=243.255, width=70.6242, height=35.0683, cameraPosition=(-94.8201, 
    195.872, -95.8706), cameraUpVector=(-0.623469, -0.303544, 0.720519), 
    cameraTarget=(4.20771, 51.0785, 28.228), viewOffsetX=9.399, 
    viewOffsetY=-1.21893)
del mdb.models['DFE2_final'].boundaryConditions['BC-1']
session.viewports['Viewport: 1'].view.setValues(nearPlane=160.895, 
    farPlane=240.901, width=43.6893, height=21.6938, viewOffsetX=1.11599, 
    viewOffsetY=-6.67431)
session.viewports['Viewport: 1'].view.setValues(nearPlane=160.684, 
    farPlane=241.112, width=43.6321, height=21.6654, cameraPosition=(-95.8297, 
    193.416, -97.9311), cameraUpVector=(-0.682919, -0.567145, 0.4604), 
    cameraTarget=(3.19815, 48.622, 26.1675), viewOffsetX=1.11453, 
    viewOffsetY=-6.66557)
session.viewports['Viewport: 1'].view.setValues(nearPlane=156.361, 
    farPlane=245.436, width=100.965, height=50.1339, viewOffsetX=15.4362, 
    viewOffsetY=-3.1024)
session.viewports['Viewport: 1'].view.setValues(nearPlane=187.669, 
    farPlane=218.995, width=121.181, height=60.1722, cameraPosition=(-148.104, 
    78.7868, -130.928), cameraUpVector=(-0.361097, 0.157576, 0.919118), 
    cameraTarget=(11.8326, 66.0976, 12.0116), viewOffsetX=18.527, 
    viewOffsetY=-3.72359)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['DFE2_final'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
session.viewports['Viewport: 1'].view.setValues(nearPlane=189.497, 
    farPlane=217.168, width=74.5877, height=37.0363, viewOffsetX=15.7431, 
    viewOffsetY=-3.20751)
session.viewports['Viewport: 1'].view.setValues(nearPlane=163.469, 
    farPlane=243.4, width=64.3431, height=31.9494, cameraPosition=(-138.688, 
    189.052, -43.6189), cameraUpVector=(-0.107262, -0.245855, 0.963354), 
    cameraTarget=(19.3625, 55.4658, 14.2376), viewOffsetX=13.5808, 
    viewOffsetY=-2.76696)
session.viewports['Viewport: 1'].view.setValues(nearPlane=163.612, 
    farPlane=243.258, width=77.5352, height=38.4999, viewOffsetX=15.8799, 
    viewOffsetY=-3.2156)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E14_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#a00 #fe #0:2 #a0000 #fe00 #0:2 #a000000', 
    ' #fe0000 #0:3 #fe00000a #0:3 #a00 #fe #0:2', 
    ' #a0000 #fe00 #0:2 #a000000 #fe0000 #0:3 #fe00000a', 
    ' #0:3 #a00 #fe #0:2 #a0000 #fe00 #0:2', ' #a000000 #fe0000 ]', ), )
region = a.Set(nodes=nodes1, name='Set-66122')
mdb.models['DFE2_final'].EncastreBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=155.432, 
    farPlane=249.666, width=73.6585, height=36.5749, cameraPosition=(-110.221, 
    217.124, 25.0247), cameraUpVector=(0.0630384, -0.454762, 0.888379), 
    cameraTarget=(22.968, 49.1536, 10.2155), viewOffsetX=15.0859, 
    viewOffsetY=-3.05482)
del mdb.models['DFE2_final'].boundaryConditions['BC-1']
session.viewports['Viewport: 1'].view.setValues(nearPlane=174.743, 
    farPlane=233.023, width=82.8101, height=41.1191, cameraPosition=(-173.808, 
    147.816, -29.0268), cameraUpVector=(0.173705, -0.0253266, 0.984472), 
    cameraTarget=(19.5249, 61.3949, 7.39344), viewOffsetX=16.9602, 
    viewOffsetY=-3.43436)
session.viewports['Viewport: 1'].view.setValues(nearPlane=174.373, 
    farPlane=233.187, width=82.6348, height=41.0321, cameraPosition=(-176.61, 
    147.816, 0.19805), cameraUpVector=(0.332664, -0.0253266, 0.942705), 
    cameraTarget=(20.077, 61.3949, 4.44838), viewOffsetX=16.9243, 
    viewOffsetY=-3.42709)
session.viewports['Viewport: 1'].view.setValues(width=87.1351, height=43.2667, 
    cameraPosition=(1.85845, 251.212, 2.57268), cameraUpVector=(0, 0, 1), 
    cameraTarget=(1.85845, 47.4323, 2.57268), viewOffsetX=0, viewOffsetY=0)
session.viewports['Viewport: 1'].view.setValues(nearPlane=146.138, 
    farPlane=257.286, width=73.0327, height=36.2642, cameraPosition=(-1.99205, 
    251.212, 2.57268), cameraTarget=(-1.99205, 47.4323, 2.57268))
session.viewports['Viewport: 1'].view.setValues(nearPlane=146.089, 
    farPlane=257.335, width=73.0081, height=36.252, cameraPosition=(-5.96222, 
    251.212, 2.57268), cameraTarget=(-5.96222, 47.4323, 2.57268))
session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-5.96222, 
    251.212, 2.57268), cameraUpVector=(-0.557622, 0, -0.830095), cameraTarget=(
    -5.96222, 47.4323, 2.57268))
session.viewports['Viewport: 1'].view.setValues(cameraPosition=(197.817, 
    47.4323, 2.57268), cameraUpVector=(0, 1, 0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=172.714, 
    farPlane=217.42, width=247.12, height=122.706, viewOffsetX=-30.3195, 
    viewOffsetY=-3.67271)
session.viewports['Viewport: 1'].view.setValues(nearPlane=171.725, 
    farPlane=218.409, width=245.705, height=122.004, cameraPosition=(197.817, 
    47.4323, -48.6067), cameraTarget=(-5.96222, 47.4323, -48.6067), 
    viewOffsetX=-30.146, viewOffsetY=-3.65169)
session.viewports['Viewport: 1'].view.setValues(nearPlane=157.083, 
    farPlane=253.252, width=224.755, height=111.601, cameraPosition=(65.6701, 
    139.356, -175.77), cameraUpVector=(-0.286074, 0.877439, 0.385049), 
    cameraTarget=(-31.0748, 41.7779, -25.2879), viewOffsetX=-27.5756, 
    viewOffsetY=-3.34033)
session.viewports['Viewport: 1'].view.setValues(nearPlane=157.744, 
    farPlane=250.823, width=225.701, height=112.071, cameraPosition=(63.8089, 
    139.356, -175.77), cameraTarget=(-32.936, 41.7779, -25.2879), 
    viewOffsetX=-27.6916, viewOffsetY=-3.35438)
session.viewports['Viewport: 1'].view.setValues(width=225.144, height=111.794, 
    cameraPosition=(-2.0842, 243.029, -6.73689), cameraUpVector=(0, 0, 1), 
    cameraTarget=(-2.0842, 38.745, -6.73689), viewOffsetX=0, viewOffsetY=0)
session.viewports['Viewport: 1'].view.setValues(nearPlane=129.06, 
    farPlane=257.998, width=184.052, height=91.3903, cameraUpVector=(0.296966, 
    0, 0.954888))
session.viewports['Viewport: 1'].view.setValues(nearPlane=128.648, 
    farPlane=258.41, width=183.465, height=91.0988, cameraPosition=(-2.0842, 
    243.029, -5.45697), cameraTarget=(-2.0842, 38.745, -5.45697))
session.viewports['Viewport: 1'].view.setValues(nearPlane=128.642, 
    farPlane=258.416, width=183.457, height=91.0949, cameraPosition=(1.34306, 
    243.029, -5.45697), cameraTarget=(1.34306, 38.745, -5.45697))
session.viewports['Viewport: 1'].view.setValues(cameraPosition=(5.32582, 
    243.029, -5.45697), cameraTarget=(5.32582, 38.745, -5.45697))
session.viewports['Viewport: 1'].view.setValues(cameraPosition=(5.32582, 
    243.029, -5.45697), cameraUpVector=(-0.405908, 0, -0.913914), 
    cameraTarget=(5.32582, 38.745, -5.45697))
session.viewports['Viewport: 1'].view.setValues(nearPlane=150.047, 
    farPlane=249.177, width=213.983, height=106.253, cameraPosition=(-34.1007, 
    171.116, -150.745), cameraUpVector=(-0.873009, 0.23046, 0.429818), 
    cameraTarget=(7.51688, 42.7414, 2.61714))
session.viewports['Viewport: 1'].view.setValues(nearPlane=179.766, 
    farPlane=227.501, width=256.366, height=127.298, cameraPosition=(-12.7467, 
    36.2889, -199.344), cameraUpVector=(-0.991636, 0.0902851, 0.0922266), 
    cameraTarget=(7.01707, 45.8972, 3.75465))
session.viewports['Viewport: 1'].view.setValues(nearPlane=142.474, 
    farPlane=258.145, width=203.184, height=100.891, cameraPosition=(-41.8335, 
    184.873, -137.475), cameraUpVector=(-0.618406, 0.440874, 0.650542), 
    cameraTarget=(7.11001, 45.4224, 3.55696))
session.viewports['Viewport: 1'].view.setValues(nearPlane=176.327, 
    farPlane=228.846, width=251.464, height=124.864, cameraPosition=(0.744196, 
    69.7307, -198.255), cameraUpVector=(-0.999389, 0.0191446, 0.0292554), 
    cameraTarget=(6.26521, 47.707, 4.76294))
session.viewports['Viewport: 1'].view.setValues(nearPlane=149.835, 
    farPlane=252.512, width=213.683, height=106.104, cameraPosition=(-36.886, 
    160.011, -160.056), cameraUpVector=(-0.906369, 0.196053, 0.374245), 
    cameraTarget=(6.58051, 46.9505, 4.44287))
session.viewports['Viewport: 1'].view.setValues(nearPlane=152.304, 
    farPlane=250.662, width=217.205, height=107.852, cameraPosition=(-69.8765, 
    -62.7209, -147.452), cameraUpVector=(-0.926264, 0.217383, 0.307863), 
    cameraTarget=(7.09054, 50.3939, 4.24803))
session.viewports['Viewport: 1'].view.setValues(nearPlane=162.834, 
    farPlane=240.132, width=97.6546, height=48.4901, viewOffsetX=14.3934, 
    viewOffsetY=-2.83123)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E1_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66123')
mdb.models['DFE2_final'].EncastreBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E2_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66124')
mdb.models['DFE2_final'].EncastreBC(name='BC-2', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E18_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66125')
mdb.models['DFE2_final'].EncastreBC(name='BC-3', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E17_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66126')
mdb.models['DFE2_final'].EncastreBC(name='BC-4', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E16_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66127')
mdb.models['DFE2_final'].EncastreBC(name='BC-5', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E15_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66128')
mdb.models['DFE2_final'].EncastreBC(name='BC-6', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E3_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66129')
mdb.models['DFE2_final'].EncastreBC(name='BC-7', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E4_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66130')
mdb.models['DFE2_final'].EncastreBC(name='BC-8', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E14_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66131')
mdb.models['DFE2_final'].EncastreBC(name='BC-9', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E5_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66132')
mdb.models['DFE2_final'].EncastreBC(name='BC-10', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E6_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66133')
mdb.models['DFE2_final'].EncastreBC(name='BC-11', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E13_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66134')
mdb.models['DFE2_final'].EncastreBC(name='BC-12', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E12_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66135')
mdb.models['DFE2_final'].EncastreBC(name='BC-13', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E11_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66136')
mdb.models['DFE2_final'].EncastreBC(name='BC-14', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E10_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66137')
mdb.models['DFE2_final'].EncastreBC(name='BC-15', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E9_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66138')
mdb.models['DFE2_final'].EncastreBC(name='BC-16', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E8_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66139')
mdb.models['DFE2_final'].EncastreBC(name='BC-17', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E7_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#ffffffff:4 #ff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66140')
mdb.models['DFE2_final'].EncastreBC(name='BC-18', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=166.641, 
    farPlane=255.987, width=99.9381, height=49.624, cameraPosition=(-129.477, 
    -92.2553, 87.4789), cameraUpVector=(-0.105534, 0.576061, 0.810566), 
    cameraTarget=(-3.05815, 45.8591, 5.7823), viewOffsetX=14.7299, 
    viewOffsetY=-2.89743)
session.viewports['Viewport: 1'].view.setValues(nearPlane=173.444, 
    farPlane=275.064, width=104.018, height=51.6499, cameraPosition=(38.5197, 
    -133.833, 127.693), cameraUpVector=(-0.165466, 0.530446, 0.831413), 
    cameraTarget=(-1.08675, 31.4498, 14.3595), viewOffsetX=15.3313, 
    viewOffsetY=-3.01572)
session.viewports['Viewport: 1'].view.setValues(nearPlane=163.31, 
    farPlane=278.184, width=97.9404, height=48.632, cameraPosition=(-38.4969, 
    -163.539, 45.5456), cameraUpVector=(-0.510218, 0.279484, 0.813368), 
    cameraTarget=(-6.98745, 32.5986, -2.0841), viewOffsetX=14.4355, 
    viewOffsetY=-2.83951)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E1_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66141')
mdb.models['DFE2_final'].DisplacementBC(name='BC-19', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E2_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66142')
mdb.models['DFE2_final'].DisplacementBC(name='BC-20', createStepName='Initial', 
    region=region, u1=UNSET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=172.006, 
    farPlane=274.098, width=103.156, height=51.2216, cameraPosition=(25.6503, 
    -139.803, 119.747), cameraUpVector=(-0.525921, 0.416311, 0.741682), 
    cameraTarget=(-2.14131, 27.6304, 6.05861), viewOffsetX=15.2042, 
    viewOffsetY=-2.99071)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E3_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66143')
mdb.models['DFE2_final'].DisplacementBC(name='BC-21', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
mdb.models['DFE2_final'].boundaryConditions['BC-19'].setValues(u3=UNSET)
mdb.models['DFE2_final'].boundaryConditions['BC-20'].setValues(u1=SET, 
    u3=UNSET)
session.viewports['Viewport: 1'].view.setValues(nearPlane=164.287, 
    farPlane=272.503, width=98.5268, height=48.9232, cameraPosition=(-102.133, 
    -141.821, -14.6777), cameraUpVector=(-0.595412, 0.283188, 0.751857), 
    cameraTarget=(-9.98552, 40.4464, -10.3554), viewOffsetX=14.5219, 
    viewOffsetY=-2.8565)
session.viewports['Viewport: 1'].view.setValues(nearPlane=169.749, 
    farPlane=267.041, width=35.5576, height=17.656, viewOffsetX=25.7948, 
    viewOffsetY=-3.90875)
session.viewports['Viewport: 1'].view.setValues(nearPlane=173.703, 
    farPlane=275.618, width=36.3858, height=18.0673, cameraPosition=(-53.4669, 
    -163.826, 49.1558), cameraUpVector=(-0.608046, 0.343309, 0.715834), 
    cameraTarget=(-10.0051, 28.0254, -5.93744), viewOffsetX=26.3957, 
    viewOffsetY=-3.99979)
session.viewports['Viewport: 1'].view.setValues(nearPlane=172.017, 
    farPlane=277.303, width=59.1119, height=29.3518, viewOffsetX=32.4894, 
    viewOffsetY=-4.65723)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
session.viewports['Viewport: 1'].view.setValues(nearPlane=183.686, 
    farPlane=286.613, width=63.1216, height=31.3428, cameraPosition=(19.3542, 
    -168.031, 92.5364), cameraUpVector=(-0.437485, 0.313846, 0.842679), 
    cameraTarget=(-7.27411, 16.8617, 9.85099), viewOffsetX=34.6932, 
    viewOffsetY=-4.97314)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E4_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66144')
mdb.models['DFE2_final'].DisplacementBC(name='BC-22', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=183.034, 
    farPlane=287.265, width=62.8975, height=31.2316, viewOffsetX=34.7041, 
    viewOffsetY=-4.28723)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E5_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66145')
mdb.models['DFE2_final'].DisplacementBC(name='BC-23', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E6_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66146')
mdb.models['DFE2_final'].DisplacementBC(name='BC-24', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E7_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66147')
mdb.models['DFE2_final'].DisplacementBC(name='BC-25', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=171.563, 
    farPlane=279.995, width=58.9556, height=29.2742, cameraPosition=(-45.2593, 
    -169.353, 36.989), cameraUpVector=(-0.538727, 0.258694, 0.801779), 
    cameraTarget=(-13.8625, 27.9624, -5.57893), viewOffsetX=32.5291, 
    viewOffsetY=-4.01854)
a = mdb.models['DFE2_final'].rootAssembly
a.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=6.69)
session.viewports['Viewport: 1'].view.setValues(nearPlane=170.114, 
    farPlane=286.439, width=58.4577, height=29.027, cameraPosition=(-27.6044, 
    -171.624, 54.6749), cameraUpVector=(-0.50077, 0.271874, 0.821775), 
    cameraTarget=(-13.3329, 24.2799, -1.44099), viewOffsetX=32.2544, 
    viewOffsetY=-3.9846)
session.viewports['Viewport: 1'].view.setValues(nearPlane=171.723, 
    farPlane=284.829, width=35.9711, height=17.8614, viewOffsetX=26.3885, 
    viewOffsetY=-6.18059)
session.viewports['Viewport: 1'].view.setValues(nearPlane=170.845, 
    farPlane=285.707, width=45.837, height=22.7602, viewOffsetX=27.2231, 
    viewOffsetY=-1.97903)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    seeds=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    seeds=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=SHADED)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=SHADED)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=HIDDEN)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=HIDDEN)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    renderStyle=WIREFRAME)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    renderStyle=WIREFRAME)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=SHADED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=170.845, 
    farPlane=285.707, width=45.837, height=22.7602, viewOffsetX=25.3833, 
    viewOffsetY=0.848792)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
session.viewports['Viewport: 1'].view.setValues(nearPlane=187.775, 
    farPlane=282.184, width=50.3792, height=25.0157, cameraPosition=(38.2184, 
    -133.39, 147.906), cameraUpVector=(-0.332855, 0.545766, 0.768991), 
    cameraTarget=(-8.17683, 18.8173, 19.7992), viewOffsetX=27.8986, 
    viewOffsetY=0.932903)
session.viewports['Viewport: 1'].view.setValues(nearPlane=184.368, 
    farPlane=285.591, width=91.8379, height=45.6018, viewOffsetX=33.6913, 
    viewOffsetY=2.22042)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MACRO-1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0 #ffffffc0 #fff ]', ), )
region = a.Set(nodes=nodes1, name='Set-66148')
mdb.models['DFE2_final'].DisplacementBC(name='BC-26', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=182.423, 
    farPlane=287.537, width=116.387, height=57.7915, viewOffsetX=38.2437, 
    viewOffsetY=2.17609)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
    bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON, seeds=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF, seeds=OFF)
mdb.Job(name='Job-1', model='DFE2_final', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numCpus=1, numGPUs=0)
p = mdb.models['DFE2_final'].parts['BEAM']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['DFE2_final'].parts['FIBRE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=11.597, 
    farPlane=18.1233, width=11.2499, height=5.58613, viewOffsetX=0.0492229, 
    viewOffsetY=0.095452)
p = mdb.models['DFE2_final'].parts['FIBRE']
e = p.elements
elements = e.getSequenceFromMask(mask=('[#ffffffff:101 #1 ]', ), )
region = p.Set(elements=elements, name='Set-4')
p = mdb.models['DFE2_final'].parts['FIBRE']
p.SectionAssignment(region=region, sectionName='Fibre', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a1 = mdb.models['DFE2_final'].rootAssembly
a1.regenerate()
a = mdb.models['DFE2_final'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
p = mdb.models['DFE2_final'].parts['FIBRE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=11.4299, 
    farPlane=18.2904, width=13.3495, height=6.62863, viewOffsetX=0.0396312, 
    viewOffsetY=0.257136)
session.viewports['Viewport: 1'].view.setValues(nearPlane=11.094, 
    farPlane=18.8797, width=12.9571, height=6.43382, cameraPosition=(4.36807, 
    12.4084, 14.6948), cameraUpVector=(-0.518925, 0.421583, -0.74363), 
    cameraTarget=(2.6624, 2.59944, 3.66306), viewOffsetX=0.0384664, 
    viewOffsetY=0.249579)
p = mdb.models['DFE2_final'].parts['MATRICE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['DFE2_final'].parts['BEAM']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=169.216, 
    farPlane=260.538, width=172.229, height=85.5196, viewOffsetX=2.79441, 
    viewOffsetY=-2.87831)
p = mdb.models['DFE2_final'].parts['FIBRE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['DFE2_final'].parts['MATRICE']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14.9979, 
    farPlane=28.5872, width=21.2791, height=10.5661, viewOffsetX=1.39224, 
    viewOffsetY=-0.522584)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14.0257, 
    farPlane=26.6717, width=19.8996, height=9.8811, cameraPosition=(0.583595, 
    14.9989, 19.4605), cameraUpVector=(-0.428309, 0.413728, -0.803356), 
    cameraTarget=(2.45428, 1.48921, 2.46331), viewOffsetX=1.30198, 
    viewOffsetY=-0.488706)
a = mdb.models['DFE2_final'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Error in job Job-1: 72 nodes are missing degree of freedoms. The MPC/Equation/kinematic coupling constraints can not be formed. The nodes have been identified in node set ErrNodeMissingDofConstrDef.
#: Job Job-1: Analysis Input File Processor aborted due to errors.
#: Error in job Job-1: Analysis Input File Processor exited with an error - Please see the  Job-1.dat file for possible error messages if the file exists.
#: Job Job-1 aborted due to errors.
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
del mdb.models['DFE2_final'].boundaryConditions['BC-26']
session.viewports['Viewport: 1'].view.setValues(nearPlane=181.893, 
    farPlane=288.066, width=116.049, height=57.6238, cameraPosition=(35.718, 
    -128.91, 154.135), cameraUpVector=(-0.179221, 0.600959, 0.778927), 
    cameraTarget=(-10.6772, 23.2976, 26.0279), viewOffsetX=38.1328, 
    viewOffsetY=2.16978)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E8_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66149')
mdb.models['DFE2_final'].DisplacementBC(name='BC-26', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E9_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66150')
mdb.models['DFE2_final'].DisplacementBC(name='BC-27', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E10_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66151')
mdb.models['DFE2_final'].DisplacementBC(name='BC-28', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E11_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66152')
mdb.models['DFE2_final'].DisplacementBC(name='BC-29', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E12_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66153')
mdb.models['DFE2_final'].DisplacementBC(name='BC-30', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E13_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66154')
mdb.models['DFE2_final'].DisplacementBC(name='BC-31', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E14_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66155')
mdb.models['DFE2_final'].DisplacementBC(name='BC-32', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E15_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66156')
mdb.models['DFE2_final'].DisplacementBC(name='BC-33', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E16_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66157')
mdb.models['DFE2_final'].DisplacementBC(name='BC-34', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E17_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66158')
mdb.models['DFE2_final'].DisplacementBC(name='BC-35', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['DFE2_final'].rootAssembly
n1 = a.instances['MATRICE_E18_GP1'].nodes
nodes1 = n1.getSequenceFromMask(mask=('[#0:42 #ffff0000 #ffffffff:3 #ffffff ]', 
    ), )
region = a.Set(nodes=nodes1, name='Set-66159')
mdb.models['DFE2_final'].DisplacementBC(name='BC-36', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=206.222, 
    farPlane=289.278, width=131.571, height=65.3311, cameraPosition=(133.631, 
    -87.2216, 165.034), cameraUpVector=(-0.172316, 0.66155, 0.729835), 
    cameraTarget=(9.83483, 17.5573, 40.8293), viewOffsetX=43.2332, 
    viewOffsetY=2.45999)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Error in job Job-1: 72 nodes are missing degree of freedoms. The MPC/Equation/kinematic coupling constraints can not be formed. The nodes have been identified in node set ErrNodeMissingDofConstrDef.
#: Job Job-1: Analysis Input File Processor aborted due to errors.
#: Error in job Job-1: Analysis Input File Processor exited with an error - Please see the  Job-1.dat file for possible error messages if the file exists.
#: Job Job-1 aborted due to errors.
session.viewports['Viewport: 1'].view.setValues(nearPlane=207.274, 
    farPlane=288.225, width=109.838, height=54.5398, viewOffsetX=37.3872, 
    viewOffsetY=-1.38937)
mdb.jobs['Job-1'].writeInput(consistencyChecking=OFF)
#: The job input file has been written to "Job-1.inp".
mdb.saveAs(pathName='C:/temp/fe2')
#: The model database has been saved to "C:\temp\fe2.cae".
