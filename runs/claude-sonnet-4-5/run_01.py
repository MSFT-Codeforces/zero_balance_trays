
def solve(a, b, k):
    total_sum = a + 2 * b
    
    # Check if solution is possible
    if total_sum % 2 != 0:
        return None
    
    target = total_sum // 2
    
    # Calculate x and y
    y = target - k
    x = 2 * k - target
    
    # Check validity
    if 0 <= x <= a and 0 <= y <= b:
        return (x, y)
    else:
        return None

t = int(input())
for _ in range(t):
    a, b, q = map(int, input().split())
    
    # Read all queries
    queries = []
    while len(queries) < q:
        queries.extend(map(int, input().split()))
    
    # Process each query
    for k in queries[:q]:
        result = solve(a, b, k)
        if result is None:
            print(-1)
        else:
            print(result[0], result[1])
