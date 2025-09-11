import os
import requests
from datetime import datetime, timedelta
import time


start_date = datetime(2018, 4, 10)
end_date = datetime(2025, 8, 20)
base_url = "https://www.caiso.com/outlook/history/{date}/{file}.csv"
output_dirs = {
    "fuelsource": "supply_trend",
    "co2": "co2_per_resource"
}

for folder in output_dirs.values():
    os.makedirs(folder, exist_ok=True)

def download_file(url, path, max_retries=3):
    for _ in range(max_retries):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                return True
        except Exception:
            time.sleep(1)
    return False


current = start_date
while current <= end_date:
    date_str = current.strftime("%Y%m%d")
    for file_key, folder in output_dirs.items():
        file_path = os.path.join("data", folder, f"{date_str}.csv")
        if not os.path.exists(file_path):
            url = base_url.format(date=date_str, file=file_key)
            download_file(url, file_path)
    current += timedelta(days=1)
