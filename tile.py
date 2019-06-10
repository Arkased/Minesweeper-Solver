# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 22:00:41 2019

@author: kevin
"""

class Tile():
    def __init__(self):
        self.num_adjacent = 0
        self.is_revealed = False
        self.is_mine = False
        self.was_triggered = False
        
    def reveal(self):
        """
        Reveals the mine, returns whether a mine was revealed, None if mine
        was already revealed
        """
        if not self.is_revealed:
            self.is_revealed = True
            if self.is_mine:
                self.was_triggered = True
                return True
            else:
                return False
        
    def test_str(self):
        if self.is_mine:
            if self.was_triggered:
                return '@'
            else:
                return '*'
        elif not self.num_adjacent:
            if self.is_revealed:
                return ' '
            else:
                return '_'
        else:
            return str(self.num_adjacent)
        
    def __str__(self):
        if self.is_revealed:
            if self.is_mine:
                return '*'
            elif not self.num_adjacent:
                return ' '
            else:
                return str(self.num_adjacent)
        else:
            return 'X'
        
class Test_Tile(Tile):
    def __init__(self, code):
        super().__init__()
        if code == '_' or code == '':
            return
        elif code == '*' or code == 'a':
            self.is_mine = True
        elif code == ' ':
            self.is_revealed = True
        else:
            raise TypeError('invalid code: ' +  str(code))
        
