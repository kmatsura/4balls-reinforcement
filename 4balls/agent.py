class Agent:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.Q = 
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

    def calc_score(self):
        """
        盤面の評価値を計算する。ルールで決まったら期待報酬の計算はしない。
        """
        pass

    def calc_rule_score(self):
        """
        ルールで評価値をチェックする。
        """
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