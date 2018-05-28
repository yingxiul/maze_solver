import sys
import os


def run(maze_input, value_out, qvalue_out, policy_out, epoch, discount):
    maze_file = open(maze_input, 'r')
    maze_raw = maze_file.read().splitlines()
    maze = getMaze(maze_raw)
    # print(maze)

    # recorder 2d list contains tuple (value, action)
    recorder = initValue(len(maze), len(maze[0]))
    # print(recorder)

    res = update(recorder, maze, epoch, discount)
    # print(res)

    qvalue = getQ(res, maze, discount)
    # print(qvalue)

    valstr = convertValPol(res, 0, maze)
    # print(valstr)
    polstr = convertValPol(res, 1, maze)
    # print(polstr)
    qvalstr = convertQ(qvalue, maze)
    # print(qvalstr)

    value_file = open(value_out, 'w')
    value_file.write(valstr)
    qvalue_file = open(qvalue_out, 'w')
    qvalue_file.write(qvalstr)
    policy_file = open(policy_out, 'w')
    policy_file.write(polstr)

    maze_file.close()
    value_file.close()
    qvalue_file.close()
    policy_file.close()


def update(recorder, maze, epoch, gamma):
    h = len(recorder)
    w = len(recorder[0])
    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for num in range(epoch):
        new = initValue(h, w)
        for i in range(h):
            for j in range(w):
                # print("(i, j) =", (i, j))
                if (maze[i][j] == "G"):
                    new[i][j] = (0, None)
                    continue
                elif (maze[i][j] == "*"):
                    new[i][j] = (None, None)
                    continue
                val_max = None
                for k in range(4):
                    act = dirs[k]
                    # print(act)
                    next_x = min(max(i + act[0], 0), h - 1)
                    next_y = min(max(j + act[1], 0), w - 1)
                    # print("next = ", (next_x, next_y))
                    next = maze[next_x][next_y]
                    if (next == "*"):
                        next_x = i
                        next_y = j
                    # print("recorder = ", recorder[i][j])
                    cur_val = -1 + gamma * recorder[next_x][next_y][0]
                    if (val_max == None or val_max < cur_val):
                        val_max = cur_val
                        new[i][j] = (val_max, float(k))
        recorder = new
    return recorder


def getQ(recorder, maze, gamma):
    res = []
    h = len(recorder)
    w = len(recorder[0])
    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for i in range(h):
        row = []
        for j in range(w):
            if (maze[i][j] == "G"):
                row.append([0.0, 0.0, 0.0, 0.0])
                continue
            elif (maze[i][j] == "*"):
                row.append([None, None, None, None])
                continue
            qvals = []
            for k in range(4):
                act = dirs[k]
                next_x = min(max(i + act[0], 0), h - 1)
                next_y = min(max(j + act[1], 0), w - 1)
                next = maze[next_x][next_y]
                if (next == "*"):
                    next_x = i
                    next_y = j
                cur_val = -1 + gamma * recorder[next_x][next_y][0]
                qvals.append(cur_val)
            row.append(qvals)
        res.append(row)
    return res

############################
###########Helper###########

def getMaze(raw):
    for i in range(len(raw)):
        line = list(raw[i])
        raw[i] = line
    return raw


def initValue(height, width):
    res = []
    for i in range(height):
        row = [(0, 0)] * width
        res.append(row)
    return res


def convertValPol(recorder, index, maze):
    res = ""
    h = len(recorder)
    w = len(recorder[0])
    for i in range(h):
        for j in range(w):
            if (maze[i][j] == "G"): num = 0.0
            elif (maze[i][j] == "*"): continue
            else: num = recorder[i][j][index]
            temp = str(i) + " " + str(j) + " " + str(num) + "\n"
            res += temp
    return res


def convertQ(qvals, maze):
    res = ""
    h = len(maze)
    w = len(maze[0])
    for i in range(h):
        for j in range(w):
            if (maze[i][j] == "*"): continue
            temp = ""
            for k in range(4):
                s = str(i)+" "+str(j)+" "+str(k)+" "+str(qvals[i][j][k]) + "\n"
                temp += s
            res += temp
    return res



if __name__ == '__main__':
    maze_input = sys.argv[1]
    value_out = sys.argv[2]
    qvalue_out = sys.argv[3]
    policy_out = sys.argv[4]
    epoch = int(sys.argv[5])
    discount = float(sys.argv[6])

    run(maze_input, value_out, qvalue_out, policy_out, epoch, discount)