import numpy as np
import os
from datetime import datetime
import pandas as pd

def load_nk_data(substrate_file, layer_file):
    """
    Load refractive index data from provided substrate and layer files.
    
    :param substrate_file: Full path for the substrate data file.
    :param layer_file: Full path for the layer data file.
    :return: Wavelengths, refractive indices and extinction coefficients.
    """
    base_dir = os.path.dirname(__file__)
    nk_folder = os.path.join(base_dir,"..", "assets", "Materials")
    substrate_path = os.path.join(nk_folder, substrate_file)
    layer_path = os.path.join(nk_folder, layer_file)


    if not os.path.isfile(substrate_path):
        raise FileNotFoundError(f"Substrate file '{substrate_file}' not found.")
    if not os.path.isfile(layer_path):
        raise FileNotFoundError(f"Layer file '{layer_file}' not found.")

    # Load data
    try:
        lam_s, n_substrat, k_substrat = np.loadtxt(substrate_path, unpack=True)
        lam_layer, n_layer, k_layer = np.loadtxt(layer_path, unpack=True)
    except ValueError as e:
        raise ValueError(f"Error loading data from files: {e}")

    return lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer

def load_nk_data_maxwell_garnett(substrate_file, layer_file, nanoparticle_file):
    """
    Load refractive index data from provided substrate and layer files.
    
    :param substrate_file: Full path for the substrate data file.
    :param layer_file: Full path for the layer data file.
    :return: Wavelengths, refractive indices and extinction coefficients.
    """
    base_dir = os.path.dirname(__file__)
    nk_folder = os.path.join(base_dir,"..", "assets", "Materials")
    substrate_path = os.path.join(nk_folder, substrate_file)
    layer_path = os.path.join(nk_folder, layer_file)
    nanoparticle_path = os.path.join(nk_folder, nanoparticle_file)


    if not os.path.isfile(substrate_path):
        raise FileNotFoundError(f"Substrate file '{substrate_file}' not found.")
    if not os.path.isfile(layer_path):
        raise FileNotFoundError(f"Layer file '{layer_file}' not found.")
    if not os.path.isfile(nanoparticle_path):
        raise FileNotFoundError(f"Nanoparticle file '{nanoparticle_file}' not found.")

    # Load data
    try:
        lam_s, n_substrat, k_substrat = np.loadtxt(substrate_path, unpack=True)
        lam_layer, n_layer, k_layer = np.loadtxt(layer_path, unpack=True)
        lam_p, n_pigment, k_pigment = np.loadtxt(nanoparticle_path, unpack=True)
    except ValueError as e:
        raise ValueError(f"Error loading data from files: {e}")

    return lam_s, n_substrat, k_substrat, lam_layer, n_layer, k_layer, lam_p, n_pigment, k_pigment



def save_supervector(supervector, thickness, dlam):
    """
    Save the supervector, thickness, and dlam data to a CSV file in a timestamped folder.

    :param supervector: The calculated supervector data (2D array with psi and delta).
    :param thickness: The thickness data (1D array).
    :param dlam: The wavelength data (1D array).
    """
    base_dir = os.path.dirname(__file__)
    results_path = os.path.join(base_dir,"..", 'results')

    # Create the 'results' directory if it doesn't exist
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Get current date and time for the folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_folder = os.path.join(results_path, timestamp)

    # Create a timestamped folder
    os.makedirs(timestamped_folder, exist_ok=True)

    try:
        # Prepare the data for saving
        psi_values = supervector[0:len(dlam), :]  # psi values for each thickness
        delta_values = supervector[len(dlam):2 * len(dlam), :]  # delta values for each thickness
        
        # Create a list to hold the data
        rows = []
        for jj, thickness_value in enumerate(thickness):
            for ii in range(len(dlam)):
                rows.append([psi_values[ii, jj], delta_values[ii, jj], dlam[ii], thickness_value])

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=["psi", "delta", "wavelength", "thickness"])

        # Save the DataFrame to a CSV file
        supervector_file = os.path.join(timestamped_folder, "supervector.csv")
        df.to_csv(supervector_file, index=False)

        print(" *** Data written successfully to 'results' folder ***")
    except Exception as e:
        raise IOError(f"Error saving data: {e}")


def save_supervector_maxwell_garnett(supervector, thickness, vfractions, dlam):
    """
    Save the supervector and additional data to a CSV file with a timestamp.

    :param supervector: The calculated supervector data (3D array).
    :param thickness: The thickness data (1D array).
    :param vfractions: The volume fractions data (1D array).
    :param dlam: The wavelength data (1D array).
    """
    base_dir = os.path.dirname(__file__)
    results_path = os.path.join(base_dir,"..", 'results')

    # Create the 'results' directory if it doesn't exist
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Get current date and time for the folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_folder = os.path.join(results_path, timestamp)

    # Create a timestamped folder
    os.makedirs(timestamped_folder, exist_ok=True)

    try:
        # Prepare the data for saving
        rows = []
        for kk, vf in enumerate(vfractions):  # Iterate over each volume fraction
            for jj, thickness_value in enumerate(thickness):  # Iterate over each thickness
                for ii in range(supervector.shape[0] // 2):  # Iterate over each wavelength
                    psi_value = supervector[ii, jj, kk]  # psi value
                    delta_value = supervector[ii + len(dlam), jj, kk]  # delta value
                    rows.append([psi_value, delta_value, dlam[ii], thickness_value, vf])

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=["psi", "delta", "wavelength", "thickness", "vfraction"])

        # Save the DataFrame to a CSV file
        supervector_file = os.path.join(timestamped_folder, "supervector_maxwell_garnett.csv")
        df.to_csv(supervector_file, index=False)

        print(" *** Data written successfully to 'results' folder ***")
    except Exception as e:
        raise IOError(f"Error saving data: {e}")

    
def load_wavelengths(filename):
    """
    Load wavelength data from a file in the assets/wavelength directory.
    
    :param filename: Name of the wavelengths data file (without path).
    :return: Wavelengths as a numpy array.
    """
    base_dir = os.path.dirname(__file__)
    wavelengths_folder = os.path.join(base_dir,"..", "assets", "wavelength")
    file_path = os.path.join(wavelengths_folder, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Wavelengths file '{file_path}' not found.")

    # Load data
    try:
        dlam = np.loadtxt(file_path)
    except ValueError as e:
        raise ValueError(f"Error loading wavelengths from file: {e}")

    return dlam

def save_supervector_lorentzian(supervector, thickness, dlam, lorentz_params_list):
    """
    Save the supervector and additional data to a CSV file with a timestamp.

    :param supervector: The calculated supervector data (3D array: psi and delta values).
    :param thickness: The thickness data (1D array).
    :param dlam: The wavelength data (1D array).
    :param lorentz_params_list: List of Lorentzian parameters [(lambda0, gamma, amplitude), ...].
    """
    base_dir = os.path.dirname(__file__)
    results_path = os.path.join(base_dir,"..", 'results')

    # Create the 'results' directory if it doesn't exist
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Get current date and time for the folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_folder = os.path.join(results_path, timestamp)
    os.makedirs(timestamped_folder, exist_ok=True)

    try:
        # Prepare the data for saving
        rows = []
        for zz, lorentz_params in enumerate(lorentz_params_list):  # Iterate over each set of Lorentzian parameters
            for jj, thickness_value in enumerate(thickness):  # Iterate over each thickness
                for ii in range(supervector.shape[0] // 2):  # Iterate over each wavelength
                    psi_value = supervector[ii, jj, zz]  # psi value
                    delta_value = supervector[ii + len(dlam), jj, zz]  # delta value
                    lorentz_params = lorentz_params_list[zz]  # Cela renvoie un tuple
                    rows.append([psi_value, delta_value, dlam[ii], thickness_value] + list(lorentz_params))  # Utilisation du tuple entier
                                        
        # Create a DataFrame
        df = pd.DataFrame(rows, columns=["psi", "delta", "wavelength", "thickness", "lambda0", "gamma", "amplitude"])

        # Save the DataFrame to a CSV file
        supervector_file = os.path.join(timestamped_folder, "supervector_lorentzian.csv")
        df.to_csv(supervector_file, index=False)

        print(" *** Data written successfully to 'results' folder ***")
    except Exception as e:
        raise IOError(f"Error saving data: {e}")
