from reportlab.lib.pagesizes import landscape, A5
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

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
    doc = SimpleDocTemplate("result/report.pdf", pagesize=landscape(A5),topMargin=0*inch, bottomMargin=0*inch)
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
    print("PDF file 'report.pdf' generated successfully.")