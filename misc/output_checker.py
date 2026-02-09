
import os
import re
from typing import Tuple, List, Optional

_INT_RE = re.compile(r"-?\d+\Z")


def _normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def _parse_int(tok: str, ctx: str) -> Tuple[bool, Optional[int], str]:
    if not _INT_RE.match(tok):
        return False, None, f"{ctx}: expected integer token, got {tok!r}"
    try:
        return True, int(tok), "OK"
    except Exception as e:
        return False, None, f"{ctx}: cannot parse integer {tok!r}: {e}"


def _tokenize_input(input_text: str) -> List[str]:
    return _normalize_newlines(input_text).split()


def _split_output_lines_strict(output_text: str) -> Tuple[bool, List[str], str]:
    """
    Strict output rules:
    - Allow at most one trailing '\n' at EOF.
    - Do not otherwise tolerate extra empty lines.
    """
    out = _normalize_newlines(output_text)

    # Allow exactly one trailing newline (optional), but not more.
    if out.endswith("\n"):
        out2 = out[:-1]
        if out2.endswith("\n"):
            return False, [], "Output: more than one trailing newline is not allowed"
        out = out2

    if out == "":
        return True, [], "OK"
    return True, out.split("\n"), "OK"


def _validate_solution(a: int, b: int, k: int, x: int, y: int) -> Tuple[bool, str]:
    # Check basic bounds on chosen tiles
    if x < 0:
        return False, f"x={x} must be non-negative"
    if y < 0:
        return False, f"y={y} must be non-negative"
    if x > a:
        return False, f"x={x} exceeds a={a}"
    if y > b:
        return False, f"y={y} exceeds b={b}"

    # Must put exactly k tiles in Sun tray
    if x + y != k:
        return False, f"x+y={x+y} does not equal k={k}"

    # Net energy check:
    # Sun = x + 2y
    # Moon = (a-x) + 2(b-y)
    # Net = Sun - Moon
    net = (x + 2 * y) - ((a - x) + 2 * (b - y))
    if net != 0:
        return False, f"net energy is {net}, expected 0"
    return True, "OK"


def check(input_text: str, output_text: str) -> Tuple[bool, str]:
    inp = _tokenize_input(input_text)
    if not inp:
        return False, "Input: empty"

    ok, t, msg = _parse_int(inp[0], "Input: t")
    if not ok:
        return False, msg
    if t is None or t < 1:
        return False, f"Input: t must be >= 1, got {t}"

    idx = 1
    queries: List[Tuple[int, int, int, int, int]] = []  # (case_no, query_no, a, b, k)
    for case_no in range(1, t + 1):
        if idx + 2 >= len(inp):
            return False, f"Input: case {case_no} missing a b q"
        ok, a, msg = _parse_int(inp[idx], f"Input: case {case_no} a")
        if not ok:
            return False, msg
        ok, b, msg = _parse_int(inp[idx + 1], f"Input: case {case_no} b")
        if not ok:
            return False, msg
        ok, q, msg = _parse_int(inp[idx + 2], f"Input: case {case_no} q")
        if not ok:
            return False, msg
        idx += 3

        if a is None or b is None or q is None:
            return False, f"Input: case {case_no} failed to parse a/b/q"
        if q < 1:
            return False, f"Input: case {case_no} q must be >= 1, got {q}"
        if idx + q > len(inp):
            return False, f"Input: case {case_no} expected {q} query integers k, but input ended early"

        for qi in range(1, q + 1):
            ok, k, msg = _parse_int(inp[idx], f"Input: case {case_no} query {qi} k")
            if not ok:
                return False, msg
            idx += 1
            if k is None:
                return False, f"Input: case {case_no} query {qi} failed to parse k"
            queries.append((case_no, qi, a, b, k))

    ok, out_lines, msg = _split_output_lines_strict(output_text)
    if not ok:
        return False, msg

    expected_lines = len(queries)
    if len(out_lines) != expected_lines:
        return False, f"Output: expected exactly {expected_lines} lines (one per query), got {len(out_lines)} lines"

    for i, (case_no, qi, a, b, k) in enumerate(queries):
        line_no = i + 1
        line = out_lines[i]

        # Strict per-line whitespace constraints
        if line == "":
            return False, f"Output line {line_no} (case {case_no} query {qi}): empty line is not allowed"
        if line != line.strip():
            return False, f"Output line {line_no} (case {case_no} query {qi}): leading/trailing spaces are not allowed"
        if "\t" in line:
            return False, f"Output line {line_no} (case {case_no} query {qi}): tabs are not allowed"
        if "  " in line:
            return False, f"Output line {line_no} (case {case_no} query {qi}): multiple consecutive spaces are not allowed"

        if line == "-1":
            # Cannot validate impossibility without solving; accept "-1" as format-correct.
            continue

        parts = line.split(" ")
        if len(parts) != 2:
            return (
                False,
                f"Output line {line_no} (case {case_no} query {qi}): expected '-1' or two integers 'x y', got {line!r}",
            )

        ok, x, msg = _parse_int(parts[0], f"Output line {line_no} (case {case_no} query {qi}) x")
        if not ok:
            return False, msg
        ok, y, msg = _parse_int(parts[1], f"Output line {line_no} (case {case_no} query {qi}) y")
        if not ok:
            return False, msg
        assert x is not None and y is not None

        # Validate that (x,y) is a correct distribution for this query.
        valid, vmsg = _validate_solution(a, b, k, x, y)
        if not valid:
            return False, f"Case {case_no} query {qi}: invalid output {x} {y}: {vmsg}"

    return True, "OK"


if __name__ == "__main__":
    in_path = os.environ.get("INPUT_PATH")
    out_path = os.environ.get("OUTPUT_PATH")
    if not in_path or not out_path:
        raise SystemExit("INPUT_PATH and OUTPUT_PATH environment variables are required")
    with open(in_path, "r", encoding="utf-8") as f:
        input_text = f.read()
    with open(out_path, "r", encoding="utf-8") as f:
        output_text = f.read()
    res, _ = check(input_text, output_text)
    print("True" if res else "False")
