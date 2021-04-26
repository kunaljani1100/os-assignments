#include<stdio.h>
#include<unistd.h>
#include<sys/types.h>
#include<fcntl.h>
#include<sys/wait.h>
#include<stdlib.h>
#include<string.h>

#define TRUE 1

void type_prompt(){
	printf("sh>>");
}

char **read_command(char *command){
	char **parameters;
	//printf("%s",command);
	int i = 0;
	int word = 0;
	int j = 0;
	/***
	while(command[i] != '\0'){
		if(command[i] != ' '){
			parameters[word][j++] = command[i];
		}
		else{
			word++;
			j = 0;
		}
	}
	***/
	return parameters;
}

void main(){
	while(TRUE){
		int status;
		char *command;
		char **parameters;
		type_prompt();
		scanf("%s",command);
		//parameters = read_command(command);
		//printf("%s",parameters[0]);
		if(fork() != 0){
			waitpid(-1,NULL,0);
		}
		else{
			execve(command,parameters,0);
		}
	}
}
