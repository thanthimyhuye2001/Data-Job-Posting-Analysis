# =============================================================================
# crawl_careerviet_2_group.py
# Crawl job listings từ CareerViet lĩnh vực data, kết hợp 2 nhóm giao diện
# =============================================================================

'''
── KHUNG CHÍNH ────────────────────────────────────────────────────────────────

1. IMPORT                           Khai báo các thư viện/module
2. CẤU HÌNH & HỆ THỐNG              Các biến toàn cục quan trọng
3. LOGGING                          Khai báo nhật ký -> theo dõi & gỡ lỗi
4. CÁC FUNCTION LẤY TỪNG TRƯỜNG     Khai báo các function để lấy từng trường (Group 1 và Group 2)
5. VÒNG LẶP CHÍNH                   Cào url trong 1 page -> cào chi tiết từng url -> lưu vào CSV -> next page
6. ENTRY POINT                      Khối lệnh kích hoạt hàm main() -> thực thi toàn bộ program
───────────────────────────────────────────────────────────────────────────────
'''

# ── 1. IMPORT ────────────────────────────────────────────────────────────────────

import time
import re
import datetime
import csv
import logging
import sys
import os
import random

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ── 2. CẤU HÌNH & HỆ THỐNG ───────────────────────────────────────────────────────
KEYWORDS = [
    "Data Analyst", "Business Intelligence", "Data Visualization", "Product Analyst", "Marketing Analyst",
    "Data Engineer", "Data Architect", "Data Warehouse", "ETL", "Analytics Engineer", "Cloud Data",
    "Data Scientist", "Machine Learning", "AI Engineer", "NLP Engineer", "Computer Vision Engineer", "Algorithm Engineer", "MLOps Engineer",
    "Database Administrator", "Data Modeler", "Data Governance Specialist", "Data Quality Analyst", "Database Developer",
    "Big Data Engineer", "Quantitative Analyst"
]


BASE_URL_TEMPLATE = "https://careerviet.vn/viec-lam/{keyword}-k-sortdv-trang-{page}-vi.html"

MAX_PAGES = 60  # Giới hạn tối đa số page để crawl cho mỗi keyword

OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data_raw", "data_careerviet.csv")

# Config stdout to use UTF-8 instead of cp1252 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# ── 3. LOGGING ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Logging", "logging_careerviet.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)


# ── 4. CÁC FUNCTION LẤY TỪNG TRƯỜNG ─────────────────────────────────────────────

def get_links(soup):
    all_links = []
    try:
        # 1. Tìm container chứa danh sách công việc
        job_list_box = soup.find("div", class_="jobs-side-list", id="jobs-side-list-content")

        if job_list_box:
            # 2. Tìm tất cả các thẻ <a> chứa link job.
            a_tags = job_list_box.select('h2 a.job_link[href]')
            
            for a in a_tags:
                raw_link = a.get('href')
                
                if raw_link:
                    # 3. Làm sạch link
                    clean_link = "https://careerviet.vn" + raw_link.split('?')[0]
                    all_links.append(clean_link)
                    
    except Exception as e:
        logging.error(f"Lỗi khi lấy danh sách link: {e}")
        pass
        
    return all_links

# ====== HÀM CHO GROUP 1 (GIAO DIỆN CHUẨN) ======
def get_title(soup):
    try:
        title_tag = soup.find('h1', class_='title')
        if title_tag:
            return title_tag.get_text(separator=' ', strip=True)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy title: {e}")
        return None

def get_company(soup):
    try:
        company_tag = soup.find('a', class_=re.compile(r'(?=.*job-company-name)', re.IGNORECASE))
        if company_tag:
            return company_tag.get_text(strip=True)
        return None
    except Exception:
        return None

def get_location(box_info):
    try:
        if not box_info:
            return None
        location_box = box_info.find('div', class_='map')
        if location_box:
            location_tag = location_box.find('p')
            if location_tag:
                return location_tag.get_text(strip=True)
        return None
    except Exception:
        return None

def get_careerviet_job_details(box_info):
    job_info = {}
    try:
        if not box_info:
            return job_info
        li_tags = box_info.find_all('li')
        for li in li_tags:
            strong_tag = li.find('strong')
            p_tag = li.find('p')
            if strong_tag and p_tag:
                key = strong_tag.get_text(strip=True)
                value = p_tag.get_text(separator=" ", strip=True)
                job_info[key] = value
        return job_info
    except Exception as e:
        logging.error(f"Lỗi lấy details: {e}")
        return job_info

def get_education_level(box_info):
    """Tìm và lấy trực tiếp thông tin "Bằng cấp" trong khối 'Thông tin khác'."""
    try:
        if not box_info:
            return None
        other_box_title = box_info.find('h3', class_="detail-title", string='Thông tin khác')
        if other_box_title:
            other_box = other_box_title.parent
            edu_tag = other_box.find('li', string=re.compile(r'Bằng cấp', re.IGNORECASE))
            if edu_tag:
                raw_text = edu_tag.get_text(strip=True)
                if ':' in raw_text:
                    return raw_text.split(':', 1)[1].strip() 
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy Bằng cấp: {e}")
        return None

def extract_paragraph_content(box_info, heading_keyword):
    """Hàm đa năng trích xuất mô tả, yêu cầu, phúc lợi"""
    try:
        if not box_info:
            return None
        pattern_string = re.compile(rf'{heading_keyword}', re.IGNORECASE)
        h2_tag = box_info.find('h2', class_='detail-title', string=pattern_string)

        if h2_tag:
            content_parts = []
            for sibling in h2_tag.find_next_siblings():
                text = sibling.get_text(separator='. ', strip=True)
                if text:
                    content_parts.append(text)

            raw_text = ' '.join(content_parts)
            clean_text = re.sub(r'[•\*●\-\+\−]', '', raw_text)
            final_text = ' '.join(clean_text.split())
            
            if final_text.startswith(('-', '=', '+', '@')):
                final_text = "'" + final_text
        
            return final_text
            
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy {heading_keyword}: {e}")
        return None

def get_job_description(box_info):
    return extract_paragraph_content(box_info, "Mô tả công việc")

def get_job_requirements(box_info):
    return extract_paragraph_content(box_info, "Yêu Cầu Công Việc")

def get_benefits(box_info):
    return extract_paragraph_content(box_info, "Phúc lợi")


# ============================================================================
# ====== HÀM CHO GROUP 2 (GIAO DIỆN ĐẶC BIỆT / VIP)                     ======
# ============================================================================

def get_title_2(head_box):
    try:
        if not head_box:
            return None
        title_tag = head_box.find('h2')
        if title_tag:
            return title_tag.get_text(separator=' ', strip=True)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy title 2: {e}")
        return None

def get_company_2(head_box):
    try:
        if not head_box:
            return None
        company_tag = head_box.find('a', class_=re.compile(r'(?=.*company)', re.IGNORECASE))
        if company_tag:
            return company_tag.get_text(strip=True)
        return None
    except Exception:
        return None

def get_general_info_2(box_info):
    info_dict = {}
    try:
        if not box_info:
            return info_dict
        tr_tags = box_info.find_all('tr')
        for tr in tr_tags:
            td_tags = tr.find_all('td')
            if len(td_tags) == 2:
                key = td_tags[0].get_text(strip=True)
                raw_value = td_tags[1].get_text(separator=" ", strip=True)
                clean_value = raw_value.replace(" ,", ",")
                info_dict[key] = clean_value
        return info_dict
    except Exception as e:
        logging.error(f"Lỗi khi lấy thông tin chung 2: {e}")
        return info_dict

def get_location_2(new_soup, job_info):
    try:
        location_dict = job_info.get('Địa điểm')
        if not location_dict:
            box_location = new_soup.find('div', class_='detail-row info-place-detail')
            if box_location:
                location_tag = box_location.find('div', class_='place')
                if location_tag:
                    return location_tag.get_text(strip=True)
        else:
            return location_dict
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy Địa điểm 2: {e}")
        return None

def get_education_level_2(new_soup):
    try:
        other_box_title = new_soup.find('h3', class_="detail-title", string='Thông tin khác')
        if other_box_title:
            other_box = other_box_title.parent
            edu_tag = other_box.find(
                lambda tag: tag.name == 'li' and 'Bằng cấp' in tag.get_text(strip=True)
            )
            if edu_tag:
                raw_text = edu_tag.get_text(strip=True)
                if ':' in raw_text:
                    return raw_text.split(':', 1)[1].strip() 
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy Bằng cấp 2: {e}")
        return None

def extract_paragraph_content_2(new_soup, heading_keyword):
    try:
        pattern_string = re.compile(rf'{heading_keyword}', re.IGNORECASE)
        h2_tag = new_soup.find(['h2', 'h3'], class_='detail-title', string=pattern_string)

        if h2_tag:
            content_parts = []
            for sibling in h2_tag.find_next_siblings():
                text = sibling.get_text(separator='. ', strip=True)
                if text:
                    content_parts.append(text)

            raw_text = ' '.join(content_parts)
            clean_text = re.sub(r'[•\*●\-\+\−]', '', raw_text)
            final_text = ' '.join(clean_text.split())
            
            if final_text.startswith(('-', '=', '+', '@')):
                final_text = "'" + final_text
        
            return final_text
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy {heading_keyword} 2: {e}")
        return None

def get_job_description_2(new_soup):
    return extract_paragraph_content_2(new_soup, "Mô tả công việc")

def get_job_requirements_2(new_soup):
    return extract_paragraph_content_2(new_soup, "Yêu Cầu Công Việc")

def get_benefits_2(new_soup):
    return extract_paragraph_content_2(new_soup, "Phúc lợi")


# ── 5. VÒNG LẶP CHÍNH ────────────────────────────────────────────────────────────

def main():
    options = uc.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)

    # Thêm user-data-dir để tránh lỗi Crash (no such window) khi dùng temp profile
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    profile_dir = os.path.join(current_dir, "careerviet_profile")
    options.add_argument(f"--user-data-dir={profile_dir}")

    # Khởi tạo Undetected Chromedriver
    driver = uc.Chrome(options=options, version_main=148) 
    driver.set_window_size(900, 1080)
    driver.set_window_position(900, 0)
    
    csv_columns = [
        "index", "job_url", "search_keyword", "job_title", "company_name", 
        "location", "posted_date", "deadline_date", "category", "work_type", 
        "salary", "experience", "level_employee", "education_level", 
        "description", "requirements", "benefits", "source_site"
    ]

    # ── TẠO FILE CSV & CHECK TRÙNG LẶP DATA ──────────────────────────────────
    
    global_index = 1
    scraped_links = set()
    
    if os.path.exists(OUTPUT_CSV):
        try:
            with open(OUTPUT_CSV, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    link = row.get("job_url")
                    if link:
                        scraped_links.add(link)
                    try:
                        idx = int(row.get("index", 0))
                        if idx >= global_index:
                            global_index = idx + 1
                    except ValueError:
                        pass
            logging.info(f"Đã quét file CSV cũ. Bắt đầu nối từ index {global_index}. Đã lưu {len(scraped_links)} links.")
            print(f"File cũ tồn tại. Số job đã cào: {len(scraped_links)}. Bắt đầu từ index {global_index}.")
        except Exception as e:
            logging.error(f"Lỗi khi đọc file CSV cũ: {e}")
    else:
        try:
            with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=csv_columns)
                writer.writeheader()
        except IOError:
            logging.error("Lỗi khi tạo file CSV mới")
            print("Lỗi tạo file CSV.")
            driver.quit()
            return

    # ── CRAWL DATA ────────────────────────────────────────────────────────────
    
    for raw_keyword in KEYWORDS:
        # CareerViet url keyword chuẩn hoá thường dùng "-"
        formatted_keyword = raw_keyword.lower().replace(' ', '-')
        
        logging.info(f"==> BẮT ĐẦU CÀO KEYWORD: '{raw_keyword}' (URL: {formatted_keyword})")
        print(f"\n{'='*60}")
        print(f"BẮT ĐẦU QUÉT KEYWORD: {raw_keyword.upper()}")
        print(f"{'='*60}\n")
        
        for page in range(1, MAX_PAGES + 1):
            logging.info(f"keyword '{raw_keyword}' - Cào page {page} ===")
            print(f"\n---> keyword '{raw_keyword}' - Cào page {page} ===")
            
            target_url = BASE_URL_TEMPLATE.format(keyword=formatted_keyword, page=page)
            
            try:
                driver.get(target_url)
                time.sleep(random.uniform(3, 6))
            except Exception as e:
                logging.error(f"Lỗi tải trang tổng {target_url}: {e}")
                continue
            
            # Cuộn trang xuống cuối
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_list_box = soup.find("div", class_="jobs-side-list", id="jobs-side-list-content")
            
            if not job_list_box:
                logging.info(f"Không tìm thấy job list ở trang {page} cho '{raw_keyword}'. Dừng cào từ khóa này.")
                print(f"[THÔNG BÁO] Trang {page} không chứa job nào, hoặc đã hết. Chuyển sang từ khóa khác.")
                break
                
            job_tags = job_list_box.select('h2 a.job_link[href]')
            if len(job_tags) == 0:
                logging.info(f"Trang {page} rỗng cho '{raw_keyword}'. Dừng.")
                print(f"[THÔNG BÁO] Trang {page} rỗng. Chuyển.")
                break
                
            links = get_links(soup)
            logging.info(f"Tìm thấy {len(links)} job links ở trang {page}.")
            print(f"Từ khóa '{raw_keyword}' | Trang {page} tìm thấy {len(links)} job links.")
            
            for i, job_link in enumerate(links):
                if job_link in scraped_links:
                    logging.info(f"Bỏ qua job đã cào: {job_link}")
                    print(f"Bỏ qua job đã cào: {job_link}")
                    continue
                    
                logging.info(f"Đang cào job {i+1}/{len(links)} (page {page}): {job_link}")
                print(f"Đang cào job {i+1}/{len(links)} (page {page}): {job_link}")
                
                try:
                    driver.get(job_link)
                    time.sleep(random.uniform(3, 6))
                    
                    last_inner = driver.execute_script("return document.body.scrollHeight")
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        new_inner = driver.execute_script("return document.body.scrollHeight")
                        if new_inner == last_inner:
                            break
                        last_inner = new_inner
                    
                    new_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    box_info = new_soup.find('section', class_='job-detail-content')
                    
                    if box_info:
                        # ===== CÀO GIAO DIỆN CHUẨN (GROUP 1) =====
                        job_info_dict = get_careerviet_job_details(box_info)
                        job_data_dict = {
                            "index":              global_index,
                            "job_url":            job_link,
                            "search_keyword":     raw_keyword,
                            "job_title":          get_title(new_soup),
                            "company_name":       get_company(new_soup),
                            "location":           get_location(box_info),
                            "posted_date":        job_info_dict.get("Ngày cập nhật"),
                            "deadline_date":      job_info_dict.get("Hết hạn nộp"),
                            "category":           job_info_dict.get("Ngành nghề"),
                            "work_type":          job_info_dict.get("Hình thức"),
                            "salary":             job_info_dict.get("Lương"),
                            "experience":         job_info_dict.get("Kinh nghiệm"),
                            "level_employee":     job_info_dict.get("Cấp bậc"),
                            "education_level":    get_education_level(box_info),
                            "description":        get_job_description(box_info),
                            "requirements":       get_job_requirements(box_info),
                            "benefits":           get_benefits(box_info),
                            "source_site":        "careerviet.vn"
                        }
                    else:
                        # ===== CÀO GIAO DIỆN ĐẶC BIỆT/VIP (GROUP 2) =====
                        logging.info(f"Không có box_info chuẩn, chuyển sang bóc tách Group 2 cho: {job_link}")
                        print(f"Phát hiện giao diện đặc biệt/VIP, áp dụng logic Group 2...")
                        
                        head_box = new_soup.find('div', class_='head-left')
                        box_info_2 = new_soup.find('div', class_='box-info')
                        job_info_dict_2 = get_general_info_2(box_info_2)
                        
                        job_data_dict = {
                            "index":              global_index,
                            "job_url":            job_link,
                            "search_keyword":     raw_keyword,
                            "job_title":          get_title_2(head_box),
                            "company_name":       get_company_2(head_box),
                            "location":           get_location_2(new_soup, job_info_dict_2),
                            "posted_date":        job_info_dict_2.get("Ngày cập nhật"),
                            "deadline_date":      job_info_dict_2.get("Hết hạn nộp"),
                            "category":           job_info_dict_2.get("Ngành nghề"),
                            "work_type":          job_info_dict_2.get("Hình thức"),
                            "salary":             job_info_dict_2.get("Lương"),
                            "experience":         job_info_dict_2.get("Kinh nghiệm"),
                            "level_employee":     job_info_dict_2.get("Cấp bậc"),
                            "education_level":    get_education_level_2(new_soup),
                            "description":        get_job_description_2(new_soup),
                            "requirements":       get_job_requirements_2(new_soup),
                            "benefits":           get_benefits_2(new_soup),
                            "source_site":        "careerviet.vn"
                        }
                    
                    with open(OUTPUT_CSV, mode="a", newline="", encoding="utf-8-sig") as file:
                        writer = csv.DictWriter(file, fieldnames=csv_columns)
                        writer.writerow(job_data_dict)
                    
                    scraped_links.add(job_link)
                    global_index += 1
                    
                except Exception as e:
                    logging.error(f"Lỗi khi cào dữ liệu bên trong job {job_link}: {e}")
                    continue

    driver.quit()
    print("\n[HOÀN THÀNH] Đã cào xong dữ liệu CareerViet!")


# ── 6. ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
