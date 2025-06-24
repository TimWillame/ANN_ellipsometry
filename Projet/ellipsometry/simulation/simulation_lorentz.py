import os
import numpy as np
from scipy import interpolate
import time
from tmm.tmm_core import ellips
from ..data_handling import load_nk_data, save_supervector_lorentzian


def air(wavelength):
    """
    Returns the refractive index of air (assumed constant).

    Parameters
    ----------
    wavelength : float or array
        Wavelength(s) in nm.

    Returns
    -------
    complex
        Refractive index of air (1 + 0j).
    """
    return 1 + 0j


def lorentzian_contribution(wavelengths, amplitude, lambda0, gamma):
    """
    Calculate Lorentzian contribution to the complex refractive index.

    Parameters
    ----------
    wavelengths : array_like
        Wavelength values (nm).
    amplitude : float
        Amplitude parameter of the Lorentzian.
    lambda0 : float
        Central wavelength of the Lorentzian (nm).
    gamma : float
        Broadening parameter (nm).

    Returns
    -------
    numpy.ndarray
        Complex Lorentzian permittivity contribution.
    """
    w2 = wavelengths ** 2
    l02 = lambda0 ** 2
    gam2 = gamma ** 2
    eps_real = amplitude * w2 * (w2 - l02) / ((w2 - l02) ** 2 + gam2 * w2)
    eps_imag = amplitude * wavelengths ** 3 * gamma / ((w2 - l02) ** 2 + gam2 * w2)
    return eps_real + 1j * eps_imag


def run_simulation_lorentzien(dlam, angle=70, substrate='sicr.nk', layers=None, nanoparticle_material='Au.nk'):
    """
    Simulate ellipsometric data including Lorentzian contributions to the refractive index.

    Parameters
    ----------
    dlam : array_like
        Wavelength range (nm).
    angle : float, optional
        Incidence angle in degrees (default is 70).
    substrate : str, optional
        Filename for substrate refractive index data (default is 'sicr.nk').
    layers : tuple, optional
        Tuple containing (material filename, thickness array).
    nanoparticle_material : str, optional
        Material of nanoparticles ('Au.nk' or 'Ag.nk').

    Returns
    -------
    supervector : numpy.ndarray
        Simulated ellipsometric data with shape (2 * nwave, num_thickness, num_lorentz_params).
    lorentz_params_sets : list of tuples
        List of Lorentzian parameter sets (lambda0, gamma, amplitude) used in simulation.
    """
    if layers is None:
        raise ValueError("Layer must be defined with a material and a thickness range.")

    material, thickness_range = layers

    # Load refractive index data for substrate and layer
    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer = load_nk_data(substrate, material)

    # Convert wavelengths from microns to nm
    lam_s *= 1000
    lam_layer *= 1000

    # Interpolate refractive indices
    fsubs_r = interpolate.interp1d(lam_s, n_substrat)
    fsubs_i = interpolate.interp1d(lam_s, k_substrat)
    flayer_r = interpolate.interp1d(lam_layer, n_layer)
    flayer_i = interpolate.interp1d(lam_layer, k_layer)

    # Filter wavelengths within interpolation bounds
    min_wavelength = max(np.min(lam_s), np.min(lam_layer))
    max_wavelength = min(np.max(lam_s), np.max(lam_layer))
    filtered_dlam = dlam[(dlam >= min_wavelength) & (dlam <= max_wavelength)]

    if len(filtered_dlam) == 0:
        raise ValueError(f"All wavelengths are out of interpolation bounds: {min_wavelength} to {max_wavelength} nm")

    # Set Lorentzian parameters for Au or Ag nanoparticles
    if nanoparticle_material == 'Au.nk':
        lambda0 = 500
        gamma = 50
        amplitude = 0.150
    elif nanoparticle_material == 'Ag.nk':
        lambda0 = 405
        gamma = 40
        amplitude = 0.150
    else:
        raise ValueError("Invalid nanoparticle material. Choose 'Au.nk' or 'Ag.nk'.")

    # Generate multiple Lorentzian parameter sets with noise
    lorentz_params_sets = []
    num_params_sets = 30
    for _ in range(num_params_sets):
        R = np.random.uniform(10, 100)
        perturbed_lambda0 = lambda0 + 0.6 * (R - 10) ** 0.9
        perturbed_gamma = gamma + 0.2 * (R - 10) ** 1.1
        perturbed_amplitude = amplitude + 0.0025 * R - 0.000015 * R ** 2
        perturbed_gamma = max(perturbed_gamma, 1)
        perturbed_amplitude = max(perturbed_amplitude, 0.01)
        lorentz_params_sets.append((perturbed_lambda0, perturbed_gamma, perturbed_amplitude))

    # Initialize supervector to store psi and delta for each thickness and parameter set
    nwave = filtered_dlam.size
    num_thickness = thickness_range.size
    supervector = np.zeros((2 * nwave, num_thickness, num_params_sets))

    time0 = time.perf_counter()

    # Compute ellipsometric parameters for each thickness and Lorentzian parameter set
    for jj, thickness in enumerate(thickness_range):
        for zz, (lambda0_p, gamma_p, amplitude_p) in enumerate(lorentz_params_sets):
            psis = np.zeros(nwave)
            deltas = np.zeros(nwave)

            lorentzian_eps = lorentzian_contribution(filtered_dlam, amplitude_p, lambda0_p, gamma_p)
            lorentzian_nk = np.sqrt(0.5 * (np.abs(lorentzian_eps) + np.real(lorentzian_eps))) - \
                            1j * np.sqrt(0.5 * (np.abs(lorentzian_eps) - np.real(lorentzian_eps)))

            for ii, wave in enumerate(filtered_dlam):
                indice_layer = flayer_r(wave) + 1j * flayer_i(wave) + lorentzian_nk[ii]
                indice_substrate = fsubs_r(wave) + 1j * fsubs_i(wave)
                n_list = [air(wave), indice_layer, indice_substrate]

                e_data = ellips(n_list, [np.inf, thickness, np.inf], angle * np.pi / 180, wave)
                psis[ii] = e_data['psi'] * 180 / np.pi
                deltas[ii] = e_data['Delta'] * 180 / np.pi

            supervector[0:nwave, jj, zz] = psis
            supervector[nwave:2 * nwave, jj, zz] = deltas

    time1 = time.perf_counter()
    print(" *** Generation time:", time1 - time0, "sec")
    print(f"Number of Lorentzian parameter sets: {len(lorentz_params_sets)}")

    # Save results
    save_supervector_lorentzian(supervector, thickness_range, filtered_dlam, lorentz_params_sets)

    return supervector, lorentz_params_sets
