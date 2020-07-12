import os
from flask import Flask, render_template, request
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  
import argparse
import cv2

# construct th
# import our OCR function


# define a folder to store and later serve the images


# root_dir = "C:\\Users\\Developer Tayub\\Desktop\\dataset\\LabelledRice\\Labelled"
root_dir = "C:\\Users\\Developer Tayub\\Documents\\test\\static"


UPLOAD_FOLDER = '/static/'
# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            print(file.filename)

            image = cv2.imread(file.filename)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            gray = cv2.threshold(gray, 127, 255,
                cv2.THRESH_TRUNC)[1]
            
            # filenamemaybe = "{}.png".format(os.getpid())

            # location ="C:\\Users\\Developer Tayub\\Documents\\test" + UPLOAD_FOLDER + filenamemaybe

            location= os.path.join(root_dir,"file_ic_gray.png")    
            location_ori= os.path.join(root_dir,"file_ic_ori.png")    
            print(location)

            cv2.imwrite(location, gray)

            cv2.imwrite(location_ori, image)
            new_filename= os.path.basename(location)


            extracted_text = pytesseract.image_to_string(Image.open(location))
            print(extracted_text)

                        # call the OCR function on it
            #extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='IC Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=location)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', debug=True,port=5000)