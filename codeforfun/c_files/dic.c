#include "stdio.h"
#include "stdlib.h"
#include "string.h"

char src[]="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(),.?";

void show(char *str)
{
    printf("%s\n",str);
}

/*
 *Function that create a char array and return it
 */
char *getCharArray(char length)
{
    return (char*)malloc(sizeof(char)*length);
}

/*
 *Function that create a int array and return it
 */
int *getIntArray(int length)
{
    return (int*)malloc(sizeof(int)*length);
}


/*
 *print the code
 */
void showCode(int *array,int length)
{
    char *result=getCharArray(length);
    for(int i;i<length;i++)
    {
        result[i]=src[array[i]];
    }
    show(result);
}

int isdone(int  *array,int length)
{
    for(int i=0;i<length;i++)
    {
        if(array[i]!=(strlen(src)-1))
            return 1;
    }
    return 0;
}

/*
 *Function to generate a string 
 */
void getCode(int length)
{
    FILE *file;
    file=fopen("dic.dat","wr");
    if (file)
    {
        printf("successful open file dic.dat\n");
    }
    else
    {
        printf("error open file dic.dat\n");
        return ;
    }
    printf("creating dictionary\n");
    int *indexs=getIntArray(length);
    int count=0;
    //init array indexs
    for (int i = 0; i < length; ++i)
    {
        indexs[i]=-1;
    }

    while(isdone(indexs,length))
    {
        int pos=0;
        indexs[pos]++;
        if(indexs[pos]>strlen(src)-1)
        {
            do {
                indexs[pos]=0;
                pos++;
                indexs[pos]++;
            } while(indexs[pos]>strlen(src)-1);

        }
        else
        {
            char *result=getCharArray(length);
            for(int i=0;i<length;i++)
            {
                result[i]=src[indexs[i]];
            }
            fprintf(file,"%s\n",result);
        }

    }
    fclose(file);
    printf("dictionary create successful,date stored in dic.dat");
}

/*
 *this is main Function 
 */
int main(int argc, char *argv[])
{
    /*printf("Please input code max length:");*/
    /*scanf("%d",&length);*/
    int length=atoi(argv[1]);
    getCode(length);
    return 0;
}
