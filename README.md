[![Build Status](https://travis-ci.com/rmcew/Checkers-exercise.png?branch=master)](https://travis-ci.com/rmcew/Checkers-exercise)


# Checkers-exercise
## Exercise Requirements

* Take as input an 8x8 checkerboard (grid). Each square has either a red checker, a black checker, or no checker on it. (These are not placed according to the rules of checkers, but can be placed on any of the 64 squares.) You decide the format and delivery of the input/output.  
* Using your programming language of choice, write a program to evaluate whether there are 4 checkers of the same color (red or black) in a consecutive line anywhere on the board, horizontally, vertically, or diagonally. 
* Write automated tests to verify that your program functions correctly.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to have Python 3 to run this project, it will not run in 2.x. Python 3.71. was used to develop the project. 3.6 has been tested as well.

```
Download Python from https://www.python.org/downloads/
```

### Installing

Download / install Python 3 from the link above. Then install pygame using pip

```
pip install pygame
```

Clone / download and unzip Checkers-exercise and cd in to the folder containing checkers.py. Run the game

```
python Checkers.py
```

**Note: This assumes you have python in your environment path**

All wins will be saved to wins.csv

## Running the tests

To run the automated tests, run checkers-test.py

```
python Checkers-test.py
```


## Built With

* [Pygame](https://www.pygame.org)

## Authors

* **Ross McEwen** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

checkers.py was taken from https://github.com/everestwitman/Pygame-Checkers/blob/master/checkers.py and heavily adapted to suit this project's requirements
