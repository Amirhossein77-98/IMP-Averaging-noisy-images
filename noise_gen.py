import numpy as np

def add_salt_and_pepper_noise(image, amount) -> list:
    """
    Adds salt-and-pepper noise to an image.
    :param image: Input image
    :param amount: Proportion of image pixels to replace with noise
    :return: Image with salt-and-pepper noise
    """

    # Converts the input image to a floating-point format (values between 0.0 and 1.0).
    # Divides each pixel value by 255 to normalize it to the [0, 1] range.
    image_float = np.float32(image) / 255.0

    # Creates random values for each pixel in the image.
    # These random values determine whether a pixel becomes “salt” (white) or “pepper” (black).
    random_values = np.random.rand(*image.shape[:2])

    # Set pixels to 1 (salt) or 0 (pepper) based on random values
    image_float[random_values < (amount / 2)] = 0 # If a random value is less than half of the specified amount, set the pixel value to 0 (black) for “pepper.”
    image_float[random_values > (1 - amount / 2)] = 1 # If a random value is greater than (1 - half of the amount), set the pixel value to 1 (white) for “salt.”

    # Converts the modified floating-point image back to an 8-bit format (values between 0 and 255).
    noisy_image = np.uint8(image_float * 255)
    return noisy_image