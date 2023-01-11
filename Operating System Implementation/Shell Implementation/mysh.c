#include "kernel/types.h"
#include "kernel/fcntl.h"
#include "user/user.h"
#include "stddef.h"

int arraylen(char** a);
int count_char(char c, char** a);
int count_char_in_string(char c, char* a);
void runcmd(char** args);

char* strcat(char* first, const char* second) {
  char* end_of_first = first + strlen(first);
  for(int i = 0; i < strlen(second); i++) {
    *end_of_first++ = second[i];
  }
  *end_of_first = '\0';
  return first;
}


char* special = "<>|;";

char** getargs (char* input) {
  int speech_flag = 0;
  int number_of_args = 0;
  char** args = (char**)malloc(sizeof(char)*1024);
  char* temp_args = (char*)malloc(sizeof(char)*100);
  for (int i = 0; i < strlen(input); i++) {
    if (speech_flag  == 0) {
      if (input[i] == 34) {
        speech_flag = 1;
      } else if (input[i] != 32 && strchr(special, input[i]) == NULL) {
        char a[2];
        a[0] = input[i];
        a[1] = '\0';
        strcat(temp_args, a);
        if(i == strlen(input)-2) {
          args[number_of_args] = (char*)malloc(sizeof(char)*strlen(temp_args));
          strcpy(args[number_of_args], temp_args);
          memset(temp_args, 0, sizeof(char)*100);
        }
      } else if (strchr(special, input[i]) != NULL) {
        if(input[i-1] != 32 && input[i+1] != 34 && input[i-1] != 34) {
          args[number_of_args] = (char*)malloc(sizeof(char)*strlen(temp_args));
          strcpy(args[number_of_args], temp_args);
          memset(temp_args, 0, sizeof(char)*100);
          number_of_args++;
        }
        char a[2];
        a[1] = '\0';
        a[0] = input[i];
        strcat(temp_args, a);
        if (strchr(special, input[i+1]) == NULL && input[i+1] != 32) {
          args[number_of_args] = (char*)malloc(sizeof(char)*strlen(temp_args));
          strcpy(args[number_of_args], temp_args);
          memset(temp_args, 0, sizeof(char)*100);
          number_of_args++;
        }
      } else if (input[i] == 32) {
        if(input[i-1] != 32 && input[i-1] != 34) {
          args[number_of_args] = (char*)malloc(sizeof(char)*strlen(temp_args));
          strcpy(args[number_of_args], temp_args);
          memset(temp_args, 0, sizeof(char)*100);
          number_of_args++;
        }
        for (int j = 1; j < strlen(input)-i; j++) {
          if (input[i+j] != 32) {
            if (strchr(special, input[i+j]) == NULL) {
              i += (j-1);
              break;
            } else {
              i += (j-1);
              break;
            }
          }
        }
      }
    } else {
      if (input[i] != 34) {
        char a[2];
        a[0] = input[i];
        a[1] = '\0';
        strcat(temp_args, a);
      } else if (i == strlen(input)-2) {
        args[number_of_args] = (char*)malloc(sizeof(char)*strlen(temp_args));
        strcpy(args[number_of_args], temp_args);
        memset(temp_args, 0, sizeof(char)*100);
        continue;
      }else {
        speech_flag = 0;
        if (input[i+1] == 32) {
          args[number_of_args] = (char*)malloc(sizeof(char)*strlen(temp_args));
          strcpy(args[number_of_args], temp_args);
          memset(temp_args, 0, sizeof(char)*100);
          number_of_args++;
        }
      }
    }
  }
  return args;
}

 void runcmd(char** args) {
  if(count_char('|', args) > 0) {
    int p[2];
    pipe(p);
    char** left = (char**)malloc(sizeof(char)*1024);
    char** right = (char**)malloc(sizeof(char)*1024);
    int left_count = 0;
    int right_count = 0;
    int right_flag = 0;
    for(int i = 0; i < arraylen(args); i++) {
      if(strcmp(args[i], "|") == 0 && right_flag == 0) {
          right_flag = 1;
          continue;
        }
      if (right_flag == 1) {
        right[right_count] = (char*)malloc(sizeof(char)*strlen(args[i]));
        strcpy(right[right_count], args[i]);
        right_count++;
      } else {
        left[left_count] = (char*)malloc(sizeof(char)*strlen(args[i]));
        strcpy(left[left_count], args[i]);
        left_count++;
      }
    }
    if (fork() == 0) {
      close(1);
      dup(p[1]);
      close(p[0]);
      close(p[1]);
      if(left[0][0] != '/') {
        char forward[2];
        forward[0] = '/';
        forward[1] = '\0';
        strcat(forward, left[0]);
        strcpy(left[0], forward);
      }
      runcmd(left);
      exit(0);
    } else if (count_char('|', right) != 0 || count_char('>', right) != 0 || count_char('<', right) == 0) {
      if (fork() == 0) {
        close(p[1]);
        close(0);
        dup(p[0]);
        close(p[0]);
        if(right[0][0] != '/'){
          char forward[2];
          forward[0] = '/';
          forward[1] = '\0';
          strcat(forward, right[0]);
          strcpy(right[0], forward);
        }
        runcmd(right);
        exit(0);
      }
    } else {
      if(fork() == 0) {
        runcmd(right);
        exit(0);
      }
    }
    close(p[0]);
    close(p[1]);
    wait(0);
    wait(0);
  } else if(count_char('>', args) > 0 || count_char('<', args) > 0) {
    int tempcount = 0;
    char** temp = (char**)malloc(sizeof(char)*100);
      for (int i = 0; i < arraylen(args); i++) {
        if (strcmp("<", args[i]) == 0) {
          close(0);
          open(args[arraylen(args)-1], O_RDWR);
          if(temp[0][0] != '/'){
            char forward[2];
            forward[0] = '/';
            forward[1] = '\0';
            strcat(forward, temp[0]);
            strcpy(temp[0], forward);
          }
          exec(temp[0], temp);
        } else if (strcmp(">", args[i]) == 0) {
          close(1);
          open(args[arraylen(args)-1], O_TRUNC | O_CREATE | O_RDWR);;
          if(temp[0][0] != '/') {
            char forward[2];
            forward[0] = '/';
            forward[1] = '\0';
            strcat(forward, temp[0]);
            strcpy(temp[0], forward);
          }
          exec(temp[0], temp);
        } else {
          temp[tempcount] = (char*)malloc(sizeof(char)*strlen(args[i]));
          strcpy(temp[tempcount], args[i]);
          tempcount++;
        }

      }
      memset(temp, 0, sizeof(char)*100);
  } else {
    if (arraylen(args) == 0) {
      exit(0);
    }
    exec(args[0], args);
    printf("exec has failed\n");
    exit(0);
  }

}


void split_semi(char** args) {
  int number_semi = count_char(';', args);
  if(number_semi > 0) {
    int temp_counter = 0;
    char** temp_command = (char**)malloc(sizeof(char)*1024);
    for (int i = 0; i < arraylen(args); i++) {
      if (strcmp(args[i], ";") == 0) {
        if (fork() == 0) {
          runcmd(temp_command);
          exit(0);
        }
        temp_counter = 0;
        memset(temp_command, 0, sizeof(char)*1024);
      } else if (i == arraylen(args)-1) {
        temp_command[temp_counter] = (char*)malloc(sizeof(char)*100);
        strcpy(temp_command[temp_counter], args[i]);
        if (fork() == 0) {
          runcmd(temp_command);
          exit(0);
        }
      } else {
        temp_command[temp_counter] = (char*)malloc(sizeof(char)*100);
        strcpy(temp_command[temp_counter], args[i]);
        temp_counter++;
      }
      wait(0);
    }
  } else {
    runcmd(args);
    }
}

int count_char(char c, char** a) {
  int i = 0;
  int count = 0;
  char letter[2];
  letter[0] = c;
  letter[1] = '\0';
  while(a[i] != NULL) {
    if (strcmp(a[i], letter) == 0) {
      count++;
    }
    i++;
  }
  return count;
}

int count_char_in_string(char c, char* a) {
  int count = 0;
  for(int i = 0; i < strlen(a); i++) {
    if (a[i] == c) {
      count++;
    }
  }
  return count;
}


int arraylen(char** a) {
  int i = 0;
  int count = 0;
  while(a[i] != NULL) {
    count++;
    i++;
  }
  return count;
}


int main(int argc, char *argv[]) {
  while (1) {
    printf(">>> ");
    char* input = (char*)malloc(sizeof(char)*200);
    char** arguments = (char**)malloc(1024);
    read(0, input, 200);
    arguments = getargs(input);
    if(count_char_in_string(34, input) % 2 != 0) {
      printf("YOU MUST CLOSE YOUR SPEECH MARKS\n");
      continue;
    }
    if (strcmp(arguments[0], "cd") == 0) {
     chdir(arguments[1]);
   } else if (strcmp(arguments[0], "quit") == 0) {
      exit(0);
   } else if (fork() == 0 ){
      split_semi(arguments);
      exit(0);
    }
    wait(0);
    memset(arguments, 0, 1024);
    memset(input, 0, sizeof(char)*200);
  }
  exit(0);
}
