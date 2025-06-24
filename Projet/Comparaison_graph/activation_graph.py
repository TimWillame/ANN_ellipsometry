import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_activation_function_performance():
    """
    Generate comparative bar plots showing:
    1. Test loss across different activation functions.
    2. Training time across different activation functions.
    
    The results are compared for three simulation models:
    - Standard
    - Maxwell-Garnett
    - Lorentz

    Saves the figure as 'performance_activation.png'.

    Returns:
        None
    """
    # Configure plot aesthetics
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["axes.edgecolor"] = "0.15"
    plt.rcParams["axes.linewidth"] = 1.25

    # Custom academic blue palette
    blues_palette = {
        "Standard": "#5B9BD5",
        "Maxwell-Garnett": "#2E75B6",
        "Lorentz": "#9BC2E6"
    }

    # Performance and timing data for each model
    datasets = {
        'Standard': {
            'activations': ['relu', 'leaky_relu', 'elu', 'tanh', 'sigmoid'],
            'test_loss': [0.0026, 0.0063, 0.0122, 0.0095, 0.0714],
            'time': [1.21, 0.53, 0.87, 0.77, 0.84]
        },
        'Maxwell-Garnett': {
            'activations': ['relu', 'leaky_relu', 'elu', 'tanh', 'sigmoid'],
            'test_loss': [0.0033, 0.0024, 0.0050, 0.0049, 0.0023],
            'time': [19.29, 24.17, 26.13, 25.62, 27.41]
        },
        'Lorentz': {
            'activations': ['relu', 'leaky_relu', 'elu', 'tanh', 'sigmoid'],
            'test_loss': [0.0061, 0.0065, 0.0088, 0.0088, 0.0061],
            'time': [28.64, 24.64, 27.13, 21.36, 28.28]
        }
    }

    # Create subplots for test loss and training time
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300)
    x = np.arange(len(datasets['Standard']['activations']))
    width = 0.25

    # --- Plot Test Loss ---
    for i, (name, data) in enumerate(datasets.items()):
        ax1.bar(x + i * width, data['test_loss'], width=width * 0.85,
                color=blues_palette[name], edgecolor='white', linewidth=0.5, label=name)

    ax1.set_xticks(x + width)
    ax1.set_xticklabels(datasets['Standard']['activations'])
    ax1.set_ylabel('Test Loss', fontsize=14, labelpad=10)
    ax1.set_ylim(0, 0.025)
    ax1.grid(axis='y', linestyle=':', linewidth=0.5, zorder=0, color='lightgray')
    ax1.set_title('Performance of Activation Functions', fontsize=16, pad=15, fontweight='bold')

    # --- Plot Training Time ---
    for i, (name, data) in enumerate(datasets.items()):
        ax2.bar(x + i * width, data['time'], width=width * 0.85,
                color=blues_palette[name], edgecolor='white', linewidth=0.5, label=name)

    ax2.set_ylabel('Training Time (s)', fontsize=14, labelpad=10)
    ax2.set_ylim(0, 140)
    ax2.grid(axis='y', linestyle=':', linewidth=0.5, zorder=0, color='lightgray')
    ax2.set_title('Training Time per Activation Function', fontsize=16, pad=15, fontweight='bold')
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(datasets['Standard']['activations'])

    # --- Add legend and layout adjustments ---
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels,
               loc='upper center',
               ncol=3,
               bbox_to_anchor=(0.5, 1.02),
               frameon=False,
               fontsize=14)

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, hspace=0.5)
    plt.savefig('performance_activation.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

# Call the function
plot_activation_function_performance()
