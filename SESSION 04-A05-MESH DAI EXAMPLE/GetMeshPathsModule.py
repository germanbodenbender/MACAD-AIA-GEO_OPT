#AIA - GEOMETRY OPTIMIZATION SEMINAR
#STUDENT: German Otto Bodenbender
#EXERCISE 04

from pathlib import Path
folder = Path("C:\Program Files\Rhino 7\System")

import rhinoinside
import ghhops_server as hs

rhinoinside.load(str(folder))

import Rhino
import Rhino.Geometry as rg
hops = hs.Hops(app=rhinoinside)

import networkx as nx
import MeshPaths as mp

@hops.component(
    "/MeshPathWalker",
    name="MeshPathWalker",
    description=" Make a networkx graph with mesh vertices as nodes and mesh edges as edges ",
    inputs=[
        hs.HopsMesh("Mesh","M","Mesh to make networkx graph for"),
        hs.HopsString("WeightMode","W","Weight Mode"),
        hs.HopsString("GraphType","T","Mesh Graph Type"),
        hs.HopsLine("SLine","L", "Line to process"),
        hs.HopsString("mode" ,"m", "Shortest Path Mode")
    ],
    outputs=[
        hs.HopsPoint("ShortestPath", "SP" ,"Shortest Path",hs.HopsParamAccess.LIST),
        hs.HopsString("FacesIndex", "I" ,"Faces indexes",hs.HopsParamAccess.LIST)
    ]
)

def MeshPathWalker(mesh,weightMode,GraphType,SLine,mode):
    return mp.meshwalker(mesh,weightMode,GraphType,SLine,mode)

if __name__ == "__main__":
    hops.start()