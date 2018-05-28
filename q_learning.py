import sys
import os
import random
import copy


def run(maze_input, value_out, qvalue_out, policy_out, epoch, max_len,
        rate, gamma, epsilon):
    [res, maze] = update(maze_input, epoch, max_len, rate, gamma, epsilon)
    # print(res)
    [val, pol] = getVal(res, maze)
    # print(val)
    # print(pol)
    str_val = convert(val)
    # print(str_val)
    str_pol = convert(pol)
    # print(str_pol)
    str_q = convertQ(res, maze)
    # print(str_q)

    val_file = open(value_out, 'w')
    q_file = open(qvalue_out, 'w')
    pol_file = open(policy_out, 'w')
    val_file.write(str_val)
    q_file.write(str_q)
    pol_file.write(str_pol)
    val_file.close()
    q_file.close()
    pol_file.close()


def update(maze_input, epoch, max_len, rate, gamma, epsilon):
    env = Environment(maze_input)
    recorder = initQValue(env.h, env.w)
    for i in range(epoch):
        # print("************************************************")
        new = copy.deepcopy(recorder)
        env.reset()
        count = 0
        while(count < max_len):
            # print("----------------")
            # print("recorder: ", recorder)
            count += 1
            (cur_x, cur_y) = env.cur
            qvals = recorder[cur_x][cur_y]
            # print("cur_pos = ", (cur_x, cur_y))
            # print("cur_vals = ", qvals)
            if(random.uniform(0, 1) < 1 - epsilon):
                # print("caseA")
                max_index = qvals.index(max(qvals))
            else:
                max_index = random.randint(0, 3)
                # print("caseB")
            # print("max_index = ", max_index)
            [next_x, next_y, reward, stop] = env.step(max_index)
            # print("call step: ", (next_x, next_y), reward, stop)
            cur_val = recorder[cur_x][cur_y][max_index]
            # print("cur_val = ", cur_val)
            next_val = max(recorder[next_x][next_y])
            # print("next_val = ", next_val)
            new_val = (1 - rate) * cur_val + rate * (reward + gamma * next_val)
            # print(new_val)
            new[cur_x][cur_y][max_index] = new_val
            if (stop == 1):
                # print("terminate!")
                break
        recorder = new
    return [recorder, env.maze]


def getVal(recorder, maze):
    h = len(recorder)
    w = len(recorder[0])
    res_val = []
    res_pol = []
    for i in range(h):
        row_val = []
        row_pol = []
        for j in range(w):
            if (maze[i][j] == "*"):
                row_val.append(None)
                row_pol.append(None)
                continue
            val = max(recorder[i][j])
            pol = recorder[i][j].index(val)
            row_val.append(val)
            row_pol.append(pol)
        res_val.append(row_val)
        res_pol.append(row_pol)
    return [res_val, res_pol]


###########################
######### Helper ##########

def initQValue(height, width):
    res = []
    for i in range(height):
        row = []
        for j in range(width):
            row .append([0, 0, 0, 0])
        res.append(row)
    return res


def convert(values):
    h = len(values)
    w = len(values[0])
    res = ""
    for i in range(h):
        for j in range(w):
            val = values[i][j]
            if (val == None): continue
            temp = str(i) + " " + str(j) + " " + str(val) + "\n"
            res += temp
    return res


def convertQ(recorder, maze):
    h = len(recorder)
    w = len(recorder[0])
    res = ""
    for i in range(h):
        for j in range(w):
            if (maze[i][j] == "*"): continue
            qvals = recorder[i][j]
            temp = ""
            for k in range(4):
                s = str(i)+" "+str(j)+" "+str(k)+" "+str(qvals[k])+"\n"
                temp += s
            res += temp
    return res


##########################
######### CLASS ##########

class Environment(object):
    def __init__(self, filename):
        maze_file = open(filename, 'r')
        maze_raw = maze_file.read().splitlines()
        self.maze = self.getMaze(maze_raw)
        self.h = len(self.maze)
        self.w = len(self.maze[0])
        self.cur = (self.h - 1, 0)
        self.goal = (0, self.w - 1)
        self.dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        maze_file.close()

    def step(self, act_index):
        action = self.dirs[act_index]
        next_x = min(max(self.cur[0] + action[0], 0), self.h - 1)
        next_y = min(max(self.cur[1] + action[1], 0), self.w - 1)
        next = self.maze[next_x][next_y]
        if (next == "*"):
            next_x = self.cur[0]
            next_y = self.cur[1]
        self.cur = (next_x, next_y)
        return [self.cur[0], self.cur[1], -1, int(self.cur == self.goal)]

    def reset(self):
        self.cur = (self.h - 1, 0)
        return self.cur

    def getMaze(self, raw):
        for i in range(len(raw)):
            line = list(raw[i])
            raw[i] = line
        return raw


#########################
######### MAIN ##########

if __name__ == '__main__':
    maze_input = sys.argv[1]
    value_out = sys.argv[2]
    qvalue_out = sys.argv[3]
    policy_out = sys.argv[4]
    epoch = int(sys.argv[5])
    max_len = int(sys.argv[6])
    rate = float(sys.argv[7])
    discount = float(sys.argv[8])
    epsilon = float(sys.argv[9])


    run(maze_input, value_out, qvalue_out, policy_out, epoch, max_len,
        rate, discount, epsilon)