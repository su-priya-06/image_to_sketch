import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import cv2
from sketch import convert_to_sketch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SKETCH_FOLDER'] = 'static/sketches'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SKETCH_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    sketch_filename = None
    if request.method == 'POST':
        uploaded_file = request.files['image']
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(img_path)

            # Convert to sketch
            sketch = convert_to_sketch(img_path)
            sketch_filename = f"sketch_{filename}"
            sketch_path = os.path.join(app.config['SKETCH_FOLDER'], sketch_filename)
            cv2.imwrite(sketch_path, sketch)

            return render_template('index.html',
                                   original_image=img_path,
                                   sketch_image=sketch_path,
                                   download_link=sketch_filename)

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['SKETCH_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
