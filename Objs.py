#  Copyright (c) 2020.

def level(level, exp):
    r = False
    if level in range(1, 10) and exp == 10:
        r = True

    elif level in range(11, 20) and exp == 50:
        r = True

    elif level in range(21, 45) and exp == 100:
        r = True

    elif level in range(46, 100) and exp == 200:
        r = True

    else: r = True if exp == 300 else False

    return r