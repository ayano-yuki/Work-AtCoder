n, x = map(int, input().split())
problems = []
for _ in range(n):
    s, c, p = map(int, input().split())
    problems.append((s, c, p / 100.0))

memo = {}

def get_max_expected_score(money_left, solved_mask):
    if (money_left, solved_mask) in memo:
        return memo[(money_left, solved_mask)]

    max_expected = 0
    for i in range(n):
        if not (solved_mask & (1 << i)):
            score, cost, prob = problems[i]
            if money_left >= cost:
                expected_if_correct = score + get_max_expected_score(money_left - cost, solved_mask | (1 << i))
                expected_if_incorrect = get_max_expected_score(money_left - cost, solved_mask)
                expected_value = prob * expected_if_correct + (1 - prob) * expected_if_incorrect
                max_expected = max(max_expected, expected_value)

    memo[(money_left, solved_mask)] = max_expected
    return max_expected

result = get_max_expected_score(x, 0)
print(f"{result:.10f}")
