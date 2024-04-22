# Image Processing Project: Noise Analysis and Denoising

This project is an implementation of an Image Processing class exercise focused on analyzing the effects of salt-and-pepper noise on an image and performing denoising operations using an averaging technique.

## Features

- Generate multiple noisy samples from an original image by adding varying amounts of salt-and-pepper noise.
- Group the noisy samples into different sample sizes (1, 5, 10, 50, 100, 500).
- Calculate the average and variance of the noisy samples for each sample group.
- Denoise the samples by averaging them within each sample group.
- Save the denoised images and the calculated statistics to a CSV file.
- Generate a PDF report with the original image, denoised images, and sample statistics.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- ReportLab
- PyPDF2

The specific package versions required are listed in the `requirements.txt` file.

## Installation

1. Clone the repository or download the project files.
2. Install the required packages by running `pip install -r requirements.txt`.

## Usage

1. Place the original image file named "original.jpg" in the project directory.
2. Run the `main.py` script.
3. The noisy samples will be generated in the "noisy_samples" folder.
4. The denoised images will be saved in the "result" folder.
5. The CSV file with statistics will be saved as "result/results.csv".
6. The PDF report will be saved as "result/report.pdf".

## Project Structure

- `main.py`: The main script that orchestrates the project's execution.
- `noise_gen.py`: Contains functions for generating salt-and-pepper noise.
- `noise_var_calc.py`: Contains functions for calculating the average and variance of noisy samples.
- `report_gen.py`: Contains functions for generating the PDF report.

## Credits

This project was implemented by Amirhossein Gholizadeh as part of an Image Processing class exercise. The project utilizes the following resources:

- OpenCV documentation: https://docs.opencv.org
- Machine Learning Knowledge: https://machinelearningknowledge.ai
- GeeksforGeeks: https://www.geeksforgeeks.org
- Stack Overflow: https://stackoverflow.com
- YouTube tutorials
- ReportLab documentation: https://docs.reportlab.com
- Copilot (Microsoft Copilot)
- Claude (Anthropic's AI assistant)