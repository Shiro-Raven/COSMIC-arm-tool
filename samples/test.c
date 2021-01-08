#include <stdio.h>

int square(int x){
	return x * x;
}

int factorial(int x){
	if(x == 0){
		return 1;
	}

	return x * factorial(x -1);
}

int main(){
	int x = 5;
	x = x + 5;
	int y = square(x);
	y = factorial(y);
	printf("%d\n", y);
	return 0;
}
