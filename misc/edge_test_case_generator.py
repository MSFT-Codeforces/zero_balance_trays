
# Generates 15 edge input files for the problem, printed in the required format.

LLONG_MAX = 9223372036854775807
LLONG_MIN = -9223372036854775808

def format_queries(queries, per_line=10):
    lines = []
    for i in range(0, len(queries), per_line):
        lines.append(" ".join(str(x) for x in queries[i:i + per_line]))
    return "\n".join(lines)

inputs = []

# Input 1: a=b=0; includes k=0 (only possible), k>0, negative k, duplicate query
inputs.append("\n".join([
    "1",
    "0 0 4",
    "0 1",
    "-1 0",
]))

# Input 2: parity-all-impossible (a odd => a+2b odd), mix in-range/out-of-range
inputs.append("\n".join([
    "1",
    "1 0 3",
    "0 1 2",
]))

# Input 3: only 1-tiles (b=0), includes solvable k=a/2 and nearby ks + out-of-range
a, b = 10, 0
queries = [0, 5, 10, 4, 6, 11]  # 11 out of range (a+b=10)
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=6),
]))

# Input 4: only 2-tiles (a=0), includes solvable k=b/2, plus other ks
a, b = 0, 6
queries = [0, 3, 6, 2, 4]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=5),
]))

# Input 5: boundary case x=0 and y=b simultaneously (valid)
# a=4,b=2 => S=8,T=4, k=2 => x=0,y=2
a, b = 4, 2
queries = [2, 1, 3, 0]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=4),
]))

# Input 6: boundary case y=0 and x=a (valid)
# a=8,b=4 => S=16,T=8, k=8 => x=8,y=0
a, b = 8, 4
queries = [8, 7, 9, 0]  # all in-range since a+b=12
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=4),
]))

# Input 7: boundary x=a but y neither 0 nor b (valid)
# a=6,b=5 => S=16,T=8, k=7 => x=6,y=1
a, b = 6, 5
queries = [7, 6, 8]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=3),
]))

# Input 8: boundary y=b with x>=0 (valid)
# a=10,b=2 => S=14,T=7, k=5 => y=2=b, x=3
a, b = 10, 2
queries = [5, 4, 6, 2]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=4),
]))

# Input 9: negative x candidate (should reject)
# a=2,b=2 => S=6,T=3, k=1 => x=-1, y=2
a, b = 2, 2
queries = [1, 2, 3, 0]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=4),
]))

# Input 10: y=b+1 candidate (should reject)
# a=14,b=2 => S=18,T=9; k=6 => y=3=b+1 invalid
a, b = 14, 2
queries = [6, 7, 5, 9]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=4),
]))

# Input 11: huge positive out-of-range k to catch overflow if 2*k computed before range-check
a, b = 100, 100
queries = [LLONG_MAX, 0, a + b]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=3),
]))

# Input 12: huge negative out-of-range k to catch overflow / sign handling
a, b = 100, 100
queries = [LLONG_MIN, -1, 100]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=3),
]))

# Input 13: many small testcases (t=10) to stress per-test overhead and mixed behaviors
tests = []
tests.append(("0 0 1", "0"))      # solvable
tests.append(("1 0 1", "0"))      # parity impossible (a odd)
tests.append(("2 0 1", "1"))      # only ones, solvable
tests.append(("0 1 1", "1"))      # only twos, impossible
tests.append(("4 1 1", "2"))      # mixed
tests.append(("4 2 1", "2"))      # x=0,y=b boundary solvable
tests.append(("3 3 1", "3"))      # parity impossible (a odd)
tests.append(("6 0 1", "3"))      # only ones, solvable
tests.append(("0 4 1", "2"))      # only twos, solvable
tests.append(("1000000000000000000 0 1", "500000000000000000"))  # large a, solvable

inp13_lines = ["10"]
for header, ks in tests:
    inp13_lines.append(header)
    inp13_lines.append(ks)
inputs.append("\n".join(inp13_lines))

# Input 14: queries spanning multiple lines with irregular breaks; includes negative and out-of-range
a, b, q = 20, 10, 9  # a+b = 30
inputs.append("\n".join([
    "1",
    f"{a} {b} {q}",
    "0 1 29",
    "30 31",
    "-1 15 16",
    "14",
]))

# Input 15: very large a,b; boundary-adjacent ks, duplicates, extremes, out-of-range
a = 10**18
b = 10**18
# For a=b=1e18: S=3e18, T=1.5e18, valid k range: [7.5e17, 1.25e18]
k_lo = 750000000000000000
k_hi = 1250000000000000000

queries = []
# around lower boundary
queries += [k_lo - 2, k_lo - 1, k_lo, k_lo + 1, k_lo + 2]
# around upper boundary
queries += [k_hi - 2, k_hi - 1, k_hi, k_hi + 1, k_hi + 2]
# some middle values
queries += [
    800000000000000000, 900000000000000000, 1000000000000000000,
    1100000000000000000, 1200000000000000000
]
# duplicates
queries += [k_lo, k_hi, 1000000000000000000, 1000000000000000000]
# extremes / likely invalid but in-range / out-of-range
queries += [0, a + b, a + b + 1, -1]

# fill up to 60 queries with alternating valid-range and out-of-range
while len(queries) < 60:
    base = k_lo + (len(queries) * 1234567) % (k_hi - k_lo)  # within [k_lo, k_hi)
    queries.append(base)
    if len(queries) < 60:
        queries.append(a + b + (len(queries) % 5) + 1)  # out-of-range

queries = queries[:60]
inputs.append("\n".join([
    "1",
    f"{a} {b} {len(queries)}",
    format_queries(queries, per_line=8),
]))

# Print in the required wrapper format
print("Test Cases:")
for i, s in enumerate(inputs, 1):
    print(f"Input {i}:")
    print(s)
    if i != len(inputs):
        print()
