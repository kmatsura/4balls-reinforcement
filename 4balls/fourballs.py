from pprint import pprint
import random

class FourBalls:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.finish = 0
        self.winner = 0
        self.board = [[0 for _ in range(w)] for _ in range(h)]
        self.board_height = [0 for _ in range(w)]
        self.cand = [i for i in range(w)]
        self.hist = []

    def put_ball(self, col, c):
        if self.board[0][col] != 0:
            print("columns is full.")
            return -1
        else:
            d = self.board_height[col]
            self.board_height[col] += 1
            self.board[self.h - d -1][col] = c
            self.hist.append((self.h-d-1, col))
            self.finish = self.check_four(col, self.h-d-1, c)
            if self.finish != 0:
                self.winner = c
                # print("winner is {}".format(c))
            if self.board[0][col] != 0:
                self.cand.remove(col)
            return
    
    def check_four(self, x, y, c):
        """
        4列ができてるか確認する。
        コマを置いた場所かその周りは絶対4列の頂点になっていることを利用する。
        """
        x_list = [x-1, x, x+1]
        y_list = [y-1, y, y+1]
        if -1 in x_list:
            x_list.remove(-1)
        if self.w in x_list:
            x_list.remove(self.w)
        if -1 in y_list:
            y_list.remove(-1)
        if self.h in y_list:
            y_list.remove(self.h)
        for i in x_list:
            for j in y_list:
                if self.board[j][i] != c:
                    continue
                else:
                    if self.look_around(j, i) == 1:
                        return 1
        return 0
    
    def look_around(self, x, y):
        """
        自分が端点となる4列がないかチェック
        """
        flag = 0
        c = self.board[x][y]
        xvec_list = [1, 0, -1]
        yvec_list = [1, 0, -1]
        if x >= self.h - 3:
            xvec_list.remove(1)
        if x <= 2:
            xvec_list.remove(-1)
        if y >= self.w - 3:
            yvec_list.remove(1)
        if y <= 2:
            yvec_list.remove(-1)
        for xvec in xvec_list:
            for yvec in yvec_list:
                if xvec == 0 and yvec == 0:
                    continue
                else:
                    for i in range(4):
                        check2 = self.board[x + i*xvec][y + i*yvec]
                        if c != check2:
                            break
                    else:
                        flag = 1
        return flag


if __name__ == "__main__":
    fb = FourBalls(7, 4)
    n = 0
    while(fb.finish == 0 and fb.cand):
        col = random.choice(fb.cand)
        c = n%2 + 1
        fb.put_ball(col, c)
        n += 1
    pprint(fb.board)
    print(fb.finish)
    pprint(fb.board_height)
