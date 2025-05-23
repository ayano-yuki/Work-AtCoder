N = int(input())

# バックトラッキング（再帰的構築）
def generate(s, open_cnt, close_cnt):
    if len(s) == N:
        print(s)
        return
    if open_cnt < N // 2:
        generate(s + '(', open_cnt + 1, close_cnt)
    if close_cnt < open_cnt:
        generate(s + ')', open_cnt, close_cnt + 1)

if N % 2 == 0:
    generate('', 0, 0)
