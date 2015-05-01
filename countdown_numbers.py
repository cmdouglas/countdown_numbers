#! /usr/bin/env python3

import argparse
from itertools import combinations
from biae import BinaryIntegerArithmeticExpression as E
from search import SearchNode, AStarSearch

class CountDown:
    
    def __init__(self, numbers, goal):
        self.numbers = numbers
        self.goal = goal
        
    def find_solution(self, tolerance=0):
        def _id(node):
            expressions = node.data['expressions']
            expressions = sorted(expressions, key=lambda e: e.value)
            return ";".join([str(e) for e in expressions])
            
        def is_goal(node):
            expressions = node.data['expressions']
            for e in expressions:
                if abs(e.value - self.goal) <= tolerance:
                    return True
            
            return False
            
        def heuristic(node):
            expressions = node.data['expressions']
            diffs = [abs(e.value - self.goal) for e in expressions]
            return min(diffs)
            
        def possible_moves(node):
            expressions = node.data['expressions']
            moves = []
            for (op1, op2) in combinations(expressions, 2):
                moves.extend([
                    (op1, '+', op2, op1.value + op2.value),
                    (op1, '*', op2, op1.value * op2.value),
                    (op1, '-', op2, op1.value - op2.value),
                    (op2, '-', op1, op2.value - op1.value)
                ])
                
                
                if op2.value > 0 and op1.value % op2.value == 0:
                    moves.append((op1, '/', op2, int(op1.value / op2.value)))
                    
                if op1.value > 0 and op2.value % op1.value == 0:
                    moves.append((op2, '/', op1, int(op2.value / op1.value)))
                    
            return moves
            
        def apply_move(node, move):
            op1, operator, op2, value = move;
            expressions = node.data['expressions'][:]
            expressions.remove(op1)
            expressions.remove(op2)
            
            new_expression = E(op1=op1, op2=op2, o=operator)
            expressions.append(new_expression)
            data = {
                'expressions': expressions
            }
            
            return SearchNode(data, _id, possible_moves, apply_move)
            
        expressions = []
        for number in self.numbers:
            expressions.append(E(number))
            
        data = {
            'expressions': expressions
        }
        
        start_node = SearchNode(data, _id, possible_moves, apply_move)
        
        search = AStarSearch(start_node, is_goal, heuristic)
        
        path = search.do_search()
        
        if not path:
            return "No solution found"
        
        for move, node in path:
            op1, operator, op2, value = move
            print ("{op1} {operator} {op2} = {val}".format(
                op1=op1.value,
                op2=op2.value,
                operator=operator,
                val=value
            ))
        
        
        for e in node.data['expressions']:
            if abs(e.value - self.goal) <= tolerance:
                return e
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", type=int, nargs='+')
    parser.add_argument("-g", "--goal", type=int)
    args = parser.parse_args()
    
    c = CountDown(args.numbers, args.goal)
    print(c.find_solution())
        
            