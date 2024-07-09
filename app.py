from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cartoonize_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    gray = cv2.medianBlur(gray, 5)

    # Perform adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # Combine color and edges
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Save the cartoon image temporarily
    cartoon_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cartoonized_image.jpg')
    cv2.imwrite(cartoon_path, cartoon)

    return cartoon_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartoonize', methods=['POST'])
def cartoonize():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    # If the user does not select a file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded image to a temporary location
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg')
        file.save(image_path)

        # Perform cartoonization
        cartoon_path = cartoonize_image(image_path)

        # Redirect to the result page
        return render_template('cartoonized.html', cartoon_image=cartoon_path)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
