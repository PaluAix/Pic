from flask import Flask, request, send_file, render_template
import os
import zipfile
from PIL import Image
import shutil
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
UNZIP_FOLDER = 'unzipped'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UNZIP_FOLDER'] = UNZIP_FOLDER

# 确保上传和解压的文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UNZIP_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 处理上传的文件
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.zip'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            unzip_and_classify(filepath)
            return render_template('download_links.html', categories=list_categories())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new Zip File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def unzip_and_classify(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(UNZIP_FOLDER)
        for foldername, subfolders, filenames in os.walk(UNZIP_FOLDER):
            for filename in filenames:
                if filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif')):
                    image_path = os.path.join(foldername, filename)
                    try:
                        with Image.open(image_path) as img:
                            width, height = img.size
                            size_folder = f'{width}x{height}'
                            size_folder_path = os.path.join(UNZIP_FOLDER, size_folder)
                            if not os.path.exists(size_folder_path):
                                os.makedirs(size_folder_path)
                            shutil.move(image_path, size_folder_path)
                    except Exception as e:
                        print(f'Error processing image {filename}: {e}')

def list_categories():
    return [d for d in os.listdir(UNZIP_FOLDER) if os.path.isdir(os.path.join(UNZIP_FOLDER, d))]

@app.route('/download/<category>')
def download_category(category):
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        category_path = os.path.join(UNZIP_FOLDER, category)
        for root, dirs, files in os.walk(category_path):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, arcname=file)
    memory_file.seek(0)
    return send_file(memory_file, download_name=f'{category}.zip', as_attachment=True, mimetype='application/zip')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
