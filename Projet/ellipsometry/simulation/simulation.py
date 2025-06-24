# ellipsometry_project/simulation.py

from __future__ import division, print_function, absolute_import
import numpy as np
import tmm
from tmm.tmm_core import ellips
from scipy import interpolate
import time
from ..data_handling import load_nk_data, save_supervector, load_wavelengths  # Importer le module

# Define a function for the air index
def air(long_onde):
    return 1 + 0j

# Function for simulation
def run_simulation(dlam, angle=70, substrate='sicr.nk', layers=None):
    """
    Simuler les données ellipsométriques.

    Args:
    dlam -- longueurs d'onde
    angle -- Angle d'incidence
    substrate -- Matériau du substrat
    layers -- liste avec un tuple (matériau, plage d'épaisseur)

    Return:
    Supervector -- Données simulées
    """

    if layers is None:
        raise ValueError("Layer must be defined with a material and a thickness range.")
    print(f"layers: {layers}")
    material, thickness_range = layers

    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer = load_nk_data(substrate, material)

    # Conversion
    lam_s *= 1000
    lam_layer *= 1000

    # Créer des fonctions d'interpolation
    fsubs_r = interpolate.interp1d(lam_s, n_substrat)
    fsubs_i = interpolate.interp1d(lam_s, k_substrat)
    flayer_r = interpolate.interp1d(lam_layer, n_layer)
    flayer_i = interpolate.interp1d(lam_layer, k_layer)

    # Filtrer les longueurs d'onde qui sont en dehors des bornes des données interpolées
    min_wavelength = max(np.min(lam_s), np.min(lam_layer))
    max_wavelength = min(np.max(lam_s), np.max(lam_layer))
    filtered_dlam = dlam[(dlam >= min_wavelength) & (dlam <= max_wavelength)]

    if len(filtered_dlam) == 0:
        raise ValueError(f"All wavelengths in dlam are out of bounds. Valid range: {min_wavelength} to {max_wavelength} nm")

    # Init parameters
    degree = np.pi / 180
    angle_rad = angle * degree
    nwave = np.size(filtered_dlam)
    supervector = np.zeros((2 * nwave, np.size(thickness_range)))

    # Timer
    time0 = time.perf_counter()

    # Calculate Ellipso
    for jj, thickness in enumerate(thickness_range):
        psis = np.zeros(nwave)
        deltas = np.zeros(nwave)
        for ii, wave in enumerate(filtered_dlam):
            indice_layer = flayer_r(wave) + 1j * flayer_i(wave)
            indice_substrate = fsubs_r(wave) + 1j * fsubs_i(wave)
            n_list = [air(wave), indice_layer, indice_substrate]
            e_data = ellips(n_list, [np.inf, thickness, np.inf], angle_rad, wave)
            psis[ii] = e_data['psi'] / degree
            deltas[ii] = e_data['Delta'] / degree
        supervector[0:nwave, jj] = psis
        supervector[nwave:2 * nwave, jj] = deltas

    # Stop timer
    time1 = time.perf_counter()
    dtime = time1 - time0
    print(" *** Generation time", dtime, " sec")

    # Save data using the new module
    save_supervector(supervector, thickness_range, filtered_dlam)  # Sauvegarder les résultats avec le module
    return supervector

if __name__ == "__main__":
    dlam = np.linspace(400, 700, 301)
    run_simulation(dlam, layers=('sio2.nk', np.array([50, 100, 150, 200, 250])))