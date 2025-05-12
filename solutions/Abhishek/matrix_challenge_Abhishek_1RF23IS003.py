import numpy as np
import time
import tracemalloc
import cProfile
import pstats

class Matrix2D:
    
    __slots__ = ['mat']

    def __init__(self, data):
       
        if isinstance(data, list):
            data = np.array(data)
        if not isinstance(data, np.ndarray):
            raise TypeError("Data must be a list or NumPy array")
        if data.ndim == 1:
            data = data.reshape(1, -1) 
        elif data.ndim != 2:
            raise ValueError("Only 1D or 2D matrices are allowed")
        self.mat = data

    def __add__(self, other):
       
        if isinstance(other, Matrix2D):
            return Matrix2D(self.mat + other.mat)
        else:
            return Matrix2D(self.mat + other)

    def __sub__(self, other):
        
        if isinstance(other, Matrix2D):
            return Matrix2D(self.mat - other.mat)
        else:
            return Matrix2D(self.mat - other)

    def __mul__(self, other):
       
        if isinstance(other, Matrix2D):
            return Matrix2D(self.mat * other.mat)
        else:
            return Matrix2D(self.mat * other)

    def __matmul__(self, other):
       
        if not isinstance(other, Matrix2D):
            raise TypeError("Matrix multiplication requires another Matrix2D")
        return Matrix2D(self.mat @ other.mat)

    def __pow__(self, power):
       
        return Matrix2D(np.power(self.mat, power))

    def __str__(self):
        return str(self.mat)

    def __repr__(self):
        return f"Matrix2D({repr(self.mat)})"

    def shape(self):
        return self.mat.shape


def demo_complex_expression():
    
    A = Matrix2D([[1, 2], [3, 4]])
    B = Matrix2D([5, 6])  
    result = (A + B) @ ((A - B) ** 2)
    print("Result of (A + B) @ (A - B) ** 2:")
    print(result)
    return result


def time_expression():
   
    start = time.perf_counter()
    for _ in range(1000):
        A = Matrix2D([[1, 2], [3, 4]])
        B = Matrix2D([5, 6])
        result = (A + B) @ ((A - B) ** 2)
    end = time.perf_counter()
    print(f"Time per iteration: {(end - start)/1000:.6f} seconds")


def memory_footprint():
  
    tracemalloc.start()
    for _ in range(1000):
        A = Matrix2D([[1, 2], [3, 4]])
        B = Matrix2D([5, 6])
        result = (A + B) @ ((A - B) ** 2)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Memory usage: {peak / 1024:.2f} KB")


def profile_cprofile():
 
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(1000):
        A = Matrix2D([[1, 2], [3, 4]])
        B = Matrix2D([5, 6])
        result = (A + B) @ ((A - B) ** 2)
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME).print_stats(5)


if __name__ == "__main__":
    demo_complex_expression()
    time_expression()
    memory_footprint()
    print("\ncProfile Results:")
    profile_cprofile()
