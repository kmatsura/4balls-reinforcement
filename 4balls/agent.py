import os
import random
import pickle
import copy


class Agent:

    def __init__(self, w, h, c, lr=0.01, mode="reinforce"):
        """
        mode = reinforce or random
        """
        self.h = h
        self.w = w
        self.c = c
        self.oc = int(c*-1 + 3)  # opponent colorf: 1->2, 2->1
        self.lr = lr
        self.mode = mode
        self.W = (self.w-2) * self.h * (self.w-2) ** 2 *\
            (self.h-2) ** 2 * (self.w-1)**2  * (self.h-1) ** 2 + 1
        self.Q = self.get_init_prob()  # 二次元配列state*cand これが学習するパラメータ

    def get_init_prob(self):
        init_prob = 1 / self.W * 7.
        Q = [[init_prob for _ in range(7)] for _ in range(self.W)]
        assert len(Q) == self.W, (len(Q), self.W)
        return Q

    def load_param(self, file_path):
        """
        保存していたパラメータを読み込む。(pickle形式)
        """
        with open(file_path, 'rb') as f:
            self.Q = pickle.load(f)

    def save_param(self, save_path, file_name=None):
        """
        学習したパラメータを保存する。(pickle形式)
        """
        if not file_name:
            import datetime
            now_time = str(datetime.datetime.now())
            file_name = now_time.replace(" ", "-").split(".")[0]
        file_name = "learned_param-" + file_name + ".pkl"
        with open(os.path.join(save_path, file_name), 'wb') as f:
            pickle.dump(self.Q, f)
        print("save parameters in {}".format(file_name))

    def calc_score_and_col(self, game):
        """
        盤面の評価値を計算する。ルールで決まったら期待報酬の計算はしない。
        """
        col = self.calc_rule_score(game)
        # print(col)
        if col:
            return col
        elif self.mode == "random":
            cand = game.cand
            col = random.choice(cand)
            return col
        elif self.mode == "reinforce":
            col = self.calc_rein_score(game)
            return col

    def calc_rule_score(self, game):
        """
        ルールで評価値をチェックする。
        1. 自分がリーチのときは、4つ目を置く。(報酬+1)
        2. 相手に3マスの直線があった場合は、リーチなので、(塞げる場合は)片方を塞ぐ。
        3. 相手に2マスの直線があり、その後一つ飛ばしで両端が空いている場合は、片方を塞がなければ負けてしまうので、（塞げる場合)片方を塞ぐ。
        4.  相手に2マスの直線があり、両端が空いている場合は、片方を塞がなければ負けてしまうので、（塞げる場合)片方を塞ぐ。
        """
        p1 = self.check_rule1(game)
        if p1:
            # print("rule1")
            encodered_state = self.encode_board(game)
            for i in range(7):
                self.Q[encodered_state][i] = 1
            return p1
        p2 = self.check_rule2(game)
        if p2:
            # print("rule2")
            return p2
        p3 = self.check_rule3(game)
        if p3:
            # print("rule3")
            return p3
        p4 = self.check_rule4(game)
        if p4:
            # print("rule4")
            return p4
        return None

    def check_rule1(self, game):
        """
        1. 自分が3マス揃っていてもう１マス延長して価値な場合。
        八方向全探索で自分の色の3マスの直線を探す。自分が4列の頂点になる場合のみ探してる。
        反対側の空いているところを返す。
        2. 間の1マスを埋めたら勝ちなパターンooxoみたいな。
        """
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
                                            check = game.board[i +
                                                               v*x_vec+1][j+v*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                                for v in range(4):
                                    if v == 0:
                                        continue
                                    if v == 1:
                                        if check != 0:
                                            break
                                    if v > 1:
                                        if check != self.c:
                                            break
                                else:
                                    col = j + y_vec
                                    if i + x_vec == self.h-1:
                                        return col
                                    check = game.board[i+x_vec+1][j+y_vec]
                                    if check != 0:
                                        return col
                                for v in range(4):
                                    if v == 0:
                                        continue
                                    if v == 2:
                                        if check != 0:
                                            break
                                    if v == 1 or v == 3:
                                        if check != self.c:
                                            break
                                else:
                                    col = j + 2 * y_vec
                                    if i + 2 * x_vec == self.h-1:
                                        return col
                                    check = game.board[i+2*x_vec+1][j+2*y_vec]
                                    if check != 0:
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
                                            check = game.board[i +
                                                               v*x_vec+1][j+v*y_vec]
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
                                            check = game.board[i +
                                                               v*x_vec+1][j+v*y_vec]
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
                                            check = game.board[i +
                                                               1*x_vec+1][j+1*y_vec]
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
                                            check = game.board[i +
                                                               2*x_vec+1][j+2*y_vec]
                                            if check != 0:  # 下が埋まっている。
                                                return col
                else:
                    continue
        return None

    def calc_rein_score(self, game):
        """
        強化学習でスコアを計算する
        """
        state = self.encode_board(game)
        col = self.calc_expected_reward(game, state)
        return col

    def encode_board(self, game):
        """
        盤面を数値にエンコーディングする。
        計算リソースの都合上自分のだけ見る。
        """
        dim_f1a = self.filter1(game, self.c)  # 0~(self.w-2)*(self.h)
        assert 0 <= dim_f1a <= (self.w-2)*(self.h), (dim_f1a, (self.w-2)*(self.h))
        dim_f2a = self.filter2(game, self.c)  # 0~(self.w-2)*(self.h-2)
        assert 0 <= dim_f2a <= (self.w-2)*(self.h-2), dim_f2a
        dim_f3a = self.filter3(game, self.c)
        assert 0 <= dim_f3a <= (self.w-2)*(self.h-2), dim_f3a
        dim_f4a = self.filter4(game, self.c)
        assert 0 <= dim_f4a <= (self.w-1)*(self.h-1), dim_f4a
        dim_f5a = self.filter5(game, self.c)
        assert 0 <= dim_f5a <= (self.w-1)*(self.h-1), dim_f5a
        state_num = 0
        state_num += dim_f1a * (self.w-2) * \
            (self.h-2) ** 2 * (self.w-1) * (self.h-1) ** 2
        state_num += dim_f2a * (self.w-2) * (self.h-2) * \
            (self.w-1) * (self.h-1) ** 2
        state_num += dim_f3a * (self.w-1) * (self.h-1) ** 2
        state_num += dim_f4a * (self.w-1) * (self.h-1)
        state_num += dim_f5a
        assert 0 <= state_num < len(self.Q), (state_num, len(self.Q))
        return state_num

    def filter1(self, game, c):
        """
        横スプリットを検索する。(cxcみたいなやつ)
        """
        for i in range(self.h):
            for j in range(self.w):
                if j == 0 or j == self.w-1:
                    continue
                check = game.board[i][j]
                if check != 0:
                    continue
                else:
                    if game.board[i][j+1] != c:
                        continue
                    if game.board[i][j-1] != c:
                        continue
                    # i:0~self.h-1, j:1~self.w-2
                    num = i*(self.w-2) + j
                    return num
        return 0

    def filter2(self, game, c):
        """
        左斜めスプリットを検索する。
        """
        for i in range(self.h):
            for j in range(self.w):
                if i == 0 or i == self.h-1:
                    continue
                if j == 0 or j == self.w-1:
                    continue
                if game.board[i][j] != 0:
                    continue
                else:
                    if game.board[i+1][j-1] != c:
                        continue
                    if game.board[i-1][j+1] != c:
                        continue
                    num = (i-1)*(self.w-2) + j
                    return num
        return 0

    def filter3(self, game, c):
        """
        右斜めスプリットを検索する。
        """
        for i in range(self.h):
            for j in range(self.w):
                if i == 0 or i == self.h-1:
                    continue
                if j == 0 or j == self.w-1:
                    continue
                if game.board[i][j] != 0:
                    continue
                else:
                    if game.board[i-1][j+1] != c:
                        continue
                    if game.board[i+1][j-1] != c:
                        continue
                    num = (i-1)*(self.w-2) + j
                    return num
        return 0

    def filter4(self, game, c):
        """
        右下角を検索する。」こういうの。
        """
        for i in range(self.h):
            for j in range(self.w):
                if i == 0:
                    continue
                if j == 0:
                    continue
                if game.board[i][j] != c:
                    continue
                else:
                    if game.board[i][j-1] != c:
                        continue
                    if game.board[i-1][j] != c:
                        continue
                    num = (i-1)*(self.w-1) + j
                    return num
        return 0

    def filter5(self, game, c):
        """
        左下角を検索する。」これの左右反転。
        """
        for i in range(self.h):
            for j in range(self.w):
                if i == 0:
                    continue
                if j == self.w-1:
                    continue
                if game.board[i][j] != c:
                    continue
                else:
                    if game.board[i][j+1] != c:
                        continue
                    if game.board[i-1][j] != c:
                        continue
                    num = (i-1)*(self.w-1) + j
                    return num
        return 0

    def calc_expected_reward(self, game, state):
        """
        各行動の期待報酬を計算して、期待報酬が最大になる行動を返す。
        """
        cand_list = game.cand
        score = 0
        ans_col = cand_list[0]
        for cand in cand_list:
            tmp_score = self.Q[state][cand]
            if score < tmp_score:
                ans_col = cand
                score = tmp_score
        predicted_next_state = self.predict_opponent_action(game, ans_col)
        predicted_next_score = max(self.Q[predicted_next_state])
        self.Q[state][cand] += self.lr*predicted_next_score  # update parameter
        return ans_col

    def predict_opponent_action(self, game, col):
        """
        相手の気持ちになって考える。
        """
        tmp_game = copy.deepcopy(game)
        tmp_game.put_ball(col, self.c)
        # 相手の気持ちになる。
        self.c, self.oc = self.oc, self.c
        op_state = self.encode_board(tmp_game)
        op_cand_list = tmp_game.cand
        op_score = 0
        predicted_col = op_cand_list[0]
        for cand in op_cand_list:
            tmp_score = self.Q[op_state][cand]
            if op_score < tmp_score:
                predicted_col = cand
                op_score = tmp_score
        tmp_game.put_ball(predicted_col, self.c)
        predicted_next_state = self.encode_board(tmp_game)
        # 元に戻る。
        self.c, self.oc = self.oc, self.c
        return predicted_next_state

    def lose(self, game):
        """
        敗北時にQ値を更新する。
        """
        i, j = game.hist[-1]
        game.board[i][j] = 0  # 1つ前の状態に戻す。
        lose_state = self.encode_board(game)
        for a in range(7):
            self.Q[lose_state][a] = -1
