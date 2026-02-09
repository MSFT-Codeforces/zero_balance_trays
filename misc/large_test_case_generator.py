
import random

LLONG_MIN = -(2**63)
LLONG_MAX = 2**63 - 1


def chunked_lines(nums, chunk_sizes):
    """Return a string with nums split across lines with variable chunk sizes (cycled)."""
    out = []
    i = 0
    cs_i = 0
    n = len(nums)
    while i < n:
        c = chunk_sizes[cs_i % len(chunk_sizes)]
        cs_i += 1
        out.append(" ".join(str(x) for x in nums[i:i + c]))
        i += c
    return "\n".join(out)


def fixed_lines(nums, per_line=20):
    """Return a string with nums split into lines, per_line numbers each."""
    out = []
    for i in range(0, len(nums), per_line):
        out.append(" ".join(str(x) for x in nums[i:i + per_line]))
    return "\n".join(out)


def build_input(testcases, per_line=20, variable_chunks=None):
    """
    Build one complete input string.
    testcases: list of (a, b, ks_list)
    """
    parts = [str(len(testcases))]
    for (a, b, ks) in testcases:
        parts.append(f"{a} {b} {len(ks)}")
        if variable_chunks is None:
            parts.append(fixed_lines(ks, per_line=per_line))
        else:
            parts.append(chunked_lines(ks, variable_chunks))
    return "\n".join(parts)


def feasible_y_range(a, b):
    """
    For even a (parity-feasible), compute feasible y range:
    T = (a + 2b)/2, y in [ceil((T-a)/2), floor(T/2)] intersect [0,b].
    """
    T = (a + 2 * b) // 2
    # ceil((T-a)/2) for integer arithmetic; if negative, y>=0 dominates anyway.
    lo = max(0, (T - a + 1) // 2)
    hi = min(b, T // 2)
    return T, lo, hi


def gen_solvable_ks(a, b, count, rng):
    """Generate k values that are guaranteed solvable by sampling feasible y and using k=T-y."""
    T, lo, hi = feasible_y_range(a, b)
    if lo > hi:
        return []
    span = hi - lo + 1
    ks = []
    for i in range(count):
        if span == 1:
            y = lo
        else:
            y = lo + (i * 104729 + rng.randrange(span)) % span
        ks.append(T - y)
    return ks


def gen_random_inrange_ks(total, count, rng):
    """Generate random k in [0,total]."""
    return [rng.randrange(0, total + 1) for _ in range(count)]


def inject_extremes(ks, total):
    """Overwrite first few k with extreme/out-of-range 64-bit values."""
    extremes = [-1, total + 1, LLONG_MAX, LLONG_MIN]
    for i, v in enumerate(extremes):
        if i < len(ks):
            ks[i] = v
        else:
            ks.append(v)


def make_input_1():
    # Max a,b and max q; mix solvable/in-range and out-of-range + overflow-risk k
    rng = random.Random(1)
    a = 10**18
    b = 10**18
    total = a + b
    q = 200_000

    ks = gen_solvable_ks(a, b, 50_000, rng)
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    inject_extremes(ks, total)
    return build_input([(a, b, ks)], per_line=25)


def make_input_2():
    # Parity all impossible: a odd => S=a+2b odd; still large q with mixed k including in-range
    rng = random.Random(2)
    a = 10**18 - 1
    b = 10**18
    total = a + b
    q = 200_000

    ks = gen_random_inrange_ks(total, q, rng)
    inject_extremes(ks, total)
    # Boundary-adjacent values
    for i in range(10):
        ks[i + 10] = i
        ks[i + 25] = total - i
    return build_input([(a, b, ks)], per_line=30)


def make_input_3():
    # b=0 (only ones), huge a; only k=a/2 solvable
    rng = random.Random(3)
    a = 10**18
    b = 0
    total = a + b
    k_sol = a // 2
    q = 100_000

    near = [k_sol - 2, k_sol - 1, k_sol, k_sol + 1, k_sol + 2]
    ks = near * 10_000  # 50k
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    inject_extremes(ks, total)
    return build_input([(a, b, ks)], per_line=20)


def make_input_4():
    # a=0 (only twos), huge b; only k=b/2 solvable when b even
    rng = random.Random(4)
    a = 0
    b = 10**18
    total = a + b
    k_sol = b // 2
    q = 100_000

    near = [k_sol - 2, k_sol - 1, k_sol, k_sol + 1, k_sol + 2]
    ks = near * 10_000  # 50k
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    inject_extremes(ks, total)
    return build_input([(a, b, ks)], per_line=20)


def make_input_5():
    # Maximum t, tiny q per test (overhead/indexing), values near 1e18
    rng = random.Random(5)
    t = 20_000
    testcases = []
    for i in range(t):
        a = 10**18 - (i % 1000)         # varied parity
        b = 10**18 - ((i * 7) % 1000)
        total = a + b

        r = rng.randrange(100)
        if r < 70:
            k = rng.randrange(0, total + 1)
        elif r < 85:
            k = total + 1
        elif r < 95:
            k = -1
        else:
            k = LLONG_MAX if (i % 2 == 0) else LLONG_MIN

        testcases.append((a, b, [k]))
    return build_input(testcases, per_line=1)


def make_input_6():
    # Skew: b tiny; only two possible y values; many near-boundary ks
    rng = random.Random(6)
    a = 10**18
    b = 1
    total = a + b
    q = 50_000

    T = (a + 2 * b) // 2
    k0 = T       # y=0
    k1 = T - 1   # y=1

    pattern = [k0 - 2, k0 - 1, k0, k0 + 1, k0 + 2,
               k1 - 2, k1 - 1, k1, k1 + 1, k1 + 2]
    ks = pattern * 3000  # 30k
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    inject_extremes(ks, total)
    return build_input([(a, b, ks)], per_line=25)


def make_input_7():
    # Skew: a tiny; essentially one feasible k; many values around it + boundaries
    rng = random.Random(7)
    a = 2
    b = 10**18
    total = a + b
    q = 50_000

    T = (a + 2 * b) // 2
    _, lo, hi = feasible_y_range(a, b)  # here lo==hi
    y = lo
    k_sol = T - y

    ks = [k_sol] * 10_000
    ks += [k_sol - 1, k_sol + 1, 0, total, total - 1, 1] * 2000  # 12k
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    inject_extremes(ks, total)
    return build_input([(a, b, ks)], per_line=20)


def make_input_8():
    # Duplicates + boundaries + random order, large values
    rng = random.Random(8)
    a = 10**18
    b = 10**18 - 2
    total = a + b
    q = 100_000

    T = (a + 2 * b) // 2
    interesting = [
        0, 1, 2, total - 2, total - 1, total,
        T - 2, T - 1, T, T + 1, T + 2,
        -1, total + 1, LLONG_MAX, LLONG_MIN
    ]

    ks = []
    for _ in range(4000):
        ks.extend(interesting)  # 60k
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    return build_input([(a, b, ks)], per_line=30)


def make_input_9():
    # Multi-line query input with irregular line breaks, very large q
    rng = random.Random(9)
    a = 10**18 - 2
    b = 10**18 - 3
    total = a + b
    q = 200_000

    ks = gen_solvable_ks(a, b, 30_000, rng)
    ks += gen_random_inrange_ks(total, q - len(ks), rng)
    rng.shuffle(ks)
    inject_extremes(ks, total)

    return build_input([(a, b, ks)], variable_chunks=[1, 2, 5, 3, 7, 4, 6])


def make_input_10():
    # Multiple testcases in one input; mix parity-possible with parity-impossible
    rng = random.Random(10)

    a1 = 10**18
    b1 = 10**18 - 1
    total1 = a1 + b1
    q1 = 100_000
    ks1 = gen_solvable_ks(a1, b1, 20_000, rng)
    ks1 += gen_random_inrange_ks(total1, q1 - len(ks1), rng)
    rng.shuffle(ks1)
    inject_extremes(ks1, total1)

    a2 = 10**18 - 1
    b2 = 10**18 - 1
    total2 = a2 + b2
    q2 = 100_000
    ks2 = gen_random_inrange_ks(total2, q2, rng)
    inject_extremes(ks2, total2)

    return build_input([(a1, b1, ks1), (a2, b2, ks2)], per_line=28)


def main():
    inputs = [
        make_input_1(),
        make_input_2(),
        make_input_3(),
        make_input_4(),
        make_input_5(),
        make_input_6(),
        make_input_7(),
        make_input_8(),
        make_input_9(),
        make_input_10(),
    ]

    print("Test Cases:")
    for i, s in enumerate(inputs, 1):
        print(f"Input {i}:")
        print(s)
        if i != len(inputs):
            print()


if __name__ == "__main__":
    main()
