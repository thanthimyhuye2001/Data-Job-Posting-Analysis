# =============================================================================
# crawl_vietnamworks.py
# Crawl job listings từ VietnamWorks lĩnh vực data
# Tác giả: Thân Thị Mỹ Huyền
# =============================================================================

'''
── KHUNG CHÍNH ────────────────────────────────────────────────────────────────

1. IMPORT                           Khai báo các thư viện/module
2. CẤU HÌNH & HỆ THỐNG              Các biến toàn cục quan trọng
3. LOGGING                          Khai báo nhật ký -> theo dõi & gỡ lỗi
4. CÁC FUNCTION LẤY TỪNG TRƯỜNG     Khai báo các function để lấy từng trường
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
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


# ── 2. CẤU HÌNH & HỆ THỐNG ───────────────────────────────────────────────────────

# Chị Thơm: BA nó ko liên quan đến data em ạ -> loại bỏ "Bussiness Analyst" khỏi list keyword
KEYWORDS = [
    "Data Analyst", "Business Intelligence", "Data Visualization", "Product Analyst", "Marketing Analyst",
    "Data Engineer", "Data Architect", "Data Warehouse", "ETL", "Analytics Engineer", "Cloud Data",
    "Data Scientist", "Machine Learning", "AI Engineer", "NLP Engineer", "Computer Vision Engineer", "Algorithm Engineer", "MLOps Engineer",
    "Database Administrator", "Data Modeler", "Data Governance Specialist", "Data Quality Analyst", "Database Developer",
    "Big Data Engineer", "Quantitative Analyst"
]


# Chuỗi mẫu URL. Parameter {keyword} và {page} sẽ được truyền vào sau qua hàm .format()
# Job đc sort theo "ngày đăng mới nhất" 
BASE_URL_TEMPLATE = "https://www.vietnamworks.com/viec-lam?q={keyword}&page={page}&sorting=lasted"


# MAX_PAGES = 60  # Giới hạn tối đa số page để crawl cho mỗi keyword cho lần đầu crawl job
MAX_PAGES = 50  # Giới hạn tối đa số page để crawl cho mỗi keyword


OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data_raw", "data_vietnamworks.csv")


# Config stdout to use UTF-8 instead of cp1252 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')



# ── 3. LOGGING ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Logging", "logging_vietnamworks.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)




# ── 4. CÁC FUNCTION LẤY TỪNG TRƯỜNG ─────────────────────────────────────────────

def human_scroll(driver):
    """Mô phỏng cuộn trang chậm từ từ như người thật để web load ảnh và thẻ HTML bị lazy-load"""
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            total_height = int(driver.execute_script("return document.body.scrollHeight"))
            for i in range(1, total_height, random.randint(300, 700)):
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(random.uniform(0.1, 0.4))
            
            time.sleep(random.uniform(1.5, 2.5))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        logging.error(f"Lỗi khi scroll: {e}")

def get_link(soup):
    """Lấy danh sách link gốc job (loại bỏ query params tracking trùng lặp)."""
    try:
        job_data = soup.find("div", class_="block-job-list")
        list_job_links_tag = job_data.find_all('a', attrs={'class': 'img_job_card'})
        all_link = []
        for link_tag in list_job_links_tag:
            href = link_tag.get('href', '')
            # Tách chuỗi tại dấu '?' và chỉ lấy phần URL gốc ở phía trước
            clean_href = href.split('?')[0]
            if clean_href:
                all_link.append("https://www.vietnamworks.com" + clean_href)
    except Exception as e:
        logging.error(f"⚠️ Lỗi khi xử lý job link: {e} --> page trống")
        all_link = []
    return all_link

def get_title(soup):
    """Lấy tiêu đề công việc."""
    try:
        return soup.find('h1', attrs={'name': 'title'}).text.strip()
    except AttributeError:
        return None

def get_company(soup):
    """Lấy tên công ty."""
    try:
        return soup.find('a', attrs={'name': 'label'}).text.strip()
    except AttributeError:
        return None

def get_local(soup):
    """Lấy địa điểm làm việc."""
    try:
        return soup.find_all('span', attrs={'name': 'paragraph'})[-1].text.strip()
    except AttributeError:
        return None

def get_deadline_date(soup):
    """Tính ngày hết hạn nộp hồ sơ."""
    try:
        raw_text = soup.find('span', attrs={'name': 'paragraph'}).text.strip()
        match = re.search(r'\d+', raw_text)
        if not match:
            return None
        number = int(match.group())
        now = datetime.datetime.now()
        
        if 'giờ' in raw_text:
            deadline = now
        elif 'ngày' in raw_text:
            deadline = now + datetime.timedelta(days=number)
        elif 'tháng' in raw_text:
            deadline = now + datetime.timedelta(days=number * 30)
        else:
            return None
            
        return deadline.strftime('%Y-%m-%d')
    except Exception:
        return None

def get_salary(soup):
    """Lấy mức lương."""
    try:
        return soup.find_all('span', attrs={'name': 'label'})[0].text.strip()
    except AttributeError:
        return None

def get_date_posted(soup):
    """Lấy ngày đăng tuyển."""
    try:
        label = soup.find("label", string="NGÀY ĐĂNG")
        return label.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_category(soup):
    """Lấy ngành nghề."""
    try:
        label_category = soup.find("label", string="NGÀNH NGHỀ")
        return label_category.find_next("p").find_all(string=True)[-1].strip()
    except AttributeError:
        return None

def get_field(soup):
    """Lấy lĩnh vực."""
    try:
        label_field = soup.find("label", string="LĨNH VỰC")
        return label_field.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_exprience(soup):
    """Lấy số năm kinh nghiệm tối thiểu."""
    try:
        label_exprience = soup.find("label", string="SỐ NĂM KINH NGHIỆM TỐI THIỂU")
        return label_exprience.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_edu(soup):
    """Lấy trình độ học vấn tối thiểu."""
    try:
        label_edu = soup.find("label", string="TRÌNH ĐỘ HỌC VẤN TỐI THIỂU")
        return label_edu.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_hire_num(soup):
    """Lấy số lượng tuyển dụng."""
    try:
        label_hire_num = soup.find("label", string="SỐ LƯỢNG TUYỂN DỤNG")
        return label_hire_num.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_job_type(soup):
    """Lấy loại hình làm việc."""
    try:
        label_job_type = soup.find("label", string="LOẠI HÌNH LÀM VIỆC")
        return label_job_type.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_job_level(soup):
    """Lấy cấp bậc."""
    try:
        label_job_level = soup.find("label", string="CẤP BẬC")
        return label_job_level.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_skill(soup):
    """Lấy kỹ năng yêu cầu."""
    try:
        label_skill = soup.find("label", string="KỸ NĂNG")
        return label_skill.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_age(soup):
    """Lấy độ tuổi mong muốn."""
    try:
        label_age = soup.find("label", string="ĐỘ TUỔI MONG MUỐN")
        return label_age.find_next("p").get_text(strip=True)
    except AttributeError:
        return None

def get_job_description(soup):
    """Lấy mô tả công việc, làm sạch dữ liệu văn bản."""
    try:
        h2_anchor = soup.find('h2', string=lambda t: t and "Mô tả công việc" in t)
        content_div = h2_anchor.find_next(lambda tag: tag.name == 'div' and tag.find('p'))
        raw_text = content_div.get_text(separator=' ', strip=True)
        clean_text = re.sub(r'[•\*●]', '', raw_text)
        final_text = ' '.join(clean_text.split())
        if final_text.startswith(('-', '=', '+', '@')):
            final_text = "'" + final_text
        return final_text
    except AttributeError:
        return None

def get_job_requirements(soup):
    """Lấy yêu cầu công việc, làm sạch dữ liệu văn bản."""
    try:
        h2_anchor = soup.find('h2', string=lambda t: t and "Yêu cầu công việc" in t)
        content_div = h2_anchor.find_next(lambda tag: tag.name == 'div' and tag.find('p'))
        raw_text = content_div.get_text(separator=' ', strip=True)
        clean_text = re.sub(r'[•\*●]', '', raw_text)
        final_text = ' '.join(clean_text.split())
        if final_text.startswith(('-', '=', '+', '@')):
            final_text = "'" + final_text
        return final_text
    except AttributeError:
        return None

def get_benefits(soup):
    """Lấy danh sách các phúc lợi."""
    try:
        h2_anchor = soup.find('h2', string=lambda t: t and "phúc lợi" in t.lower())
        container = h2_anchor.find_parent('div') 
        benefit_blocks = container.find_all('div', attrs={'data-benefit-name': True})
        
        benefit_list = [block.find('p').get_text(strip=True) for block in benefit_blocks if block.find('p')]
        return "|".join(benefit_list) if benefit_list else None
    except Exception:
        return None

def get_is_urgent(soup):
    """Kiểm tra có nhãn Tuyển gấp / Urgent không từ thẻ label cụ thể."""
    try:
        labels = soup.find_all('span', attrs={'name': 'label'})
        for label in labels:
            text = label.get_text(strip=True).lower()
            if 'urgent' in text or 'tuyển gấp' in text:
                return "Yes"
        return "No"
    except Exception:
        return "No"




# ── 5. VÒNG LẶP CHÍNH ────────────────────────────────────────────────────────────

def main():
    options = uc.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)
    driver = uc.Chrome(options=options, version_main=148)
    driver.set_window_size(900, 1080)
    driver.set_window_position(900, 0)
    
    # Định nghĩa tên cột theo chuẩn snake_case
    csv_columns = [
        "index", "job_link", "keyword", "title", "company", "location", "salary", 
        "date_posted", "deadline_date", "category", "field", "job_type", 
        "job_level", "experience", "education", "hire_number", "age", 
        "skills", "is_urgent", "description", "requirements", "benefits"
    ]


    # ── TẠO FILE CSV & CHECK TRÙNG LẶP DATA ──────────────────────────────────
    
    global_index = 1
    scraped_links = set()
    
    # Kiểm tra xem file đã tồn tại chưa để lấy danh sách link đã cào (chống trùng)
    # và tìm index lớn nhất để tiếp tục tăng
    if os.path.exists(OUTPUT_CSV):
        try:
            with open(OUTPUT_CSV, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    link = row.get("job_link")
                    if link:
                        scraped_links.add(link)
                    
                    try:
                        idx = int(row.get("index", 0))
                        if idx >= global_index:
                            global_index = idx + 1
                    except ValueError:
                        pass
            logging.info(f"Đã tìm thấy file CSV cũ. Bắt đầu nối thêm từ index {global_index}. Đã có {len(scraped_links)} job được cào.")
            print(f"Đã quét được {len(scraped_links)} job từ file cũ. Bắt đầu nối thêm từ index {global_index}.")
        except Exception as e:
            logging.error(f"Lỗi khi đọc file CSV cũ: {e}")
    else:
        try:
            with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=csv_columns)
                writer.writeheader()
        except IOError:
            logging.error("Lỗi khi tạo file CSV")
            print("Lỗi khi tạo file CSV")
            driver.quit()
            return


    # ── CRAWL JOB CHI TIẾT ────────────────────────────────────────────────────
    
    for raw_keyword in KEYWORDS:
        # Chuẩn hóa keyword cho URL (ví dụ: 'Data Analyst' -> 'data-analyst')
        formatted_keyword = raw_keyword.lower().replace(' ', '-')
        
        logging.info(f"==> BẮT ĐẦU CÀO KEYWORD: {raw_keyword} (URL: {formatted_keyword})")
        print(f"\n{'='*60}")
        print(f"BẮT ĐẦU QUÉT KEYWORD: {raw_keyword.upper()}")
        print(f"{'='*60}\n")
        
        for page in range(1, MAX_PAGES + 1):
            logging.info(f"keyword '{raw_keyword}' - Cào page {page} ===")
            print(f"keyword '{raw_keyword}' - Cào page {page} ===")
            
            # Sử dụng .format() để điền giá trị vào biến toàn cục BASE_URL_TEMPLATE
            target_url = BASE_URL_TEMPLATE.format(keyword=formatted_keyword, page=page)
            driver.get(target_url)
            time.sleep(3)
            
            # Cuộn trang mượt mà như người thật để load hết job card
            human_scroll(driver)
                
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            links = get_link(soup)
            
            # KỊCH BẢN THỰC TẾ: Nếu trang không có job nào (VD từ khóa ngách chỉ có 2 trang), ta ngắt ngay vòng lặp trang.
            if not links:
                logging.info(f"Không tìm thấy job nào ở trang {page} cho từ khóa '{raw_keyword}'. Dừng cào từ khóa này.")
                print(f"\n[INFO] Hết job cho từ khóa '{raw_keyword}' tại trang {page}. Chuyển sang từ khóa tiếp theo.\n")
                break
                
            logging.info(f"Từ khóa '{raw_keyword}' | Trang {page} tìm thấy {len(links)} job links.")
            print(f"Từ khóa '{raw_keyword}' | Trang {page} tìm thấy {len(links)} job links.")
            
            # Cào chi tiết từng job trong trang vừa lấy được
            for i, job_link in enumerate(links):
                # Kiểm tra xem link này đã được cào trước đó chưa
                if job_link in scraped_links:
                    logging.info(f"Bỏ qua job đã cào: {job_link}")
                    print(f"Bỏ qua job đã cào: {job_link}")
                    continue
                    
                logging.info(f"Đang cào job {i+1}/{len(links)} (page {page}): {job_link}")
                print(f"Đang cào job {i+1}/{len(links)} (page {page}): {job_link}")
                
                try:
                    driver.get(job_link)
                    time.sleep(3)
                    
                    # Click các nút Xem đầy đủ và Xem thêm
                    try:
                        xem_full_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Xem đầy đủ mô tả công việc')]")
                        driver.execute_script("arguments[0].click();", xem_full_btn)
                        time.sleep(1.5)
                    except NoSuchElementException:
                        pass
                        
                    for btn_text in ['Thông tin việc làm', 'Các phúc lợi dành cho bạn']:
                        try:
                            xpath = f"//h2[normalize-space()='{btn_text}']/following::button[normalize-space()='Xem thêm'][1]"
                            xem_them_btn = driver.find_element(By.XPATH, xpath)
                            driver.execute_script("arguments[0].click();", xem_them_btn)
                            time.sleep(1)
                        except NoSuchElementException:
                            pass
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    job_data = {
                        "index":            global_index,
                        "job_link":         job_link,
                        "keyword":          raw_keyword,
                        "title":            get_title(soup),
                        "company":          get_company(soup),
                        "location":         get_local(soup),
                        "salary":           get_salary(soup),
                        "date_posted":      get_date_posted(soup),
                        "deadline_date":    get_deadline_date(soup),
                        "category":         get_category(soup),
                        "field":            get_field(soup),
                        "job_type":         get_job_type(soup),
                        "job_level":        get_job_level(soup),
                        "experience":       get_exprience(soup),
                        "education":        get_edu(soup),
                        "hire_number":      get_hire_num(soup),
                        "age":              get_age(soup),
                        "skills":           get_skill(soup),
                        "is_urgent":        get_is_urgent(soup),
                        "description":      get_job_description(soup),
                        "requirements":     get_job_requirements(soup),
                        "benefits":         get_benefits(soup)
                    }
                    
                    # Ghi ngay dòng này vào file CSV (chế độ append "a") là viết thêm vào file
                    try:
                        with open(OUTPUT_CSV, mode="a", newline="", encoding="utf-8-sig") as file:
                            writer = csv.DictWriter(file, fieldnames=csv_columns)
                            writer.writerow(job_data)
                        scraped_links.add(job_link)
                    except IOError:
                        logging.error("Lỗi khi ghi dòng mới vào file CSV")
                    
                    global_index += 1
                    
                except Exception as e:
                    logging.error(f"Lỗi khi cào job {job_link}: {e}")
                    continue

    driver.quit()
    print("Hoàn thành quá trình cào dữ liệu!")




# ── 6. ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
