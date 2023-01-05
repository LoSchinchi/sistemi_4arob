import queue

def main():
    coda = queue.Queue()
    coda.put(3)
    coda.put(6)
    print(coda.queue)


if __name__ == '__main__':
    main()
