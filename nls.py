import numpy as np
from scipy.optimize import least_squares

from data import P_aktual, tahun

t = (tahun - tahun[0]).astype(float)
P0 = P_aktual[0]


def model_logistik(t, M, r):
    return M / (1 + ((M - P0) / P0) * np.exp(-r * t))


def residual(parameter):
    M, r = parameter
    return model_logistik(t, M, r) - P_aktual


hasil = least_squares(
    residual,
    x0=[1700.0, 0.3],
    bounds=([P_aktual.max() + 1e-6, 1e-9], [np.inf, np.inf]),
    ftol=1e-12,
    xtol=1e-12,
    gtol=1e-12,
)

if not hasil.success:
    raise RuntimeError(f"Optimasi NLS gagal: {hasil.message}")

M, r = hasil.x

if __name__ == "__main__":
    print("Nonlinear Least Squares (NLS)")
    print(f"M = {M:.6f} MW")
    print(f"r = {r:.8f} per tahun")
