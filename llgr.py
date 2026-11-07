import numpy as np

from data import P_aktual as P, tahun

x = P[:-1]
delta_t = np.diff(tahun)
y = np.diff(P) / (delta_t * x)

b, a = np.polyfit(x, y, deg=1)

if a <= 0 or b >= 0:
    raise ValueError("Regresi tidak menghasilkan r > 0 dan M > 0.")

r = a
M = -a / b

if __name__ == "__main__":
    print("Linearized Logistic Growth Regression (LLGR)")
    print(f"M = {M:.6f} MW")
    print(f"r = {r:.8f} per tahun")
