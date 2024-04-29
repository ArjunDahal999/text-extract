import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import re
import requests
from io import BytesIO
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def ok():
    return {"message": "Hello World"}

@app.post("/extract_emails/")
async def extract_emails_from_image(image_url: str):
    response = requests.get(image_url)
    img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)

    reader = easyocr.Reader(['en'], gpu=True)
    text = []
    text_ = reader.readtext(img)

    for  t in (text_):
        if "@" in t[1]:  
            text.append(t[1].strip().replace(" ", ".")) 
        else:
            text.append(t[1].strip())

    # Define email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find and print all email addresses in the text
    extracted_emails = []
    for email in text:
        if re.search(email_pattern, email):
            extracted_emails.append(email)

    return {"extracted_emails": extracted_emails,"Other Data":text}

