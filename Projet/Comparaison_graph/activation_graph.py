import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configuration du style
plt.style.use('default')
sns.set_theme(style="whitegrid") 
plt.rcParams["font.family"] = "serif"
plt.rcParams["axes.edgecolor"] = "0.15"
plt.rcParams["axes.linewidth"] = 1.25

# Palette de bleus académique personnalisée
blues_palette = {
    "Standard": "#5B9BD5",  # Bleu Office moyen
    "Maxwell-Garnett": "#2E75B6",  # Bleu Office foncé
    "Lorentz": "#9BC2E6"   # Bleu Office clair
}

# Données organisées par dataset
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

# Création des graphiques
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300)

# Graphique des performances (Test Loss)
x = np.arange(len(datasets['Standard']['activations']))  # Positions des groupes
width = 0.25  # Largeur des barres

for i, (dataset_name, data) in enumerate(datasets.items()):
    ax1.bar(x + i*width, data['test_loss'], width=width*0.85, color=blues_palette[dataset_name], edgecolor='white', linewidth=0.5, label=dataset_name)

ax1.set_xticks(x + width)
ax1.set_xticklabels(datasets['Standard']['activations'])
ax1.set_ylabel('Test Loss', fontsize=14, labelpad=10)
ax1.set_ylim(0, 0.025)
ax1.grid(axis='y', linestyle=':', linewidth=0.5, zorder=0, color='lightgray')
ax1.set_title('Performance pour les fonctions d\'activation', fontsize=16, pad=15, fontweight='bold')

# Graphique des temps d'exécution
for i, (dataset_name, data) in enumerate(datasets.items()):
    ax2.bar(x + i*width, data['time'],  width=width*0.85, color=blues_palette[dataset_name], edgecolor='white', linewidth=0.5, label=dataset_name)

ax2.set_ylabel('Temps (s)', fontsize=14, labelpad=10)
ax2.set_ylim(0, 140)
ax2.grid(axis='y', linestyle=':', linewidth=0.5, zorder=0, color='lightgray')
ax2.set_title('Temps d\'entrainements', fontsize=16, pad=15, fontweight='bold')
ax2.set_xticks(x + width)
ax2.set_xticklabels(datasets['Standard']['activations'])


# Légende
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