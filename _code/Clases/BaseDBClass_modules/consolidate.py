# this function is slightly modified as it recreates the db dict when doing so

def consolidate(S) :
    S._initialize_the_DB()

    with open(S._file_path,'w', encoding=S._encoding) as file :
        for key, value in S._dictDB.items() :
            file.write(str(key) + ":" + str(value) + "\r\n")