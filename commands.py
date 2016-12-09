from datetime import datetime

def time():
    return str(datetime.now().time())

command_to_functions = {'time': time()}
