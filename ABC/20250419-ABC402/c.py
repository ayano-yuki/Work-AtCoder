N, M = map(int, input().split())

recipe_ingredients = []
ingredient_to_recipes = [[] for _ in range(N + 1)]
blocked_count = []

for i in range(M):
    tmp = list(map(int, input().split()))
    K = tmp[0]
    A = tmp[1:]
    recipe_ingredients.append(A)
    blocked_count.append(K)
    for ing in A:
        ingredient_to_recipes[ing].append(i)

B = list(map(int, input().split()))

eatable = 0
result = []

for b in B:
    for recipe_idx in ingredient_to_recipes[b]:
        blocked_count[recipe_idx] -= 1
        if blocked_count[recipe_idx] == 0:
            eatable += 1
    result.append(eatable)

for r in result:
    print(r)
