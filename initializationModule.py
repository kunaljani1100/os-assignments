# Compute the number of resources used of each type.

def initializeTotalUsedMatrix(numResources, numProcesses, allocation):
	totalUsed = []

	for i in range(numResources):
		total = 0
		for j in range(numProcesses):
			total += allocation[j][i]
		totalUsed.append(total)
	
	return totalUsed
	
# Compute the number of resources each type that is available to the user.

def initializeRemainingAvailableMatrix(totalAvailable, totalUsed):
	remainingAvailable = []

	for i in range(len(totalUsed)):
		remainingAvailable.append(totalAvailable[i] - totalUsed[i])

	return remainingAvailable

# Compute the number of remaining resources that is needed by each user.
	
def initializeRemainingNeed(numProcesses, numResources, maxNeed, allocation):
	remainingNeed = []

	for i in range(numProcesses):
		remainingNeedForProcess = []
		for j in range(numResources):
			remainingNeedForProcess.append(maxNeed[i][j] - allocation[i][j])
		remainingNeed.append(remainingNeedForProcess)
		
	return remainingNeed
