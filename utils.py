# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:39:19 2019

@author: kevin
"""

def print_grid(grid):
    for row in grid:
        out = ''
        for tile in row:
            out += tile + ' '
        print(out)
        
def get_adjacent_coords(grid, coords):
        """
        Returns the coords of all tiles adjacent to given coords.
        """
        adj_coords = []
        l, w = coords
        for length in range(max([l - 1, 0]), min([l + 2, len(grid)])):
            for width in range(max([w - 1, 0]), min([w + 2, len(grid[length])])):
                adj_coords.append([length, width])
        adj_coords.remove([l, w])
        return adj_coords