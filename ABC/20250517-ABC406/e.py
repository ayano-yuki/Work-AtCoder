MOD = 998244353

T = int(input())
for _ in range(T):
    N, K = map(int, input().split())
    bits = bin(N)[2:]
    L = len(bits)

    dp = [[[ (0,0) for _ in range(2)] for _ in range(K+2)] for _ in range(L+1)]
    dp[0][0][0] = (1, 0)

    for pos in range(L):
        bit_val = int(bits[pos])
        pow_val = 1 << (L - 1 - pos)
        for count in range(K+1):
            for less in range(2):
                cnt, sm = dp[pos][count][less]
                if cnt == 0:
                    continue
                for b in [0, 1]:
                    if count + b > K:
                        continue
                    if less == 0 and b > bit_val:
                        continue
                    new_less = less
                    if less == 0 and b < bit_val:
                        new_less = 1
                    new_count = count + b
                    new_cnt, new_sm = dp[pos+1][new_count][new_less]
                    new_cnt = (new_cnt + cnt) % MOD
                    new_sm = (new_sm + sm + b * pow_val * cnt) % MOD
                    dp[pos+1][new_count][new_less] = (new_cnt, new_sm)

    ans = (dp[L][K][0][1] + dp[L][K][1][1]) % MOD
    print(ans)
