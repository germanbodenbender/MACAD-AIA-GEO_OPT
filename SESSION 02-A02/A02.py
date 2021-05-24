# MACAD // AIA + GEOMETRY OPTIMIZATION
# GERMAN OTTO BODENBENDER
# ASSIGNMENT 02 - 2021/04/11


"""Provides a scripting component.
    Inputs:
        m: a mesh
        s: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        """
        
import Rhino
import Rhino.Geometry as rg
import Rhino.Render as rr
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th 
import math



#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a

m.FaceNormals.ComputeFaceNormals()
a = m.FaceNormals 





#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

b = []

vector3d = []

for i in range(len(a)):
    x = m.Faces.GetFaceCenter(i)
    vec = rg.Vector3d(x)
    b.append(x)
    vector3d.append(vec)

#print(vec)


#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

sVec = Rhino.RhinoDoc.ActiveDoc.Lights.Sun.Vector

c = []
for i in range(len(a)):
    z = rg.Vector3d.VectorAngle(a[i], sVec)
    c.append(z)



#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

exploded=[]
mesh_copy = rg.Mesh.Duplicate(m)

for i in range(len(mesh_copy.Faces)):
    extract_faces= mesh_copy.Faces.ExtractFaces([0])
    exploded.append(extract_faces)

d = exploded


#z = meshduplicate.Faces.ExtractFaces([i])
#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!



#Create lines based on the normal and the lenght is based on the sun angle
lines=[]
for i in range(len(m.Faces)):
    line=rg.Line(b[i],a[i], c[i]/2)
    lines.append(line)


#Trying to get the mesh edges
p = d[1].GetNakedEdges()
#Gives a polyline curve as a result



#Trying to use the mesh edges to do a tapered extrude, but having the issue of "1. Solution exception:expected Curve, got Polyline"
mesh_edges = []
for i in range(len(m.Faces)):
    x = d[i].GetNakedEdges()
    lnnurb = x[0].ToNurbsCurve()
    mesh_edges.append(lnnurb)


#Create offseted planes to use for the rectangules (FAILED)
"""
plane = []
for i in range(len(m.Faces)):

    pl = rg.Plane(g[i],a[i])
    h.append(plane)
"""


#Create Brep tapered  (FAILED)
"""
extrude = []
for i in range(len(m.Faces)):
    ex = rg.Brep.CreateFromTaperedExtrude(mesh_edges[i], 0.1, vector3d[i], b[i], c[i], 0)
    extrude.append(ex)
brep = th.list_to_tree(extrude)
"""

#Create mesh edges extrusion (FAILED)
"""
extrude = []
for i in range(len(m.Faces)):
    ex = rg.Extrusion.Create(mesh_edges[i],0.3,True)
    extrude.append(ex)
brep = th.list_to_tree(extrude)
"""

#Create pipe extrusion from lines and lenght based on sun vector
pipes = []
for i in range(len(lines)):
    pi = rg.Brep.CreateFromSweep(rg.LineCurve(lines[i]),mesh_edges[i],True,0.1)
    pipes.append(pi)
expipe = th.list_to_tree(pipes)


