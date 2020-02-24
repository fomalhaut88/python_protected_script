def is_prime(n):
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


if 'limit' not in globals():
    limit = 100
limit = int(limit)

s = 0
for n in range(2, limit):
    if is_prime(n):
        s += 1
print(s)
