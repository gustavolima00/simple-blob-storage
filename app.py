from flask import Flask, request, send_from_directory
import os
import time

app = Flask(__name__)
BASE_UPLOAD_FOLDER = './uploads'
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)


def create_folder_if_not_exist(folder_path):
    os.makedirs(folder_path, exist_ok=True)

@app.route('/list', methods=['GET'])
def list_files():
    path_prefix = request.args.get('path_prefix', '')
    list_files = request.args.get('files', 'true').lower() == 'true'
    list_folders = request.args.get('folders', 'true').lower() == 'true'

    full_folder_path = os.path.join(BASE_UPLOAD_FOLDER, path_prefix)
    if not os.path.isdir(full_folder_path):
        return f'Folder {path_prefix} does not exist', 404

    items = []
    for item in os.listdir(full_folder_path):
        item_path = os.path.join(full_folder_path, item)
        if os.path.isdir(item_path) and list_folders:
            item_type = 'folder'
        elif os.path.isfile(item_path) and list_files:
            item_type = 'file'
        else:
            continue

        item_metadata = {
            'name': item,
            'type': item_type,
            'size': os.path.getsize(item_path),
            'last_modified': time.ctime(os.path.getmtime(item_path))
        }
        items.append(item_metadata)

    return {'items': items}, 200


@app.route('/upload/<path:folder_path>', methods=['POST'])
def upload_file(folder_path):
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    full_folder_path = os.path.join(BASE_UPLOAD_FOLDER, folder_path)
    create_folder_if_not_exist(full_folder_path)
    filepath = os.path.join(full_folder_path, file.filename)
    file.save(filepath)
    return f'File {file.filename} uploaded successfully to {folder_path}', 200


@app.route('/download/<path:file_path>', methods=['GET'])
def download_file(file_path):
    directory, filename = os.path.split(file_path)
    return send_from_directory(os.path.join(BASE_UPLOAD_FOLDER, directory), filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
