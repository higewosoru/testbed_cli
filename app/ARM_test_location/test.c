#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

#define MAX_DIR_LEN 255
#define MS_DELAY 5000 //delay for a few seconds to simulate a long program.

void rough_delay(int number_of_ms) 
{ 
    // Converting time into milli_seconds 
   // int milli_seconds = 1000 * number_of_seconds; 
  
    // Storing start time 
    clock_t start_time = clock(); 
  
    // looping till required time is not achieved 
    while (clock() < start_time + number_of_ms) {
        printf("Delaying: testestestestest"); 
    }
} 

static int list_dir (const char * dir_name)
{
    DIR * d;
    struct dirent *e;

    char parent[200];
    snprintf(parent, sizeof(parent), "%s/..", dir_name);
    d = opendir(parent);


    if (d == NULL) {
        printf("Unkown parent directory. \n");
	return -1;
    }

    printf("Parent Directory: %s \n",d);
    return 0;
}


int main(int argc, char *argv[]) {
  if (argc>1) {
    printf("Test file run w/ arg: %s \n", argv[1]);
    /*FILE* fp = fopen(argv[1], "r");
    fseek(fp, 0L, SEEK_END);
    size_t sz = ftell(fp);
    char *buffer = malloc((sz) * sizeof(char));
    rewind(fp);
    fread(buffer, sz, (sz/sizeof(char)), fp);
    printf("%s \n", buffer);
    free(buffer);*/
  }

  else {
    printf("Test file run without test file. \n");
  }

  //rough_delay(MS_DELAY);

  char dir_name[MAX_DIR_LEN];
  getcwd(dir_name, MAX_DIR_LEN);
  if (dir_name!=NULL) {
    printf("%s \n", dir_name);
  }
  else {
    printf("Couldn't get CWD. \n");
  }
  //list_dir(".");
  return 0;
}
