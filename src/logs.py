
def log(*args):
    with open('log.txt','a') as file:
        file.write(f'{" ".join(args)} \n')