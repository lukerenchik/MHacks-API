import sys, io, pathlib, fitz
from PIL import Image
import re
import ChatGPT
import visionFromFile
def remove_non_standard_characters(s):
    # This regular expression pattern keeps only letters, digits, spaces, and some punctuation
    pattern = r"[^A-Za-z0-9 ,.!?]"
    # Substitute non-standard characters with an empty string
    return re.sub(pattern, '', s)

def parseText(fname):
    with fitz.open(fname) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])
        text = remove_non_standard_characters(text)
        text = ChatGPT.GPTRewrite(text)
    return text
    # write as a binary file to support non-ASCII characters
    pathlib.Path("text.txt").write_bytes(text.encode())

def parseImages(fname):
    pdf_file = fitz.open(fname)
    imageDescriptions = []
    for page_index in range(len(pdf_file)):

        # get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images()

        # printing number of images found in this page
        if image_list:
            pass
                #print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            pass
                #print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(), start=1):
            # get the XREF of the image
            xref = img[0]

            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # get the image extension
            image_ext = base_image["ext"]

            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert('RGB')
            # save it to local disk
            image.save(open(f"image{page_index + 1}_{image_index}.jpg", "wb"))
            image_description = visionFromFile.describe_image(f"image{page_index + 1}_{image_index}.jpg")
            imageDescriptions.append(image_description)
    return imageDescriptions




#parseText("docs/michigan_maryland.pdf")
#parseImages("docs/michigan_maryland.pdf")