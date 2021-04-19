import os
import signal
import sys
	
# This function will redirect the input to a location in file instead of accepting the user's input from the console.

def redirectInputAndExecute(command, parameters, newenv):

	# We find the location of the symbol to redirect the input. The file name where the input is redirected is generally located in the index immediately
	# ahead of the location of the redirect symbol.
	redirectLocation = parameters.index('>')
	fileName = parameters[redirectLocation + 1]
	parameters = parameters[0:redirectLocation]
	pid = os.fork()
	
	# If the process is a parent process, we wait for the child process to finish input redirection execution.
	if(pid != 0):
		try:
			os.waitpid(pid, 0)
		except KeyboardInterrupt:
			os.kill(pid,signal.SIGINT)
	
	# If the process is a child process, then we use a file descriptor to redirect the input so that input can be accepted from a particular file.
	else:
		fd = os.open(fileName,os.O_RDONLY | os.O_CREAT)
		os.dup2(fd, 0)
		try:
			os.execvpe(command, parameters, newenv)
		except Exception:
			print(command + ": bad command")
			os._exit(-1)

	
# This function will redirect the output to a location in file instead of writing the output to the console.	
	
def redirectOutputAndExecute(command, parameters, newenv):

	# We find the location of the symbol to redirect the output. The file name where the input is redirected is generally located in the index immediately
	# ahead of the location of the redirect symbol.
	redirectLocation = parameters.index('<')
	fileName = parameters[redirectLocation + 1]
	parameters = parameters[0:redirectLocation]
	pid = os.fork()
	
	# If the process is a parent process, we will wait until the child process has finished writing to the file.
	if(pid != 0):
		try:
			os.waitpid(pid, 0)
		except KeyboardInterrupt:
			os.kill(pid,signal.SIGINT)
			
	# If the process is a child process, then we use a file descriptor to redirect the output so that the output can be written to a particular file.
	else:
		fd = os.open(fileName,os.O_WRONLY | os.O_CREAT)
		os.dup2(fd, 1)
		try:
			os.execvpe(command, parameters, newenv)
		except Exception:
			print(command + ": bad command")
			os._exit(-1)



# This function will run the background job when it detects '&' character as the last word in the command line. 		
		
def runBackgroundJob(command, parameters, newenv):
	
	pid = os.fork()
	
	# Remove the '&' command from the list of parameters.
	parameters = parameters[0:len(parameters) - 1]
	
	# If the process is a child process, we execute the process directly execute the command. If the process is a parent process, we will not wait for
	# the child process to complete execution.
	if(pid == 0):
		try:
			os.execvpe(command, parameters, newenv)
		except Exception:
			print(command + ": bad command")
			os._exit(-1)



# This function enables the use of pipe. The standard output as well as the standard input are redirected when pipes are used.

def usePipeAndExecute(command, parameters, newenv):
	
	# Get the location of the '|' symbol
	pipeLocation = parameters.index('|')
	
	# The descriptor for reading and writing to the pipe are initialized using the pipe() function.
	r, w = os.pipe()
	
	# Get the command from the left of the '|' symbol that writes to the pipe.
	writeParameters = parameters[0:pipeLocation]
	
	# Get the command from the right of the '|' symbol that reads from the pipe.
	readParameters = parameters[pipeLocation + 1:len(parameters)]
	pid = os.fork()
	
	# If the process is not a child process, then a second level child process is created from the first level child process after closing the write descriptor.
	if(pid != 0):
		try:
			os.close(w)
			os.waitpid(pid,0)
			pid2 = os.fork()
			
			# If the process is not a first level or second level child process, then it waits until the reading from pipe is completed.
			if(pid2 != 0):
				try:
					os.waitpid(pid2,0)
				except KeyboardInterrupt:
					os.kill(pid2, signal.SIGINT)
			
			# If the process is a second level child process, then it will read the contents of the pipe and execute the requored instruction.
			# The read process is blocked when a write is being made to the pipe.
			else:
				os.dup2(r, 0)
				try:
					os.execvpe(readParameters[0], readParameters, newenv)
				except Exception:
					print(command + ": bad command")
					os._exit(-1)

				
		except KeyboardInterrupt:
			os.kill(pid,signal.SIGINT)
	
	# If the process is a child process, we close the read descriptor and redirect the write descriptor to the pipe.
	else:	
		os.close(r)
		os.dup2(w, 1)
		try:
			os.execvpe(command, writeParameters, newenv)
		except Exception:
			print(command + ": bad command")
			os._exit(-1)



# This function check the type of command whether it is an input redirect, output redirect, pipe, background, or a regular command based on the symbols present in the
# parameters list.  

def checkCommandTypeAndExecute(command, parameters, newenv):
	
	# The '<' symbol is the symbol to redirect the output.
	if '<' in parameters:
		redirectOutputAndExecute(command, parameters, newenv)
		
	# The '>' symbol is the symbol to redirect the input.
	elif '>' in parameters:
		redirectInputAndExecute(command, parameters, newenv)
		
	# The '|' symbol indicates that 2 processes will communicate using pipes.
	elif '|' in parameters:
		usePipeAndExecute(command, parameters, newenv)	
	
	# The '&' symbol indicates that the process will be run as a background process, that means that the user can give commands as input while the process is 
	# running.
	elif '&' in parameters:
		runBackgroundJob(command, parameters, newenv)
	
	# If none of the symbols are present, we can run our command mormally.
	else:
	
		# We create a child process from the parent process.
		pid = os.fork()
		
		# If the process is not a child process, we wait for the child process to complete execution using waitpid(). In case a keyboard interrupt is 
		# caught while waiting for the child process to complete its task, then the SIGINT signal is sent to the child process, and the program would 
		# terminate under normal circunstances.
		if(pid != 0):
			try:
				os.waitpid(pid, 0)
			except KeyboardInterrupt:
				os.kill(pid,signal.SIGINT)
		
		# If the process is a child process, then the command is executed using execvpe() which does not return. During the execution of this command, the 
		# command is considered a bad command if the file corresponding to the command is not found. 
		else:
			try:
				os.execvpe(command, parameters, newenv)
			except Exception:
				print(command + ": bad command")
				os._exit(-1)
