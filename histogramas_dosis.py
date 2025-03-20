# -*- coding: utf-8 -*-
"""Histogramas_Dosis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dDKwCWSxCBkB8zGvU8V2_TD9ldKu-nXT
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf

#Data extraida en funcion de profundidad
# Datos en formato texto (extraidos directamente de la app lector VIDAR)
data_text = """
Bin Center,Original Image Pixels,Clipped Image Pixels
41.0409,511,511
42.0409,3725,3725
43.0409,3428,3428
44.0409,3215,3215
45.0409,1189,1189
46.0409,476,476
"""

# 1) Parsear el texto para generar los arrays
lines = data_text.strip().split('\n')
header = lines[0]  # "Bin Center,Original Image Pixels,Clipped Image Pixels"
lines = lines[1:]  # Omitir la línea de cabecera

bin_centers = []
original_pixels = []
#clipped_pixels = []

for line in lines:
    bc_str, op_str, cp_str = line.split(',')
    bin_centers.append(float(bc_str))
    original_pixels.append(float(op_str))
   # clipped_pixels.append(float(cp_str))

# Convertir a arreglos numpy
bin_centers = np.array(bin_centers)
original_pixels = np.array(original_pixels)
#clipped_pixels = np.array(clipped_pixels)

# Gaussiana simple
def gauss(x, A, mu, sigma):
    return A * np.exp(-((x - mu)**2) / (2 * sigma**2))

# Suma de dos gaussianas
def double_gauss(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return (A1 * np.exp(-((x - mu1)**2) / (2 * sigma1**2)) +
            A2 * np.exp(-((x - mu2)**2) / (2 * sigma2**2)))

# Gaussiana asimétrica (Skew Normal)
def skew_gauss(x, A, mu, sigma, alpha):
    """
    Función Gaussiana Asimétrica (Skew Normal).
    Parámetros:
      A     -> Amplitud
      mu    -> Ubicación (centro)
      sigma -> Escala
      alpha -> Factor de asimetría (alpha>0 => cola a la derecha, alpha<0 => cola a la izquierda)

    Fórmula:
      f(x) = A * 2 * phi(z) * Phi(alpha * z)
      donde z = (x - mu)/sigma
      phi(z) = (1 / sqrt(2*pi)) * exp(-z^2 / 2)
      Phi(z) = 0.5 * [1 + erf(z / sqrt(2))]
    """
    z = (x - mu) / sigma
    pdf = (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * z**2)
    cdf = 0.5 * (1.0 + erf(alpha * z / np.sqrt(2.0)))
    return A * 2.0 * pdf * cdf

def sse_and_aic(model_func, x, y, popt):
    y_pred = model_func(x, *popt)
    residuals = y - y_pred
    sse = np.sum(residuals**2)
    n = len(y)
    k = len(popt)
    aic = n * np.log(sse / n) + 2 * k
    rmse = np.sqrt(sse / n)
    return sse, rmse, aic

# Modelo 1: Gaussiana simple
p0_gauss = [max(original_pixels), np.mean(bin_centers), np.std(bin_centers)]
popt_gauss, pcov_gauss = curve_fit(gauss, bin_centers, original_pixels, p0=p0_gauss)
sse_gauss, rmse_gauss, aic_gauss = sse_and_aic(gauss, bin_centers, original_pixels, popt_gauss)

# Modelo 2: Suma de dos gaussianas
# Estimación inicial: se divide la amplitud, se asume dos centros cercanos a la media ±5 y sigma aproximado en 10
p0_double = [max(original_pixels)/2, np.mean(bin_centers)-5, 10,
             max(original_pixels)/2, np.mean(bin_centers)+5, 10]
popt_double, pcov_double = curve_fit(double_gauss, bin_centers, original_pixels, p0=p0_double)
sse_double, rmse_double, aic_double = sse_and_aic(double_gauss, bin_centers, original_pixels, popt_double)

# Modelo 3: Gaussiana asimétrica (Skew Normal)
p0_skew = [max(original_pixels), np.mean(bin_centers), np.std(bin_centers), 0]  # alpha=0 indica simetría
popt_skew, pcov_skew = curve_fit(skew_gauss, bin_centers, original_pixels, p0=p0_skew)
sse_skew, rmse_skew, aic_skew = sse_and_aic(skew_gauss, bin_centers, original_pixels, popt_skew)

x_fit = np.linspace(bin_centers.min(), bin_centers.max(), 500)
y_gauss = gauss(x_fit, *popt_gauss)
y_double = double_gauss(x_fit, *popt_double)
y_skew = skew_gauss(x_fit, *popt_skew)

plt.figure(figsize=(12, 8))
plt.bar(bin_centers, original_pixels, width=0.8, alpha=0.4, label="Datos", color="skyblue")
plt.plot(x_fit, y_gauss, 'r-', label="Gaussiana Simple")
plt.plot(x_fit, y_double, 'g--', label="Suma de dos Gaussianas")
plt.plot(x_fit, y_skew, 'b-', label="Gaussiana Asimétrica")
plt.xlabel("Bin Center (cGy)")
plt.ylabel("Cantidad de píxeles")
plt.title("Histograma y Ajustes para p = 4 cm")
plt.legend()
plt.tight_layout()
plt.show()

print("=== Modelo Gaussiana Simple ===")
print(f"Parámetros: A = {popt_gauss[0]:.2f}, mu = {popt_gauss[1]:.2f}, sigma = {popt_gauss[2]:.2f}")
print(f"SSE = {sse_gauss:.2f}, RMSE = {rmse_gauss:.2f}, AIC = {aic_gauss:.2f}\n")

print("=== Modelo Suma de dos Gaussianas ===")
print(f"Parámetros: A1 = {popt_double[0]:.2f}, mu1 = {popt_double[1]:.2f}, sigma1 = {popt_double[2]:.2f},"
      f" A2 = {popt_double[3]:.2f}, mu2 = {popt_double[4]:.2f}, sigma2 = {popt_double[5]:.2f}")
print(f"SSE = {sse_double:.2f}, RMSE = {rmse_double:.2f}, AIC = {aic_double:.2f}\n")

print("=== Modelo Gaussiana Asimétrica (Skew Normal) ===")
print(f"Parámetros: A = {popt_skew[0]:.2f}, mu = {popt_skew[1]:.2f}, sigma = {popt_skew[2]:.2f}, alpha = {popt_skew[3]:.2f}")
print(f"SSE = {sse_skew:.2f}, RMSE = {rmse_skew:.2f}, AIC = {aic_skew:.2f}\n")

# Calcular los residuales para cada modelo
res_gauss  = original_pixels - gauss(bin_centers, *popt_gauss)
res_double = original_pixels - double_gauss(bin_centers, *popt_double)
res_skew   = original_pixels - skew_gauss(bin_centers, *popt_skew)

# Crear una figura con tres subgráficas para comparar los residuales
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Residuales de la Gaussiana Simple
axs[0].scatter(bin_centers, res_gauss, color='r', label=f'Residuales (RMSE={rmse_gauss:.2f})')
axs[0].axhline(0, color='black', linestyle='--')
axs[0].set_ylabel("Residuales")
axs[0].set_title("Residuales Gaussiana Simple")
axs[0].legend()

# Residuales de la Suma de Gaussianas
axs[1].scatter(bin_centers, res_double, color='g', label=f'Residuales (RMSE={rmse_double:.2f})')
axs[1].axhline(0, color='black', linestyle='--')
axs[1].set_ylabel("Residuales")
axs[1].set_title("Residuales Suma de Gaussianas")
axs[1].legend()

# Residuales de la Gaussiana Asimétrica
axs[2].scatter(bin_centers, res_skew, color='b', label=f'Residuales (RMSE={rmse_skew:.2f})')
axs[2].axhline(0, color='black', linestyle='--')
axs[2].set_xlabel("Bin Center (cGy)")
axs[2].set_ylabel("Residuales")
axs[2].set_title("Residuales Gaussiana Asimétrica")
axs[2].legend()

plt.tight_layout()
plt.show()