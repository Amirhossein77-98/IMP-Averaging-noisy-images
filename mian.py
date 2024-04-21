import cv2
import numpy as np
import os
import csv

# Reading the image
image_path = "original.jpg"
image = cv2.imread(image_path)

def add_salt_and_pepper_noise(image, amount):
    pass

# Create directories to save noisy samples and results
os.makedirs("noisy_samples", exist_ok=True)
os.makedirs("result", exist_ok=True)

# Generate noisy samples
samples = 500
for i in range(samples):
    noise_amount = np.random.uniform(0.01, 0.05)
    noisy_samples = add_salt_and_pepper_noise(image, amount=noise_amount)