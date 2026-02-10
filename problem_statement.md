Time Limit: **1 seconds**

Memory Limit: **32 MB**

You have a multiset of tiles containing exactly $a$ tiles of value $1$ and exactly $b$ tiles of value $2$.

For each query, you must place every tile into exactly one of two trays:

- **Sun tray** (adds to the sum)
- **Moon tray** (subtracts from the sum)

The net energy is defined as:

$$(\text{sum in Sun tray})-(\text{sum in Moon tray})$$

In the query, an integer $k$ is given: **exactly $k$ tiles must be placed into the Sun tray** (so the remaining $a+b-k$ tiles go to the Moon tray).

For each query you receive an integer $k$. **If $k \notin [0,a+b]$**, then it is impossible to place exactly $k$ tiles in the Sun tray (there are only $a+b$ tiles); **output $-1$** in that case. Otherwise, determine whether it is possible to make the net energy exactly $0$ with exactly $k$ tiles in the Sun tray.

- If possible, output two integers $x$ and $y$:
  - $x$ = number of value-$1$ tiles placed into the Sun tray
  - $y$ = number of value-$2$ tiles placed into the Sun tray
- Otherwise output $-1$.

**Why net energy $0$ fixes the Sun tray sum:** The total value of all tiles is $a+2b$. Every tile is in Sun or Moon, so $(\text{Sun sum})+(\text{Moon sum})=a+2b$. Net energy $0$ means $(\text{Sun sum})-(\text{Moon sum})=0$, so Sun sum equals Moon sum. Hence $2\cdot(\text{Sun sum})=a+2b$, so the Sun tray sum must equal $(a+2b)/2$. That is an integer only when $a+2b$ is even (i.e. $a$ is even).

**When $k \in [0,a+b]$**, the Sun tray has sum $x+2y$ (since it contains $x$ tiles of value $1$ and $y$ tiles of value $2$). For net energy $0$ we need $x+2y=(a+2b)/2$, and we also need $x+y=k$. These two linear equations in $x$ and $y$ have exactly one solution when $(a+2b)/2$ is an integer (i.e. $a$ is even): subtracting $x+y=k$ from $x+2y=(a+2b)/2$ gives $y=(a+2b)/2-k$, and then $x=k-y=2k-(a+2b)/2$. So the **only candidate** pair is
$$x=2k-(a+2b)/2,\qquad y=(a+2b)/2-k.$$
A distribution is **possible** if and only if $a$ is even and this candidate satisfies $0 \le x \le a$ and $0 \le y \le b$. **Output** this pair when it is valid; otherwise output $-1$. The output is therefore deterministic for every input.

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

- $1 \le t \le 2 \cdot 10^4$
- $0 \le a,b \le 10^{18}$
- $1 \le q \le 2 \cdot 10^5$
- The sum of $q$ over all test cases is at most $2 \cdot 10^5$
- Each query integer $k$ fits in signed 64-bit; $k$ may be any such value (if $k \notin [0,a+b]$, output $-1$ for that query)
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
In the first example, **test case 1** has $a=0$, $b=2$. The total sum is $S=a+2b=4$, so the Sun tray must have sum $S/2=2$.  
- For $k=1$, the only way to get sum $2$ using exactly one tile is to place one "2" in Sun: $(x,y)=(0,1)$.  
- For $k=0$, Sun sum would be $0\ne 2$, so it is impossible.

In the first example, **test case 2** has $a=3$, $b=1$, so $S=a+2b=5$ is odd. Since $S/2$ is not an integer, net energy $0$ cannot be achieved for any $k$, hence all queries output $-1$.

In the first example, **test case 3** has $a=2$, $b=3$, so $S=a+2b=8$ and the Sun tray must have sum $S/2=4$. For each query we need
$$x+y=k,\quad x+2y=4.$$
- $k=1$ gives maximum Sun sum $2$, so impossible.  
- $k=2$ gives $y=2$, $x=0$, so output $0\ 2$.  
- $k=3$ gives $y=1$, $x=2$, so output $2\ 1$.  
- $k=4$ gives $y=0$, $x=4$ but $x>a=2$, so impossible.

In the first example, **test case 1** of the second sample has $a=4$, $b=1$, so $S=a+2b=6$ and the Sun tray must have sum $S/2=3$.  
- $k=3$: solving $x+y=3$ and $x+2y=3$ gives $(x,y)=(3,0)$.  
- $k=1$: would require $y=2$ (not possible since $b=1$), so $-1$.  
- $k=3$ again gives $(3,0)$.  
- $k=2$: solving gives $(x,y)=(1,1)$.  
- $k=0$: Sun sum would be $0\ne 3$, so $-1$.  
- $k=4$: solving forces $y<0$, so $-1$.