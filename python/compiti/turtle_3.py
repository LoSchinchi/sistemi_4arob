from turtle import *
from random import randint

N_SEC = 2 * 60 * 60
_1CM = 20

def main():
    robot = Turtle()
    robot.speed(0)
    for _ in range(N_SEC):
        robot.right(randint(0, 3) * 90)
        robot.forward(_1CM)
    done()

if __name__ == '__main__':
    main()