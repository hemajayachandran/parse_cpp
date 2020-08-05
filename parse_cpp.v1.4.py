#!/usr/bin/env python
"""Usage: call with <filename> <typename>
"""
import sys
import clang.cindex
from clang.cindex import CursorKind
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import re


dictionary = {}
dependency_order = defaultdict(list)

def process_decl(node):
    # This function will insert the declared variables(node) into a dictionary
    for child_node in node.get_children():
        if child_node.kind == CursorKind.VAR_DECL:
            if child_node.spelling not in dictionary.keys():
                dictionary[child_node.spelling] = []
    return

def process_right_nodes_for(node, left_expr):
    # This function will process the right nodes of the input node

    for child_node in node.get_children():
        if child_node.kind == CursorKind.BINARY_OPERATOR:
            process_right_nodes_for(child_node, left_expr)
        elif child_node.kind == CursorKind.UNEXPOSED_EXPR:
            if left_expr in dictionary.keys():
                dependency_order[left_expr].append(child_node.spelling)
        elif child_node.kind == CursorKind.PAREN_EXPR:
            process_right_nodes_for(child_node, left_expr)
    return

def process_binary_operation(node):
    # This function will parse the node associated with binary/compound operations

    left_expr = ''
    for child_node in node.get_children():
        if child_node.kind == CursorKind.DECL_REF_EXPR:
            left_expr = child_node.spelling
        elif child_node.kind == CursorKind.INTEGER_LITERAL:
            dependency_order[left_expr].append(left_expr)
        elif child_node.kind == CursorKind.BINARY_OPERATOR:
            # Calling function process_right_nodes_for() to process the right child nodes
            process_right_nodes_for(child_node, left_expr)
        elif child_node.kind == CursorKind.UNEXPOSED_EXPR:
            if left_expr in dictionary.keys():
                dependency_order[left_expr].append(child_node.spelling)
        elif child_node.kind == CursorKind.PAREN_EXPR:
            process_right_nodes_for(child_node, left_expr)
    return


def find_for_loop_iteration(list_of_tokens):
    # This function will find the number of times the loop will execute

    start, step, stop = 0, 0, 0
    for i in range(len(list_of_tokens)):
        text = list_of_tokens[i]
        if re.search("^[a-z][=]\d$", text):
            start = int(''.join(re.findall("\d", text)))
        elif re.search("^[a-z][<]\d$", text):
            stop = int(''.join(re.findall("\d", text)))
        elif re.search("^[a-z][<][=]\d$", text):
            stop = int(''.join(re.findall("\d", text))) + 1
        elif re.search("^[a-z][+][+]$", text):
            step = 1
        elif re.search("^[a-z][-][-]$", text):
            step = -1
    k = (stop - start)/step
    print("********Number of iterations*******", k)
    print('\n')

    return



def process_for_loop(node, string):
    # This function gets the for loop statement and store it into a list after doing a split function
    children = list(node.get_children())
    operator_min_begin = (children[0].location.line, children[0].location.column)
    operator_max_end = (children[len(children)-1].location.line, children[len(children)-1].location.column)
    for token in cursor.get_tokens():
        if (operator_min_begin < (token.extent.start.line,token.extent.start.column) and operator_max_end >= (token.extent.end.line, token.extent.end.column)):
            if token.spelling != ')':
                string = string + token.spelling
    list_of_tokens = string.split(';')

    # Calling function find_for_loop_iterations()
    find_for_loop_iteration(list_of_tokens)

    return


def process_compound_statement(node):
    # This function parses the child nodes of CursorKind.COMPOUND_STMT

    for child_node in node.get_children():
        if child_node.kind == CursorKind.DECL_STMT:
            process_decl(child_node)
        elif child_node.kind == CursorKind.BINARY_OPERATOR or child_node.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
            process_binary_operation(child_node)
        elif child_node.kind == CursorKind.FOR_STMT:
            process_for_loop(child_node, '')

    return


def draw_graph(dependency_order):
    # This function will draw a graph using adjacency list of nodes

    g = nx.DiGraph()
    g.add_nodes_from(dependency_order)
    for node, edges in dependency_order.items():
        for edge in edges:
            g.add_edge(node, edge)
    nx.draw(g,with_labels=True)
    plt.draw()
    plt.show()

    return



def parse_cpp(current_node):
    # This function parses the cpp code

    count = len(list(current_node.get_children()))
    if current_node.kind == CursorKind.COMPOUND_STMT:
        # Calling function process_compound_statement()
        process_compound_statement(current_node)
    for child_node in current_node.get_children():
        parse_cpp(child_node)

    return
        

if __name__ == "__main__":

    # Set library path with python binding libclang
    clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')
    index = clang.cindex.Index.create()
    translation_unit = index.parse(sys.argv[1])
    cursor = translation_unit.cursor
    print('Translation unit:', translation_unit.spelling)
    print('\n')
    # Calling function parse_cpp() by passing the root node of translation unit
    parse_cpp(cursor)

    # Displaying the adjacency list graph representation
    print("######Graph using adjacency list######")
    print(dependency_order)
    for node, edges in dependency_order.items():
        print(node + " -> ", edges)
    
    # Calling function draw_graph()
    draw_graph(dependency_order)
