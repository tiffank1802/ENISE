# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2025.HF3 replay file
# Internal Version: 2025_05_19-14.22.38 RELr427 199275
# Run by ktongue on Fri Feb  6 08:52:05 2026
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=326.873443603516, 
    height=208.144454956055)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('projet_composite.cae')
#: The model database "C:\Users\ktongue\OneDrive - ENISE\ENISE1\S9\Methodes Numériques avancées\projet_composite.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['Fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numCpus=1, numGPUs=0)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['Fibre']
p.seedPart(size=0.11, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Fibre']
p.generateMesh()
p = mdb.models['Model-1'].parts['Matrice']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Matrice']
p.seedPart(size=0.67, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Matrice']
p.generateMesh()
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       4
#: Number of Node Sets:          4
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14.9384, 
    farPlane=28.6467, width=21.2731, height=10.5672, viewOffsetX=-0.156201, 
    viewOffsetY=0.38494)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.6122, 
    farPlane=28.4375, width=22.2326, height=11.0438, cameraPosition=(-1.96751, 
    13.5547, 20.5971), cameraUpVector=(-0.391885, 0.418353, -0.819394), 
    cameraTarget=(0.157458, -0.0981789, 3.74479), viewOffsetX=-0.163247, 
    viewOffsetY=0.402302)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.0519, 
    farPlane=28.5261, width=21.4347, height=10.6474, cameraPosition=(17.4367, 
    8.50499, 13.2743), cameraUpVector=(-0.497286, 0.705934, -0.504345), 
    cameraTarget=(0.17312, -0.414311, 3.40868), viewOffsetX=-0.157388, 
    viewOffsetY=0.387863)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.1093, 
    farPlane=28.4686, width=21.5164, height=10.688, cameraPosition=(17.4219, 
    8.50026, 13.3045), cameraUpVector=(-0.467464, 0.694845, -0.546504), 
    cameraTarget=(0.158317, -0.419041, 3.43886), viewOffsetX=-0.157988, 
    viewOffsetY=0.389342)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.5117, 
    farPlane=28.2009, width=22.0895, height=10.9727, cameraPosition=(3.54771, 
    7.12309, 23.7066), cameraUpVector=(-0.0384174, 0.767029, -0.640461), 
    cameraTarget=(0.126096, -0.411418, 3.54628), viewOffsetX=-0.162196, 
    viewOffsetY=0.399712)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#40 ]', ), )
xe1 = a.instances['Part-1-1'].edges
xEdges1 = xe1.getSequenceFromMask(mask=('[#2000 ]', ), )
region = a.Set(faces=faces1, xEdges=xEdges1, name='Set-1')
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.3087, 
    farPlane=28.3218, width=21.8005, height=10.8291, cameraPosition=(14.7461, 
    2.1061, -12.6046), cameraUpVector=(-0.0404122, 0.82945, 0.557118), 
    cameraTarget=(-0.329239, -0.314752, 2.94493), viewOffsetX=-0.160074, 
    viewOffsetY=0.394482)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#20 ]', ), )
region = a.Set(faces=faces1, name='Set-2')
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#2 ]', ), )
region = a.Set(faces=faces1, name='Set-3')
mdb.models['Model-1'].XasymmBC(name='BC-3', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.3252, 
    farPlane=28.3053, width=21.824, height=10.8408, cameraPosition=(14.8939, 
    1.97969, -12.481), cameraUpVector=(-0.297903, 0.899913, 0.318449), 
    cameraTarget=(-0.181461, -0.441164, 3.06852), viewOffsetX=-0.160247, 
    viewOffsetY=0.394908)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.3255, 
    farPlane=28.305, width=21.8245, height=10.841, cameraPosition=(14.7985, 
    2.04977, -12.5626), cameraUpVector=(-0.136553, 0.871771, 0.470497), 
    cameraTarget=(-0.276894, -0.371081, 2.98691), viewOffsetX=-0.16025, 
    viewOffsetY=0.394917)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14.9571, 
    farPlane=28.9282, width=21.2998, height=10.5804, cameraPosition=(-12.3294, 
    9.0046, -12.425), cameraUpVector=(0.392817, 0.70588, 0.58943), 
    cameraTarget=(-0.39515, -0.393661, 3.20071), viewOffsetX=-0.156397, 
    viewOffsetY=0.385423)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#8 ]', ), )
region = a.Set(faces=faces1, name='Set-4')
mdb.models['Model-1'].XasymmBC(name='BC-4', createStepName='Initial', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
session.viewports['Viewport: 1'].setValues(displayedObject=None)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       8
#: Number of Node Sets:          11
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
mdb.models['Model-1'].boundaryConditions['BC-1'].move('Initial', 'Step-1')
mdb.models['Model-1'].boundaryConditions['BC-1'].move('Step-1', 'Initial')
mdb.models['Model-1'].boundaryConditions['BC-2'].suppress()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
mdb.models['Model-1'].boundaryConditions['BC-2'].resume()
mdb.models['Model-1'].boundaryConditions['BC-2'].setValuesInStep(
    stepName='Step-1', u3=1.0)
mdb.models['Model-1'].boundaryConditions['BC-2'].setValuesInStep(
    stepName='Step-1', u3=-1.0)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.2014, 
    farPlane=28.6839, width=17.9803, height=8.93148, viewOffsetX=-1.77927, 
    viewOffsetY=0.181518)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       8
#: Number of Node Sets:          11
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S33'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Max. Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E33'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E22'), )
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.2817, 
    farPlane=28.6036, width=18.0752, height=8.97866, cameraPosition=(-12.1817, 
    9.56395, -12.2014), cameraUpVector=(0.568096, 0.69117, 0.446712), 
    cameraTarget=(-0.247464, 0.165693, 3.42434), viewOffsetX=-1.78866, 
    viewOffsetY=0.182477)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
mdb.models['Model-1'].boundaryConditions['BC-3'].suppress()
mdb.models['Model-1'].boundaryConditions['BC-4'].suppress()
odb = session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb']
session.viewports['Viewport: 1'].setValues(displayedObject=odb)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.Job(name='Job-sans-symetrie', model='Model-1', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numCpus=1, numGPUs=0)
mdb.jobs['Job-sans-symetrie'].submit(consistencyChecking=OFF)
#: The job input file "Job-sans-symetrie.inp" has been submitted for analysis.
#: Job Job-sans-symetrie: Analysis Input File Processor completed successfully.
#: Job Job-sans-symetrie: Abaqus/Standard completed successfully.
#: Job Job-sans-symetrie completed successfully. 
session.viewports['Viewport: 1'].setValues(
    displayedObject=session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb'])
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-sans-symetrie.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-sans-symetrie.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       8
#: Number of Node Sets:          11
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S33'), )
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.7591, 
    farPlane=28.2122, width=11.316, height=5.62108, viewOffsetX=-1.56589, 
    viewOffsetY=0.697984)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.7067, 
    farPlane=28.2646, width=11.2784, height=5.60239, viewOffsetX=1.57408, 
    viewOffsetY=-0.236933)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.7065, 
    farPlane=28.2648, width=11.2782, height=5.60231, viewOffsetX=1.53317, 
    viewOffsetY=-0.189279)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Max. Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E33'), )
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S33'), )
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.5265, 
    farPlane=26.4027, width=16.1192, height=8.00703, cameraPosition=(-21.8332, 
    2.31607, 3.85039), cameraUpVector=(0.326503, 0.0750562, -0.942211), 
    cameraTarget=(-0.210305, -0.363435, 3.42019))
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.4255, 
    farPlane=26.5037, width=16.0263, height=7.96088, cameraPosition=(-21.8332, 
    2.31607, 3.85039), cameraUpVector=(0.446118, 0.839042, 0.311427), 
    cameraTarget=(-0.210305, -0.363435, 3.42019))
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.124, 
    farPlane=28.0719, width=13.9096, height=6.90944, cameraPosition=(-15.4228, 
    12.0521, -6.12945), cameraUpVector=(0.775868, 0.573237, 0.263492), 
    cameraTarget=(-0.160086, -0.287164, 3.34201))
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.2932, 
    farPlane=27.9029, width=14.0652, height=6.98673, viewOffsetX=2.36262, 
    viewOffsetY=-0.466915)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='RF', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.2943, 
    farPlane=27.9018, width=14.0662, height=6.98722, viewOffsetX=2.29479, 
    viewOffsetY=-0.543357)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Max. Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E33'), )
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.0599, 
    farPlane=28.1361, width=17.7402, height=8.81223, viewOffsetX=2.51572, 
    viewOffsetY=-0.753662)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14.9839, 
    farPlane=28.2121, width=17.6506, height=8.76774, cameraPosition=(-15.3741, 
    12.1469, -6.08445), cameraUpVector=(0.763378, 0.577567, 0.289259), 
    cameraTarget=(-0.111373, -0.192368, 3.38701), viewOffsetX=2.50302, 
    viewOffsetY=-0.749857)
session.viewports['Viewport: 1'].view.setValues(width=18.7762, height=9.32683, 
    viewOffsetX=2.57673, viewOffsetY=-0.790951)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.3318, 
    farPlane=28.4787, width=19.2132, height=9.54393, cameraPosition=(-16.2939, 
    12.4087, -4.76904), cameraUpVector=(0.774162, 0.57705, 0.260165), 
    cameraTarget=(-0.316538, -0.0538496, 3.25128), viewOffsetX=2.63671, 
    viewOffsetY=-0.809362)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.298, 
    farPlane=28.5125, width=19.1708, height=9.52286, viewOffsetX=3.84716, 
    viewOffsetY=-1.29355)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Mises'), )
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['Matrice']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Fibre']
a1.Instance(name='Fibre-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
del a.features['Fibre-1']
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#8 ]', ), )
region = a.Set(faces=faces1, name='Set-5')
mdb.models['Model-1'].EncastreBC(name='BC-5', createStepName='Step-1', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
mdb.models['Model-1'].boundaryConditions['BC-1'].suppress()
mdb.models['Model-1'].boundaryConditions['BC-2'].suppress()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.6346, 
    farPlane=27.9471, width=12.9601, height=6.43777, cameraPosition=(10.3793, 
    7.25918, -14.3912), cameraUpVector=(0.276205, 0.523308, 0.806139), 
    cameraTarget=(-0.215039, -0.377118, 3.28241))
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#2 ]', ), )
region = a.Set(faces=faces1, name='Set-6')
mdb.models['Model-1'].DisplacementBC(name='BC-6', createStepName='Step-1', 
    region=region, u1=1.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=16.3068, 
    farPlane=27.4691, width=13.5173, height=6.71455, cameraPosition=(-3.03055, 
    7.6262, -16.95), cameraUpVector=(-0.302042, 0.675713, 0.672445), 
    cameraTarget=(-0.101572, -0.380224, 3.30406))
session.viewports['Viewport: 1'].view.setValues(nearPlane=16.2059, 
    farPlane=27.7225, width=13.4337, height=6.673, cameraPosition=(-7.60266, 
    4.27469, -16.8167), cameraUpVector=(0.0212581, 0.835625, 0.548889), 
    cameraTarget=(-0.0833502, -0.366867, 3.30353))
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
mdb.models['Model-1'].boundaryConditions['BC-4'].resume()
mdb.models['Model-1'].boundaryConditions['BC-3'].resume()
mdb.models['Model-1'].boundaryConditions['BC-3'].suppress()
mdb.models['Model-1'].boundaryConditions['BC-4'].resume()
mdb.models['Model-1'].boundaryConditions['BC-4'].suppress()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].view.setValues(width=12.6333, height=6.27545, 
    viewOffsetX=-0.330104, viewOffsetY=-0.0017035)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.Job(name='Job-3-dir1-sans-sym', model='Model-1', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numCpus=1, numGPUs=0)
mdb.jobs['Job-3-dir1-sans-sym'].submit(consistencyChecking=OFF)
#: The job input file "Job-3-dir1-sans-sym.inp" has been submitted for analysis.
#: Job Job-3-dir1-sans-sym: Analysis Input File Processor completed successfully.
#: Job Job-3-dir1-sans-sym: Abaqus/Standard completed successfully.
#: Job Job-3-dir1-sans-sym completed successfully. 
session.viewports['Viewport: 1'].setValues(
    displayedObject=session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-1.odb'])
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-3-dir1-sans-sym.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-3-dir1-sans-sym.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       10
#: Number of Node Sets:          13
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-3-dir1-sans-sym.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].setValues(
    displayedObject=session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-3-dir1-sans-sym.odb'])
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.0317, 
    farPlane=28.1671, width=13.8248, height=6.86728, viewOffsetX=1.97974, 
    viewOffsetY=-0.667536)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Max. Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E11'), )
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
mdb.models['Model-1'].boundaryConditions['BC-4'].resume()
mdb.models['Model-1'].boundaryConditions['BC-3'].resume()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.Job(name='Job-4-dir1-sym', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, numCpus=1, numGPUs=0)
mdb.jobs['Job-4-dir1-sym'].submit(consistencyChecking=OFF)
#: The job input file "Job-4-dir1-sym.inp" has been submitted for analysis.
#: Job Job-4-dir1-sym: Analysis Input File Processor completed successfully.
#: Job Job-4-dir1-sym: Abaqus/Standard completed successfully.
#: Job Job-4-dir1-sym completed successfully. 
session.viewports['Viewport: 1'].setValues(
    displayedObject=session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-3-dir1-sans-sym.odb'])
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-4-dir1-sym.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-4-dir1-sym.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       10
#: Number of Node Sets:          13
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.0317, 
    farPlane=28.1671, width=13.8248, height=6.86728, viewOffsetX=2.16351, 
    viewOffsetY=-0.884486)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Max. Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'E11'), )
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
    'EVOL', 'IVOL'))
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
mdb.jobs['Job-4-dir1-sym'].submit(consistencyChecking=OFF)
#: The job input file "Job-4-dir1-sym.inp" has been submitted for analysis.
#: Job Job-4-dir1-sym: Analysis Input File Processor completed successfully.
#: Job Job-4-dir1-sym: Abaqus/Standard completed successfully.
#: Job Job-4-dir1-sym completed successfully. 
o3 = session.openOdb(
    name='C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-4-dir1-sym.odb')
#: Model: C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-4-dir1-sym.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     3
#: Number of Meshes:             3
#: Number of Element Sets:       10
#: Number of Node Sets:          13
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='IVOL', outputPosition=INTEGRATION_POINT, )
session.viewports['Viewport: 1'].view.setValues(nearPlane=15.3042, 
    farPlane=28.2809, width=15.9296, height=7.91283, viewOffsetX=0.139485, 
    viewOffsetY=-0.0795456)
odb = session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-4-dir1-sym.odb']
session.writeFieldReport(fileName='IVOL1s.rpt', append=ON, 
    sortItem='Element Label', odb=odb, step=0, frame=1, 
    outputPosition=INTEGRATION_POINT, variable=(('IVOL', INTEGRATION_POINT), ), 
    stepFrame=SPECIFY)
odb = session.odbs['C:/Users/ktongue/OneDrive - ENISE/ENISE1/S9/Methodes Numériques avancées/Job-4-dir1-sym.odb']
session.writeFieldReport(fileName='S11_Ss.rpt', append=ON, 
    sortItem='Element Label', odb=odb, step=0, frame=1, 
    outputPosition=INTEGRATION_POINT, variable=(('IVOL', INTEGRATION_POINT), (
    'S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ), stepFrame=SPECIFY)
