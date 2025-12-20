# -*- coding: utf-8 -*-

import pandas as pd

def texttoint(text: str)-> int:
    '''
    Converts text to integer.
    
    Parameters
    ----------
    text : str
        text to convert to integer.

    Returns
    -------
    int
        Returns the number represented by text or 0 if text is empty.

    '''
    if text == '':
        return 0
    return int(text)

def wrangle(input_network: str, vertices_name: list)-> pd.DataFrame:
    '''
    Parses a string into a dataframe
    
    Parameters
    ----------
    input_network : str
        string to be parsed into a dataframe.
    vertices_name : list
        list of names for columns and rows of the dataframe.

    Returns
    -------
    df : pd.DataFrame
        Dataframe whose entries represent the nodes in the graph network.

    '''
    extracted_lines = input_network.splitlines() 
    lines_list = [line.split(',') for line in extracted_lines]
    parsed_network = [[texttoint(cost) if cost != '-' else 0 for cost in line] for line in lines_list]
    df = pd.DataFrame(parsed_network, index=vertices_name, columns=vertices_name)
    return df

def get_unique_nodes(df: pd.DataFrame)-> list:
    '''
    Gets all unique nodes of the network from the dataframe.

    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe whose entries represent the nodes in the graph network.

    Returns
    -------
    vertices : list
        list of unique nodes in the network.

    '''
    vertices = []
    seen = []
    for row in df.index:
        temp = []
        for column in df.columns:
            if row == column:
                continue
            if df.loc[row, column] == 0:
                continue
            if row+column in seen or column+row in seen:
                continue
            temp.append([row, column, df.loc[row, column]])
            seen.append(row+column)
        if temp:
            vertices.append(temp)
    return vertices

def get_nodes(df: pd.DataFrame)-> list:
    '''
    Gets all possible nodes of the network from the dataframe.

    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe whose entries represent the nodes in the graph network.

    Returns
    -------
    vertices : list
        list of all nodes in the network.

    '''
    vertices = []
    for row in df.index:
        temp = []
        for column in df.columns:
            if row == column:
                continue
            if df.loc[row, column] == 0:
                continue
            temp.append([row, column, df.loc[row, column]])
        if temp:
            vertices.append(temp)
            
    #Sorting the edges in each node by cost        
    vertices = [sorted(nodes, key=lambda x: x[2]) for nodes in vertices]
    
    return vertices


def get_shortest_edges(vertices: list)-> list:
    '''
    Gets list of all the shortest edges connected to each node in the network.

    Parameters
    ----------
    vertices : list
        All nodes in the the network

    Returns
    -------
    shortest_edges: list
        list of all the shortest edges connected to each node.

    '''
    shortest_edges = []
    for line in vertices:
        shortest_edges.append(line[0])
    return shortest_edges

def find_unique_node(edges):
    '''
    Removes duplicate edges in a list of nodes

    Parameters
    ----------
    edges : list
        list of nodes in the network.

    Returns
    -------
    edges : list
        list of unique nodes.

    '''
    selected = []
    for edge in edges:
        row, column = edge[:2]
       
        if row+column in selected or column+row in selected:
            edges.remove(edge)
        else:
            selected.append(row+column)

    return edges

def get_connected_nodes(shortest_edges):
    '''
    Gets the list of name of nodes that are connected in the network

    Parameters
    ----------
    shortest_edges : list
        List of edges in the network..

    Returns
    -------
    connected_nodes: list
        List of nodes that are connected in the network

    '''
    connected_nodes = shortest_edges[0][:2]
    edge_name = [node[:2] for node in shortest_edges]
#    print(edge_name)
    for i in range(2):
        for name in edge_name:
            if name[0] not in connected_nodes:
                if name[1] not in connected_nodes:
                    continue
                connected_nodes.append(name[0])
            else:
                if name[1] not in connected_nodes:
                    connected_nodes.append(name[1])
    return connected_nodes

def add_isolated_node(node_names: list, vertices: list, shortest_edges: list,
                      isolated_nodes: list, connected_nodes: list)-> int:
    '''
    Adds isolated nodes to the connected nodes

    Parameters
    ----------
   node_names: list
       list of node names
       
    vertices : list
        List of all nodes in the network.
        
    shortest_edges : list
        List of all shortest edges for each node in the network.
        
    isolated_nodes : list
        list of unconnected nodes.
        
    connected_nodes : list
        List of names of coneected nodes.
    

    Returns
    -------
    int:
    Number of newly added nodes.

    '''
    initial_length = len(shortest_edges)
    while isolated_nodes:
        tmp = isolated_nodes[0]
        new_node = vertices[node_names.index(tmp)][1]   
        shortest_edges.append(new_node)
        connected_nodes = get_connected_nodes(shortest_edges)        
        isolated_nodes = [x for x in node_names if x not in connected_nodes]
    
    final_length = len(shortest_edges)
    return final_length - initial_length

def network_cost(graph: list)-> int:
    '''
    Calculates the cost of an entire network

    Parameters
    ----------
    graph : list
        Network to calculate its cost.

    Returns
    -------
    sum : int
        Total cost of the network.

    '''
    sum = 0
    for edge in graph:
        sum += edge[2]
    return sum

def maximum_saving(input_network: str)-> int:
    '''
    Calculate the maximum cost that can be saved by taking the shortest path.

    Parameters
    ----------
    input_network : str
        String containing the network nodes and their corresponding pair cost.

    Returns
    -------
    int
        maximum saved cost.

    '''
    vertices_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    #Parsing the network string into a dataframe such that each row represent
    # a node in the network and each entry represent the cost of an edge in the network
    df = wrangle(input_network, vertices_name)
    
    #Extracting all nodes from the network
    all_nodes = get_nodes(df)
    
    #Extracting the shortest edges from each node
    shortest_edges = get_shortest_edges(all_nodes)
    
    #Removing duplicate edges from the shortest edges
    shortest_edges = find_unique_node(shortest_edges)
    
    #Check if there is any isolated nodes
    connected_nodes = get_connected_nodes(shortest_edges)
    isolated_nodes = [x for x in vertices_name if x not in connected_nodes]
    
    #Adding isolated nodes if they exist
    add_isolated_node(vertices_name, all_nodes, shortest_edges, isolated_nodes, connected_nodes)
    
    #Calculating the maximum network cost
    unique_nodes =  get_unique_nodes(df)
    all_unique_edges = [edge for node in unique_nodes for edge in node]
    max_cost = network_cost(all_unique_edges)
    
    #Calculating the minimum network cost
    min_cost = network_cost(shortest_edges)
    print(min_cost)
    #Calculating the maximum saving
    max_saving = max_cost - min_cost
    
    return max_saving

#Example Usage
input_network = '''-,14,10,19,-,-,-
14,-,-,15,18,-,-
10,-,-,26,,29,-
19,15,26,-,16,17,21
-,18,-,16,-,-,9
-,-,29,17,-,-,25
-,-,-,21,9,25,-
'''
max_saving = maximum_saving(input_network)
print(max_saving)
    

