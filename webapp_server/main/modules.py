import random
import string

STRING_CHAR = string.ascii_lowercase+string.ascii_uppercase+string.digits
def randomstring(length = 10):
    return ''.join(random.sample(STRING_CHAR, length))