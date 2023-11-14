#include "Fibonacci.hpp"

#include <cassert>

std::vector<int> fibonacciVector(int num_elements) {
    assert(num_elements >= 0);

    // Create an empty vector with the required space.
    std::vector<int> elements(num_elements);

    if (num_elements >= 1) {
        elements[0] = 1;
    }
    if (num_elements >= 2) {
        elements[1] = 1;
    }

    for (int i=2; i<num_elements; i++) {
        elements[i] = elements[i-1] + elements[i-2];
    }

    return elements;
}
