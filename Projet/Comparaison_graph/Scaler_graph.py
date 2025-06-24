import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set modern and readable style
sns.set(style="whitegrid", font_scale=1.1)
plt.rcParams["font.family"] = "sans-serif"

def plot_average_test_loss_by_scaler(data: list[tuple[str, str, str, float]]) -> None:
    """
    Plot the average test loss for each (X_scaler, Y_scaler) combination.

    Parameters:
    - data (list of tuples): Each tuple contains:
        - dataset name (str)
        - X_scaler name (str)
        - Y_scaler name (str)
        - test loss (float)

    Output:
    - A horizontal bar plot displaying the average test loss for each scaler combination.
    """

    # Convert raw data into a DataFrame
    df = pd.DataFrame(data, columns=["Dataset", "X_scaler", "Y_scaler", "Test_Loss"])

    # Compute mean test loss per (X_scaler, Y_scaler) combination across datasets
    mean_losses = df.groupby(["X_scaler", "Y_scaler"])["Test_Loss"].mean().reset_index()
    mean_losses_sorted = mean_losses.sort_values("Test_Loss")

    # Color palette: exclude lightest tones for better contrast
    n = len(mean_losses_sorted)
    palette = sns.color_palette("Blues", n_colors=n + 4)[4:]
    colors = list(reversed(palette))

    # Create horizontal bar plot
    plt.figure(figsize=(10, 6))
    bar_labels = [f"{x} / {y}" for x, y in zip(mean_losses_sorted.X_scaler, mean_losses_sorted.Y_scaler)]
    bars = plt.barh(
        y=bar_labels,
        width=mean_losses_sorted.Test_Loss,
        color=colors
    )

    # Annotate bars with their corresponding values
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.001, bar.get_y() + bar.get_height() / 2,
                 f"{width:.4f}", va='center', fontsize=12)

    # Plot aesthetics
    plt.xlabel("Average Test Loss across 3 datasets", fontsize=14)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

# --- Data ---

data = [
    ("Standard", "Standard", "Standard", 0.0454),
    ("Standard", "Standard", "MinMax", 0.0354),
    ("Standard", "Standard", "Robust", 0.0832),
    ("Standard", "MinMax", "Standard", 0.0223),
    ("Standard", "MinMax", "MinMax", 0.0135),
    ("Standard", "MinMax", "Robust", 0.0196),
    ("Standard", "Robust", "Standard", 0.0195),
    ("Standard", "Robust", "MinMax", 0.0093),
    ("Standard", "Robust", "Robust", 0.0561),

    ("Maxwell-Garnett", "Standard", "Standard", 0.0262),
    ("Maxwell-Garnett", "Standard", "MinMax", 0.0043),
    ("Maxwell-Garnett", "Standard", "Robust", 0.0103),
    ("Maxwell-Garnett", "MinMax", "Standard", 0.0204),
    ("Maxwell-Garnett", "MinMax", "MinMax", 0.0026),
    ("Maxwell-Garnett", "MinMax", "Robust", 0.0079),
    ("Maxwell-Garnett", "Robust", "Standard", 0.0346),
    ("Maxwell-Garnett", "Robust", "MinMax", 0.0066),
    ("Maxwell-Garnett", "Robust", "Robust", 0.0135),

    ("Lorentz", "Standard", "Standard", 0.0327),
    ("Lorentz", "Standard", "MinMax", 0.0047),
    ("Lorentz", "Standard", "Robust", 0.0118),
    ("Lorentz", "MinMax", "Standard", 0.0546),
    ("Lorentz", "MinMax", "MinMax", 0.0055),
    ("Lorentz", "MinMax", "Robust", 0.0154),
    ("Lorentz", "Robust", "Standard", 0.0925),
    ("Lorentz", "Robust", "MinMax", 0.0183),
    ("Lorentz", "Robust", "Robust", 0.0353),
]

# --- Plotting ---

plot_average_test_loss_by_scaler(data)
