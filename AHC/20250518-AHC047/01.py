# 焼きなまし
import random
import math
import time
from collections import defaultdict

# 定数
M = 12
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']
L = 10**6  # 生成する文字列の長さ

# 入力受け取り
def read_input():
    N, M, L = map(int, input().split())
    patterns = []
    for _ in range(N):
        s, p = input().split()
        patterns.append((s, int(p)))
    return patterns

# 初期解生成
def generate_initial_solution():
    C = [random.choice(LETTERS) for _ in range(M)]
    A = []
    for _ in range(M):
        probs = [random.randint(0, 100) for _ in range(M)]
        s = sum(probs)
        probs = [x * 100 // s for x in probs]
        diff = 100 - sum(probs)
        probs[0] += diff
        A.append(probs)
    return C, A

# 評価関数（ダミーの高速近似）
def evaluate(C, A, patterns):
    # 文字列を数千文字だけ生成して、各パターンが現れる確率をモンテカルロで見積もる
    count = defaultdict(int)
    for _ in range(20):  # サンプル回数（精度と速度トレードオフ）
        s = generate_string(C, A, 3000)
        found = set()
        for i, (pat, _) in enumerate(patterns):
            if pat in s:
                found.add(i)
        for i in found:
            count[i] += 1

    score = 0
    for i, (pat, p) in enumerate(patterns):
        qi = count[i] / 20  # 出現率
        score += qi * p
    return round(score)

def generate_string(C, A, length):
    s = [C[0]]
    state = 0
    for _ in range(length - 1):
        r = random.randint(0, 99)
        acc = 0
        for j in range(M):
            acc += A[state][j]
            if r < acc:
                state = j
                break
        s.append(C[state])
    return ''.join(s)

# 焼きなまし
def simulated_annealing(patterns, time_limit=1.8):
    start = time.time()
    C, A = generate_initial_solution()
    best_C, best_A = C[:], [row[:] for row in A]
    best_score = evaluate(C, A, patterns)

    T0, T1 = 1000, 1e-2
    iteration = 0

    while time.time() - start < time_limit:
        iteration += 1
        temp = T0 * ((T1 / T0) ** ((time.time() - start) / time_limit))

        # 近傍を生成
        new_C, new_A = C[:], [row[:] for row in A]
        if random.random() < 0.5:
            # 文字を1つ変える
            i = random.randint(0, M - 1)
            new_C[i] = random.choice(LETTERS)
        else:
            # 遷移確率を微調整
            i = random.randint(0, M - 1)
            j1, j2 = random.sample(range(M), 2)
            if new_A[i][j1] > 0:
                new_A[i][j1] -= 1
                new_A[i][j2] += 1

        new_score = evaluate(new_C, new_A, patterns)
        delta = new_score - best_score

        if delta > 0 or random.random() < math.exp(delta / temp):
            C, A = new_C, new_A
            if new_score > best_score:
                best_C, best_A = new_C[:], [row[:] for row in new_A]
                best_score = new_score

    return best_C, best_A, best_score

# 出力形式に変換
def output_solution(C, A):
    for i in range(M):
        print(C[i], *A[i])

# メイン
def main():
    patterns = read_input()
    C, A, score = simulated_annealing(patterns)
    output_solution(C, A)

if __name__ == "__main__":
    main()
