from turtle import *

PATH_FILE_READER = 'file.csv'


def main():
    t = Turtle()
    dizTur = {'forward': t.forward, 'right': t.right, 'left': t.left, 'back': t.back}

    fp = open(PATH_FILE_READER)
    for line in fp.readlines():
        list_ = line.split(', ')
        dizTur[list_[0]](int(list_[1]))
    
    done()

if __name__ == '__main__':
    main()