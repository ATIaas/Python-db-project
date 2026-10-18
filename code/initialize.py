# Creates the data file if it doesn't exist, leaves existing data alone
def init(FILE):
    open(FILE, 'a').close()
    return "Data file ready"