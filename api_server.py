# ===================================================================
# File: api_server.py
# ===================================================================
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from pterodactyl_manager import PterodactylManager

app = Flask(__name__)
CORS(app) 
ptero_manager = PterodactylManager()

@app.route('/')
def home():
    return "API Server for Mod Downloader is running."

@app.route('/api/mod-list', methods=['GET'])
def get_mod_list():
    """Endpoint trả về danh sách các mod trên server."""
    mods = ptero_manager.list_mods()
    if mods is None:
        return jsonify({"error": "Không thể lấy danh sách mod từ Pterodactyl."}), 500
    return jsonify({"mods": mods})

@app.route('/api/mod-download-url', methods=['GET'])
def get_mod_download_url():
    """Endpoint trả về URL tải tạm thời cho một mod cụ thể."""
    mod_filename = request.args.get('filename')
    if not mod_filename:
        abort(400, description="Thiếu tham số 'filename'.")
    
    url = ptero_manager.get_mod_download_url(mod_filename)
    if not url:
        abort(404, description=f"Không tìm thấy file '{mod_filename}' hoặc không thể tạo link tải.")
    
    return jsonify({"download_url": url})

# Dòng này không cần thiết khi chạy với Gunicorn, nhưng giữ lại cũng không sao
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


