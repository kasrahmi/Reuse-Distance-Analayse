import csv
import sys,os

cmd = "find . -type f  -name 'A*.csv' | awk -F/ '{print $NF}'"
traceFiles = os.popen(cmd).read().split("\n")
traceFiles.pop()
for traceFile in traceFiles:
    listOutput = []
    windowBase = 60000000000
    windowList = []
    while windowBase <= 8 * 1024 * 60000000000:
        windowList.append(windowBase)
        windowBase *= 2
    for windowSize in windowList:
        listSaver = {}
        rowsNumbers = 0
        temporalsAssigns = 0
        with open(traceFile, 'r') as file:
            rows = file.readlines()
            temp1 = 0
            for row in rows:
             rowsNumbers += 1
             time_stamp, _, offset, _, _, _, _, _ = row.strip().split(',')
             x = int(time_stamp) - int(temp1)
             print(x)
             temp1 = time_stamp
             if offset not in listSaver.keys():
                listSaver[offset] = int(time_stamp)
             else:
                if int(time_stamp) - int(listSaver[offset]) <= int(windowSize):
                    temporalsAssigns += 1
                listSaver[offset] = int(time_stamp)

        listOutput.append(temporalsAssigns / rowsNumbers)

    with open('Temporal.csv', 'a', newline='') as outFile:
        writer = csv.writer(outFile)
        index = 1
        for i in range(len(listOutput)):
            writer.writerow([traceFile, str(index) + "min", listOutput[i]])
            index *= 2

