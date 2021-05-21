
def log(*args):
    with open('log.txt','+a') as file:
        for e in args:
            file.write(f'{e} \n')
            print(e)