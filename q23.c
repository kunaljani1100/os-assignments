#include<stdio.h>
#include<unistd.h>
#include<sys/types.h>
#include<fcntl.h>
void main(){
	char buffer[100];
	int fd = open("file.txt",O_RDONLY);
	lseek(fd,3,SEEK_SET);
	read(fd,&buffer,4);
	printf("%s",buffer);
}
