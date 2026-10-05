# Converts a key into a position by concatenating the ASCII values of each character in the key
# Lets limit it to 100 total possible entries
def convert(key):
    position = ""
    for c in key:
        position = position + str(ord(c))
    position = int(position)
    position = position % 100
    return position