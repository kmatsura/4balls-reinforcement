# 4balls-reinforcement
4木並べゲームと強化学習によるゲームAIの実装

# 遊び方(How to play)
- 学習済みのモデルと戦う。
```
python3 4balls/demo.py -m reinforce
```
- 未学習のモデルと戦う。
```
python3 4balls/demo.py -m random
```
- モデルの訓練をする。
```
python3 4balls/train.py -n 訓練回数
```
- モデルの評価をする。
```
python3 4balls/eval.py
```
