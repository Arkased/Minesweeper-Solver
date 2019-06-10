# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:11:14 2018

@author: kevin
"""

import numpy as np
from tile import Tile, Test_Tile
from csv import reader
from utils import get_adjacent_coords, print_grid

class Minefield:
    def __init__(self, length, width, num_mines):
        self._grid = [[Tile() for _ in range(width)] for _ in range(length)]
        self._l = length
        self._w = width
        self._game_ongoing = True
        self._num_remaining = length * width - num_mines
        
        # Generate mines
        tiles = []
        for w in range(width):
            for l in range(length):
                tiles.append([l,w])
        indecies = np.random.choice(len(tiles), num_mines, False)
        mine_coords = [tiles[index] for index in indecies]
        for coords in mine_coords:
            l, w = coords
            self._grid[l][w].is_mine = True
            self._count_adjacent_mines([l, w])
            
    def __repr__(self):
        return repr(self._grid)
    
# =============================================================================
# Interfaces    
# =============================================================================
    
    def reveal_tile(self, coords, first = True, recur = True):
        length, width = coords
        tile = self._grid[length][width]
        is_mine = tile.reveal()
        if is_mine:
            self._lose_game()
        # If revealed tile has no adjacent mines, reveal all non-revealed adjacent mines
        elif tile.num_adjacent == 0:
            for coords in get_adjacent_coords(self._grid, [length, width]):
                l = coords[0]
                w = coords[1]
                if not self._grid[l][w].is_revealed and recur:
                    self.reveal(l, w, False)
        
        if is_mine == False: # and != None
            self._num_remaining -= 1
            if not self._num_remaining:
                self._win_game()
                
        return self.inspect_tile(coords)
            
    def inspect_tile(self, coords):
        return str(self._grid[coords[0]][coords[1]])
            
    def get_player_grid_view(self):
        return [[str(tile) for tile in row] for row in self._grid]
    
# =============================================================================
# Getters
# =============================================================================
    
    def get_game_ongoing(self):
        return self._game_ongoing
    
    def get_l(self):
        return self._l
    
    def get_w(self):
        return self.w
    
    def get_num_remaining(self):
        return self._num_remaining
    
# =============================================================================
# Game Control
# =============================================================================
    
    def _lose_game(self):
        self._game_ongoing = False
        print('lost')
        
    def _win_game(self):
        self._game_ongoing = False
        print('won')
        
    
# =============================================================================
# Printing to Console
# =============================================================================
    
    def _get_all_grid_view(self):
        """
        For debugging only.
        """
        return [[tile.test_str() for tile in row] for row in self._grid]
        
    def _print_all(self):
        """
        For debugging only.
        """
        print_grid(self.all_view())

    def _print_player_view(self):
        print_grid(self.get_player_grid_view())
            
    
            
# =============================================================================
# Utils
# =============================================================================
        
    def _get_adjacent_tiles(self, coords):
        tiles = []
        l, w = coords
        for length in range(max([l - 1, 0]), min([l + 2, self._l])):
            for width in range(max([w - 1, 0]), min([w + 2, self._w])):
                tiles.append([length, width])
        tiles.remove([l, w])
        return tiles
    
    def _count_adjacent_mines(self, coords = None):
        """
        Updates the number of mines adjacent to given coords, or all mines if
        no coords are given.
        """
        if not coords:
            for l in range(self._l):
                for w in range(self._w):
                    self._count_adjacent_mines([l, w])
        else:
            l, w = coords
            if self._grid[l][w].is_mine:
                for tile_coords in get_adjacent_coords(self._grid, [l, w]):
                    length = tile_coords[0]
                    width = tile_coords[1]
                    self._grid[length][width].num_adjacent += 1
    
        
class Testfield(Minefield):
    def __init__(self, inp):
        """
        Generates a Minefield based on a passed 2-D array of codes or filename.
        """
        try:
            with open(inp, newline = '') as csvfile:
                code_grid = list(reader(csvfile))
        except:
            pass
        
        assert type(code_grid) == list
        
        self._l = len(code_grid)
        self._w = len(code_grid[0])
        
        num_not = 0
        # Generate grid from code_grid
        self._grid = []
        for row in code_grid:
            assert len(row) == self._w
            out = []
            for code in row:
                if code == '*' or code == '@' or code == 'a' or code == ' ':
                    num_not += 1
                out.append(Test_Tile(code))
            self._grid.append(out)
            
        self._game_ongoing = True
        self._num_remaining = self._l * self._w - num_not
        
        self._count_adjacent_mines()
        