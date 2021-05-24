"""
Name: MeshPaths
Updated: 141031
Author: Anders Holden Deleuran (CITA/KADK)
Copyright: Creative Commons - Attribution 4.0 International
GitHub: www.github.com/AndersDeleuran/MeshAnalysis
Contact: adel@kadk.dk
"""
import rhinoinside
rhinoinside.load()
import Rhino  
import Rhino.Geometry as rg
import networkx as nx

def meshwalker(mesh,weightMode,GraphType,SLine,mode):
    # Create graph
    g = nx.Graph()
    a=mesh
    if GraphType == "vertexGraph":
        for i in range(a.Vertices.Count):
            # Get vertex as point3D
            pt3D=rg.Point3d(a.Vertices[i])
            # Add node to graph and get its neighbours
            g.add_node(i,point=pt3D)
            neighbours = a.Vertices.GetConnectedVertices(i)
            # Add edges to graph
            for n in neighbours:  
                if n > i:
                    p1=rg.Point3d.FromPoint3f(a.Vertices[i])
                    p2=rg.Point3d.FromPoint3f(a.Vertices[n])
                    line = rg.Line(p1,p2)
                    if weightMode == "edgeLength":
                          w = line.Length
                    elif weightMode == "sameWeight":
                          w = 1
                    g.add_edge(i,n,weight=w,line=line)
    elif GraphType == "faceGraph":
        for i in range(a.Faces.Count):
            # Add node to graph and get its neighbours
            g.add_node(i,point=a.Faces.GetFaceCenter(i))
            neighbours = a.Faces.AdjacentFaces(i)
            # Add edges to graph
            for n in neighbours:
                if n > i:
                    p1=a.Faces.GetFaceCenter(i)
                    p2=a.Faces.GetFaceCenter(n)
                    line = rg.Line(p1,p2)
                    if weightMode == "edgeLength":
                         w = line.Length
                    elif weightMode == "sameWeight":
                         w = 1
                    g.add_edge(i,n,weight=w,line=line)

    Nodes = [g.nodes[i]["point"] for i in g.nodes()]
    Edges = [e[2]["line"] for e in g.edges(data=True)]
    Stats = "Nodes: " + str(len(Nodes)) + "\n" + "Edges: " + str(len(Edges))

    def hasPath(graph,source,target):
        
        """ Return True if graph has a path from source to target, False otherwise """
        
        try:
            sp = nx.shortest_path(graph,source,target)
        except nx.NetworkXNoPath:
            return False
        return True
    
    def shortestWalk(g,SLine,mode,GraphType):
        
        # Get index of closest nodes to line endpoints

        if GraphType == "vertexGraph":

            nPts=a.Vertices
            nPts_m=[]
            for i in nPts:
                pt=rg.Point3d.FromPoint3f(i)
                nPts_m.append(pt)
            nPts=Rhino.Collections.Point3dList(nPts_m)
        elif GraphType == "faceGraph":
            nPts=a.Faces.Count
            nPts_m=[]
            for i in range(nPts):
                pt=a.Faces.GetFaceCenter(i)
                nPts_m.append(pt)
            nPts=Rhino.Collections.Point3dList(nPts_m)

        start = nPts.ClosestIndex(SLine.From)
        end = nPts.ClosestIndex(SLine.To)
        
        # Check that start and end are not the same node
        if start == end:
            
            print ("Start and end node is the same")
            
        else:
            
            # Check that a path exist between the two nodes
            if hasPath(g,start,end):
            
                # Calculate shortest path
                
                if mode == "dijkstra_path":
                    sp = nx.dijkstra_path(g,start,end,weight = "weight")
                    
                elif mode == "shortest_path":
                    sp = nx.shortest_path(g,start,end,weight = "weight")
                    
                # Make polyline through path
                pts = [g.nodes[i]["point"] for i in sp]
                #get points indexes 
                indexes=[]
                for i in pts:
                    ind= nPts.ClosestIndex(i)
                    indexes.append(ind)

                return [pts,indexes]
                
    FinalPath0=shortestWalk(g,SLine,mode,GraphType)[0]
    FinalPath1=shortestWalk(g,SLine,mode,GraphType)[1]

    return FinalPath0, FinalPath1
    