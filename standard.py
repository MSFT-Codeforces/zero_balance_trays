"""Solve the "Zero Balance Trays" problem using closed-form equations."""

from __future__ import annotations

import sys


def iter_ints(data: bytes):
    """Yield integers parsed from a bytes buffer.

    Args:
        data: Entire standard input as bytes.

    Yields:
        The parsed integers in the order they appear in the input.
    """
    length = len(data)
    index = 0

    while index < length:
        while index < length and data[index] <= 32:
            index += 1
        if index >= length:
            return

        sign = 1
        if data[index] == 45:  # '-'
            sign = -1
            index += 1

        value = 0
        while index < length and 48 <= data[index] <= 57:
            value = value * 10 + (data[index] - 48)
            index += 1

        yield sign * value


def solve_query(
    ones_count: int,
    twos_count: int,
    sun_tile_count: int,
    half_total_value: int,
) -> str:
    """Answer a single query for a fixed (a, b) test case.

    Args:
        ones_count: Number of value-1 tiles (a).
        twos_count: Number of value-2 tiles (b).
        sun_tile_count: Required number of tiles in the Sun tray (k).
        half_total_value: H = (a + 2b) / 2, valid only when a is even.

    Returns:
        "-1" if impossible, otherwise a string "x y".
    """
    total_tiles = ones_count + twos_count
    if sun_tile_count < 0 or sun_tile_count > total_tiles:
        return "-1"

    twos_in_sun = half_total_value - sun_tile_count
    ones_in_sun = 2 * sun_tile_count - half_total_value

    if 0 <= ones_in_sun <= ones_count and 0 <= twos_in_sun <= twos_count:
        return f"{ones_in_sun} {twos_in_sun}"

    return "-1"


def main() -> None:
    """Read input, process all test cases, and print answers."""
    data = sys.stdin.buffer.read()
    integer_iterator = iter_ints(data)

    test_case_count = next(integer_iterator)
    outputs: list[str] = []

    for test_case_index in range(test_case_count):
        ones_count = next(integer_iterator)
        twos_count = next(integer_iterator)
        query_count = next(integer_iterator)

        if ones_count % 2 != 0:
            for query_index in range(query_count):
                _ignored_k = next(integer_iterator)
                outputs.append("-1")
            continue

        half_total_value = ones_count // 2 + twos_count

        for query_index in range(query_count):
            sun_tile_count = next(integer_iterator)
            outputs.append(
                solve_query(
                    ones_count=ones_count,
                    twos_count=twos_count,
                    sun_tile_count=sun_tile_count,
                    half_total_value=half_total_value,
                )
            )

    sys.stdout.write("\n".join(outputs))


if __name__ == "__main__":
    main()