import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def main() -> None:
    """Generate a spiral mandala with an Alex Grey-inspired palette."""
    # -- Visionary Dream generator --
    # Resolution for museum-quality output
    WIDTH, HEIGHT = 1024, 1024

    # Create a spectral palette inspired by Alex Grey
    colors = [
        (48/255, 0/255, 108/255),   # deep indigo
        (0/255, 33/255, 105/255),   # cosmic blue
        (0/255, 148/255, 68/255),   # vivid green
        (241/255, 243/255, 54/255), # radiant yellow
        (255/255, 153/255, 0/255),  # luminous orange
        (208/255, 0/255, 0/255),    # crimson red
        (115/255, 0/255, 128/255)   # ultraviolet magenta
    ]
    cmap = LinearSegmentedColormap.from_list("alex_grey", colors, N=256)

    # Prepare a radial grid for symmetrical patterns
    x = np.linspace(-4 * np.pi, 4 * np.pi, WIDTH)
    y = np.linspace(-4 * np.pi, 4 * np.pi, HEIGHT)
    X, Y = np.meshgrid(x, y)

    # Calculate spiral waves to form a mandala
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    Z = np.sin(R + Theta * 3) * np.cos(R * 2 - Theta * 5)

    # Render the visionary art
    plt.figure(figsize=(WIDTH/100, HEIGHT/100), dpi=100)
    plt.axis("off")
    plt.imshow(Z, cmap=cmap, interpolation="bilinear")
    plt.tight_layout(pad=0)

    # Save the final image
    plt.savefig("Visionary_Dream.png", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    main()

