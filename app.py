import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_file
import sys
sys.path.append('C:/Users/NEW/Desktop/Flaskapp/mrsketcherapp/Lib/site-packages/')
import cv2

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (19, 19), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=256)
    return final_result

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sketch_img = make_sketch(img)
            sketch_img_name = filename.rsplit('.', 1)[0] + "_sketch.jpg"
            sketch_img_path = os.path.join(app.config['UPLOAD_FOLDER'], sketch_img_name)
            cv2.imwrite(sketch_img_path, sketch_img)
            return render_template('home.html', org_img_name=filename, sketch_img_name=sketch_img_name)
    return render_template('home.html')

@app.route('/download/<path:filename>')
def download(filename):
    sketch_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(sketch_img_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
