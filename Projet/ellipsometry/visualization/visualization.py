from __future__ import division, print_function, absolute_import
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from ..data_handling import load_wavelengths, load_nk_data

# --- Data Loading ---

def load_data(substrate_material, layer_material):
    """
    Load optical data for substrate and layer materials.

    Args:
        substrate_material (str): Filename or identifier for substrate material data.
        layer_material (str): Filename or identifier for layer material data.

    Returns:
        tuple: 
            lam_s (np.ndarray): Wavelengths for substrate.
            n_substrate (np.ndarray): Refractive index (n) of substrate.
            k_substrate (np.ndarray): Extinction coefficient (k) of substrate.
            lam_layer (np.ndarray): Wavelengths for layer.
            n_layer (np.ndarray): Refractive index (n) of layer.
            k_layer (np.ndarray): Extinction coefficient (k) of layer.
    """
    lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer = load_nk_data(substrate_material, layer_material)
    return lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer


# --- Visualization Functions ---

def visualize_results(ax, canvas, supervector, thickness_range, thickness_index, dlam):
    """
    Plot ellipsometric Psi and Delta for a selected thickness.

    Args:
        ax (matplotlib.axes.Axes): Matplotlib axis to plot on.
        canvas (object): GUI canvas object with a draw() method to update the plot.
        supervector (np.ndarray): Ellipsometric data array containing Psi and Delta.
        thickness_range (list or np.ndarray): List of thickness values used in the simulation.
        thickness_index (int): Index of the selected thickness in thickness_range.
        dlam (np.ndarray): Wavelength values corresponding to the data.

    Returns:
        None
    """
    ax.clear()
    nwave = np.size(dlam)

    if thickness_index < 0 or thickness_index >= len(thickness_range):
        print("Invalid thickness index")
        return

    psis = supervector[:nwave, thickness_index]
    deltas = supervector[nwave:2 * nwave, thickness_index]

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
    Plot ellipsometric Psi and Delta for selected thickness and volume fraction.

    Args:
        ax (matplotlib.axes.Axes): Matplotlib axis to plot on.
        canvas (object): GUI canvas object with a draw() method to update the plot.
        supervector (np.ndarray): Ellipsometric data array containing Psi and Delta.
        thickness_range (list or np.ndarray): List of thickness values used in the simulation.
        thickness_index (int): Index of the selected thickness in thickness_range.
        vfractions (list or np.ndarray): List of volume fractions used in the simulation.
        vf_index (int): Index of the selected volume fraction in vfractions.
        dlam (np.ndarray): Wavelength values corresponding to the data.

    Returns:
        None
    """
    ax.clear()
    nwave = np.size(dlam)

    psis = supervector[:nwave, thickness_index, vf_index]
    deltas = supervector[nwave:2 * nwave, thickness_index, vf_index]

    ax.plot(dlam, psis, '-r', label='Psi')
    ax.plot(dlam, deltas, '-b', label='Delta')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('ψ (red), Δ (blue)')
    thickness_value = thickness_range[thickness_index]
    vf_value = vfractions[vf_index] * 100  # convert to percentage
    ax.set_title(f'Ellipsometric Data for Thickness {thickness_value} nm, {vf_value:.1f}% Volume Fraction')
    ax.legend()
    canvas.draw()


def visualize_results_lorentzian(ax, canvas, supervector, thickness_range, thickness_index, lorentz_params_list, lorentz_index, dlam):
    """
    Plot ellipsometric Psi and Delta for selected thickness and Lorentzian parameters.

    Args:
        ax (matplotlib.axes.Axes): Matplotlib axis to plot on.
        canvas (object): GUI canvas object with a draw() method to update the plot.
        supervector (np.ndarray): Ellipsometric data array containing Psi and Delta.
        thickness_range (list or np.ndarray): List of thickness values used in the simulation.
        thickness_index (int): Index of the selected thickness in thickness_range.
        lorentz_params_list (list of tuples): List of Lorentzian parameter sets, each tuple as (lambda0, gamma, amplitude).
        lorentz_index (int): Index of the selected Lorentzian parameter set.
        dlam (np.ndarray): Wavelength values corresponding to the data.

    Returns:
        None
    """
    ax.clear()
    nwave = np.size(dlam)

    lorentz_params = lorentz_params_list[lorentz_index]

    psis = supervector[:nwave, thickness_index, lorentz_index]
    deltas = supervector[nwave:2 * nwave, thickness_index, lorentz_index]

    ax.plot(dlam, psis, '-r', label='Psi')
    ax.plot(dlam, deltas, '-b', label='Delta')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('ψ (red), Δ (blue)')
    
    thickness_value = thickness_range[thickness_index]
    lambda0 = round(lorentz_params[0], 2)
    gamma = round(lorentz_params[1], 2)
    amplitude = round(lorentz_params[2], 2)
    ax.set_title(
        f'Ellipsometric Data for Thickness {thickness_value} nm\n'
        f'Lorentzian Params: λ0={lambda0} nm, γ={gamma} nm, Amplitude={amplitude}'
    )
    ax.legend()
    canvas.draw()
