from fourballs import FourBalls
from agent import Agent
import argparse
import datetime

def main(args):
    """
    エージェントの性能を評価する。
    """
    n = int(args.n_iter)
    agent1 = Agent(7, 4, 1)
    agent2 = Agent(7, 4, 1, mode="random")
    agent1.load_param(args.path)
    param = agent1.Q.copy()
    w1 = 0
    w2 = 0
    for i in range(n):
        fb = FourBalls(7, 4)
        agent1.Q = param.copy()
        while(fb.finish == 0 and fb.cand):
            col = agent1.calc_score_and_col(fb)
            fb.put_ball(col, agent1.c)
            if fb.finish != 0:
                w1 += 1
                break
            col = agent2.calc_score_and_col(fb)
            fb.put_ball(col, 2)
            if fb.finish != 0:
                w2 += 1
    print("agent1(trained) win rate: {}".format(w1/n))
    print("agent2(random) win rate: {}".format(w2/n))
    print("Done.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="The path which load model parameters.", default="./data/model_parameters/learned_param-2000_vsrandom.pkl")
    parser.add_argument("-n", "--n_iter", help="The number of iterations.", default=10000)
    args  = parser.parse_args()
    main(args)