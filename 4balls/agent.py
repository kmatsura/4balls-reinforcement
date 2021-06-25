import random


class Agent:
    def __init__(self, w, h, c, mode="reinforce"):
        """
        mode = reinforce or random
        """
        self.h = h
        self.w = w
        self.c = c
        self.oc = int(c*-1 + 3)  # opponent color
        self.mode = mode
        pass

    def load_param(self, param):
        """
        保存していたパラメータを読み込む。
        """
        pass

    def save_param(self):
        """
        学習したパラメータを保存する。
        """
        pass

    def encode_board(self, game):
        """
        盤面を数値にエンコーディングする。
        """
        pass

    def calc_score_and_col(self, game):
        """
        盤面の評価値を計算する。ルールで決まったら期待報酬の計算はしない。
        """
        point = self.calc_rule_score(game)
        print(point)
        if point:
            return point
        elif self.mode == "random":
            cand = game.cand
            col = random.choice(cand)
            return col

        pass

    def calc_rule_score(self, game):
        """
        ルールで評価値をチェックする。
        1. 自分がリーチのときは、4つ目を置く。
        2. 相手に3マスの直線があった場合は、リーチなので、(塞げる場合は)片方を塞ぐ。
        3. 相手に2マスの直線があり、その後一つ飛ばしで両端が空いている場合は、片方を塞がなければ負けてしまうので、（塞げる場合)片方を塞ぐ。
        4.  相手に2マスの直線があり、両端が空いている場合は、片方を塞がなければ負けてしまうので、（塞げる場合)片方を塞ぐ。
        """
        p1 = self.check_rule1(game)
        if p1:
            print("rule1")
            return p1
        p2 = self.check_rule2(game)
        if p2:
            print("rule2")
            return p2
        p3 = self.check_rule3(game)
        if p3:
            print("rule3")
            return p3
        p4 = self.check_rule4(game)
        if p4:
            print("rule4")
            return p4
        return None

    def check_rule1(self, game):
        """
        八方向全探索で自分の色の3マスの直線を探す。自分が4列の頂点になる場合のみ探してる。
        反対側の空いているところを返す。
        """
        # print(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                x_vec_list = [-1, 0, 1]  # xが縦方向
                y_vec_list = [-1, 0, 1]  # yが横方向
                if game.board[i][j] == self.c:  # iが縦方向, jが横方向
                    if i >= self.h - 3:
                        x_vec_list.remove(1)
                    if i <= 2:
                        x_vec_list.remove(-1)
                    if j >= self.w - 3:
                        y_vec_list.remove(1)
                    if j <= 2:
                        y_vec_list.remove(-1)
                    # print(i, j, x_vec_list, y_vec_list)
                    for x_vec in x_vec_list:
                        for y_vec in y_vec_list:
                            if x_vec == 0 and y_vec == 0:
                                continue
                            else:
                                for v in range(4):
                                    # print(i, j, v, i+v*x_vec, j+v*y_vec)
                                    check = game.board[i+v*x_vec][j+v*y_vec]
                                    if v < 3:
                                        if check != self.c:
                                            break
                                    if v == 3:
                                        if check == 0:
                                            col = j+v*y_vec
                                            if i+v*x_vec == self.h-1:  # 最下列
                                                return col
                                            check = game.board[i+v*x_vec+1][j+v*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                else:
                    continue
        return None

    def check_rule2(self, game):
        """
        check_rule1の実装の色を変えるだけ。
        """
        for i in range(self.h):
            for j in range(self.w):
                x_vec_list = [-1, 0, 1]  # xが縦方向
                y_vec_list = [-1, 0, 1]  # yが横方向
                if game.board[i][j] == self.oc:  # iが縦方向, jが横方向
                    if i >= self.h - 3:
                        x_vec_list.remove(1)
                    if i <= 2:
                        x_vec_list.remove(-1)
                    if j >= self.w - 3:
                        y_vec_list.remove(1)
                    if j <= 2:
                        y_vec_list.remove(-1)
                    # print(i, j, x_vec_list, y_vec_list)
                    for x_vec in x_vec_list:
                        for y_vec in y_vec_list:
                            if x_vec == 0 and y_vec == 0:
                                continue
                            else:
                                for v in range(4):
                                    # print(i, j, v, i+v*x_vec, j+v*y_vec)
                                    check = game.board[i+v*x_vec][j+v*y_vec]
                                    if v < 3:
                                        if check != self.oc:
                                            break
                                    if v == 3:
                                        if check == 0:
                                            col = j+v*y_vec
                                            if i+v*x_vec == self.h-1:  # 最下列
                                                return col
                                            check = game.board[i+v*x_vec+1][j+v*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                else:
                    continue
        return None


    def check_rule3(self, game):
        """
        check_rule2の実装の検索条件をかえる。空白相手相手空白という文字列を探す。
        """
        for i in range(self.h):
            for j in range(self.w):
                x_vec_list = [-1, 0, 1]  # xが縦方向
                y_vec_list = [-1, 0, 1]  # yが横方向
                if game.board[i][j] == 0:  # iが縦方向, jが横方向
                    if i >= self.h - 3:
                        x_vec_list.remove(1)
                    if i <= 2:
                        x_vec_list.remove(-1)
                    if j >= self.w - 3:
                        y_vec_list.remove(1)
                    if j <= 2:
                        y_vec_list.remove(-1)
                    # print(i, j, x_vec_list, y_vec_list)
                    for x_vec in x_vec_list:
                        for y_vec in y_vec_list:
                            if x_vec == 0 and y_vec == 0:
                                continue
                            else:
                                for v in range(4):
                                    # print(i, j, v, i+v*x_vec, j+v*y_vec)
                                    check = game.board[i+v*x_vec][j+v*y_vec]
                                    if v == 0:
                                        continue
                                    elif v < 3:
                                        if check != self.oc:
                                            break
                                    elif v == 3:
                                        if check == 0:
                                            col = j+v*y_vec
                                            if i+v*x_vec == self.h-1:  # 最下列
                                                return col
                                            check = game.board[i+v*x_vec+1][j+v*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                else:
                    continue
        return None

    def check_rule4(self, game):
        """
        check_rule2の実装を変更する。相手空白相手相手か相手相手空白相手という文字列を探す。
        """
        for i in range(self.h):
            for j in range(self.w):
                x_vec_list = [-1, 0, 1]  # xが縦方向
                y_vec_list = [-1, 1]  # yが横方向(縦はありえないので0を消す。)
                if game.board[i][j] == self.oc:  # iが縦方向, jが横方向
                    if i >= self.h - 3:
                        x_vec_list.remove(1)
                    if i <= 2:
                        x_vec_list.remove(-1)
                    if j >= self.w - 3:
                        y_vec_list.remove(1)
                    if j <= 2:
                        y_vec_list.remove(-1)
                    # print(i, j, x_vec_list, y_vec_list)
                    for x_vec in x_vec_list:
                        for y_vec in y_vec_list:
                            if x_vec == 0 and y_vec == 0:
                                continue
                            else:
                                for v in range(4):
                                    # print(i, j, v, i+v*x_vec, j+v*y_vec)
                                    check = game.board[i+v*x_vec][j+v*y_vec]
                                    if v == 1:
                                        if check != 0:
                                            break
                                    elif v == 0 or v == 2:
                                        if check != self.oc:
                                            break
                                    elif v == 3:
                                        if check == 0:
                                            col = j+1*y_vec
                                            if i+1*x_vec == self.h-1:  # 最下列
                                                return col
                                            check = game.board[i+1*x_vec+1][j+1*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                                for v in range(4):
                                    # print(i, j, v, i+v*x_vec, j+v*y_vec)
                                    check = game.board[i+v*x_vec][j+v*y_vec]
                                    if v == 2:
                                        if check != 0:
                                            break
                                    elif v == 0 or v == 1:
                                        if check != self.oc:
                                            break
                                    elif v == 3:
                                        if check == 0:
                                            col = j+2*y_vec
                                            if i+2*x_vec == self.h-1:  # 最下列
                                                return col
                                            check = game.board[i+2*x_vec+1][j+2*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                else:
                    continue
        return None

    def calc_rein_score(self):
        """
        強化学習でスコアを計算する
        """
        pass

    def conv2D(self, board, filter):
        """
        盤面の畳み込みを行う。
        """
        pass

    def calc_expected_reward(self):
        """
        各行動の期待報酬を計算して、期待報酬が最大になる行動を返す。
        """

    def put_ball(self, game):
        """
        ボールを配置する。
        """
        pass
