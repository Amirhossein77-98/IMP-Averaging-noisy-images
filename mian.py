"""
Image Processing Project: Noise Analysis and Denoising

This project aims to analyze the effects of salt-and-pepper noise on an image and perform denoising operations
using an averaging technique. The project involves the following steps:

1. Read an original image.
2. Generate multiple noisy samples by adding varying amounts of salt-and-pepper noise.
3. Group the noisy samples into different sample sizes (1, 5, 10, 50, 100, 500).
4. For each sample size, calculate the average and variance of the noisy samples.
5. Denoise the samples by averaging them within each sample group.
6. Save the denoised images and the calculated statistics to a CSV file.
7. Generate a PDF report with the original image, denoised images, and sample statistics.

Usage:
   1. Ensure that the required dependencies are installed.
   2. Place the original image file named "original.jpg" in the project directory.
   3. Run the main.py script.
   4. The noisy samples will be generated in the "noisy_samples" folder.
   5. The denoised images will be saved in the "result" folder.
   6. The CSV file with statistics will be saved as "result/results.csv".
   7. The PDF report will be saved as "result/results.pdf".

Note: This project is part of an Image Processing class exercise and is intended for educational purposes.

Author: Amirhossein Gholizadeh
"""

import cv2
import numpy as np
import os
import csv
from noise_gen import add_salt_and_pepper_noise
from noise_var_calc import calculate_average_and_variance
from report_gen import generate_pdf_report

def main() -> None:
    # Reading the image
    image_path = "original.jpg"
    image = cv2.imread(image_path)

    # Create directories to save noisy samples and results
    os.makedirs("noisy_samples", exist_ok=True)
    os.makedirs("result", exist_ok=True)

    # Generate noisy samples
    samples = 500
    print(f"Generating {samples} noisy images...")
    for i in range(samples):
        noise_amount = np.random.uniform(0.01, 0.1)
        noisy_samples = add_salt_and_pepper_noise(image, amount=noise_amount)
        cv2.imwrite(f"noisy_samples/noisy_sample_{i}.jpg", noisy_samples)

    # Select sample groups and calculate statistics
    sample_sizes = [1, 5, 10, 50, 100, 500]
    results = []

    print("Averaging operation started...")
    # For each value of k (sample group size), perform the following steps.
    for k in sample_sizes:
        #Read the corresponding number of noisy samples (based on k). Each sample is loaded as a grayscale image.
        selected_samples = [cv2.imread(f"noisy_samples/noisy_sample_{i}.jpg", cv2.IMREAD_GRAYSCALE) for i in range(k)]
        # Calculate the average and variance for this group of noisy samples.
        avg, var = calculate_average_and_variance(np.mean(selected_samples, axis=0))
        results.append((k, avg, var))

        # Create resulting image for this sample group by averaging the selected samples
        resulting_image = np.mean(selected_samples, axis=0) # Based on the formula: g̅(x, y) = (1/k) * Σ(i=1 to k) gi(x, y)
        cv2.imwrite(f"result/result_for_{k}_samples.jpg", resulting_image)
        print(f"Saved the results for {k} smples in \"result\" folder")

    # Save results to a csv file
    csv_filename = "result/results.csv"
    # Write the sample group size, average, and average variance for each group.
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sample Groups", "Average", "Average Variance"])
        for row in results:
            writer.writerow(row)

    generate_pdf_report(sample_sizes)
    print(f"Finished the operation successfully. To see the results please check the \"result\" folder")

if __name__ == "__main__":
    main()