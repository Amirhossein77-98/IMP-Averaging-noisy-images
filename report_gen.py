from reportlab.lib.pagesizes import landscape, A5
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import csv

def add_snapshot() -> None:
    from PyPDF2 import PdfReader, PdfWriter
    # Open the existing PDF
    existing_pdf = PdfReader("result/report.pdf")
    pdf_writer = PdfWriter()

    # Add all pages from the existing PDF to the writer
    for page in existing_pdf.pages:
        pdf_writer.add_page(page)

    # Open the PDF file to append
    pdf_to_append = PdfReader("snapshots/snapshots.pdf")

    # Append pages from the new PDF to the writer
    for page in pdf_to_append.pages:
        pdf_writer.add_page(page)

    # Write out the combined PDF
    with open("result/report.pdf", "wb") as out_file:
        pdf_writer.write(out_file)

def generate_pdf_report(samples) -> None:
    """
    Generate a PDF report with the original image, denoised images, and sample statistics.

    Args:
        samples (list): List of sample sizes used for denoising.

    This function creates a PDF report using the ReportLab library. The report includes the following elements:
        - Original image
        - Denoised images for each sample size, grouped in rows of 3
        - Titles for each denoised image indicating the sample size

    The PDF report is saved as "result/report.pdf".
    """

    print("Generating pdf report...")

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading2"]
    subtitle_style = styles["Heading3"]

    # Set up the PDF document
    doc = SimpleDocTemplate("result/report.pdf", pagesize=landscape(A5), topMargin=0*inch, bottomMargin=0*inch)
    elements = []

    # Add the original image with title
    original_image = Image("original.jpg", width=3.5*inch, height=4*inch)
    elements.append(Paragraph("Author: Amirhossein Gholizadeh"))
    elements.append(Paragraph("Course: Image Processing"))
    elements.append(Paragraph("Chapter: 2"))
    elements.append(Paragraph("Original Image", title_style))
    elements.append(original_image)

    # Add the denoised images with titles
    image_files = [f"result/result_for_{i}_samples.jpg" for i in samples]
    titles = ["k=1", "k=5", "k=10", "k=50", "k=100", "k=500"]
    table_data = []
    for i in range(0, len(image_files), 3):
        # Create a new row for the table
        row = []
        for j in range(3):
            # Check if there is an image file for this position
            if i + j < len(image_files):
                # Create an Image object for the denoised image file
                image = Image(image_files[i + j], width=1.5*inch, height=2*inch)
                # Create a Paragraph object for the title
                title = Paragraph(titles[i + j], subtitle_style)
                # Append the image and title as a list to the row
                row.append([image, title])
        # Append the row to the table data
        table_data.append(row)
    # Create a Table object with the table data and set column widths
    table = Table(table_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    # Set the vertical alignment for all cells in the table
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(Spacer(0, 0.3*inch))
    elements.append(Paragraph("Denoised Images", title_style))
    elements.append(Spacer(0, 0.3*inch))
    elements.append(table)

    # Add the sample statistics table from CSV file
    with open('result/results.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_data = list(csv_reader)

    # Create a table from the CSV data
    stats_table = Table(csv_data, colWidths=[inch, 1.5*inch, 1.5*inch])
    stats_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
    elements.append(Spacer(0, 0.3*inch))
    elements.append(Paragraph("Sample Statistics", title_style))
    elements.append(Spacer(0, 0.3*inch))
    elements.append(stats_table)

    # Build the PDF document
    doc.build(elements)
    add_snapshot()
    print("PDF file 'report.pdf' generated successfully.")