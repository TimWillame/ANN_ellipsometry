# ellipsometry_project/simulation.py

from __future__ import division, print_function, absolute_import
import numpy as np
import tmm
from tmm.tmm_core import ellips
from scipy import interpolate
import time
from ..data_handling import load_nk_data, save_supervector, load_wavelengths

def air(wavelength):
    """
    Return refractive index of air.

    Args:
        wavelength (float or array): Wavelength(s) in nm.

    Returns:
        complex: Refractive index of air (1 + 0j).
    """
    return 1 + 0j

def run_simulation(dlam, angle=70, substrate='sicr.nk', layers=None):
    """
    Simulate ellipsometric data for a given material layer on a substrate.

    Args:
        dlam (np.ndarray): Array of wavelengths in nm.
        angle (float, optional): Incidence angle in degrees. Default is 70.
        substrate (str, optional): Filename for substrate optical constants. Default 'sicr.nk'.
        layers (tuple, optional): Tuple with (material filename, thickness_range array).

    Returns:
        np.ndarray: Supervector containing simulated Psi and Delta values.
                    Shape: (2 * number of wavelengths, number of thickness points).
    """
    if layers is None:
        raise ValueError("Layer must be defined with a material and a thickness range.")

    material, thickness_range = layers

    # Load optical constants for substrate and layer
    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer = load_nk_data(substrate, material)

    # Convert from micrometers to nanometers
    lam_s *= 1000
    lam_layer *= 1000

    # Create interpolation functions for real and imaginary parts of refractive indices
    fsubs_r = interpolate.interp1d(lam_s, n_substrat)
    fsubs_i = interpolate.interp1d(lam_s, k_substrat)
    flayer_r = interpolate.interp1d(lam_layer, n_layer)
    flayer_i = interpolate.interp1d(lam_layer, k_layer)

    # Filter wavelengths to valid interpolation range
    min_wavelength = max(np.min(lam_s), np.min(lam_layer))
    max_wavelength = min(np.max(lam_s), np.max(lam_layer))
    filtered_dlam = dlam[(dlam >= min_wavelength) & (dlam <= max_wavelength)]

    if len(filtered_dlam) == 0:
        raise ValueError(f"All wavelengths in dlam are out of bounds. Valid range: {min_wavelength} to {max_wavelength} nm")

    degree = np.pi / 180
    angle_rad = angle * degree
    nwave = filtered_dlam.size
    supervector = np.zeros((2 * nwave, thickness_range.size))

    start_time = time.perf_counter()

    # Calculate ellipsometric parameters Psi and Delta for each thickness and wavelength
    for jj, thickness in enumerate(thickness_range):
        psis = np.zeros(nwave)
        deltas = np.zeros(nwave)
        for ii, wave in enumerate(filtered_dlam):
            n_layer_complex = flayer_r(wave) + 1j * flayer_i(wave)
            n_substrate_complex = fsubs_r(wave) + 1j * fsubs_i(wave)
            n_list = [air(wave), n_layer_complex, n_substrate_complex]
            e_data = ellips(n_list, [np.inf, thickness, np.inf], angle_rad, wave)
            psis[ii] = e_data['psi'] / degree
            deltas[ii] = e_data['Delta'] / degree
        supervector[0:nwave, jj] = psis
        supervector[nwave:2 * nwave, jj] = deltas

    end_time = time.perf_counter()
    print(f"*** Generation time: {end_time - start_time:.4f} sec")

    # Save simulation results
    save_supervector(supervector, thickness_range, filtered_dlam)

    return supervector

if __name__ == "__main__":
    dlam = np.linspace(400, 700, 301)
    run_simulation(dlam, layers=('sio2.nk', np.array([50, 100, 150, 200, 250])))
