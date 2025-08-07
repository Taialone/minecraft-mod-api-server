# ===================================================================
# File: pterodactyl_manager.py
# ===================================================================
import os
import requests

# Lấy thông tin từ biến môi trường (Environment Variables) trên Render
PTERODACTYL_PANEL_URL = os.environ.get("PTERODACTYL_PANEL_URL")
PTERODACTYL_SERVER_ID = os.environ.get("PTERODACTYL_SERVER_ID")
PTERODACTYL_API_KEY = os.environ.get("PTERODACTYL_API_KEY")

class PterodactylManager:
    """Lớp quản lý việc tương tác với Pterodactyl API."""
    def __init__(self):
        # Kiểm tra xem các biến môi trường đã được thiết lập chưa khi khởi tạo
        if not all([PTERODACTYL_PANEL_URL, PTERODACTYL_SERVER_ID, PTERODACTYL_API_KEY]):
            raise ValueError("Một hoặc nhiều biến môi trường Pterodactyl chưa được thiết lập trên hosting.")
        
        self.base_url = f"{PTERODACTYL_PANEL_URL}/api/client/servers/{PTERODACTYL_SERVER_ID}"
        self.headers = {
            "Authorization": f"Bearer {PTERODACTYL_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint, method='GET', params=None):
        """Hàm trợ giúp để thực hiện các yêu cầu API."""
        try:
            response = requests.request(method, f"{self.base_url}{endpoint}", headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi API Pterodactyl: {e}")
            return None

    def list_mods(self):
        """Lấy danh sách các file trong thư mục /mods."""
        data = self._make_request("/files/list", params={"directory": "/mods"})
        if not data or "data" not in data:
            return []
        
        mods = [
            {
                "filename": item["attributes"]["name"],
                "size": item["attributes"]["size"]
            }
            for item in data["data"]
            if item["attributes"]["is_file"] and item["attributes"]["name"].endswith(".jar")
        ]
        return mods

    def get_mod_download_url(self, filename):
        """Lấy URL tải tạm thời cho một file mod."""
        encoded_filename = requests.utils.quote(f"/mods/{filename}")
        data = self._make_request(f"/files/download?file={encoded_filename}")
        if data and "attributes" in data:
            return data["attributes"]["url"]
        return None
