#!/usr/sbin/python
# -*- coding: utf-8 -*-

import argparse
import networkx as nx
import time
import math

import graph.io as io
import graph.printing as gprint

DESCRIPTION = 'Plot NetworkX graph which specified in YAML file'

def assign_labels(graph):
    '''create dict with human-readable labels, assigned to nodes'''
    labels = {}
    for node in graph.nodes_iter(data=True):
        try:
            labels[node[0]] = "{first_name} {last_name}".format(**node[1])
        except KeyError as e:
            print("There is no such data attribute: {0}" \
                  " in {1}".format(e, node[0]))
    return labels

def assign_colors(graph):
    '''assign colors to nodes by total number of friends'''
    color_list = []
    for node in graph.nodes_iter(data=True):
        try:
            friends_total = float(node[1]['friends_total'])
            node_color = math.log(friends_total)
            color_list.append(node_color)
        except (KeyError, ValueError):
            color_list.append(1)
    return color_list
    
def assign_node_sizes(graph, default_size = 100):
    '''assign node sizes by number of friends contained in graph'''
    sizes = []
    for node in graph.nodes_iter():
        sizes.append((1 + graph.degree(node)) * default_size)
    return sizes

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('path', type=str,
                    help='path to file which contains graph data.')
parser.add_argument('-o', '--output', type=str,
                    help='path to file for writing plot image')
parser.add_argument('--with-latex', action='store_true',
                    help='use LaTeX for text processing') 
parser.add_argument('--no-labels', action='store_true',
                    help='draw graph without labels')
parser.add_argument('--dpi', type=int, help='set dpi')


args = parser.parse_args()

# configure pyplot before import
if args.with_latex:
    from matplotlib import rc
    rc('font',**{'family':'sans-serif','sans-serif':['Monospace']})
    rc('text', usetex=True)
    rc('text.latex', unicode=True)
    rc('text.latex', preamble = '\\usepackage[utf8]{inputenc}')
    rc('text.latex', preamble = '\\usepackage[russian]{babel}')

import matplotlib.pyplot as plt

try:
    start_time = time.time()
    G = io.read_graph((args.path))
    nx.draw(G,
            labels = assign_labels(G),
            node_size = assign_node_sizes(G),
            node_color = assign_colors(G),
            with_labels=not args.no_labels)

    if args.output:
        # store plot to file
        plt.savefig(args.output, dpi=args.dpi)
        gprint.print_elapsed_time(time.time() - start_time)
    else:
        # interactive drawing
        gprint.print_elapsed_time(time.time() - start_time)
        plt.show()
except FileNotFoundError:
    print("Please, specify existing YAML source!")
