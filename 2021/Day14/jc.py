from multiprocessing import Pool
from time import perf_counter


def f(x):
	return x * x

if __name__ == '__main__':
	tic = perf_counter()
	with Pool(15) as p:
		result = p.map(f, [1, 2, 3])
	toc = perf_counter()
	print(f"Time taken: {toc - tic:0.4f} seconds")

	print(result)
