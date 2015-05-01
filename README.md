# Countdown Numbers Solver

Requirements: Python 3.4 + 

Usage: python3 countdown_nubers.py [numbers -g goal]

If you omit numbers and goal, it will generate a random problem and solve it.

examples:

	$ python3 countdown_numbers.py 25 50 75 100 3 6 -g 952
	Trying to reach 952 with numbers [25, 50, 75, 100, 3, 6] and tolerance 0

	75 * 6 = 450
	100 + 3 = 103
	450 / 50 = 9
	103 * 9 = 927
	25 + 927 = 952

	Solution: 25 + (100 + 3) * 75 * 6 / 50 = 952

	$ python3 countdown_numbers.py 25 50 75 100 3 6 -g 962
	Trying to reach 962 with numbers [25, 50, 75, 100, 3, 6] and tolerance 0

	No solution.
	Trying to reach 962 with numbers [25, 50, 75, 100, 3, 6] and tolerance 1

	50 * 6 = 300
	100 / 25 = 4
	300 - 4 = 296
	3 * 296 = 888
	75 + 888 = 963

	Solution: 75 + 3 * (50 * 6 - (100 / 25)) = 963
	(1 away)
	
	$ python3 countdown_numbers.py
	Trying to reach 956 with numbers [25, 50, 8, 7, 5, 9] and tolerance 0

	25 * 8 = 200
	200 - 7 = 193
	5 * 193 = 965
	965 - 9 = 956

	Solution: 5 * (25 * 8 - 7) - 9 = 956