from math import log, exp, e

def custom_exp(x):
    return e**x

def main():
    for i in range(10):
        x = 10**(i-2)
        print(x)
        for j in range(1000):
            logx = log(x)
            # x = exp(logx)
            x = custom_exp(logx)
        print(x)

if __name__ == '__main__':
    main()