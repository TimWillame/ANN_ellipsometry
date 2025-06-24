import os
import numpy as np
from scipy.optimize import curve_fit
from scipy import interpolate
import matplotlib.pyplot as plt
from .simulation_maxwell_garnett import maxwell_garnett
from ..data_handling import load_nk_data_maxwell_garnett, load_nk_data, save_supervector_lorentzian
from datetime import datetime
import pandas as pd 
import time
import tmm
from tmm.tmm_core import ellips
import numpy as np
from ..data_handling import load_nk_data, save_supervector_lorentzian

def air(long_onde):
    return 1 + 0j

def lorentzian_contribution(wavelengths, amplitude, lambda0, gamma):
    """ Calcule la contribution lorentzienne à l'indice de réfraction complexe. """
    w2 = wavelengths ** 2
    w3 = wavelengths ** 3
    l02 = lambda0 ** 2
    gam2 = gamma ** 2
    eps_real = amplitude * w2 * (w2 - l02) / ((w2 - l02) ** 2 + gam2 * w2)
    eps_imag = amplitude * w3 * gamma / ((w2 - l02) ** 2 + gam2 * w2)
    return eps_real + 1j * eps_imag


def run_simulation_lorentzien(dlam, angle=70, substrate='sicr.nk', layers=None, nanoparticle_material='Au.nk'):
    """
    Simuler les données ellipsométriques avec la contribution lorentzienne.
    """
    if layers is None:
        raise ValueError("Layer must be defined with a material and a thickness range.")
    material, thickness_range = layers

    # Charger les données de l'indice de réfraction
    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer = load_nk_data(substrate, material)
    
    # Conversion nm → microns
    lam_s *= 1000
    lam_layer *= 1000

    # Interpolation des indices
    fsubs_r = interpolate.interp1d(lam_s, n_substrat)
    fsubs_i = interpolate.interp1d(lam_s, k_substrat)
    flayer_r = interpolate.interp1d(lam_layer, n_layer)
    flayer_i = interpolate.interp1d(lam_layer, k_layer)

    # Filtrage des longueurs d'onde
    min_wavelength = max(np.min(lam_s), np.min(lam_layer))
    max_wavelength = min(np.max(lam_s), np.max(lam_layer))
    filtered_dlam = dlam[(dlam >= min_wavelength) & (dlam <= max_wavelength)]

    if len(filtered_dlam) == 0:
        raise ValueError(f"All wavelengths in dlam are out of bounds. Valid range: {min_wavelength} to {max_wavelength} nm")

    # Définir les paramètres lorentziens pour Au ou Ag
    if nanoparticle_material == 'Au.nk':
        lambda0 = 500  # nm
        gamma = 50  # nm
        amplitude = 0.150
    elif nanoparticle_material == 'Ag.nk':
        lambda0 = 405  # nm
        gamma = 40  # nm
        amplitude = 0.150
    else:
        raise ValueError("Invalid nanoparticle material. Choose 'Au.nk' or 'Ag.nk'.")

    # Initialiser une liste pour stocker les jeux de paramètres lorentziens
    lorentz_params_sets = []
    num_params_sets = 30  # Nombre de jeux de paramètres à générer (peut être ajusté)
    
    for _ in range(num_params_sets):
        # Ajouter du bruit aux paramètres de la Lorentzienne
        R = np.random.uniform(10, 100)
        perturbed_lambda0 = lambda0 + 0.6 * (R - 10)**0.9               # Redshift non-linéaire
        perturbed_gamma = gamma + 0.2 * (R - 10)**1.1                   # Élargissement plus rapide
        perturbed_amplitude = amplitude + 0.0025 * R - 0.000015 * R**2
        # perturbed_lambda0 = lambda0 + np.random.uniform(-50, 50)
        # perturbed_gamma = gamma + np.random.uniform(-10, 10)
        # perturbed_amplitude = amplitude + np.random.uniform(0.05, 0.2)
        perturbed_gamma = max(perturbed_gamma, 1)
        perturbed_amplitude = max(perturbed_amplitude, 0.01)
        lorentz_params_sets.append((perturbed_lambda0, perturbed_gamma, perturbed_amplitude))




    # Initialisation du supervecteur 3D
    nwave = np.size(filtered_dlam)
    num_thickness = np.size(thickness_range)
    num_params_sets = len(lorentz_params_sets)
    supervector = np.zeros((2 * nwave, num_thickness, num_params_sets))

    # Chronomètre
    time0 = time.perf_counter()

    # Calcul des ellipsométries pour chaque épaisseur et chaque jeu de paramètres lorentziens
    for jj, thickness in enumerate(thickness_range):
        for zz, (lambda0, gamma, amplitude) in enumerate(lorentz_params_sets):
            psis = np.zeros(nwave)
            deltas = np.zeros(nwave)
            lorentzian_eps = lorentzian_contribution(filtered_dlam, amplitude, lambda0, gamma)
            lorentzian_nk = np.sqrt(0.5 * (np.abs(lorentzian_eps) + np.real(lorentzian_eps))) - 1j * np.sqrt(0.5 * (np.abs(lorentzian_eps) - np.real(lorentzian_eps)))

            for ii, wave in enumerate(filtered_dlam):
                indice_layer = flayer_r(wave) + 1j * flayer_i(wave) + lorentzian_nk[ii]
                indice_substrate = fsubs_r(wave) + 1j * fsubs_i(wave)
                n_list = [air(wave), indice_layer, indice_substrate]
                e_data = ellips(n_list, [np.inf, thickness, np.inf], angle * np.pi / 180, wave)
                psis[ii] = e_data['psi'] / np.pi * 180  # Conversion en degrés
                deltas[ii] = e_data['Delta'] / np.pi * 180  # Conversion en degrés

            # Stocker les résultats dans le supervecteur 3D
            supervector[0:nwave, jj, zz] = psis
            supervector[nwave:2 * nwave, jj, zz] = deltas

    # Temps écoulé
    time1 = time.perf_counter()
    dtime = time1 - time0
    print(" *** Generation time", dtime, " sec")

    print(f"Size of lorentz_params_list: {len(lorentz_params_sets)}")


    # Sauvegarde des résultats
    save_supervector_lorentzian(supervector, thickness_range, filtered_dlam, lorentz_params_sets)

    return supervector, lorentz_params_sets
