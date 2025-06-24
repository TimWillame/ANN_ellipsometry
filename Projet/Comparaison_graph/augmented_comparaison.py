"""
Visualization of final training and test losses for three datasets 
(Standard, Maxwell-Garnett, Lorentz) with and without data augmentation.

The script generates two side-by-side bar charts:
1. Final training losses
2. Final test losses

Each chart compares results for models trained with and without data augmentation.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Plot Style Configuration ---
plt.style.use('default')
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["axes.edgecolor"] = "0.15"
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams["font.size"] = 14

# --- Loss Data ---
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

# --- Color Palette ---
palette = {
    "Sans augmentation": "#2E75B6",
    "Avec augmentation": "#5B9BD5"
}

# --- Figure Initialization ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
x = np.arange(len(data))
width = 0.35

# --- Plot: Training Loss ---
for i, aug in enumerate(["Sans augmentation", "Avec augmentation"]):
    train_losses = [data[ds][aug]["Train"] for ds in data]
    ax1.bar(
        x + i * width,
        train_losses,
        width=width,
        color=palette[aug],
        edgecolor='white',
        linewidth=0.8,
        label=aug,
        zorder=3
    )

ax1.set_ylabel('Train Loss', fontsize=16)
ax1.set_title('Final Training Loss Comparison', fontsize=18, pad=12, fontweight='bold')
ax1.set_xticks(x + width / 2)
ax1.set_xticklabels(list(data.keys()), fontsize=16)
ax1.grid(axis='y', linestyle=':', linewidth=0.8, zorder=0)

# Annotate training loss bars
for i, dataset in enumerate(data):
    for j, aug in enumerate(["Sans augmentation", "Avec augmentation"]):
        loss = data[dataset][aug]["Train"]
        ax1.text(i + j * width, loss + 0.0005, f'{loss:.4f}',
                 ha='center', va='bottom', fontsize=14)

# --- Plot: Test Loss ---
for i, aug in enumerate(["Sans augmentation", "Avec augmentation"]):
    test_losses = [data[ds][aug]["Test"] for ds in data]
    ax2.bar(
        x + i * width,
        test_losses,
        width=width,
        color=palette[aug],
        edgecolor='white',
        linewidth=0.8,
        label=aug,
        zorder=3
    )

ax2.set_ylabel('Test Loss', fontsize=16)
ax2.set_title('Final Test Loss Comparison', fontsize=18, pad=12, fontweight='bold')
ax2.set_xticks(x + width / 2)
ax2.set_xticklabels(list(data.keys()), fontsize=16)
ax2.grid(axis='y', linestyle=':', linewidth=0.8, zorder=0)

# Annotate test loss bars
for i, dataset in enumerate(data):
    for j, aug in enumerate(["Sans augmentation", "Avec augmentation"]):
        loss = data[dataset][aug]["Test"]
        ax2.text(i + j * width, loss + 0.0005, f'{loss:.4f}',
                 ha='center', va='bottom', fontsize=14)

# --- Shared Axis & Style Configurations ---
max_train_loss = max([v[aug]["Train"] for v in data.values() for aug in v])
for ax in [ax1, ax2]:
    ax.set_ylim(0, max_train_loss * 1.2)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('gray')
        ax.spines[spine].set_linewidth(1.2)

# --- Legend ---
handles, labels = ax1.get_legend_handles_labels()
fig.legend(
    handles, labels,
    loc='upper center',
    ncol=2,
    bbox_to_anchor=(0.5, 1.08),
    frameon=False,
    fontsize=16
)

# --- Layout & Export ---
plt.tight_layout()
plt.subplots_adjust(top=0.85, wspace=0.3)
plt.savefig('final_loss_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
