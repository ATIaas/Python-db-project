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
    slastnum = str(lastnum)

    while len(slastnum) < 3:
        lastnum = "0" + slastnum

    newfile = "seg-" + slastnum
    open(newfile, 'a').close()

    return newfile

def getSegment(index :dict[str, list[str]], key :str) -> str:
    with open(index[key][0], "r") as f:
        return str(f.readlines()[int(index[key][1])])

# Add tempfile protection
def writeSegment(index :dict[str, list[str]], key :str, value :str) -> dict[str, list]:
    lastfile = os.listdir(spath)[-1]

    if countlines(lastfile) >= 3:
        lastfile = createNew()

    with open(lastfile, 'a') as f:
        f.write(value + '\n')
    index[key] = [lastfile, str(countlines(lastfile))]

    return index
