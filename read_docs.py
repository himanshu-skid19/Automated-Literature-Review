from imports import *
from run_llava import *

def download_pdf(url, file_name):

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)

def extract_text_from_pdf(pdf_path, output_dir='pdf_content/'):
    """
    Extracts text from each page of a PDF file and saves each page's text as a separate text file.
    
    Parameters:
    - pdf_path (str): The file path to the PDF from which to extract text.
    - output_dir (str): The directory path where text files will be saved.
    
    Returns:
    - int: Number of pages processed and saved as text files.
    """
    data_path = Path(output_dir)
    if not data_path.exists():
        data_path.mkdir(parents=True, exist_ok=True)

    text_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text_file_path = data_path / f"page_{i}.txt"
                with open(text_file_path, "w", encoding='utf-8') as file:  # Specify UTF-8 encoding here
                    file.write(page_text)





def extract_images_from_pdf(pdf_path, save_dir='pdf_content/'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)

            image_path = os.path.join(save_dir, f'image_{page_num+1}_{xref}.png')
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)

    for i, img_bytes in enumerate(images):
        with io.BytesIO(img_bytes) as img_io:
            img = Image.open(img_io)
            plt.imshow(img)
            plt.axis('off')
            plt.title(f'Image {i+1}')
            plt.show()

    return images


def save_pdf_pages_as_images(pdf_path, output_dir):
    """
    Saves each page of a PDF as an image using PyMuPDF.

    Parameters:
    - pdf_path (str): The path to the PDF file.
    - output_dir (str): The directory where the images will be saved.

    Returns:
    - None
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Iterate through each page
    for i in range(len(doc)):
        page = doc.load_page(i)  # Load the current page
        pix = page.get_pixmap()  # Render page to an image
        image_path = os.path.join(output_dir, f"page_{i + 1}.png")
        pix.save(image_path)  # Save the image as a PNG
        print(f"Saved {image_path}")
    
    # Close the document
    doc.close()


# url = "https://arxiv.org/pdf/2401.04088.pdf"
# file_name = "mixtral.pdf"
# # download_pdf(url, file_name)

# pdf = pdfplumber.open("mixtral.pdf")
# p0 = pdf.pages[4]

# pdf_path = 'mixtral.pdf'
# output_dir = 'pages'
# # save_pdf_pages_as_images(pdf_path, output_dir)

# images = extract_images_from_pdf(file_name)



# # pdf_tables = extract_tables_from_pdf(file_name)
# # for table in pdf_tables:
# #     for row in table:
# #         print(row)