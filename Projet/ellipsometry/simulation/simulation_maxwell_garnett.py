# ellipsometry_project/simulation_maxwell_garnett.py

from __future__ import division, print_function, absolute_import
import numpy as np
import tmm
from tmm.tmm_core import ellips
from scipy import interpolate
import time
from ..data_handling import load_nk_data_maxwell_garnett, save_supervector_maxwell_garnett


def air(wavelength):
    """
    Refractive index of air (constant).

    Parameters
    ----------
    wavelength : float or array
        Wavelength(s) in nm (not used here but kept for interface consistency).

    Returns
    -------
    complex
        Complex refractive index of air (1 + 0j).
    """
    return 1 + 0j


def maxwell_garnett(fv, n1, k1, n2, k2):
    """
    Calculate the effective refractive index of a composite using Maxwell Garnett theory.

    Parameters
    ----------
    fv : float
        Volume fraction of the dispersed phase (0 < fv < 1).
    n1, k1 : float or array
        Refractive index (real and imaginary parts) of the matrix phase.
    n2, k2 : float or array
        Refractive index (real and imaginary parts) of the dispersed phase.

    Returns
    -------
    n_eff, k_eff : complex or arrays
        Effective refractive index (real and imaginary parts) of the composite material.
    """
    perm2 = (n2 ** 2 - k2 ** 2) - 1j * (2 * n2 * k2)
    perm1 = (n1 ** 2 - k1 ** 2) - 1j * (2 * n1 * k1)

    perm_effect = perm2 * (perm1 + 2 * perm2 + 2 * fv * (perm1 - perm2)) / (perm1 + 2 * perm2 - fv * (perm1 - perm2))

    n_eff = np.sqrt(0.5 * (perm_effect + np.sqrt(perm_effect.real ** 2 + perm_effect.imag ** 2)))
    k_eff = np.sqrt(0.5 * (-perm_effect.real + np.sqrt(perm_effect.real ** 2 + perm_effect.imag ** 2)))

    return n_eff, k_eff


def run_simulation_maxwell_garnett(dlam, angle=70, substrate='sicr.nk', layers=None, vfractions=None, nanoparticle_material='Au.nk'):
    """
    Simulate ellipsometric data using Maxwell Garnett effective medium theory.

    Parameters
    ----------
    dlam : array-like
        Wavelengths in nm at which to simulate.
    angle : float, optional
        Incident angle in degrees (default is 70).
    substrate : str, optional
        Substrate material filename (default is 'sicr.nk').
    layers : tuple or list, optional
        Tuple containing (material, thickness_range).
    vfractions : array-like, optional
        List or array of volume fractions of dispersed phase.
    nanoparticle_material : str, optional
        Filename of nanoparticle material optical constants (default is 'Au.nk').

    Returns
    -------
    supervector : ndarray
        Simulated ellipsometric data array of shape (2 * nwave, number_of_thicknesses, number_of_vfractions).
    """
    if layers is None or vfractions is None:
        raise ValueError("Both layers and volume fractions must be defined.")

    material, thickness_range = layers

    # Load optical constants for substrate, matrix, and nanoparticle
    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer, lam_p, n_pigment, k_pigment = load_nk_data_maxwell_garnett(
        substrate, material, nanoparticle_material)

    # Convert from microns to nm
    lam_s *= 1000
    lam_layer *= 1000
    lam_p *= 1000

    # Create interpolation functions for optical constants
    fsubs_r = interpolate.interp1d(lam_s, n_substrat)
    fsubs_i = interpolate.interp1d(lam_s, k_substrat)
    flayer_r = interpolate.interp1d(lam_layer, n_layer)
    flayer_i = interpolate.interp1d(lam_layer, k_layer)
    fpigment_r = interpolate.interp1d(lam_p, n_pigment)
    fpigment_i = interpolate.interp1d(lam_p, k_pigment)

    # Filter wavelengths within valid interpolation range
    min_wavelength = max(np.min(lam_s), np.min(lam_layer), np.min(lam_p))
    max_wavelength = min(np.max(lam_s), np.max(lam_layer), np.max(lam_p))
    filtered_dlam = dlam[(dlam >= min_wavelength) & (dlam <= max_wavelength)]

    if len(filtered_dlam) == 0:
        raise ValueError(f"All wavelengths in dlam are out of bounds. Valid range: {min_wavelength} to {max_wavelength} nm")

    # Initialize simulation parameters
    degree = np.pi / 180
    angle_rad = angle * degree
    nwave = np.size(filtered_dlam)
    supervector = np.zeros((2 * nwave, len(thickness_range), len(vfractions)))

    # Simulation loop over thickness and volume fraction
    start_time = time.perf_counter()
    for jj, thickness in enumerate(thickness_range):
        for kk, vf in enumerate(vfractions):
            psis = np.zeros(nwave)
            deltas = np.zeros(nwave)
            for ii, wave in enumerate(filtered_dlam):
                n_eff, k_eff = maxwell_garnett(vf, fpigment_r(wave), fpigment_i(wave), flayer_r(wave), flayer_i(wave))
                indice_layer = n_eff + 1j * k_eff
                indice_substrate = fsubs_r(wave) + 1j * fsubs_i(wave)
                n_list = [air(wave), indice_layer, indice_substrate]
                e_data = ellips(n_list, [np.inf, thickness, np.inf], angle_rad, wave)
                psis[ii] = e_data['psi'] / degree
                deltas[ii] = e_data['Delta'] / degree

            supervector[0:nwave, jj, kk] = psis
            supervector[nwave:2 * nwave, jj, kk] = deltas
    end_time = time.perf_counter()

    print(f" *** Generation time {end_time - start_time:.3f} sec")

    save_supervector_maxwell_garnett(supervector, thickness_range, vfractions, filtered_dlam)
    return supervector


if __name__ == "__main__":
    # Example call with parameters
    dlam = np.linspace(300, 1000, 351)  # wavelengths in nm
    angle = 70  # incident angle in degrees
    substrate = 'sicr.nk'
    layers = ('sio2.nk', np.linspace(0, 600, 601))  # material and thickness range in nm
    vfractions = [0.001, 0.01, 0.05]  # volume fractions
    run_simulation_maxwell_garnett(dlam, angle, substrate, layers, vfractions)
