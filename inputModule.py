# Accept the allocation matrix as user input.

def inputAllocationMatrix(numProcesses, numResources):
	print('Enter the allocation matrix:')
	allocation = []

	for i in range(numProcesses):
		processAllocation = []
		for j in range(numResources):
			processAllocation.append(int(input()))
		allocation.append(processAllocation)
	
	return allocation

# Accept the matrix for indicating the number of resources required for completion.
	
def inputMaxNeedMatrix(numProcesses, numResources):
	print('Enter the max need matrix:')
	maxNeed = []

	for i in range(numProcesses):
		maxProcessNeed = []
		for j in range(numResources):
			maxProcessNeed.append(int(input()))
		maxNeed.append(maxProcessNeed)
	
	return maxNeed

# Accept the input matrix indicating the number of resources available of each type.
		
def inputTotalAvailableMatrix(numResources):
	print('Enter the total availibility matrix:')
		
	totalAvailable = []

	for i in range(numResources):
		totalAvailable.append(int(input()))
		
	return totalAvailable
