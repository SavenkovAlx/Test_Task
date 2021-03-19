#!/usr/bin/python3

def dollar_at():
    for i in range(11, 80):
        if not i % 3 and not i % 5:
            print('$$@@')
        elif not i % 3:
            print('$$')
        elif not i % 5:
            print('@@')
        else:
            print(i)


if __name__ == '__main__':
    dollar_at()
