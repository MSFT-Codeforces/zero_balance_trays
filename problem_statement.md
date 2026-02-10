Time Limit: **1 seconds**

Memory Limit: **32 MB**

You have a multiset of tiles containing exactly $a$ tiles of value $1$ and exactly $b$ tiles of value $2$.

For each query, you must place every tile into exactly one of two trays:

- **Sun tray** (adds to the sum)
- **Moon tray** (subtracts from the sum)

Let $S$ be the sum of tile values in the Sun tray and $M$ the sum in the Moon tray. The net energy is $S-M$.

In the query, an integer $k$ is given: **exactly $k$ tiles must be placed into the Sun tray** (so the remaining $a+b-k$ tiles go to the Moon tray).

For each query you receive an integer $k$. **If $k$ is not in $[0,a+b]$**, then it is impossible to place exactly $k$ tiles in the Sun tray (there are only $a+b$ tiles); **output $-1$** in that case. Otherwise, determine whether it is possible to make the net energy exactly $0$ with exactly $k$ tiles in the Sun tray.

- If possible, output two integers $x$ and $y$:
  - $x$ = number of value-$1$ tiles placed into the Sun tray
  - $y$ = number of value-$2$ tiles placed into the Sun tray
- Otherwise output $-1$.

**Why net energy $0$ fixes the Sun tray sum:** The total value of all tiles is $a+2b$. Every tile is in Sun or Moon, so $S+M=a+2b$. Net energy $0$ means $S-M=0$, so $S=M$. Hence $2*S=a+2b$, so the Sun tray sum must equal $(a+2b)/2$. That is an integer only when $a+2b$ is even, i.e. $a$ is even.

**When $k$ is in $[0,a+b]$**, the Sun tray has sum $x+2y$ (since it contains $x$ tiles of value $1$ and $y$ tiles of value $2$). For net energy $0$ we need $x+2y=(a+2b)/2$, and we also need $x+y=k$. These two linear equations in $x$ and $y$ have exactly one solution when $(a+2b)/2$ is an integer, i.e. $a$ is even: subtracting $x+y=k$ from $x+2y=(a+2b)/2$ gives $y=(a+2b)/2-k$, and then $x=k-y=2k-(a+2b)/2$. So the **only candidate** pair is
$$x=2k-(a+2b)/2, y=(a+2b)/2-k.$$
A distribution is **possible** if and only if $a$ is even and this candidate satisfies $0 <= x <= a$ and $0 <= y <= b$. When valid, this is the **only** pair $(x,y)$ that satisfies the rules; you must output this pair. When invalid, output $-1$.

Queries are independent: each query uses the same multiset $(a,b)$ and does not modify it; answers depend only on the query value $k$ and the fixed $a,b$.

**Input Format:-**

The first line contains an integer $t$ — the number of test cases.

Each test case contains:
- A line with three integers $a$, $b$, $q$.
- Then $q$ integers $k$ (possibly spanning multiple lines), one per query. Each of the $q$ queries is independent and reads one $k$; the multiset is unchanged across queries.

**Output Format:-**

For each query, print:
- $-1$ if it is impossible, or
- two integers $x$ and $y$ representing a valid distribution into the Sun tray.

**Constraints:-**

- $1 <= t <= 2*10^4$
- $0 <= a,b <= 10^{18}$
- $1 <= q <= 2*10^5$
- The sum of $q$ over all test cases is at most $2*10^5$
- Each query integer $k$ fits in signed 64-bit; $k$ may be any such value (if $k$ is not in $[0,a+b]$, output $-1$ for that query)
**Examples:-**
 - **Input:**
```
3
0 2 2
1
0
3 1 3
0 2
4
2 3 4
1 2
3 4
```

 - **Output:**
```
0 1
-1
-1
-1
-1
-1
0 2
2 1
-1
```

 - **Input:**
```
1
4 1 6
3 1 3 2 0 4
```

 - **Output:**
```
3 0
-1
3 0
1 1
-1
-1
```

**Note:-**  
The following explains how each line of the example output is produced, in order. Here, **total value** means $a+2b$ (sum of all tile values).

**Example 1.**  
- **Test case 1:** $a=0$, $b=2$, $q=2$. Queries in input order: $k=1$, then $k=0$. Total value $a+2b=4$, so Sun tray must have sum $2$.  
  - **Output line 1** (query $k=1$): one tile in Sun with sum $2$ is only possible with one tile of value $2$: $(x,y)=(0,1)$ → `0 1`.  
  - **Output line 2** (query $k=0$): zero tiles in Sun gives sum $0 != 2$ → `-1`.

- **Test case 2:** $a=3$, $b=1$, $q=3$. Queries in input order: $k=0$, $k=2$, $k=4$. Total value $a+2b=5$ is odd, so $(a+2b)/2$ is not an integer; net energy $0$ is impossible for every $k$.  
  - **Output line 3** (query $k=0$) → `-1`.  
  - **Output line 4** (query $k=2$) → `-1`.  
  - **Output line 5** (query $k=4$) → `-1`.

- **Test case 3:** $a=2$, $b=3$, $q=4$. Queries in input order: $k=1$, $k=2$, $k=3$, $k=4$ (given on two lines in the input). Total value $a+2b=8$, so Sun tray must have sum $4$; we need $x+y=k$ and $x+2y=4$.  
  - **Output line 6** (query $k=1$): max Sun sum with one tile is $2<4$ → `-1`.  
  - **Output line 7** (query $k=2$): $y=2$, $x=0$; bounds hold → `0 2`.  
  - **Output line 8** (query $k=3$): $y=1$, $x=2$ → `2 1`.  
  - **Output line 9** (query $k=4$): $y=0$, $x=4$ but $x>a=2$ → `-1`.

**Example 2.**  
- **Test case 1:** $a=4$, $b=1$, $q=6$. Queries in input order: $k=3$, $k=1$, $k=3$, $k=2$, $k=0$, $k=4$. Total value $a+2b=6$, so Sun tray must have sum $3$.  
  - **Output line 1** (query $k=3$): $x+y=3$, $x+2y=3$ → $(x,y)=(3,0)$ → `3 0`.  
  - **Output line 2** (query $k=1$): $x+2y=3$ and $x+y=1$ give $y=2$, but $y <= b=1$ fails → `-1`.  
  - **Output line 3** (query $k=3$): again $(3,0)$ → `3 0`.  
  - **Output line 4** (query $k=2$): $x+y=2$, $x+2y=3$ → $(x,y)=(1,1)$ → `1 1`.  
  - **Output line 5** (query $k=0$): Sun sum would be $0 != 3$ → `-1`.  
  - **Output line 6** (query $k=4$): $x+2y=3$ and $x+y=4$ give $y=-1$ → `-1`.