import numpy as np
import os
from datetime import datetime
import pandas as pd

def load_nk_data(substrate_file, layer_file):
    """
    Load refractive index data for substrate and layer.

    Args:
        substrate_file (str): Filename for substrate data (relative to assets/Materials).
        layer_file (str): Filename for layer data (relative to assets/Materials).

    Returns:
        tuple: (lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer)
            where each is a numpy array of wavelengths, refractive indices (n),
            and extinction coefficients (k) respectively.

    Raises:
        FileNotFoundError: If any input file is missing.
        ValueError: If data loading fails due to file content errors.
    """
    base_dir = os.path.dirname(__file__)
    nk_folder = os.path.join(base_dir, "..", "assets", "Materials")
    substrate_path = os.path.join(nk_folder, substrate_file)
    layer_path = os.path.join(nk_folder, layer_file)

    if not os.path.isfile(substrate_path):
        raise FileNotFoundError(f"Substrate file '{substrate_file}' not found.")
    if not os.path.isfile(layer_path):
        raise FileNotFoundError(f"Layer file '{layer_file}' not found.")

    try:
        lam_s, n_substrat, k_substrat = np.loadtxt(substrate_path, unpack=True)
        lam_layer, n_layer, k_layer = np.loadtxt(layer_path, unpack=True)
    except ValueError as e:
        raise ValueError(f"Error loading data from files: {e}")

    return lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer


def load_nk_data_maxwell_garnett(substrate_file, layer_file, nanoparticle_file):
    """
    Load refractive index data for substrate, layer, and nanoparticles for Maxwell-Garnett model.

    Args:
        substrate_file (str): Filename for substrate data.
        layer_file (str): Filename for layer data.
        nanoparticle_file (str): Filename for nanoparticle data.

    Returns:
        tuple: (lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer, lam_p, n_pigment, k_pigment)
            numpy arrays for wavelengths, refractive indices, and extinction coefficients.

    Raises:
        FileNotFoundError: If any input file is missing.
        ValueError: If data loading fails.
    """
    base_dir = os.path.dirname(__file__)
    nk_folder = os.path.join(base_dir, "..", "assets", "Materials")
    substrate_path = os.path.join(nk_folder, substrate_file)
    layer_path = os.path.join(nk_folder, layer_file)
    nanoparticle_path = os.path.join(nk_folder, nanoparticle_file)

    if not os.path.isfile(substrate_path):
        raise FileNotFoundError(f"Substrate file '{substrate_file}' not found.")
    if not os.path.isfile(layer_path):
        raise FileNotFoundError(f"Layer file '{layer_file}' not found.")
    if not os.path.isfile(nanoparticle_path):
        raise FileNotFoundError(f"Nanoparticle file '{nanoparticle_file}' not found.")

    try:
        lam_s, n_substrat, k_substrat = np.loadtxt(substrate_path, unpack=True)
        lam_layer, n_layer, k_layer = np.loadtxt(layer_path, unpack=True)
        lam_p, n_pigment, k_pigment = np.loadtxt(nanoparticle_path, unpack=True)
    except ValueError as e:
        raise ValueError(f"Error loading data from files: {e}")

    return lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer, lam_p, n_pigment, k_pigment


def save_supervector(supervector, thickness, dlam):
    """
    Save supervector data with thickness and wavelengths to a timestamped CSV file.

    Args:
        supervector (np.ndarray): 2D array containing psi and delta data.
        thickness (np.ndarray): 1D array of thickness values.
        dlam (np.ndarray): 1D array of wavelength values.

    Raises:
        IOError: If saving the file fails.
    """
    base_dir = os.path.dirname(__file__)
    results_path = os.path.join(base_dir, "..", "results")
    os.makedirs(results_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_folder = os.path.join(results_path, timestamp)
    os.makedirs(timestamped_folder, exist_ok=True)

    try:
        psi_values = supervector[0:len(dlam), :]
        delta_values = supervector[len(dlam):2 * len(dlam), :]

        rows = []
        for jj, thickness_value in enumerate(thickness):
            for ii in range(len(dlam)):
                rows.append([psi_values[ii, jj], delta_values[ii, jj], dlam[ii], thickness_value])

        df = pd.DataFrame(rows, columns=["psi", "delta", "wavelength", "thickness"])

        supervector_file = os.path.join(timestamped_folder, "supervector.csv")
        df.to_csv(supervector_file, index=False)

        print(" *** Data written successfully to 'results' folder ***")
    except Exception as e:
        raise IOError(f"Error saving data: {e}")


def save_supervector_maxwell_garnett(supervector, thickness, vfractions, dlam):
    """
    Save Maxwell-Garnett supervector data including volume fractions to CSV.

    Args:
        supervector (np.ndarray): 3D array of psi and delta data.
        thickness (np.ndarray): 1D array of thickness values.
        vfractions (np.ndarray): 1D array of volume fraction values.
        dlam (np.ndarray): 1D array of wavelength values.

    Raises:
        IOError: If saving fails.
    """
    base_dir = os.path.dirname(__file__)
    results_path = os.path.join(base_dir, "..", "results")
    os.makedirs(results_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_folder = os.path.join(results_path, timestamp)
    os.makedirs(timestamped_folder, exist_ok=True)

    try:
        rows = []
        for kk, vf in enumerate(vfractions):
            for jj, thickness_value in enumerate(thickness):
                for ii in range(supervector.shape[0] // 2):
                    psi_value = supervector[ii, jj, kk]
                    delta_value = supervector[ii + len(dlam), jj, kk]
                    rows.append([psi_value, delta_value, dlam[ii], thickness_value, vf])

        df = pd.DataFrame(rows, columns=["psi", "delta", "wavelength", "thickness", "vfraction"])

        supervector_file = os.path.join(timestamped_folder, "supervector_maxwell_garnett.csv")
        df.to_csv(supervector_file, index=False)

        print(" *** Data written successfully to 'results' folder ***")
    except Exception as e:
        raise IOError(f"Error saving data: {e}")


def load_wavelengths(filename):
    """
    Load wavelength data from a file in assets/wavelength directory.

    Args:
        filename (str): Name of the wavelength data file.

    Returns:
        np.ndarray: Array of wavelengths.

    Raises:
        FileNotFoundError: If file not found.
        ValueError: If file content cannot be loaded.
    """
    base_dir = os.path.dirname(__file__)
    wavelengths_folder = os.path.join(base_dir, "..", "assets", "wavelength")
    file_path = os.path.join(wavelengths_folder, filename)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Wavelengths file '{file_path}' not found.")

    try:
        dlam = np.loadtxt(file_path)
    except ValueError as e:
        raise ValueError(f"Error loading wavelengths from file: {e}")

    return dlam


def save_supervector_lorentzian(supervector, thickness, dlam, lorentz_params_list):
    """
    Save Lorentzian supervector data with parameters to CSV.

    Args:
        supervector (np.ndarray): 3D array of psi and delta values.
        thickness (np.ndarray): 1D array of thickness values.
        dlam (np.ndarray): 1D array of wavelength values.
        lorentz_params_list (list of tuples): List of Lorentzian parameters tuples 
                                              (lambda0, gamma, amplitude).

    Raises:
        IOError: If saving fails.
    """
    base_dir = os.path.dirname(__file__)
    results_path = os.path.join(base_dir, "..", "results")
    os.makedirs(results_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_folder = os.path.join(results_path, timestamp)
    os.makedirs(timestamped_folder, exist_ok=True)

    try:
        rows = []
        for zz, lorentz_params in enumerate(lorentz_params_list):
            for jj, thickness_value in enumerate(thickness):
                for ii in range(supervector.shape[0] // 2):
                    psi_value = supervector[ii, jj, zz]
                    delta_value = supervector[ii + len(dlam), jj, zz]
                    rows.append([psi_value, delta_value, dlam[ii], thickness_value] + list(lorentz_params))

        df = pd.DataFrame(rows, columns=["psi", "delta", "wavelength", "thickness", "lambda0", "gamma", "amplitude"])

        supervector_file = os.path.join(timestamped_folder, "supervector_lorentzian.csv")
        df.to_csv(supervector_file, index=False)

        print(" *** Data written successfully to 'results' folder ***")
    except Exception as e:
        raise IOError(f"Error saving data: {e}")
