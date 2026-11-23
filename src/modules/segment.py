# Remember that the value of the index is a list
# list[0] is the file/segment storing the value
# list[1] is the line where the value is
# Segment format is seg-XXX

import os
spath = "src\\db_segments"

def countlines(filename :str) -> int:
    num_lines = sum(1 for _ in open('filename'))
    return num_lines

def createNew() -> str:
    lastfile = os.listdir(spath)[-1]

    lastnum = int(lastfile.split('-')[-1])
    lastnum += 1
    lastnum = str(lastnum)

    while (len(lastnum) < 3):
        lastnum = "0" + lastnum

    newfile = "seg-" + lastnum
    open(newfile, 'a').close()

    return newfile

def getSegment(index :dict[str, list], key :str) -> str:
    with open(index[key][0], "r") as f:
        return f.readlines[index[key][1]]

# Add tempfile protection
def writeSegment(index :dict[str, list], key :str, value) -> dict[str, list]:
    lastfile = os.listdir(spath)[-1]

    if countlines(lastfile) >= 3:
        lastfile = createNew()

    with open(lastfile, 'a') as f:
        f.write(value + '\n')
    index[key] = [lastfile, countlines(lastfile)]

    return index
