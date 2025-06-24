# Master's Thesis – Ellipsometry & Neural Networks (UMons)
This repository contains the code and documents related to my Master's thesis in Physics, completed at the University of Mons (UMons) during the 2024–2025 academic year. The main goal of the work is to simulate ellipsometric data and use artificial neural networks (ANNs) to predict physical parameters such as thin film thickness, volume fraction, and Lorentzian oscillator parameters.


## Neural Network 

The ANN/ directory contains several neural network models implemented in PyTorch. These models were developed to:
- Predict thin film thickness,
- Estimate volume fraction in nanocomposite materials,
- Retrieve Lorentz oscillator parameters (e.g., central wavelength, damping factor, amplitude),

Each script includes different configurations or experiments used throughout the project.

## Simulation

The ellipsometry/ folder contains a Python-based graphical user interface to generate synthetic ellipsometric data.

To launch the GUI:

```bash
cd Projet
python main.py
```

This tool lets you simulate optical responses (Ψ and Δ) based on user-defined layer parameters and materials.

## Comparaison
The comparaison_graph/ folder is used exclusively to create comparison plots from model predictions or experimental data.

## Other files
memoire.pdf: Full thesis (in French)

resume_fr.pdf: Short summary of the work (in French)

---

If you have any questions about the code or project, feel free to contact me at:

Tim.Willame@outlook.com

