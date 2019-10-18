import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from resume_parser.resume_parser import ResumeParser
# UPLOAD_FOLDER = '/Users/lv04cs/Downloads/fldirectory'
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    resume_parser = ResumeParser(filename)
    return resume_parser.get_extracted_data()
    # cli_obj = ResumeParserCli()
    # total_data = cli_obj.extract_resume_data()
    # for x in total_data:
    #     # print(x)
    #
    #     print(x['name'])
    #     print("\n")
    #     x_string = ','.join(x['skills'])
    #     # model = tf.keras.models.load_model('./Siamese-LSTM/data/SiameseLSTM.h5', custom_objects={'ManDist': ManDist})
    #     # prediction = model.predict([skill_req, x_string])
    #     # print(prediction)
    #
    # pprint(cli_obj.extract_resume_data())
    # return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                            filename)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True, threaded=True)