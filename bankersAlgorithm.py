import os
import inputModule	
import initializationModule

# This function implements the banker's algorithm. It accepts the number of processes and the number of different types of resources as the input, and accepts the required
# matrices which are the allocation matrix that represents the resources of each type allocated to each process, the maxNeed matrix that represents the number of resources
# of each type needed by each process, and the totalAvailable matrix that represents the total number of resources of each type that is available for each user. Based on
# these inputs, a recursive algorithm is detected whether the allocation state is safe or unsafe and we also keep track of the order of the processes by using a list.

def bankersAlgorithm():

	# Input the number of processes and the number of different types of resources.
	numProcesses = int(input('Enter the number of processes:'))
	numResources = int(input('Enter the number of different types of resources:'))

	# Keep track of the processes that have been completed.
	processCompleted = []

	# Allocation matrix provided as input by the user.
	allocation = inputModule.inputAllocationMatrix(numProcesses, numResources)
	
	# The maxNeed matrix represents the number of resuources of each type required for each process to proceed to completion.
	maxNeed = inputModule.inputMaxNeedMatrix(numProcesses, numResources)
		
	# The totalAvailable matrix represents the total number of resources of each type available on the system.
	totalAvailable = inputModule.inputTotalAvailableMatrix(numResources)

	# Recursively iterate and implement the banker's algorithm to detect if an unsafe state is possible.
	while True:
		
		# Compute the total number of resources used of each type by adding the values of vertical columns in the allocation matrix.
		totalUsed = initializationModule.initializeTotalUsedMatrix(numResources, numProcesses, allocation)
		
		# Subtract the totalUsed matrix from the totalAvailable matrix to compute the number of resources used for each process.
		remainingAvailable = initializationModule.initializeRemainingAvailableMatrix(totalAvailable, totalUsed)

		# Computer the number of remaining resources of each type needed by each process to proceed to completion.
		remainingNeed = initializationModule.initializeRemainingNeed(numProcesses, numResources, maxNeed, allocation)

		deadlockOccurs = True

		# Compare the remainingNeed matrix with each process of the remainingAvailable matrix and check whether the state is safe or unsafe.		
		for i in range(numProcesses):
			if i not in processCompleted:
				processCanProceed = True
				safeStateDetected = False
				for j in range(numResources):
					if remainingNeed[i][j] > remainingAvailable[j]:
						processCanProceed = False
						break
				if(processCanProceed):
					safeStateDetected = True
					processCompleted.append(i)
					for j in range(numResources):
						remainingAvailable[j] += allocation[i][j]
					for j in range(numResources):
						allocation[i][j] = 0
					deadlockOccurs = False

		# If a deadlock does not occur, then we check if all the processes are completed, else we continue iteration.
		if(not deadlockOccurs):
			if len(processCompleted) == numProcesses:
				break
		
		# Otherwise, if a deadlock is detected, we quit declaring that the state is unsafe.
		else:
			print('Unsafe state')
			break			

	# If the length of the list is equal to the number of processes, we conclude that the safe is safe.
	if(numProcesses == len(processCompleted)):
		print('Safe state')

	# Finally, we print the sequence of processes that are completed.
	print('Process sequence:',end = " ")
	for process in processCompleted:
		print(process,end = " ")

	print('\n')

if __name__ == '__main__':
	bankersAlgorithm()

