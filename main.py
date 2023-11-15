import os
from flask import Flask, request, send_file
from services.file_manager_service import FileManagerService, FileManagerServiceException
import io
from flask_cors import CORS

app = Flask(__name__)


@app.route('/list', methods=['GET'])
def list_files():
    path_prefix = request.args.get('path_prefix', '')
    list_files = request.args.get('files', 'true').lower() == 'true'
    list_folders = request.args.get('folders', 'true').lower() == 'true'
    objects = FileManagerService.list_files(
        path_prefix, list_files, list_folders)
    response = list(map(lambda obj: obj.to_dict(), objects))
    return response, 200


@app.route('/upload', methods=['POST'])
def upload_file():
    folder_path = request.args.get('folder_path', '')
    file_name = request.args.get('file_name', '')
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file_name == '':
        file_name = file.filename
    file_content = file.read()
    try:
        file_metadata = FileManagerService.save_file(
            folder_path, file_name, file_content)
        return file_metadata.to_dict(), 200
    except FileManagerServiceException as e:
        return str(e), 400


@app.route('/get-file', methods=['GET'])
def download_file():
    file_path = request.args.get('file_path', '')
    try:
        file_stream, metadata = FileManagerService.get_file(file_path)
        file_content = file_stream.read()
        file_bytes = io.BytesIO(file_content)

        return send_file(file_bytes, download_name=metadata.name, as_attachment=True)
    except FileManagerServiceException as e:
        return str(e), 400


if __name__ == '__main__':
    app_port = os.environ.get('APP_PORT', 5000)
    use_cors = os.environ.get('USE_CORS', 'false').lower() == 'true'
    print('configuration', {
        'app_port': app_port,
        'use_cors': use_cors
    })
    if use_cors:
        print('Using CORS')
        cors = CORS(app, resources={r"*": {"origins": "*"}})
    app.run(host='0.0.0.0', port=app_port)
