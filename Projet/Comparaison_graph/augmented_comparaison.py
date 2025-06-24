import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration du style académique avec des tailles de police augmentées
plt.style.use('default')
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["axes.edgecolor"] = "0.15"
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams["font.size"] = 14  # Taille de police globale augmentée

# Données extraites de vos logs (loss finales)
data = {
    "Standard": {
        "Sans augmentation": {"Train": 0.0100, "Test": 0.0048},
        "Avec augmentation": {"Train": 0.0060, "Test": 0.0044}
    },
    "Maxwell-Garnett": {
        "Sans augmentation": {"Train": 0.0040, "Test": 0.0037},
        "Avec augmentation": {"Train": 0.0022, "Test": 0.0018}
    },
    "Lorentz": {
        "Sans augmentation": {"Train": 0.0092, "Test": 0.0056},
        "Avec augmentation": {"Train": 0.0050, "Test": 0.0036}
    }
}

# Palette de couleurs
palette = {
    "Sans augmentation": "#2E75B6",  # Bleu foncé
    "Avec augmentation": "#5B9BD5"   # Bleu moyen
}

# Création de la figure avec une taille légèrement augmentée
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Positions des barres
x = np.arange(len(data))
width = 0.35

# --- Graphique Train Loss ---
for i, augmentation in enumerate(["Sans augmentation", "Avec augmentation"]):
    train_losses = [data[dataset][augmentation]["Train"] for dataset in data]
    ax1.bar(x + i*width, train_losses, width, 
            color=palette[augmentation],
            edgecolor='white',
            linewidth=0.8,  # Légèrement plus épais
            label=augmentation,
            zorder=3)

ax1.set_ylabel('Train Loss', fontsize=16)  # Taille augmentée
ax1.set_title('Comparaison des Train Loss finales', fontsize=18, pad=12, fontweight='bold')  # Taille augmentée
ax1.set_xticks(x + width/2)
ax1.set_xticklabels(list(data.keys()), fontsize=16)  # Taille augmentée
ax1.grid(axis='y', linestyle=':', linewidth=0.8, zorder=0)  # Lignes de grille plus visibles

# Ajout des valeurs sur les barres (texte plus grand)
for i, dataset in enumerate(data):
    for j, augmentation in enumerate(["Sans augmentation", "Avec augmentation"]):
        loss = data[dataset][augmentation]["Train"]
        ax1.text(i + j*width, loss + 0.0005, f'{loss:.4f}',
                ha='center', va='bottom', fontsize=14)  # Taille augmentée

# --- Graphique Test Loss ---
for i, augmentation in enumerate(["Sans augmentation", "Avec augmentation"]):
    test_losses = [data[dataset][augmentation]["Test"] for dataset in data]
    ax2.bar(x + i*width, test_losses, width, 
            color=palette[augmentation],
            edgecolor='white',
            linewidth=0.8,
            label=augmentation,
            zorder=3)

ax2.set_ylabel('Test Loss', fontsize=16)  # Taille augmentée
ax2.set_title('Comparaison des Test Loss finales', fontsize=18, pad=12, fontweight='bold')  # Taille augmentée
ax2.set_xticks(x + width/2)
ax2.set_xticklabels(list(data.keys()), fontsize=16)  # Taille augmentée
ax2.grid(axis='y', linestyle=':', linewidth=0.8, zorder=0)

# Ajout des valeurs sur les barres (texte plus grand)
for i, dataset in enumerate(data):
    for j, augmentation in enumerate(["Sans augmentation", "Avec augmentation"]):
        loss = data[dataset][augmentation]["Test"]
        ax2.text(i + j*width, loss + 0.0005, f'{loss:.4f}',
                ha='center', va='bottom', fontsize=14)  # Taille augmentée

# Configuration commune
for ax in [ax1, ax2]:
    ax.set_ylim(0, max([v[aug]["Train"] for v in data.values() for aug in v]) * 1.2)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('gray')
        ax.spines[spine].set_linewidth(1.2)  # Légèrement plus épais

# Légende unique (plus grande)
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, 
           loc='upper center', 
           ncol=2, 
           bbox_to_anchor=(0.5, 1.08),  # Position ajustée
           frameon=False,
           fontsize=16)  # Taille augmentée


# Ajustements avec plus d'espace
plt.tight_layout()
plt.subplots_adjust(top=0.85, wspace=0.3)  # Espacement ajusté

plt.savefig('comparaison_loss_finales.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()