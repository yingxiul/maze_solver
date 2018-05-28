import sys
import os


def run(maze_input, output, action_seq):
    env = Environment(maze_input)

    action_file = open(action_seq, 'r')
    actions = action_file.read().split(" ")
    res = ""
    for act in actions:
        [x, y, reward, stop] = env.step(int(act))
        s = str(x) + " " + str(y) + " " + str(reward) + " " + str(stop) + "\n"
        res += s
    # print(res)
    output_file = open(output, 'w')
    output_file.write(res)
    output_file.close()


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



if __name__ == '__main__':
    maze_input = sys.argv[1]
    output = sys.argv[2]
    action_seq = sys.argv[3]

    run(maze_input, output, action_seq)