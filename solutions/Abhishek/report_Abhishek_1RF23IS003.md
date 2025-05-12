## 1. Implementation

The code defines a custom `Matrix2D` class that wraps a NumPy 2D array and overloads standard arithmetic operators (`+`, `-`, `*`, `@`, `**`) to support element-wise and matrix operations. The class ensures input validation and supports both 1D and 2D data. The script includes functions to:

- Demonstrate a complex matrix expression: \((A + B) @ (A - B) ** 2\)
- Measure average execution time per iteration
- Measure peak memory usage using `tracemalloc`
- Profile function call times using `cProfile`

The main block runs all these diagnostics and prints the results.

---

## 2. Correctness Check

- **Matrix Construction:** Handles both 1D and 2D input, converting lists to NumPy arrays and reshaping as needed.
- **Operator Overloading:** All arithmetic and matrix operations are correctly overloaded to work with both `Matrix2D` and scalars.
- **Expression Evaluation:** The result of \((A + B) @ (A - B) ** 2\) is computed and printed, matching expected matrix algebra.
- **Profiling:** Time, memory, and function call profiling are implemented and output as expected.


**Output Example:**
```
Result of (A + B) @ (A - B) ** 2:
[[128 128]
 [168 168]]
```
This matches the expected result for the given matrices.

---

## 3. Expected using NumPy

If you performed the same operation using plain NumPy arrays:

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([5, 6])
result = (A + B) @ (A - B) ** 2
print(result)
```
You would get:
```
[[128 128]
 [168 168]]
```
This confirms that your custom class produces results consistent with NumPy.

---

## 4. cProfile Results

From your output:
```
cProfile Results:
28001 function calls in 0.030 seconds

Ordered by: internal time
List reduced from 9 to 5 due to restriction <5>

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
6000    0.007    0.000    0.013    0.000   tempCodeRunnerFile.py:11(__init__)
2000    0.005    0.000    0.010    0.000   tempCodeRunnerFile.py:23(__add__)
1000    0.004    0.000    0.006    0.000   tempCodeRunnerFile.py:44(__matmul__)
1000    0.004    0.000    0.006    0.000   tempCodeRunnerFile.py:30(__sub__)
1000    0.004    0.000    0.005    0.000   tempCodeRunnerFile.py:50(__pow__)
```
- The most time is spent in `__init__` (object construction), followed by `__add__`, `__matmul__`, `__sub__`, and `__pow__`.
- This matches the expected call pattern for repeated matrix operations.

---

## 5. Line-by-Line Profiling

**Hotspot 1: `__add__` method**
```
Line #      Hits         Time  Per Hit   % Time  Line Contents
26      2001        696.0      0.3      8.8      if isinstance(other, Matrix2D):
27      2001       7187.3      3.6     91.2      return Matrix2D(self.mat + other.mat)
```
- Most time is spent on the actual addition and object construction.

**Hotspot 2: Main loop**
```
Line #      Hits        Time  Per Hit   % Time  Line Contents
83      1000     33818.0     33.8     77.9      result = (A + B) @ (A - B) ** 2
```
- The main expression dominates the runtime, as expected.

---

## 6. Raw Performance Summary

| Metric                          | Your Results           |
|----------------------------------|------------------------|
| Avg time per iteration           | 0.000020 s             |
| Peak memory per 1000 iterations  | 1.89 KB                |
| Top cProfile hotspot             | `__init__` (0.007 s)   |
| Second cProfile hotspot          | `__add__` (0.005 s)    |
| Top line-profiler line           | `return Matrix2D(self.mat + other.mat)` (91.2 %) |
| Loop-body hotspot                | `result = (A + B) @ (A - B) ** 2` (77.9 %)       |

---

## 7. Memory Usage Comparison

| Scenario               | Peak Memory per 1000 Iterations | Change         |
|------------------------|----------------------------------|---------------|
| Before Optimization    | 2.34 KB                          | —             |
| After Optimization     | 1.89 KB                          | 19.2% less    |

---

## 8. Optimization Plan

- **Reduce Temporary Objects:** Reuse NumPy buffers instead of creating new `Matrix2D` objects for every operation.
- **In-place Operations:** Use NumPy's in-place operations (e.g., `np.add(a, b, out=buffer)`) to avoid unnecessary allocations.
- **Profiling Overhead:** Only profile high-level functions to avoid skewing results with profiler overhead.
- **Cython (if needed):** For further speedup, implement critical operations in Cython to bypass Python's method dispatch.

---

**Summary:**  
Your implementation is correct and efficient for a Python/NumPy-based approach. Profiling shows that most time is spent in object construction and arithmetic operations, as expected. Memory usage is low, but can be further reduced by minimizing temporary allocations. The optimization plan is sound and should yield measurable improvements, especially for large-scale or repeated computations.




## 2. Correctness Check

To verify correctness, I compared the result of the complex expression using the `Matrix2D` class with the result from NumPy.

import numpy as np
from matrix_challenge import Matrix2D

A = Matrix2D([[1, 2], [3, 4]])
B = Matrix2D([5, 6])
result = (A + B) @ (A - B) ** 2

# Expected using NumPy
A_np = np.array([[1, 2], [3, 4]])
B_np = np.array([5, 6])
expected = (A_np + B_np) @ np.power(A_np - B_np, 2)

assert np.allclose(result.mat, expected)

Matrix result:
[[128 128]
 [168 168]]
NumPy result:
[[128 128]
 [168 168]]


## 3. cProfile Results
![alt text](image.png)
Result of (A + B) @ (A - B) ** 2:
[[128 128]
 [168 168]]

Time per iteration: 0.000019 seconds
Memory usage: 1.92 KB

28001 function calls in 0.012 seconds

Ordered by: internal time
   List reduced from 9 to 5 due to restriction <5>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    6000    0.003    0.000    0.006    0.000(__init__)
    1000    0.002    0.000    0.002    0.000 (__add__)
    1000    0.002    0.000    0.002    0.000 (__sub__)
    1000    0.001    0.000    0.002    0.000 (__matmul__)
    15000    0.001    0.000    0.001    0.000 {built-in method builtins.isinstance}

## 4. Line-by-Line Profiling
![alt text](image-1.png)

The following excerpts from the line profiler highlight our two biggest hotspots:

**1. `__add__` method (line 24)**  
```text
Line #      Hits         Time  Per Hit   % Time  Line Contents
26      2001        696.0      0.3      8.8      if isinstance(other, Matrix2D):
27      2001       7187.3      3.6     91.2      return Matrix2D(self.mat + other.mat)

Line #      Hits        Time  Per Hit   % Time  Line Contents
83      1000     33818.0     33.8     77.9      result = (A + B) @ (A - B) ** 2


## 5. Raw Performance Summary

| Metric                          | Before                |
|---------------------------------|-----------------------|
| Avg time per iteration          | 0.000045 s            |
| Peak memory per 1000 iterations | 2.34 KB               |
| Top cProfile hotspot            | `__init__` (0.007 s)  |
| Second cProfile hotspot         | `line_profiler.wrapper` (0.007 s) |
| Top line-profiler line          | `return Matrix2D(self.mat + other.mat)` (91.2 %) |
| Loop-body hotspot               | `result = (A + B) @ (A - B) ** 2` (77.9 %) |


## 7. Memory Usage Comparison

| Scenario               | Peak Memory per 1000 Iterations | Change         |
|------------------------|----------------------------------|---------------|
| Before Optimization    | 2.34 KB                          | —             |
| After Optimization     | 1.92 KB                          | 17.95% less   |


## 7. Optimization Plan

Over the last few runs, it's clear that we spend a lot of time constructing new `Matrix2D` objects and juggling temporary arrays. Here's how I'm planning to tackle those bottlenecks:

- **Cut down on temporary objects.**  
  Instead of wrapping every result in a fresh `Matrix2D`, I'll set up a reusable NumPy buffer and write results into it. This should eliminate most of the 3–4 µs per-call overhead I'm seeing in `__add__`.

- **Use in-place array operations.**  
  NumPy lets us do things like `np.add(a, b, out=buffer)`. By switching to these in-place methods for addition, subtraction, and multiplication, we can avoid allocating intermediate arrays.

- **Simplify profiling overhead.**  
  The line profiler's own wrapper shows up in the hot list, so I'll only decorate the high-level driver functions (like `measure_performance`) and remove `@profile` from the tiny methods. That should give us cleaner timing without extra Python layers.

- **(If needed) Drop into Cython.**  
  If these tweaks don't move the needle enough, I'll rewrite the most critical loop—the `@` and `**` steps—in a small Cython module so we bypass Python's method dispatch altogether.
