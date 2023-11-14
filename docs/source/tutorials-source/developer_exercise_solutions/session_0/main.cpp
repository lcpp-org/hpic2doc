#include "Fibonacci.hpp"

#include <vector>
#include <string>
#include <iostream>

int main(int argc, char *argv[]) {
    std::vector<std::string> args(argv, argv+argc);

    if (args.size() > 2) {
        std::cout << "Too many arguments provided!" << std::endl;
        return 1;
    }
    else if (args.size() < 2) {
        std::cout << "Too few arguments provided!" << std::endl;
        return 1;
    }

    int desired_num_elements = std::stoi(args[1]);
    std::vector<int> elements = fibonacciVector(desired_num_elements);

    for (int i=0; i<desired_num_elements; i++) {
        std::cout << elements[i] << std::endl;
    }

    return 0;
}

// This will fail at different points depending on your system architecture,
// compiler version, etc., since different machines store numbers in
// different ways.
// On my machine, I started to get nonsense answers with an input of 47.
// This is because we are using int throughout this exercise.
// These are stored on my system as 32-bit integers, which can only hold
// a maximum value of 2147483647, or about 2 billion.
// The 47th Fibonacci number is 2971215073, which exceeds the max value
// for 32-bit integers, so the value "overflows" and wraps back around
// to nonsensical negative numbers.
// You should keep this in mind when you write code:
// if you must store numbers that get close to machine limits,
// at least make it easy to swap in bigger datatypes,
// such as long long integers or double-precision floating point numbers!
