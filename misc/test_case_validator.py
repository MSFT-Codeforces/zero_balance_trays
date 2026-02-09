
import sys
import re

INT_RE = re.compile(r"-?\d+$")
LL_MIN = -(2**63)
LL_MAX = 2**63 - 1

def invalid():
    sys.stdout.write("False")

def is_int_token(tok: str) -> bool:
    return bool(INT_RE.fullmatch(tok))

def to_int(tok: str) -> int:
    return int(tok)

def main():
    data = sys.stdin.read()
    if data == "":
        return invalid()

    # Split into lines, allow trailing whitespace-only lines but no empty/whitespace-only
    # lines in the middle (strict structure).
    raw_lines = data.splitlines()
    if not raw_lines:
        return invalid()

    # Remove trailing whitespace-only lines
    while raw_lines and raw_lines[-1].strip() == "":
        raw_lines.pop()

    if not raw_lines:
        return invalid()

    # Disallow leading whitespace-only lines
    if raw_lines[0].strip() == "":
        return invalid()

    # Tokenize line-by-line; enforce no whitespace-only lines in the middle
    lines = []
    for ln in raw_lines:
        if ln.strip() == "":
            return invalid()
        toks = ln.strip().split()  # allows multiple spaces/tabs; still line-structured
        for tok in toks:
            if not is_int_token(tok):
                return invalid()
        lines.append(toks)

    # First line must contain exactly one integer t
    if len(lines[0]) != 1:
        return invalid()
    t = to_int(lines[0][0])
    if not (1 <= t <= 2 * 10**4):
        return invalid()

    idx = 1
    sum_q = 0

    for _ in range(t):
        if idx >= len(lines):
            return invalid()

        # Header line: exactly 3 integers a b q
        if len(lines[idx]) != 3:
            return invalid()
        a = to_int(lines[idx][0])
        b = to_int(lines[idx][1])
        q = to_int(lines[idx][2])
        idx += 1

        if not (0 <= a <= 10**18 and 0 <= b <= 10**18):
            return invalid()
        if not (1 <= q <= 2 * 10**5):
            return invalid()

        sum_q += q
        if sum_q > 2 * 10**5:
            return invalid()

        got = 0
        while got < q:
            if idx >= len(lines):
                return invalid()
            ks = lines[idx]
            idx += 1

            if got + len(ks) > q:
                return invalid()

            for tok in ks:
                k = to_int(tok)
                if k < LL_MIN or k > LL_MAX:
                    return invalid()
            got += len(ks)

    # No extra non-empty lines after consuming all tests
    if idx != len(lines):
        return invalid()

    sys.stdout.write("True")

if __name__ == "__main__":
    main()
