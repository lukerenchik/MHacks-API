import sys, io, pathlib, fitz
from PIL import Image 

def parse(fname):
    
    with fitz.open(fname) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])

    # write as a binary file to support non-ASCII characters
    pathlib.Path("out/text.txt").write_bytes(text.encode())


    pdf_file = fitz.open(fname) 

    
    for page_index in range(len(pdf_file)): 
    
        # get the page itself 
        page = pdf_file[page_index] 
        image_list = page.get_images() 
    
        # printing number of images found in this page 
        if image_list: 
            print( 
                f"[+] Found a total of {len(image_list)} images in page {page_index}") 
        else: 
            print("[!] No images found on page", page_index) 
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
            image.save(open(f"out/image{page_index+1}_{image_index}.jpg", "wb"))
            

parse("docs/michigan_maryland.pdf")

