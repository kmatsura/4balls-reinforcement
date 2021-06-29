from fourballs import FourBalls
from agent import Agent
from pprint import pprint
import argparse

def main(mode):
    """
    人間と戦う。
    """
    fb = FourBalls(7, 4)
    n = 1
    if mode == "random":
        agent1 = Agent(7, 4, 1, mode="random")
        while(fb.finish == 0 and fb.cand):
            print("===turn {}====".format(n))
            print("computer")
            col = agent1.calc_score_and_col(fb)
            fb.put_ball(col, agent1.c)
            pprint(fb.board)
            if fb.finish != 0:
                print("Computer wins!!")
                break
            print("ボールを置く列を指定してください。")
            print("player")
            col_user = int(input())
            fb.put_ball(col_user, 2)
            pprint(fb.board)
            n += 1
            if fb.finish != 0:
                print("You win!!")
    elif mode == "reinforce":
        agent1 = Agent(7, 4, 1, mode="reinforce")
        agent1.load_param("./data/model_parameters/learned_param-2021-06-29-18:27:00.pkl")
        while(fb.finish == 0 and fb.cand):
            print("===turn {}====".format(n))
            print("computer")
            col = agent1.calc_score_and_col(fb)
            fb.put_ball(col, agent1.c)
            pprint(fb.board)
            if fb.finish != 0:
                print("Computer wins!!")
                break
            print("ボールを置く列を指定してください。")
            print("player")
            col_user = int(input())
            fb.put_ball(col_user, 2)
            pprint(fb.board)
            n += 1
            if fb.finish != 0:
                print("You win!!")





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="random or reinforce", default="random")
    args  = parser.parse_args()
    main(mode = args.mode)