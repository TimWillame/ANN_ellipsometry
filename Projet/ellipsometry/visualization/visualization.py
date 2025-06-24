from __future__ import division, print_function, absolute_import
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from ..data_handling import load_wavelengths, load_nk_data

# Load necessary data
def load_data(substrate_material, layer_material):
    """Charger les données pour le substrat et la couche
    args:
    substrate_material -- Nom du fichier
    layer_material -- Nom du fichier
    
    Return:
    Tuple contenant les données (longueurs d'onde, n, k)
    """
    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer = load_nk_data(substrate_material, layer_material)
    return lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer

# Visualization function
def visualize_results(ax, canvas, supervector, thickness_range, thickness_index, dlam):
    """
    Visualiser les résultats ellipsométriques pour une épaisseur sélectionnée.
    
    Args:
    ax -- L'axe matplotlib où les résultats seront tracés
    canvas -- Le canvas de l'interface graphique pour mettre à jour le graphique
    supervector -- Les données ellipsométriques simulées (Psi et Delta)
    thickness_range -- Liste des épaisseurs utilisées pour la simulation
    thickness_index -- Index de l'épaisseur sélectionnée dans thickness_range
    dlam -- Longueurs d'onde utilisées pour la simulation
    """
    ax.clear()
    nwave = np.size(dlam)

    # Vérifie que l'index est valide
    if thickness_index < 0 or thickness_index >= len(thickness_range):
        print("Index d'épaisseur non valide")
        return

    # Get Psi and Delta data for the selected thickness
    psis = supervector[:nwave, thickness_index]
    deltas = supervector[nwave:2 * nwave, thickness_index]

    # Plot Psi and Delta
    ax.plot(dlam, psis, '-r', label='Psi')
    ax.plot(dlam, deltas, '-b', label='Delta')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('ψ (red), Δ (blue)')
    thickness_value = thickness_range[thickness_index]
    ax.set_title(f'Ellipsometric Data for Thickness {thickness_value} nm')
    ax.legend()

    canvas.draw()

def visualize_results_maxwell_garnett(ax, canvas, supervector, thickness_range, thickness_index, vfractions, vf_index, dlam):
    """
    Visualiser les résultats ellipsométriques pour une épaisseur et une fraction volumique sélectionnées.
    
    Args:
    ax -- L'axe matplotlib où les résultats seront tracés
    canvas -- Le canvas de l'interface graphique pour mettre à jour le graphique
    supervector -- Les données ellipsométriques simulées (Psi et Delta)
    thickness_range -- Liste des épaisseurs utilisées pour la simulation
    thickness_index -- Index de l'épaisseur sélectionnée dans thickness_range
    vfractions -- Liste des fractions volumiques utilisées pour la simulation
    vf_index -- Index de la fraction volumique sélectionnée dans vfractions
    dlam -- Longueurs d'onde utilisées pour la simulation
    """
    ax.clear()
    nwave = np.size(dlam)

    # Get Psi and Delta data for the selected thickness and volume fraction
    psis = supervector[:nwave, thickness_index, vf_index]
    deltas = supervector[nwave:2 * nwave, thickness_index, vf_index]

    # Plot Psi and Delta
    ax.plot(dlam, psis, '-r', label='Psi')
    ax.plot(dlam, deltas, '-b', label='Delta')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('ψ (red), Δ (blue)')
    
    thickness_value = thickness_range[thickness_index]
    vf_value = vfractions[vf_index] * 100
    ax.set_title(f'Ellipsometric Data for Thickness {thickness_value} nm, {vf_value}% Volume Fraction')
    ax.legend()

    # Update the canvas with the new plot
    canvas.draw()

def visualize_results_lorentzian(ax, canvas, supervector, thickness_range, thickness_index, lorentz_params_list, lorentz_index, dlam):
    """
    Visualiser les résultats ellipsométriques pour une épaisseur et un jeu de paramètres lorentziens sélectionnés.
    
    Args:
    ax -- L'axe matplotlib où les résultats seront tracés
    canvas -- Le canvas de l'interface graphique pour mettre à jour le graphique
    supervector -- Les données ellipsométriques simulées (Psi et Delta)
    thickness_range -- Liste des épaisseurs utilisées pour la simulation
    thickness_index -- Index de l'épaisseur sélectionnée dans thickness_range
    lorentz_params_list -- Liste des jeux de paramètres Lorentzienne [(lambda0, gamma, amplitude), ...]
    dlam -- Longueurs d'onde utilisées pour la simulation
    """
    ax.clear()
    nwave = np.size(dlam)

    # Sélectionner les paramètres lorentziens (choisissez l'indice de votre jeu de paramètres)
    lorentz_params = lorentz_params_list[lorentz_index]  # Ici on prend le premier jeu de paramètres lorentziens, vous pouvez ajuster selon votre besoin.

    # Obtenez Psi et Delta pour l'épaisseur et le paramètre lorentzien sélectionnés
    psis = supervector[:nwave, thickness_index, lorentz_index]  # Psi pour le premier jeu de paramètres lorentziens
    deltas = supervector[nwave:2 * nwave, thickness_index, lorentz_index]  # Delta pour le premier jeu de paramètres lorentziens

    # Tracer Psi et Delta
    ax.plot(dlam, psis, '-r', label='Psi')
    ax.plot(dlam, deltas, '-b', label='Delta')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('ψ (red), Δ (blue)')
    
    # Utilisation de l'épaisseur et des paramètres lorentziens pour le titre
    thickness_value = thickness_range[thickness_index]
    lambda0 = round(lorentz_params[0], 2)  # Arrondi à 2 décimales
    gamma = round(lorentz_params[1], 2)    # Arrondi à 2 décimales
    amplitude = round(lorentz_params[2], 2) 
    ax.set_title(f'Ellipsometric Data for Thickness {thickness_value} nm\nLorentzian Params: λ0={lambda0} nm, γ={gamma} nm, Amplitude={amplitude}')
    ax.legend()

    # Mise à jour du canvas avec le nouveau graphique
    canvas.draw()
