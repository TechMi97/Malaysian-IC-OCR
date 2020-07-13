import os
from flask import Flask, render_template, request
import PIL
from PIL import ImageDraw
import argparse
import easyocr


# define a folder to store and later serve the images
root_dir = "C:\\Users\\Developer Tayub\\Documents\\test\\static"

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
            image = PIL.Image.open(file.filename)
            location= os.path.join(root_dir,"file_ic_BOX.png")    
            location_ori= os.path.join(root_dir,"file_ic_ORI.png")    
            print(location)
            image.save(location_ori)

            reader = easyocr.Reader(['en'])

            bounds = reader.readtext(location_ori)

            new_text=[]

            new_text= bounds

            detail=0

            if detail == 0: 

                new_text= [item[1] for item in new_text]

                new_text = ' '.join(str(e) for e in new_text)


            image.save(location_ori)
            draw= ImageDraw.Draw(image)
            for bound in bounds:
                p0, p1, p2, p3 = bound[0]
                draw.line([*p0, *p1, *p2, *p3, *p0], fill="yellow", width=2)
            image.save(location)
            print(bounds)            


            

            # extract the text and display it
            return render_template('upload.html',
                                   msg='IC Successfully processed',
                                   extracted_text=new_text,
                                   img_src=location)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
   
    app.run(host='0.0.0.0', debug=True,port=5000)