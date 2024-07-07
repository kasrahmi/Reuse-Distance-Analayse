import csv
import sys, os

cmd = "find . -type f  -name '*.csv' | awk -F/ '{print $NF}'"
traceFiles = os.popen(cmd).read().split("\n")
for traceFile in traceFiles:
    if traceFile == 'output.csv':
        break
    queueSizeList = [64, 128]
    for queueSize in queueSizeList:
        stridDistance = 64 * 1024
        noSequential = 0
        noStrided = 0
        noRandom = 0
        noOverlapped = 0
        noRequests = 0
        queueList = []
        # random = 0, strided = 1, overlapped = 2, sequential = 3
        with open(traceFile, 'r') as file:
            rows = file.readlines()
            for row in rows:
                 noRequests += 1
                 _, _, offset, requestSize, _, _, _, _ = row.strip().split(',')
                 newPair = (int(offset), int(offset) + int(requestSize))
                 mode = 0
                 # recognize type of request:
                 for item in queueList:
                    if item[1] == newPair[0]:
                        mode = 3
                        break
                    if not (item[0] > newPair[1] or item[1] < newPair[0]):
                        mode = 2
                    if abs(item[0] - newPair[1]) < stridDistance or abs(newPair[0] - item[1]) < stridDistance:
                        mode = max(mode, 1)
                 # update requests:
                 if mode == 0:
                    noRandom += 1
                 elif mode == 1:
                    noStrided += 1
                 elif mode == 2:
                    noOverlapped += 1
                 else:
                    noSequential += 1
                 # update queue
                 if len(queueList) == queueSize:
                    queueList.pop(0)
                 queueList.append(newPair)
        print(noRandom)
        print(noStrided)
        print(noOverlapped)
        print(noSequential)
        with open('output.csv', 'a', newline='') as outFile:
            writer = csv.writer(outFile)
            writer.writerow([traceFile, queueSize, "random", noRandom/noRequests])
            writer.writerow([traceFile, queueSize, "strided",noStrided/noRequests])
            writer.writerow([traceFile, queueSize, "overlapped", noOverlapped / noRequests])
            writer.writerow([traceFile, queueSize, "sequential", noSequential / noRequests])
