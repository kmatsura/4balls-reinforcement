import random


class Agent:
    def __init__(self, w, h, c, mode="reinforce"):
        """
        mode = reinforce or random
        """
        self.h = h
        self.w = w
        self.c = c
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
        if point:
            return point
        elif self.mode == "random":
            cand = game.cand
            col = random.choice(cand)
            return col

        pass

    def calc_rule_score(self, board):
        """
        ルールで評価値をチェックする。
        1. 自分がリーチのときは、4つ目を置く。
        2. 相手に3マスの直線があった場合は、リーチなので、(塞げる場合は)片方を塞ぐ。
        3. 相手に2マスの直線があり、その後一つ飛ばしで両端が空いている場合は、片方を塞がなければ負けてしまうので、（塞げる場合)片方を塞ぐ。
        4.  相手に2マスの直線があり、両端が空いている場合は、片方を塞がなければ負けてしまうので、（塞げる場合)片方を塞ぐ。
        """
        p1 = self.check_rule1(board)
        if p1:
            return p1
        p2 = self.check_rule2(board)
        if p2:
            return p2
        p3 = self.check_rule3(board)
        if p3:
            return p3
        p4 = self.check_rule4(board)
        if p4:
            return p4
        return None

    def check_rule1(self, board):
        pass

    def check_rule2(self, board):
        pass

    def check_rule3(self, board):
        pass

    def check_rule4(self, board):
        pass

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
