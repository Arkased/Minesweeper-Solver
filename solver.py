# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 16:07:05 2019

@author: kevin
"""

import minesweeper
from random import random
from utils import get_adjacent_coords

class Solver:
    def __init__(self, minefield):
        self._view = minefield.get_player_grid_view()
        self._minefield = minefield
    
# =============================================================================
# Interfaces
# =============================================================================
        
    def solve(self):
        """
        Attempts to solve the minefield.
        """
        while self._minefield.get_game_ongoing():
            if self._apply_all_tiles(self._reveal_zero):
                continue
            if self._apply_all_tiles(self._flag_adajcent):
                continue
            else:
                self._reveal_tile() # random guess
        
    def print_view(self):
        """
        For debugging only. Prints the view of the solver of the minefield.
        """
        for row in self._view:
            out = ''
            for ele in row:
                out += str(ele) + ' '
            print(out)
   
# =============================================================================
# Strategies
# =============================================================================
    
    def _flag_adajcent(self, coord):
        """
        If the number of unrevealed tiles adjacent to coord is equal to the
        number of unaccounted for mines, flags all adjacent, unrevealed tiles.
        
        Returns whether a tile was flagged.
        """
        l, w = coord
        try:
            num = int(self._view[l][w])
        except:
            return
        if num > 0:
            adj_coords = get_adjacent_coords(self._view, coord)
            unrevealed = list(filter(lambda coord: self._view[coord[0]][coord[1]] == 'X', adj_coords))
            if len(unrevealed) == num:
                for coord in unrevealed:
                    self._flag_tile(coord)
                return True
        return False
            

    
    def _reveal_zero(self, coord):
        """
        If all adjacent mines of coord are accounted for, reveals all adjacent,
        unrevealed tiles.
        
        Returns whether a tile was revealed.
        """
        l, w = coord
        results = []
        try:
            num = int(self._view[l][w])
        except:
            num = self._view[l][w]
        if num == 0 or num == ' ':
            for adj_coord in get_adjacent_coords(self._view, coord):
                results.append(self._reveal_tile(adj_coord))
        return any(results)
    
# =============================================================================
# Common Methods
# =============================================================================
    
    def _reveal_tile(self, coord = None):
        """
        Reveals a given coord or random coord (if passed None). Attempts to
        chain reveal if the tile revealed has all adjacent mines accounted for.
        
        Returns whether a tile was revealed
        """
        try:
            l, w = coord
        except:
            l = int(random() * len(self._view))
            w = int(random() * len(self._view[l]))
            coord = [l, w]
        if self._view[l][w] == 'X':
            self._view[l][w] = self._minefield.reveal_tile(coord, recur = False)
            self._update_tile(coord)
            self._reveal_zero(coord)
            return True
        return False
    
    def _flag_tile(self, coord):
        """
        Flags a coord in view, indicating the presence of a mine.
        """
        l, w = coord
        if self._view[l][w] == 'X':
            self._view[l][w] = '>'
            for adj_coord in get_adjacent_coords(self._view, coord):
                self._update_tile(adj_coord)
        else:
            raise ValueError('attempted to flag ' + self._view[l][w])
                
    def _update_tile(self, coord):
        """
        Updates the number of unaccounted for mines adjacent to a given coord.
        """
        base = self._minefield.inspect_tile(coord)
        try:
            num = int(base)
        except:
            if base == ' ':
                num = 0
            else:
                return
        for adj_coord in get_adjacent_coords(self._view, coord):
            l, w = adj_coord
            if self._view[l][w] == '>':
                num -= 1
        assert num >= 0
        
        l, w = coord
        self._view[l][w] = str(num)
        
# =============================================================================
# Utils
# =============================================================================

    def _apply_all_tiles(self, f):
        """
        Applies a function to all coords of the minefield.
        
        Returns True if any function call returns True, else False.
        """
        results = []
        for l in range(len(self._view)):
            for w in range(len(self._view[l])):
                results.append(f([l, w]))
        return any(results)
    
p = minesweeper.Minefield(10,10,10)
s = Solver(p)
s.solve()
s.print_view()