import numpy as np

def calculate_average_and_variance(image) -> tuple[float, float]:
    """
    Calculates average and variance for an image based on these formulas:
    - E[g(x, y)] = f(x, y)
    - σ²g(x, y) = (1/k) * σ²η(x, y)
    :param image: Input image
    :return: Average and variance
    """
    # Computes the total number of pixels in the image.
    # image.shape[0] gives the height (number of rows), and image.shape[1] gives the width (number of columns).
    total_pixels = image.shape[0] * image.shape[1]

    # Computes the average pixel value (mean) for the entire image.
    average_value = np.sum(image) / total_pixels
    # Computes the sum of squared differences between each pixel value and the average.
    squared_diff_sum = np.sum((image - average_value) ** 2)
    # Computes the variance of pixel values in the image.
    variance_value = squared_diff_sum / total_pixels
    return average_value, variance_value