from fourballs import FourBalls
from agent import Agent
from pprint import pprint


def main():
    """
    人間と戦う。
    """
    fb = FourBalls(7, 4)
    agent1 = Agent(7, 4, 1, mode="random")
    n = 1
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
    main()