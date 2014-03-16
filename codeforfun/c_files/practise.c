#include "stdio.h" 
#include "string.h"
#include "malloc.h"
#include "time.h"

char src[]={"abcdefghijklmnoqprstuvwxyz0123456789!@#$%^&*()-=_+"};
static char temp[10];
static char input[10];

int main(int argc, char *argv[])
{
    int i;
    printf("function :\n");
    printf("input some str shown to you.\n");
    printf("when you tired of doing is, type quit to exit.\n");
    printf("\n\n");
    do {
        srand(time(NULL));
        for (i = 0; i <10 ; ++i)
        {
            int r=rand()%strlen(src);
            temp[i]=src[r];
        }
        printf("please input this str :");
        for (i = 0; i <10 ; ++i)
        {
            printf("%c",temp[i]);
        }
        printf("\n\n");
        scanf("%s",input);
        printf("\n");
        if(strncmp(input,temp,10)==0) {
            printf("input completely correct \n\n");
        }
        else if (0==strcmp(input,"quit")) {
            printf("have a nice day and goodbye \n");
        }else{
            printf("input  has some error \n\n");
        }
    } while(strcmp(input,"quit"));
    return 0;
}
