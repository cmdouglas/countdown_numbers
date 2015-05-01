# Countdown Numbers Solver

Requirements: Python 3.4 + 

Usage: python3 countdown_nubers.py <numbers> -g <goal> [-t <tolerance>]

examples:

	$ python3 countdown_numbers.py 25 50 75 100 3 6 -g 952
	100 + 3 = 103
	75 * 6 = 450
	450 / 50 = 9
	103 * 9 = 927
	25 + 927 = 952

	Solution: 25 + (100 + 3) * 75 * 6 / 50 = 952

	$ python3 countdown_numbers.py 25 50 75 100 3 6 -g 962
	No solution.

	$ python3 countdown_numbers.py 25 50 75 100 3 6 -g 962 -t 1
	75 + 3 = 78
	100 * 6 = 600
	600 / 50 = 12
	78 * 12 = 936
	25 + 936 = 961

	Solution: 25 + (75 + 3) * 100 * 6 / 50 = 961
	(1 away)
