import igraph as ig

def pinguin_example():
    """
    Returns a basic example to understand the use of get_sources
    """
    input_edges = [[0,1],[1,2],[2,0]] # first strong component, and source
    input_edges += [[2,3],[3,4],[4,5],[5,3]] # second strong component
    input_edges += [[5,6],[6,7],[7,8],[8,6]] # third strong component, and dest
    input_edges += [[9,3],[9,10],[10,11],[11,9]] #fourth strong component, and source
    input_edges += [[3,12],[12,13],[13,14],[14,12]] #fifth strong component and dest
    G = ig.Graph(9,input_edges,directed=True)
    G.vs["color"] = ["#4682B4" for i in range(0,15)]

    args = {}
    args["layout"] =  G.layout("kk")
    args["bbox"] =  (500, 500)
    args["vertex_color"] = G.vs["color"]
    args["vertex_label"] = range(0,15)
    args["edge_color"] = "#ADD8E6"
    args["edge_width"]= [1]
    args["margin"] = 90
    return G, args

def lion_example():
    """
    Returns the example graph
    It already has ["name"],["color"] for nodes
    and ["color"] for edges
    """
    input_edges = [[0,4],[0,7],[0,15]] + [[1,5],[1,11],[1,6]] + [[2,4],[2,10]] + [[3,9],[3,12]]
    input_edges += [[4,16]] + [[5,24],[5,17],[5,18]] + [[6,16],[6,17],[6,19]]+ [[7,18],[7,19]]
    input_edges += [[8,25]] + [[9,4],[9,5],[9,6],[9,7],[9,8]] + [[10,8],[10,15]]
    input_edges += [[11,13],[11,14]] + [[12,13],[12,14],[12,15]]
    input_edges += [[13,21],[13,14]] + [[14,20]] + [[15,21]]
    input_edges += [[16,22],[16,23]] + [[17,22],[17,23],[17,25]] + [[18,22],[18,25]]
    input_edges += [[19,22],[19,24]] 
    input_edges +=  [[20,26],[20,27]] + [[21,26],[21,27]]
    E = ig.Graph(28,input_edges,directed=True)

    ## Labels
    for i in range(0,28):
        E.vs[i]["name"] = str(i)

    for i in range(0,28):
        E.vs[i]["color"] = "white"

    for i in range(0,4):
        E.vs[i]["name"] = "s" + str(i+1)
        E.vs[i]["color"] = "light blue"

    for i in range(4,9):
        E.vs[i]["name"] = "f" + str(i-3)
        E.vs[i]["color"] = "light green"

    for i in range(13,16):
        E.vs[i]["name"] = "f" + str(i-7)
        E.vs[i]["color"] = "light green"

    for i in range(22,28):
        E.vs[i]["name"] = "d" + str(i-22)
        E.vs[i]["color"] = "#ffae42" # Yellow orange
    
    args = {}
    args["layout"] =  E.layout("kk")
    args["bbox"] =  (700, 700)
    args["vertex_color"] = E.vs["color"]
    args["vertex_label"] = E.vs["name"]
    args["edge_color"] = "#ADD8E6"
    args["edge_width"]= [1]
    args["margin"] = 90

    return E, args