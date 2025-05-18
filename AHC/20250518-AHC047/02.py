import sys
import time
import random
from collections import defaultdict

# --- 入力の読み込み ---
N, M, L = map(int, input().split())
patterns = [input().split() for _ in range(N)]
patterns = [(s, int(p)) for s, p in patterns]

CHARS = list('abcdef')
START_TIME = time.time()
TIME_LIMIT = 1.9  # 秒以内に出力する（マージン込み）
SAMPLES = 20
SAMPLE_LENGTH = 1000
BEAM_WIDTH = 10

# --- ユーティリティ関数群 ---

def random_C():
    return [random.choice(CHARS) for _ in range(M)]

def random_A():
    A = []
    for _ in range(M):
        prob = [random.randint(0, 100) for _ in range(M)]
        s = sum(prob)
        norm = [x * 100 // s for x in prob]
        norm[-1] += 100 - sum(norm)  # 合計が100になるよう調整
        A.append(norm)
    return A

def generate_string(C, A, length):
    s = [C[0]]
    cur = 0
    for _ in range(length - 1):
        r = random.randint(0, 99)
        acc = 0
        for j in range(M):
            acc += A[cur][j]
            if r < acc:
                cur = j
                break
        s.append(C[cur])
    return ''.join(s)

def evaluate(C, A, patterns, samples=SAMPLES):
    found = [0] * len(patterns)
    for _ in range(samples):
        s = generate_string(C, A, SAMPLE_LENGTH)
        for i, (pat, _) in enumerate(patterns):
            if pat in s:
                found[i] += 1
    return round(sum((found[i] / samples) * p for i, (_, p) in enumerate(patterns)))

def neighbor(C, A):
    newC = C[:]
    newA = [row[:] for row in A]

    if random.random() < 0.5:
        i = random.randint(0, M - 1)
        newC[i] = random.choice(CHARS)
    else:
        i = random.randint(0, M - 1)
        j = random.randint(0, M - 1)
        delta = random.randint(-10, 10)
        if 0 <= newA[i][j] + delta <= 100:
            newA[i][j] += delta
            total = sum(newA[i])
            if total != 100:
                # 再正規化
                for k in range(M):
                    newA[i][k] = newA[i][k] * 100 // total
                newA[i][-1] += 100 - sum(newA[i])
    return newC, newA

# --- 初期化 ---
bestC = random_C()
bestA = random_A()
bestScore = evaluate(bestC, bestA, patterns)

# --- 焼きなまし + ビームサーチ ---
beam = [(bestScore, bestC, bestA)]

while time.time() - START_TIME < TIME_LIMIT:
    new_beam = []
    for score, C, A in beam:
        for _ in range(3):  # 各ビームから3近傍
            C2, A2 = neighbor(C, A)
            sc = evaluate(C2, A2, patterns)
            new_beam.append((sc, C2, A2))
    beam = sorted(new_beam, reverse=True)[:BEAM_WIDTH]
    if beam[0][0] > bestScore:
        bestScore, bestC, bestA = beam[0]

# --- 出力 ---
for i in range(M):
    row = [str(bestA[i][j]) for j in range(M)]
    print(f"{bestC[i]} {' '.join(row)}")
