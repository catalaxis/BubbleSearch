import igraph as ig
import random
import itertools

## USED ##
def randomized(n_size, m_size,seed=87388):
    """
    Data: int n, int m, seed = 87388
    Returns: Graph with n nodes and m edges
    *
    """
    Graph = ig.Graph(n=n_size,directed=True)
    random.seed(seed)
    RandEdges = []
    for x in range(1, m_size):
        RandEdges.append(random.sample(range(0,n_size), 2))
    Graph.add_edges(RandEdges)
    return Graph

def inverted(Graph):
    """
    Data: Graph
    Returns: an Graph with inverted edges
    """
    new_edges = []
    for i in Graph.get_edgelist():
        new_edges += [[i[1],i[0]]]
    return ig.Graph(n = Graph.vcount(), edges=new_edges,directed=True)

def bfs(Graph, Source,Inverted=False):
    """
    Data: Graph, Source or Dest, Bool (False for Source, True for Dest)
    Returns: List with all reachable nodes for the Source in Graph or its counterpart
    * Its implemented in iGraph, this method exist only to make the code more elegant and compact
    """
    # Its application it's the standard BFS
    # Implemented on the lib
    if Inverted:
        Graph = inverted(Graph)
    return Graph.bfs(Source)[0]

def reachable_dests(Graph,From,Dest,Destination=True):
    """
    Data: Graph, list of nodes, Dest, Bool (False for Dest, True for Source)
    Returns: List with all reachable destination nodes for the list of nodes given
    *
    """
    if not Destination:
        Graph = inverted(Graph)
    begin = True
    r_elements = []
    for node in From:
        if begin:
            r_elements = [x for x in bfs(Graph,node) if x in Dest]
            begin = False
            continue
        r_elements = [x for x in r_elements if x in bfs(Graph,node)]

    r_elements.sort()
    return r_elements

def get_sources(Graph, hash = False,all=False):
    """
    Data: Graph, hash = False (True if sets as set(), otherwise sets as arrays)
    Returns: Source Set, Destination Set
    * note: Each may contain a list, that is due to the equivalence of source or dest
            In strong components.
    """
    # Check Strong Components
    S = []
    D = []
    for sc in Graph.connected_components(mode="strong"):

        IN = []
        OUT = [] 
        # Check each node in Strong Component or SC
        for node in sc:
            IN += [x for x in Graph.neighborhood(node) if x not in sc if x not in IN if x not in Graph.successors(node)]
            OUT += [x for x in Graph.successors(node) if x not in sc if x not in OUT]
        

        # Add to the output the SC only if it is a source or a destination
        if IN and not OUT:
            D += [sc[0]] if not all else sc
        if OUT and not IN:
            S += [sc[0]] if not all else sc
    
    D.sort()
    S.sort()
    return S, D


def get_reachable_dest(Graph, Dest,Destination=True):
    ## Name should be changed, it's measleading
    """
    Data: Graph, Dest, Destination = False (True if Dest is Source)
    Returns: A dict where each entry is a Destination Node
            and it contains all the nodes of the Graph to which
            it is reachable.
    """
    
    colors = {}
    if Destination:
        Graph = inverted(Graph)
    for node in Dest:
        colors[node] = [x for x in bfs(Graph, node) if x !=node]
    
    return colors
            
def get_colored_nodes(Graph,Dest,Destination=True):
    """
    Data: Graph, Dest, Destination = False (True if Dest is Source)
    Returns: A dict where each entry is a node, on which it's stored its class
    """

    reachable_dict = get_reachable_dest(Graph,Dest,Destination)
    colored_set = {}
    Dest.sort()
    all_nodes = range(0,Graph.vcount())
    for v in all_nodes:
        color_class = []
        for node in Dest:
            if v in reachable_dict[node]:
                color_class += [node]
        colored_set[v] = color_class
    
    return colored_set

def color_set(Graph,Dest,Destination=True,hash=False):
    """
    Data: Graph, Dest, Destination = True (False if Dest is Source), hash = False (True if class as set())
    Returns: Class_set: A dict where each entry is a class, on which it's stored its elements (or nodes)
             Class_names: Dict where each entry is the class name, and it contains its reference
             Class_as_string: A dict where each entry is a class (list as string), on which it's stored its elements
    
    """

    Dest.sort()
    # Get all classes with itertools
    # It lets us work combination per combination
    all_classes = []
    for r in range(len(Dest)+1):
        for combination in itertools.combinations(Dest, r):
            all_classes += [list(combination)]

    if Destination:
        Graph = inverted(Graph)


    class_set = {}
    class_names = {}
    class_as_string = {}
    index = 0
    for c in all_classes:
        if not c:
            continue
        begin = True
        elements = [] #Not actually needed, exist just to prevent program warnings
        for node in c:
            if begin:
                elements = [x for x in bfs(Graph, node) if x !=node]
                begin = False
                continue
            elements = [x for x in elements if x in bfs(Graph, node)]

        if hash:
            cset = set()
            if elements:
                for e in elements:
                    cset.add(e)
            elements = cset

        class_set[index] = elements
        class_names[index] = c
        class_as_string[str(c)] = elements
        index += 1
    
    return class_set, class_names, class_as_string

## VISUALIZATION FUNCTIONS ## ==============================================================

def draw_tree(Tree, Source, Edges, Tuple_tree = True, ax = False):
    """ draw Tree with colores Source and Edges"""
    # create tree
    if Tuple_tree:
        vertex = {x[1] for x in Tree} | {x[0] for x in Tree}
        Tree_edges = Tree
        Tree = ig.Graph(directed=True)
        Tree.add_vertices(list(vertex))

    args = {}
    vcolors = ["#b5dce9" for x in range(Tree.vcount())]
    vcolors[Source] =  "light green"
    args["vertex_color"] = vcolors

    ei = 0
    for edge in Tree_edges:
        Tree.add_edge(Tree.vs.find(name=edge[0]),Tree.vs.find(name=edge[1]))
        Tree.es[ei]["color"] = "#a8ced2"
        ei+=1
    for edge in Edges:
        Tree.add_edge(Tree.vs.find(name=edge[0]),Tree.vs.find(name=edge[1]))
        Tree.es[ei]["color"] = "#b433ce"
        ei+=1

    args["vertex_label"] = Tree.vs["name"]
    args["layout"] = Tree.layout("kk")
    args["bbox"] = (400,400)
    args["margin"] = 20
    args["edge_width"]= [1]

    return ig.plot(Tree,target=ax, **args) if ax else ig.plot(Tree, **args)
        
def draw_multigraph(Graph,ax=False):

    args = {}
    args["vertex_label"] = Graph.vs["name"]
    args["vertex_color"] = "#b5dce9"
    args["edge_label"] = Graph.es["label"]
    args["edge_color"] = Graph.es["color"]
    args["layout"] =  Graph.layout("kk")
    args["bbox"] =  (600, 600)
    args["margin"] = 100
    args["edge_width"]= [1]

    return ig.plot(Graph,target=ax,**args) if ax else ig.plot(Graph, **args)

