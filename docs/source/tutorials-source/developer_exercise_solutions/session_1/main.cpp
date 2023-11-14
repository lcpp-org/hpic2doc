#include <string>
#include <vector>
#include <iostream>
#include <memory>

class Shape {
public:
    virtual double getArea() = 0;
};

class Triangle : public Shape {
public:
    Triangle(
        double base,
        double height
    ) :
        base_(base),
        height_(height)
    {}

    double getArea() {
        return 0.5 * base_ * height_;
    }

private:
    double base_, height_;
};

class Rectangle : public Shape {
public:
    Rectangle(
        double length,
        double width
    ) :
        length_(length),
        width_(width)
    {}

    double getArea() {
        return length_ * width_;
    }

private:
    double length_, width_;
};

class Circle : public Shape {
public:
    Circle(double radius) : radius_(radius) {}

    double getArea() {
        // C++20 finally includes a standard-compliant definition for pi,
        // but since you may be using an older compiler,
        // we'll just use an approximate definition here.
        double pi = 3.1415926535;
        return pi * radius_ * radius_;
    }

private:
    double radius_;
};

int main(int argc, char *argv[]) {
    std::vector<std::string> args(argv, argv+argc);

    std::vector<std::shared_ptr<Shape>> shapes;
    for (int i=1; i<argc; i++) { // Start from 1 to ignore executable name.
        std::string arg = args[i];

        if (arg == "triangle") {
            shapes.push_back(std::make_shared<Triangle>(1.0, 1.0));
        }
        else if (arg == "rectangle") {
            shapes.push_back(std::make_shared<Rectangle>(1.0, 1.0));
        }
        else if (arg == "circle") {
            shapes.push_back(std::make_shared<Circle>(1.0));
        }
        else {
            std::cout << "Invalid argument (" << arg << ") detected, ignoring." << std::endl;
        }
    }

    double total_area = 0.0;
    for (int i=0; i<shapes.size(); i++) {
        total_area += shapes[i]->getArea();
    }

    std::cout << "Total area is " << total_area << std::endl;

    return 0;
}
