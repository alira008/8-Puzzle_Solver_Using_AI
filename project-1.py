from math import sqrt, ceil, fabs
from sys import exit, argv
from puzzle import Puzzle
from sort import bubble_sort
from time import time
import multiprocessing

def main():
	#	Display the menu
	puzzle, algorithm_choice = menu()

	#	Find solution to the puzzle
	solution, _ = general_search(puzzle, algorithm_choice)

	if(type(solution) is not Puzzle):
		print (solution)

	return 0		

def general_search(problem, queuing_function):
	puzzles_tried = set()
	node_list = []
	total_nodes_count = 0
	loop_count = 0
	prev_gn = 0
	max_queue = 0
	goal = solved_puzzle(problem)

	node_list.append(problem)
	print("Expanding state")
	print(problem)
	puzzles_tried.add(tuple(problem.get_grid_1d()))

	#	Start timer
	start = time()
	while (1):
		if (len(node_list) == 0):
			return "Failure: Solution was not found"

		else:
			node = node_list.pop(0)

			if (node.is_solved(goal)):
				#	End timer
				end = time()
				print ("Goal!!!")
				print ("To solve this problem the search algorithm expanded a total of " + str(total_nodes_count) + " nodes.")
				print ("The maximum number of nodes in the queue at any one time was " + str(max_queue))
				print ("The depth of the goal node was " + str(node.get_gn()) + ".")
				print("Puzzle took {:.6f} seconds to find solution.".format(end-start))
				time_taken = end-start
				# print (puzzles_tried)
				return node, {"Total Nodes Expanded": total_nodes_count, "Max Nodes in Queue": max_queue, "Depth": node.get_gn(), "Time taken": round((end-start), 7)} 

			else:
				if(loop_count == 0):
					loop_count += 1
				elif (loop_count < 3):
					print("The best state to expand with a g(n) = " + str(node.get_gn()) + " and h(n) = " + str(node.get_heuristic()) + " is...")
					print(node)
					loop_count += 1

				#	Expand nodes
				temp_node_list, puzzles_tried = node.expand(puzzles_tried)
				#	Total nodes expanded
				total_nodes_count += len(temp_node_list)
				
				if(queuing_function == "Misplaced"):
					#	calculate the misplaced tiles of nodes
					for i in range(len(temp_node_list)):	
						calc_misplaced(temp_node_list[i], goal)
					#	Sort nodes by shortest f(n) = g(n) + h(n)
					# temp_node_list = bubble_sort(temp_node_list)
				elif(queuing_function == "Manhattan"):
					#	calculate the manhattan distances of nodes
					for i in range(len(temp_node_list)):	
						calc_manhattan(temp_node_list[i], goal)
					#	Sort nodes by shortest f(n) = g(n) + h(n)
					# temp_node_list = bubble_sort(temp_node_list)
				
				#	Append expanded nodes to the queue (node_list)
				for node in temp_node_list:
					node_list.append(node)
				#	Set the max number of elements in a queue
				if(max_queue < len(node_list)):
					max_queue = len(node_list)

				#	Sort nodes by shortest f(n) = g(n) + h(n)
				node_list = bubble_sort(node_list)

				#	Check if timer has gone over 15 minutes
				check_time = time() - start
				if (check_time > 1800.0):
					return "Failure: Went over 30 minutes.", {"Total Nodes Expanded": total_nodes_count, "Max Nodes in Queue": max_queue, "Depth": "Failure: not found", "Time taken": round((check_time), 7)} 

def calc_manhattan(problem, goal):
	grid = problem.get_grid()
	n = problem.get_size()
	gn = problem.get_gn()
	total_nums = (n*n)-1
	x_distance = 0
	y_distance = 0

	for num in range(1, total_nums):
		#	locate prev in goal node
		#	j is the row
		for j in range(n):
			#	i is the column
			for i in range(n):
				if (str(num) == goal[j][i]):
					goal_row = j
					goal_col = i

		#	locate prev in user node
		#	j is the row
		for j in range(n):
			#	i is the column
			for i in range(n):
				if (str(num) == grid[j][i]):
					row = j
					col = i

		x_distance += fabs(col - goal_col)
		y_distance += fabs(row - goal_row)
	problem.set_heuristic(x_distance + y_distance + gn)

def calc_misplaced(problem, goal):
	grid = problem.get_grid()
	n = problem.get_size()
	gn = problem.get_gn()
	misplaced_count = 0

	#	Check up until row n-1
	#	row is the row
	for row in range(n):
		#	col is the column
		for col in range(n):
			if (grid[row][col] != goal[row][col]):
				misplaced_count += 1

	#	Check last row until before the blank space
	for col in range(n-1):
		row = n-1
		if(grid[row][col] != goal[row][col]):
			misplaced_count += 1

	problem.set_heuristic(misplaced_count + gn)

def solved_puzzle(problem):
	puzzle = []
	n = problem.get_size()

	i = 1
	for rows in range(n):
		row = []
		for cols in range(n):
			row.append(str(i))
			i += 1
		puzzle.append(row)
	puzzle[n-1][n-1] = 'b'
	
	return puzzle

def menu():
	print ("Welcome to Ariel Lira's 8-puzzle solver for CS 170: Intro to AI")
	puzzle_choice = input('Type “1” to use a default puzzle, or “2” to enter your own puzzle. ')
	puzzle = get_user_puzzle(int(puzzle_choice))

	print ("\tEnter your choice of algorithm")
	print ("\t\t1. Uniform Cost Search")
	print ("\t\t2. A* with the Misplaced Tile heuristic.")
	print ("\t\t3. A* with the Manhattan distance heuristic.")
	algorithm_choice = input()

	if (algorithm_choice == '1'):
		algorithm_choice = "Uniform"
	elif (algorithm_choice == '2'):
		algorithm_choice = "Misplaced"
	else:
		algorithm_choice = "Manhattan"

	return puzzle, algorithm_choice

def get_user_puzzle(choice):

	if (choice == 1):
		default_puzzle = [['1', '2', '3'], ['4', '8', 'b'], ['7', '6', '5']]

		ret = Puzzle(default_puzzle)
	else:
		#	grid arranged in rows and columns
		grid = []

		#	Get each row for the puzzle from the user
		print ("Enter your puzzle, use a zero to represent the blank")
		#	Ask user to input first row
		row = input("\tEnter row 1, use spaces or tabs between numbers\t\t")
		#	Check numbers from user
		row = row.split()

		#	Check the number of rows and columns needed for the puzzle
		n = len(row)
		#	Check the type of puzzle
		puzzle_type = (n * n) - 1

		#	Check if the row has a 0
		#	If one of the columns is a '0' change it to 'b'
		for i in range(n):
			if (row[i] == '0'):
				row[i] = 'b'
		#	Append the row to the puzzle grid
		grid.append(row)

		#	Ask the user to enter for the remaining of the puzzle
		for i in range(1, n):
			row = input("\tEnter row " + str(i+1) + ", use spaces or tabs between numbers\t\t")
			row = row.split()

			#	Check if user input the correct amount of numbers for each row
			if (len(row) != n):
				print("\nWrong amount of numbers entered for row")
				print("For a " + str(puzzle_type) + "-puzzle, there are " + str(n) + " rows and " +str(n) + " columns for each row.")
				exit(0)

			#	Check if the row has a 0
			#	If one of the columns is a '0' change it to 'b'
			for i in range(n):
				if (row[i] == '0'):
					row[i] = 'b'

			#	Add row to the grid
			grid.append(row)

		ret = Puzzle(grid)

	return ret

#	Function to rapidly get data from test cases and output the data into a txt file for easy reading later
def testing_data():
	test_puzzles = [
		[['1', '2', '3'], ['4', '5', '6'], ['7', '8', 'b']],
		[['1', '2', '3'], ['4', '5', '6'], ['b', '7', '8']],
		[['1', '2', '3'], ['5', 'b', '6'], ['4', '7', '8']],
		[['1', '3', '6'], ['5', 'b', '2'], ['4', '7', '8']],
		[['1', '3', '6'], ['5', 'b', '7'], ['4', '8', '2']],
		[['1', '6', '7'], ['5', 'b', '3'], ['4', '8', '2']],
		[['7', '1', '2'], ['4', '8', '5'], ['6', '3', 'b']],
		[['b', '7', '2'], ['4', '6', '1'], ['3', '5', '8']]
	]
	algorithm_choices = ["Uniform", "Misplaced", "Manhattan"]

	# Array of processes
	procs = []
	print_lock = multiprocessing.Lock()

	for algo_choice in algorithm_choices:
		for j in range(len(test_puzzles)):
			p = multiprocessing.Process(target=multi_proc_search, args=(Puzzle(test_puzzles[j]), algo_choice, print_lock, ))
			procs.append(p)

	# Start each process
	for p in procs:
		p.start()

	# Wait until each process finishes
	for p in procs:
		p.join()

	return 0

#	Function that is called by each process
def multi_proc_search(puzzle, algo_choice, lock):
	solution, data = general_search(puzzle, algo_choice)

	data["Algorithm"] = algo_choice + " algorithm"
	data = str(data)
	
	# Syncronize the processes when printing	
	lock.acquire()
	fd = open("./analyze_data2.txt", "a")
	fd.write(data + "\n")
	fd.close()
	lock.release()


if __name__ == '__main__':
	if len(argv) < 2:
		main()
	else:
		testing_data()

	exit()