import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =======================#
# Figure Style Settings  #
# =======================#
plt.style.use('default')
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["axes.edgecolor"] = "0.15"
plt.rcParams["axes.linewidth"] = 1.25

# =======================#
# Data Definition        #
# =======================#
architectures = [
    "Small\n[128,128]", 
    "Medium\n[256,256,256]", 
    "Large\n[512,512,512]", 
    "Deep\n[256,256,256,256,256]", 
    "Wide\n[1024,1024]"
]

metrics = {
    "Test Loss": {
        "Standard": [0.0060, 0.0106, 0.0074, 0.0223, 0.0119],
        "Maxwell-Garnett": [0.0030, 0.0029, 0.0033, 0.0035, 0.0028],
        "Lorentz": [0.0065, 0.0059, 0.0051, 0.0060, 0.0050]
    },
    "Training Time (s)": {
        "Standard": [0.42, 0.72, 2.12, 0.86, 2.75],
        "Maxwell-Garnett": [10.59, 19.25, 63.02, 27.29, 78.20],
        "Lorentz": [17.79, 31.58, 69.13, 38.61, 133.10]
    }
}

palette = {
    "Standard": "#5B9BD5",
    "Maxwell-Garnett": "#2E75B6",
    "Lorentz": "#9BC2E6"
}

def plot_model_comparison(metrics: dict, architectures: list, palette: dict) -> None:
    """
    Plots bar charts comparing model architectures based on test loss and training time.

    Args:
        metrics (dict): Dictionary containing 'Test Loss' and 'Training Time (s)' for each model.
        architectures (list): List of architecture names.
        palette (dict): Color mapping for each model.

    Returns:
        None
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300)
    x = np.arange(len(architectures))
    width = 0.25

    # --- Subplot 1: Test Loss ---
    for i, (model, values) in enumerate(metrics["Test Loss"].items()):
        ax1.bar(x + (i - 1) * width, values, width=width * 0.85,
                color=palette[model], edgecolor='white', linewidth=0.5,
                label=model, zorder=3)

    ax1.set_ylabel('Test Loss', fontsize=14, labelpad=10)
    ax1.set_ylim(0, 0.025)
    ax1.grid(axis='y', linestyle=':', linewidth=0.5, zorder=0, color='lightgray')
    ax1.set_title('Architecture Performance', fontsize=16, pad=15, fontweight='bold')

    # --- Subplot 2: Training Time ---
    for i, (model, values) in enumerate(metrics["Training Time (s)"].items()):
        ax2.bar(x + (i - 1) * width, values, width=width * 0.85,
                color=palette[model], edgecolor='white', linewidth=0.5,
                label=model, zorder=3)

    ax2.set_ylabel('Training Time (s)', fontsize=14, labelpad=10)
    ax2.set_ylim(0, 140)
    ax2.grid(axis='y', linestyle=':', linewidth=0.5, zorder=0, color='lightgray')
    ax2.set_title('Training Time per Architecture', fontsize=16, pad=15, fontweight='bold')

    # --- Shared Configuration ---
    for ax in [ax1, ax2]:
        ax.set_xticks(x)
        ax.set_xticklabels(architectures, fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        for spine in ['left', 'bottom']:
            ax.spines[spine].set_color('gray')
            ax.spines[spine].set_linewidth(0.5)

    # --- Legend ---
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels,
               loc='upper center',
               ncol=3,
               bbox_to_anchor=(0.5, 1.02),
               frameon=False,
               fontsize=14)

    # --- Final Adjustments ---
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, hspace=0.5)
    plt.savefig('performance_architectures.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

# Run the plot
plot_model_comparison(metrics, architectures, palette)
