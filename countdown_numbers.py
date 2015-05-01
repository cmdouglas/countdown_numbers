#! /usr/bin/env python3
import random
import argparse
from itertools import combinations

from biae import BinaryIntegerArithmeticExpression as E
from search import SearchNode, AStarSearch


def get_result(n1, n2, operator):
    if operator == '+':
        result = n1 + n2
    elif operator == '-':
        result = n1 - n2
    elif operator == '*':
        result = n1 * n2
    elif operator == '/':
        result = int(n1 / n2)

    return result


class CountDownNumbersException(Exception):
    pass


class CountDownNumbers:
    def __init__(self, numbers, goal):
        self.numbers = numbers
        self.goal = goal

    def find_solution(self, tolerance=0):
        def _id(node):
            numbers = node.data['numbers']
            return tuple(sorted(numbers))

        def is_goal(node):
            numbers = node.data['numbers']
            for number in numbers:
                if abs(number - self.goal) <= tolerance:
                    return True

            return False

        def heuristic(node):
            numbers = node.data['numbers']
            diffs = [abs(n - self.goal) for n in numbers]
            return min(diffs)

        def possible_moves(node):
            numbers = node.data['numbers']
            moves = []
            for (n1, n2) in combinations(numbers, 2):

                moves.append((n1, '*', n2))
                moves.append((n1, '+', n2))

                # disallow fractions
                if n2 != 0 and n1 % n2 == 0:
                    moves.append((n1, '/', n2))

                if n1 != 0 and n2 % n1 == 0:
                    moves.append((n2, '/', n1))


                # disallow negative numbers
                if n1 >= n2:
                    moves.append((n1, '-', n2))
                else:
                    moves.append((n2, '-', n1))

            return moves

        def apply_move(node, move):
            n1, operator, n2 = move
            numbers = node.data['numbers'][:]
            numbers.remove(n1)
            numbers.remove(n2)

            result = get_result(n1, n2, operator)

            numbers.append(result)
            data = {
                'numbers': numbers
            }

            return SearchNode(data, _id, possible_moves, apply_move)

        data = {
            'numbers': self.numbers
        }

        start_node = SearchNode(data, _id, possible_moves, apply_move)

        search = AStarSearch(start_node, is_goal, heuristic)

        path = search.do_search()

        if not path:
            raise CountDownNumbersException("No path found.")

        return path, self.moves_to_expression(path)

    def moves_to_expression(self, moves):

        def extract_expression(expressions, val):
            to_extract = None
            for e in expressions:
                if e.value == val:
                    to_extract = e
                    break
            expressions.remove(to_extract)
            return to_extract

        expressions = [E(n) for n in self.numbers]
        for move in moves:
            n1, op, n2 = move
            e1 = extract_expression(expressions, n1)
            e2 = extract_expression(expressions, n2)

            result = E(op1=e1, op2=e2, o=op)
            expressions.append(result)

        mindiff, expression = min([
            (abs(e.value-self.goal), e) for e in expressions
        ])

        return expression


def report_path(path):
    for move in path:
        n1, operator, n2 = move

        print("{n1} {operator} {n2} = {val}".format(
            n1=n1,
            n2=n2,
            operator=operator,
            val=get_result(n1, n2, operator)
        ))


def generate_problem(nlarge=1):
    assert 0 <= nlarge <= 4
    nsmall = 6 - nlarge

    large = [25, 50, 75, 100]
    small = 2 * list(range(1, 11))

    numbers = random.sample(large, nlarge) + random.sample(small, nsmall)
    goal = random.randrange(101, 1000)

    return numbers, goal


def main():
    parser = argparse.ArgumentParser(description="Countdown numbers solver.")
    parser.add_argument(
        "numbers",
        type=int,
        nargs='*',
        help="the numbers used to find the goal"
    )
    parser.add_argument(
        "-g",
        "--goal",
        type=int,
        nargs="?",
        default=-1,
        help="the goal"
    )
    args = parser.parse_args()

    numbers = args.numbers
    goal = args.goal

    if (not numbers) and (goal == -1):
        numbers, goal = generate_problem(
            nlarge=random.randrange(0, 5)
        )

    c = CountDownNumbers(numbers, goal)
    tolerance = 0
    success = False

    while not success:
        print(
            "Trying to reach {g} with numbers {n} and tolerance {t}\n".format(
                n=numbers,
                g=goal,
                t=tolerance
            )
        )

        try:
            path, expression = c.find_solution(tolerance)
            report_path(path)
            print("\nSolution: {e} = {v}".format(
                e=expression, v=expression.value
            ))

            error = abs(expression.value - c.goal)
            if error > 0:
                print("({error} away)".format(error=error))

            success = True

        except CountDownNumbersException:
            print("No solution.")
            tolerance += 1

if __name__ == '__main__':
    main()
