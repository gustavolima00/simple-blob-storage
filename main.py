from flask import Flask, request, send_file
from services.file_manager_service import FileManagerService, FileDoesNotExistException
import io

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
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_path = f'{folder_path}/{file.filename}'
    file_content = file.read()
    file_metadata = FileManagerService.save_file(file_path, file_content)
    return file_metadata.to_dict(), 200


@app.route('/get-file', methods=['GET'])
def download_file():
    file_path = request.args.get('file_path', '')
    try:
        file_stream, metadata = FileManagerService.get_file(file_path)
        file_content = file_stream.read()
        file_bytes = io.BytesIO(file_content)

        return send_file(file_bytes, download_name=metadata.name, as_attachment=True)
    except FileDoesNotExistException:
        return f'File {file_path} does not exist', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
