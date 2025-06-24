# ellipsometry_project/simulation_maxwell_garnett.py

from __future__ import division, print_function, absolute_import
import numpy as np
import tmm
from tmm.tmm_core import ellips
from scipy import interpolate
import time
from ..data_handling import load_nk_data_maxwell_garnett, save_supervector_maxwell_garnett  # Importer le module

# Define a function for the air index
def air(long_onde):
    return 1 + 0j

def maxwell_garnett(fv, n1, k1, n2, k2):
    """
    Calculate the effective refractive index using the Maxwell Garnett theory.
    
    Parameters:
    - n1: Refractive index of the matrix (homogeneous phase).
    - n2: Refractive index of the dispersed phase.
    - fv: Volume fraction of the dispersed phase (0 < fv < 1).
    
    Returns:
    - n_eff: Effective refractive index of the composite.
    """
    perm2 = (n2 ** 2 - k2 ** 2) - 1j * (n2 * k2 * 2)  # permittivity of dispersed phase
    perm1 = (n1 ** 2 - k1 ** 2) - 1j * (n1 * k1 * 2)  # permittivity of matrix phase

    perm_effect = perm2 * (perm1 + 2 * perm2 + 2 * fv * (perm1 - perm2)) / (perm1 + 2 * perm2 - fv * (perm1 - perm2))  # Effective medium model

    n_eff = np.sqrt(0.5 * (perm_effect + np.sqrt(perm_effect.real ** 2 + (-perm_effect.imag) ** 2)))
    k_eff = np.sqrt(0.5 * (-perm_effect.real + np.sqrt(perm_effect.real ** 2 + (-perm_effect.imag) ** 2)))

    return n_eff, k_eff

def run_simulation_maxwell_garnett(dlam, angle=70, substrate='sicr.nk', layers=None, vfractions=None, nanoparticle_material='Au.nk'):
    """
    Simuler les données ellipsométriques en utilisant la théorie de Maxwell Garnett.

    Args:
    dlam -- Longueurs d'onde
    angle -- Angle d'incidence
    substrate -- Matériau du substrat
    layers -- Liste des couches

    Returns:
    Supervector -- Données simulées
    """
    if layers is None or vfractions is None:
        raise ValueError("Both layers and volume fractions must be defined.")

    material, thickness_range = layers

    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer, lam_p, n_pigment, k_pigment = load_nk_data_maxwell_garnett(substrate, material, nanoparticle_material)

    # Conversion
    lam_s *= 1000
    lam_layer *= 1000
    lam_p *= 1000

    # Créer des fonctions d'interpolation
    fsubs_r = interpolate.interp1d(lam_s, n_substrat)
    fsubs_i = interpolate.interp1d(lam_s, k_substrat)
    flayer_r = interpolate.interp1d(lam_layer, n_layer)
    flayer_i = interpolate.interp1d(lam_layer, k_layer)
    fpigment_r = interpolate.interp1d(lam_p, n_pigment)
    fpigment_i = interpolate.interp1d(lam_p, k_pigment)

    # Filtrer les longueurs d'onde qui sont en dehors des bornes des données interpolées
    min_wavelength = max(np.min(lam_s), np.min(lam_layer), np.min(lam_p))
    max_wavelength = min(np.max(lam_s), np.max(lam_layer), np.max(lam_p))
    filtered_dlam = dlam[(dlam >= min_wavelength) & (dlam <= max_wavelength)]

    if len(filtered_dlam) == 0:
        raise ValueError(f"All wavelengths in dlam are out of bounds. Valid range: {min_wavelength} to {max_wavelength} nm")

    # Init parameters
    degree = np.pi / 180
    angle_rad = angle * degree
    nwave = np.size(filtered_dlam)
    supervector = np.zeros((2 * nwave, len(thickness_range), len(vfractions)))

    # Timer
    time0 = time.perf_counter()

    # Calculate Ellipso
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

    # Stop timer
    time1 = time.perf_counter()
    dtime = time1 - time0
    print(" *** Generation time", dtime, " sec")

    save_supervector_maxwell_garnett(supervector, thickness_range, vfractions, filtered_dlam)
    return supervector

if __name__ == "__main__":
    # Exemple d'appel avec des paramètres spécifiques
    dlam = np.linspace(300, 1000, 351)  # Longueurs d'onde
    angle = 70  # Angle d'incidence
    substrate = 'sicr.nk'
    layers = ('sio2.nk', np.linspace(0, 600, 601))  # Matériaux et plages d'épaisseur
    vfractions = [0.001, 0.01, 0.05]  # Exemples de fractions volumiques
    run_simulation_maxwell_garnett(dlam, angle, substrate, layers, vfractions)
