
def build_inputs():
    inputs = []

    # 1) Minimum tiles (a=b=0), includes k=0, out-of-range positive, negative
    inputs.append("\n".join([
        "1",
        "0 0 3",
        "0 1 -1",
    ]))

    # 2) Parity-all-impossible (a odd => a+2b odd), multiple in-range k
    inputs.append("\n".join([
        "1",
        "1 2 4",
        "0 1 2 3",
    ]))

    # 3) Only ones (b=0), includes boundary k=0..a and one out-of-range
    inputs.append("\n".join([
        "1",
        "4 0 6",
        "0 1 2 3 4 5",
    ]))

    # 4) Only twos (a=0) with b even so at least one solvable query (k=b/2)
    inputs.append("\n".join([
        "1",
        "0 4 5",
        "0 1 2 3 4",
    ]))

    # 5) Boundary x=0 case (solution exists with x=0), plus another solvable k
    inputs.append("\n".join([
        "1",
        "2 1 2",
        "1 2",
    ]))

    # 6) Boundary y=0 case, plus a solvable interior, plus a failing near-boundary (x>a)
    inputs.append("\n".join([
        "1",
        "4 2 3",
        "4 3 5",
    ]))

    # 7) Boundary x=a with y>0 (uses all ones in Sun, still solvable)
    inputs.append("\n".join([
        "1",
        "4 4 1",
        "5",
    ]))

    # 8) Boundary y=b case (uses all twos in Sun for the solvable query), plus a failing adjacent k
    inputs.append("\n".join([
        "1",
        "6 2 2",
        "3 2",
    ]))

    # 9) Off-by-one near validity: two solvable, then just beyond (x>a) should fail
    inputs.append("\n".join([
        "1",
        "4 4 3",
        "4 5 6",
    ]))

    # 10) Out-of-range k > a+b (small a,b)
    inputs.append("\n".join([
        "1",
        "2 1 2",
        "4 100",
    ]))

    # 11) Negative k values (out-of-range)
    inputs.append("\n".join([
        "1",
        "2 1 2",
        "-1 -5",
    ]))

    # 12) Very large k near LLONG_MAX to catch overflow if computed before range check
    inputs.append("\n".join([
        "1",
        "2 2 2",
        "9223372036854775807 0",
    ]))

    # 13) Very small k near LLONG_MIN to catch overflow if computed before range check
    inputs.append("\n".join([
        "1",
        "2 2 2",
        "-9223372036854775808 1",
    ]))

    # 14) Multi-testcase input + queries spanning multiple lines (parsing robustness)
    inputs.append("\n".join([
        "3",
        "0 2 2",
        "1",
        "0",
        "3 1 3",
        "0 2",
        "4",
        "2 3 4",
        "1 2",
        "3 4",
    ]))

    # 15) Duplicate queries + random order mixture of solvable/unsolvable/in-range
    inputs.append("\n".join([
        "1",
        "4 1 6",
        "3 1 3 2 0 4",
    ]))

    return inputs


def main():
    inputs = build_inputs()
    print("Test Cases:")
    for i, s in enumerate(inputs, 1):
        print(f"Input {i}:")
        print(s)
        if i != len(inputs):
            print()  # blank line between inputs


if __name__ == "__main__":
    main()
