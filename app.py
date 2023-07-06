# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#   return "Hello World!"
#
# if __name__ == "__main__":
#   app.run()

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import urllib.request

from Algorithms import star_match

app = Flask(__name__)

UPLOAD_FOLDER = 'static/upload_star_match_files/'

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_P = '.p'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def myhome():
    return render_template('home.html')


@app.route('/algo1')
def algo1():
    return render_template('algo1.html')


@app.route('/algo2')
def algo2():
    return render_template('algo2.html')


@app.route('/algo3')
def algo3():
    return render_template('algo3.html')


@app.route('/algo4')
def algo4():
    return render_template('algo4.html')


@app.route('/forms', methods=['GET', 'POST'])
def forms():
    return render_template('forms.html')


@app.route('/process_forms', methods=['POST'])
def process_forms():
    input1 = request.form['input1']
    input2 = request.form['input2']
    input3 = request.form['input3']

    # Process the inputs using your algorithm
    # ...
    print("input1: " + input1, "input2: " + input2, "input 3: " + input3)
    return "Inputs processed successfully."


#
# @app.route('/', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     files = request.files.getlist('file')
#     if len(files) > 2:
#         error = "You are only allowed to upload a maximum of 2 files"
#         flash(error)
#         return render_template("upload.html")
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_names.append(filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         else:
#             flash('Allowed image types are -> png, jpg, jpeg, gif')
#             return redirect(request.url)
#
#     return render_template('upload.html', filenames=file_names)


def get_result(page, new_file_paths, file_urls):
    if len(file_urls) == 2:
        # Extract file url
        for index, file_url in enumerate(file_urls):
            directory, filename = os.path.split(file_url)
            directory_path = "static/upload_star_match_files/"
            direct_file_names = os.listdir(directory_path)
            print("direct_file_names", direct_file_names)
            base_name, extension = os.path.splitext(filename)
            print("base_name", base_name)

            new_base_name = "file" + str(index)
            new_file_path = os.path.join(directory_path, new_base_name + extension)
            # Rename the file
            print("new_file_path", new_file_path)
            os.rename(file_urls[index], new_file_path)
            print(new_file_path)
            new_file_paths.append(new_file_path)
        result = star_match.get_photos(new_file_paths)
        printoscreen = []
        for new_file in new_file_paths:
            print("new_file", new_file)
            new_path = new_file.replace("static/", "", 1)
            print(new_path)
            printoscreen.append(new_path)
        return render_template(page, file_urls=printoscreen)
    else:
        flash('You are only allowed to upload two files')
        directory_path = 'static/upload_star_match_files/'  # Specify the directory path
        # Get a list of files in the directory
        file_list = os.listdir(directory_path)
        # Iterate over the files and delete them
        for file_name in file_list:
            file_path = os.path.join(directory_path, file_name)
            os.remove(file_path)
        return redirect(request.url)


def upload_image(page):
    file_names = []
    Links = []
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('file')
    if len(files) != 2:
        flash("You are only allowed to upload 2 files")
        return render_template(page)
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            directory_path = 'static/upload_star_match_files/'  # Specify the directory path
            # Get a list of files in the directory
            file_list = os.listdir(directory_path)
            # Iterate over the files and delete them
            for file_name in file_list:
                file_path = os.path.join(directory_path, file_name)
                os.remove(file_path)
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    directory_path = "static/upload_star_match_files/"
    direct_file_names = os.listdir(directory_path)
    file_urls = []
    for file_name in direct_file_names:
        file_path = os.path.join(directory_path, file_name)
        file_url = urllib.parse.quote(file_path)
        file_urls.append(file_url)
        print("file_urlssss: ", file_url)
    new_file_paths = []
    return get_result(page, new_file_paths, file_urls)


@app.route('/algo1', methods=['Get', 'POST'])
def upload_image_algo1():
    return upload_image("algo1.html")


def process_file(file):
    # Perform operations on the file
    # Example: Read the file and return the contents
    content = file.read()
    return content


@app.route('/algo2', methods=['POST'])
def upload_image_algo2():
    file_names = []
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('file')
    if len(files) != 1:
        flash("You are only allowed to upload 1 file")
        return render_template("algo2.html")
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    print("filename", filename)
    return render_template("algo2.html", filenames=file_names)


@app.route('/algo3', methods=['POST'])
def upload_image_algo3():
    return upload_image("algo3.html")


@app.route('/algo4', methods=['POST'])
def upload_image_algo4():
    return upload_image("algo4.html")


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='upload_star_match_files/' + filename), code=301)


if __name__ == "__main__":
    app.run()
