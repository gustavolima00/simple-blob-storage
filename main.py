from flask import Flask, request, send_from_directory
from models.object import Object
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

        key = os.path.join(path_prefix, item)
        object_instance = Object(
            name=item,
            obj_type=item_type,
            size=os.path.getsize(item_path),
            last_modified=time.ctime(os.path.getmtime(item_path)),
            key=key
        )
        items.append(object_instance.to_dict())

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
    key = os.path.join(folder_path, file.filename)
    object_instance = Object(
        name=file.filename,
        obj_type='file',
        size=os.path.getsize(filepath),
        last_modified=time.ctime(os.path.getmtime(filepath)),
        key=key
    )
    return object_instance.to_dict(), 200


@app.route('/download/<path:key>', methods=['GET'])
def download_file(key):
    full_path = os.path.join(BASE_UPLOAD_FOLDER, key)
    if not os.path.isfile(full_path):
        return f'File {key} does not exist', 404
    return send_from_directory(BASE_UPLOAD_FOLDER, key, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
