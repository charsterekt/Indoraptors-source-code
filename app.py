import os
import keras
from keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
from numpy import expand_dims
import imghdr
import json
from flask import Flask, session, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

with open("birds.json", "r", encoding="utf8") as file:
    birds = json.load(file)

class_names = [bird for bird in birds.keys()]

model = keras.models.load_model("xce_final.h5")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eCf68dumoS3UaaDDZTW23NPKqUIy'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'


def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    img_format = imghdr.what(None, header)
    if not img_format:
        return None
    return '.' + (img_format if img_format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return render_template('413.html'), 413

@app.errorhandler(415)
def wrong_file_type(e):
    return render_template('415.html'), 415

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def predict(path):
    K.clear_session()
    img = load_img(path, target_size=(299, 299))
    data = img_to_array(img)
    samples = expand_dims(data, 0)
    datagen = ImageDataGenerator(preprocessing_function=keras.applications.xception.preprocess_input)
    test_gen = datagen.flow(samples, batch_size = 1)
    predictions = model.predict(test_gen)
    top3 = [class_names[np.argsort(predictions[0])[-i]] for i in range(1,4)]
    top3_perc = [predictions[0][np.argsort(predictions[0])[-i]] for i in range(1,4)]
    wiki_str = "https://en.wikipedia.org/wiki/{}"
    image_str = "static/images/{}.jpg"
    guess = "{} ({})".format(top3[0], birds.get(top3[0])[0])
    conf1 = "{:.1f}% confidence".format(top3_perc[0] * 100)
    guess2 = "{} ({})".format(top3[1], birds.get(top3[1])[0])
    conf2 = "{:.1f}% confidence".format(top3_perc[1] * 100)
    guess3 = "{} ({})".format(top3[2], birds.get(top3[2])[0])
    conf3 = "{:.1f}% confidence".format(top3_perc[2] * 100)
    
    wiki = wiki_str.format("_".join(top3[0].split())).replace("'s", "%27s")
    wiki2 = wiki_str.format("_".join(top3[1].split())).replace("'s", "%27s")
    wiki3 = wiki_str.format("_".join(top3[2].split())).replace("'s", "%27s")
    bird1 = image_str.format(top3[0])
    bird2 = image_str.format(top3[1])
    bird3 = image_str.format(top3[2])
    bird_info = birds.get(top3[0])[1]  # Don't need for 2 and 3
    output = [guess, guess2, guess3, wiki, wiki2, wiki3, bird1, bird2, bird3, bird_info, conf1, conf2, conf3]
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output', methods=['GET','POST'])
def output():
    try:
        if session['filename']:
            filepath = "uploads/{}".format(session['filename'])
            output = predict(filepath)
            os.remove(filepath)
            return render_template('output.html', guess1=output[0], guess2=output[1], guess3=output[2], wiki1=output[3], wiki2=output[4], 
                                                wiki3=output[5], bird1=output[6], bird2=output[7], bird3=output[8], info=output[9], 
                                                conf1=output[10], conf2=output[11], conf3=output[12])
        else:
            abort(404)
    except FileNotFoundError:
        abort(404)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    session['filename'] = secure_filename(uploaded_file.filename)
    if session['filename'] != '':
        file_ext = os.path.splitext(session['filename'])[1]
        if file_ext == '.jpeg':
            file_ext = '.jpg'
        if (
            file_ext not in app.config['UPLOAD_EXTENSIONS']
            or file_ext != validate_image(uploaded_file.stream)
        ):
            abort(415)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], session['filename']))
    return redirect(url_for('output'))
    

if __name__ == "__main__":
    app.debug = True
    app.run()