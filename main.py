from flask import Flask, request, send_from_directory
from models.object import ObjectMetadata
from services.file_manager_service import FileManagerService
import os
import time

app = Flask(__name__)
BASE_UPLOAD_FOLDER = './uploads'
FileManagerService.make_directory(BASE_UPLOAD_FOLDER, exist_ok=True)


@app.route('/list', methods=['GET'])
def list_files():
    path_prefix = request.args.get('path_prefix', '')
    list_files = request.args.get('files', 'true').lower() == 'true'
    list_folders = request.args.get('folders', 'true').lower() == 'true'
    objects = FileManagerService.list_files(
        path_prefix, list_files, list_folders)
    return objects, 200


@app.route('/upload/<path:folder_path>', methods=['POST'])
def upload_file(folder_path):
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    path = os.path.join(BASE_UPLOAD_FOLDER, folder_path)
    file_metadata = FileManagerService.save_file(
        path, file, create_folders=True)
    return file_metadata, 200


@app.route('/download/<path:key>', methods=['GET'])
def download_file(key):
    full_path = os.path.join(BASE_UPLOAD_FOLDER, key)
    if not os.path.isfile(full_path):
        return f'File {key} does not exist', 404
    return send_from_directory(BASE_UPLOAD_FOLDER, key, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
