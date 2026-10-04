import time
import re
import csv
import logging
import os
import sys

from bs4 import BeautifulSoup
import undetected_chromedriver as uc

current_dir = os.path.dirname(os.path.abspath(__file__))

INPUT_CSV = os.path.join(os.path.dirname(current_dir), "Data_raw", "data_itviec.csv")
OUTPUT_CSV = os.path.join(os.path.dirname(current_dir), "Data_raw", "data_itviec_intern.csv")

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    filename=os.path.join(os.path.dirname(current_dir), "Logging", "logging_itviec_intern.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)

def get_is_intern(soup):
    """Kiểm tra job có nhận Intern không."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            intern_tag = info_box.find('a', string=re.compile(r'Internship Accepted', re.IGNORECASE))
            if intern_tag:
                return "Yes"
        return "No"
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra intern: {e}")
        return "No"

def main():
    options = uc.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options, version_main=148) 
    driver.set_window_size(900, 1080)
    driver.set_window_position(900, 0)

    # Tạo file mới có 3 cột
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "job_url", "is_intern"])
        writer.writeheader()

    print("Bắt đầu cào dữ liệu...")
    # Đọc tuần tự từng dòng url và cào
    with open(INPUT_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = row.get("index")
            link = row.get("job_url")
            
            if link:
                print(f"Đang cào index {idx}...")
                try:
                    driver.get(link)
                    time.sleep(3)
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    is_intern = get_is_intern(soup)
                    
                    # Cào xong 1 job thì ghi luôn vào file
                    with open(OUTPUT_CSV, mode="a", newline="", encoding="utf-8-sig") as out_f:
                        writer = csv.DictWriter(out_f, fieldnames=["index", "job_url", "is_intern"])
                        writer.writerow({
                            "index": idx,
                            "job_url": link,
                            "is_intern": is_intern
                        })
                except Exception as e:
                    logging.error(f"Lỗi khi cào link {link}: {e}")

    driver.quit()
    print("Đã cào xong!")

if __name__ == "__main__":
    main()
