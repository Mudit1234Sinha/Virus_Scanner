import csv
import glob, re

# Scan for signatures just like Semantac or other anti-virus softwares
import os.path


def checkForSignatures():
    print("###### checking for virus signatures")

    # get all programs in directory
    programs = glob.glob("*.py")
    for p in programs:
        thisFileInfected = False
        file = open(p, "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            if re.search("^# starting virus code", line):
                # Found a virus
                print("!!!! virus found in file" + p)
                thisFileInfected = True

        if thisFileInfected == False:
            print(p + " appears to be clean")

    print("###### end section ######")


def getFileData():
    # get an initial scan of file size and date modified
    programs = glob.glob("*.py")
    programList = []
    for p in programs:
        programSize = os.path.getsize(p)
        programModified = os.path.getmtime(p)
        programData = [p, programSize, programModified]

        programList.append(programData)

    return programList


def WriteFileData(programs):
    if os.path.exists("fileData.txt"):
        return
    with open("fileData.txt", "w") as file:
        wr = csv.writer(file)
        wr.writerows(programs)

def checkForChanges():
    print("###### check for heuristic changes in the files ######")
    # open the fileData.txt file and compare each line to current file size and date

    with open("fileData.txt") as file:
        fileList = file.read().splitlines()
    originalFileList = []
    for each in fileList:
        items = each.split(',')
        originalFileList.append(items)

    # get current data from dictionary
    currentFileList = getFileData()


    # compare the old and current items
    for c in currentFileList:
        for o in originalFileList:
            if (c[0] == o[0]):
                # file names match
                if str(c[1]) != str(o[1]) or str(c[2]) != str(o[2]):

                    # file size or date do not match
                    print("\n########\nAlert File Mismatch!")
                    # print data value of each file
                    print("Current values = " + str(c))
                    print("Original values = " + str(o))

                else:
                    print("File " + c[0] + "appears to be unchanged")

    print("##### finished checking for changes in files")





# do an initial scan
WriteFileData(getFileData())

checkForSignatures()
checkForChanges()
