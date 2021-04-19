import os
import signal
import sys
import executeCommand


# This function reads a command of white space separated words from the user and splits the command into a list of words. 

def readCommand():
	commandLine = input()
	parameters = commandLine.split()
	command = parameters[0]
	return command, parameters


#This function is used to let the user know that the shell is ready to accept the command to the user.

def typePrompt():
	print(" sh >", end = " ")


# This function is used to catch the interrupt signal from the user and let the user know what a particular signal number was sent.

def receiveSignal(signalNumber, frame):
	print("You sent signal " + str(signalNumber) + ".")


# This function is used to exit the shell, when a user enters "quit", the shell will terminate.

def exitShell():
	sys.exit()


# This is the function to start the shell. It does not stop running unless the user enters the 'quit' command.

def startShell(newenv):
	while True:
		typePrompt()
		command, parameters = readCommand()
		
		# If the quit command is entered, the shell will terminate.
		if command == 'quit':
			exitShell()
		
		# Count the number of symbol occurences. We are not considering commands that have more than one symbol.
		countSymbols = 0
		symbols = ['<','>','|','&']
		locations = []
		location = 0
		for symbol in parameters:
			if symbol in symbols:
				countSymbols += 1
				locations.append(location)
			location += 1
		
		# We check if the symbols are located appropriately. If they are not located appropriately, then the command will not be executed.
		if 0 in locations or (len(parameters) - 1 in locations and parameters[len(parameters) - 1] != '&'):
			print(command + " : bad command")

		else:
				
			# Check for the condition and execute the command or return an error to the user based on the number of symbols in the list of parameters.
			if countSymbols <= 1:
				executeCommand.checkCommandTypeAndExecute(command, parameters, newenv)
			else:
				print(command + " : bad command.")


# This is the main function of the code, it gets the system environment, registers the interrupt signal and instructs the shell to run the recieveSignal handler when the
# SIGINT signal is sent (using the kill function or the when ctrl+c is pressed by the user). Once the signal handler is registered for SIGINT, the shell is initialized.

if __name__ == "__main__":
	newenv = os.environ.copy()
	signal.signal(signal.SIGINT,receiveSignal)
	startShell(newenv)

			
