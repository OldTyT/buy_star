import random


def random_cosmic_id():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 10
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password