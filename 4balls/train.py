
from fourballs import FourBalls
from agent import Agent
import argparse
import datetime

def main(args):
    """
    エージェントを訓練させる。
    """
    n = 1
    agent1 = Agent(7, 4, 1, mode="reinforce")
    for i in range(int(args.n_iter)):
        if i%100 == 0:
            print(i)
        fb = FourBalls(7, 4)
        agent2 = Agent(7, 4, 2, mode="random")
        while(fb.finish == 0 and fb.cand):
            col = agent1.calc_score_and_col(fb)
            fb.put_ball(col, agent1.c)
            if fb.finish != 0:
                break
            col = agent2.calc_score_and_col(fb)
            fb.put_ball(col, 2)
            n += 1
            if fb.finish != 0:
                agent1.lose(fb)
    filename = str(args.n_iter) + "_vsrandom"
    agent1.save_param(args.save_path, filename)
    print("Done.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save_path", help="The path which save model parameters.", default="./data/model_parameters")
    parser.add_argument("-n", "--n_iter", help="The number of training iterations.", default=100)
    args  = parser.parse_args()
    main(args)