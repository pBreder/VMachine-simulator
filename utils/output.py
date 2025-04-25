import time

def writing(string, delay=0.01):
    for letra in string:
        print(letra, end='')
        time.sleep(delay)
    print()
