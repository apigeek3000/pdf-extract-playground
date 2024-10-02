import os
import pypdf
import pdfminer
from pdfminer.image import ImageWriter
from pdfminer.high_level import extract_pages

def pypdf_extract_images(pdf_path, output_folder):
    """Extracts images from a PDF file and saves them to a local folder.

    Args:
        pdf_path (str): The path to the PDF file.
        output_folder (str): The path to the folder where images will be saved.
    """

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        reader = pypdf.PdfReader(pdf_file)

        # Iterate through each page of the PDF
        for page_num, page in enumerate(reader.pages):
            # Access the images on the page
            for img_num, img in enumerate(page.images):
                # Get the image data
                img_data = img.data

                # Create a unique filename for the image
                img_filename = f'page_{page_num + 1}_img_{img_num + 1}_{img.name}'
                img_path = os.path.join(output_folder, img_filename)

                # Save the image to the output folder
                try:
                    # print(f"Saving pypdf {pdf_path} image: {img_filename}")
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)
                except Exception as e:
                    print(f"ERROR saving pypdf {pdf_path} image: {img_filename}")
                    print(e)

def pdfminer_extract_images(pdf_path, output_folder):
    """Extracts images from a PDF file using pdfminer and saves them to a local folder.

    Args:
        pdf_path (str): The path to the PDF file.
        output_folder (str): The path to the folder where images will be saved.
    """

    def get_image(layout_object):
        if isinstance(layout_object, pdfminer.layout.LTImage):
            return layout_object
        if isinstance(layout_object, pdfminer.layout.LTContainer):
            for child in layout_object:
                return get_image(child)
        else:
            return None

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    pages = list(extract_pages(pdf_path))
    for page_num, page in enumerate(pages):
        # Get images on the page
        images = list(filter(bool, map(get_image, page)))

        # Write images for page to output folder
        iw = ImageWriter(output_folder)
        for image_num, image in enumerate(images):
            image.name = f'page_{page_num + 1}_img_{image_num + 1}_{image.name}'
            try:
                # print(f"Saving pdfminer {pdf_path} image: {image.name}")
                iw.export_image(image)
            except Exception as e:
                print(f"ERROR saving pdfminer {pdf_path} image: {image.name}")
                print(e)

# Extract images from the pdf
example_pdf_path = './pdfs/example.pdf'
pypdf_example_output_path = './pdfs/pypdf_example'
pdfminer_example_output_path = './pdfs/pdfminer_example'
pypdf_extract_images(example_pdf_path, pypdf_example_output_path)
pdfminer_extract_images(example_pdf_path, pdfminer_example_output_path)
