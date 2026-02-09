#include <iostream>
#include <vector>
#include <limits>
#include <cstdint>

using namespace std;

static __int128 toInt128(long long v) {
    return static_cast<__int128>(v);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        long long a, b;
        int q;
        cin >> a >> b >> q;

        for (int i = 0; i < q; i++) {
            long long k;
            cin >> k;

            // Out-of-range k is immediately impossible.
            if (k < 0 || k > a + b) {
                cout << -1 << "\n";
                continue;
            }

            bool found = false;
            long long bestX = -1, bestY = -1;

            // Brute force: enumerate all possible x (# of 1-tiles in Sun tray).
            // y is then forced by x + y = k.
            long long upperX = (a < k ? a : k);
            for (long long x = 0; x <= upperX; x++) {
                long long y = k - x;

                if (y < 0 || y > b) {
                    continue;
                }

                // Compute net energy exactly using 128-bit intermediates.
                __int128 sunSum = toInt128(x) + 2 * toInt128(y);
                __int128 moonSum = toInt128(a - x) + 2 * toInt128(b - y);
                __int128 net = sunSum - moonSum;

                if (net == 0) {
                    found = true;
                    bestX = x;
                    bestY = y;
                    // Do not early-exit; keep enumeration naive.
                }
            }

            if (!found) {
                cout << -1 << "\n";
            } else {
                cout << bestX << " " << bestY << "\n";
            }
        }
    }

    return 0;
}