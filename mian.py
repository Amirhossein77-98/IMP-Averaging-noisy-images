"""
Image Denoising Through Averaging

This script implements an image denoising technique based on averaging multiple noisy samples of an input image.
It follows these steps:

Read an input image.
Generate a specified number of noisy samples by adding salt-and-pepper noise to the input image.
For different sample group sizes (1, 5, 10, 50, 100, 500):
a. Select the corresponding number of noisy samples from the generated set.
b. Calculate the average and variance of the selected samples using the formulas: Average (Expected Value): E[g(x, y)] = f(x, y) Variance: σ²g(x, y) = (1/k) * σ²η(x, y)
c. Save the averaged result as an image.
Store the sample group sizes, averages, and average variances in a CSV file.
This implementation follows the formulas and concepts from image denoising through averaging, as discussed in image processing literature.

References:

- A powerpoint provided by Dr. Kamangar
- docs.opencv.org
- machinelearningknowledge.ai
- geeksforgeeks.org
- stackoverslow.com
- some youtube guys
- copilot.microsoft.com
- claude.ai """

import cv2
import numpy as np
import os
import csv

def add_salt_and_pepper_noise(image, amount):
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

def calculate_average_and_variance(image):
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

def generate_pdf_report(samples):
    from reportlab.lib.pagesizes import landscape, A5
    from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Table, TableStyle

    print("Generating pdf report...")

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading2"]
    subtitle_style = styles["Heading3"]

    # Set up the PDF document
    doc = SimpleDocTemplate("result/results.pdf", pagesize=landscape(A5),topMargin=0*inch, bottomMargin=0*inch)
    elements = []

    # Add the original image with title
    original_image = Image("original.jpg", width=3.5*inch, height=4*inch)
    elements.append(Paragraph("Original Image", title_style))
    elements.append(original_image)
    # Add a spacer for bottom margin
    elements.append(Spacer(0, 1*inch))

    # Add the denoised images with titles
    image_files = [f"result/result_for_{i}_samples.jpg" for i in samples]
    titles = ["k=1", "k=5", "k=10", "k=20", "k=50", "k=100"]

    table_data = []
    for i in range(0, len(image_files), 3):
        row = []
        for j in range(3):
            if i + j < len(image_files):
                image = Image(image_files[i + j], width=1.5*inch, height=2*inch)
                title = Paragraph(titles[i + j], subtitle_style)
                row.append([image, title])
        table_data.append(row)

    table = Table(table_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))

    elements.append(Spacer(0, 0.3*inch))
    elements.append(Paragraph("Denoised Images", title_style))
    elements.append(Spacer(0, 0.3*inch))
    elements.append(table)

    # Build the PDF document
    doc.build(elements)
    print("PDF file 'results.pdf' generated successfully.")

def main():
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

"""Amirhossein Gholizadeh"""