# =============================================================================
# crawl_itviec.py
# Crawl job listings từ ITviec lĩnh vực data
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

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
from dotenv import load_dotenv

# ── 2. CẤU HÌNH & HỆ THỐNG ───────────────────────────────────────────────────────

# Đọc file .env từ thư mục "Nháp test"

# 1. Lấy đường dẫn tuyệt đối của thư mục chứa file crawl_itviec.py hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Tạo đường dẫn tới file .env
# Cách hoạt động: current_dir -> lùi 1 cấp (Crawl_job) -> lùi 1 cấp (Project_full) -> lùi 1 cấp (Đồ án 2 _ 2025) -> vào "1.Nháp test" -> file ".env"
env_path = os.path.join(current_dir, "..", "..", "..", "1.Nháp test", ".env")
# 3. Chuẩn hóa đường dẫn (loại bỏ các dấu ".." thừa) để đường dẫn gọn gàng hơn
env_path = os.path.normpath(env_path)

load_dotenv(dotenv_path=env_path)

MY_EMAIL = os.getenv("ITVIEC_EMAIL")
MY_PASSWORD = os.getenv("ITVIEC_PASS")

KEYWORDS = [
    "Data Analyst", "Business Intelligence", "Data Visualization", "Product Analyst", "Marketing Analyst",
    "Data Engineer", "Data Architect", "Data Warehouse", "ETL", "Analytics Engineer", "Cloud Data",
    "Data Scientist", "Machine Learning", "AI Engineer", "NLP Engineer", "Computer Vision Engineer", "Algorithm Engineer", "MLOps Engineer",
    "Database Administrator", "Data Modeler", "Data Governance Specialist", "Data Quality Analyst", "Database Developer",
    "Big Data Engineer", "Quantitative Analyst"
]

BASE_URL_TEMPLATE = "https://itviec.com/it-jobs/{keyword}?page={page}"

MAX_PAGES = 60  # Giới hạn tối đa số trang để cào cho mỗi keyword

OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data_raw", "data_itviec.csv")

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# ── 3. LOGGING ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Logging", "logging_itviec.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)


# ── 4. CÁC FUNCTION LẤY TỪNG TRƯỜNG ─────────────────────────────────────────────

def get_title(soup):
    """Lấy tiêu đề công việc."""
    try:
        header_info = soup.find('div', class_='job-header-info')
        if header_info:
            title_tag = header_info.find('h1')
            if title_tag:
                return title_tag.get_text(strip=True)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy title: {e}")
        return None

def get_company(soup):
    """Lấy tên công ty."""
    try:
        header_info = soup.find('div', class_='job-header-info')
        if header_info:
            employer_name = header_info.find('div', class_='employer-name')
            if employer_name:
                return employer_name.text.strip()
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy company: {e}")
        return None

def get_salary(soup):
    """Lấy mức lương."""
    try:
        salary_div = soup.find('div', class_='salary')
        if salary_div:
            salary_span = salary_div.find('span')
            if salary_span:
                return salary_span.get_text(strip=True)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy salary: {e}")
        return None

def get_is_fresher(soup):
    """Kiểm tra job có nhận Fresher không."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            fresher_tag = info_box.find('a', string=re.compile(r'Fresher Accepted', re.IGNORECASE))
            if fresher_tag:
                return "Yes"
        return "No"
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra fresher: {e}")
        return "No"

def get_location(soup):
    """Lấy địa điểm làm việc."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            map_link = info_box.find('a', href=lambda href: href and "google.com/maps" in href)
            if map_link:
                parent_div = map_link.find_parent('div')
                address_span = parent_div.find('span', class_='normal-text')
                if address_span:
                    return address_span.get_text(strip=True)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy address: {e}")
        return None

def get_job_type(soup):
    """Lấy loại hình công việc (At office/Hybrid/Remote)."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            pattern = re.compile(r'(At office|Hybrid|Remote)', re.IGNORECASE)
            matched_text = info_box.find(string=pattern)
            if matched_text:
                return matched_text.strip()
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy job_type: {e}")
        return None

def get_date_posted(soup):
    """Lấy và tính toán ngày đăng tuyển."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            posted_text_node = info_box.find(string=re.compile(r'Posted', re.IGNORECASE))
            if posted_text_node:
                raw_text = posted_text_node.strip()
                match = re.search(r'\d+', raw_text)
                if match:
                    number = int(match.group())
                    now = datetime.datetime.now()
                    if 'hour' in raw_text:
                        date_posted = now
                    elif 'day' in raw_text:
                        date_posted = now - datetime.timedelta(days=number)
                    else:
                        return None
                    return date_posted.strftime('%Y-%m-%d')
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy date_posted: {e}")
        return None

def get_skills(soup):
    """Lấy danh sách các kỹ năng yêu cầu."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            skills_label = info_box.find('div', string=re.compile(r'Skills:', re.IGNORECASE))
            if skills_label:
                parent_div = skills_label.find_parent('div')
                if parent_div:
                    skill_tags = parent_div.find_all('a')
                    skills_list = [tag.get_text(strip=True) for tag in skill_tags]
                    if skills_list:
                        return ", ".join(skills_list)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy skills: {e}")
        return None

def get_job_expertise(soup):
    """Lấy thông tin chuyên môn công việc."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            expertise_label = info_box.find('div', string=re.compile(r'Job Expertise:', re.IGNORECASE))
            if expertise_label:
                parent_div = expertise_label.find_parent('div')
                if parent_div:
                    expertise_tags = parent_div.find_all('a')
                    expertise_list = [tag.get_text(strip=True) for tag in expertise_tags]
                    if expertise_list:
                        return ", ".join(expertise_list)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy job_expertise: {e}")
        return None

def get_job_domain(soup):
    """Lấy lĩnh vực, tên domain của công việc (VD: Financial Services)."""
    try:
        info_box = soup.find('div', class_='job-show-info')
        if info_box:
            domain_label = info_box.find('div', string=re.compile(r'Job Domain:', re.IGNORECASE))
            if domain_label:
                parent_div = domain_label.find_parent('div')
                if parent_div:
                    domain_tags = parent_div.find_all('div', class_='itag')
                    domain_list = []
                    for tag in domain_tags:
                        text = tag.find(string=True, recursive=False)
                        if text:
                            clean_text = text.strip()
                            if clean_text:
                                domain_list.append(clean_text)
                    if domain_list:
                        return ", ".join(domain_list)
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy job_domain: {e}")
        return None

def get_employer_info(soup, label_name):
    """Hàm đa năng để lấy các thông tin công ty dựa trên nhãn chỉ định (Company type, Country...)."""
    try:
        employer_box = soup.find('section', class_='job-show-employer-info')
        if employer_box:
            label_div = employer_box.find('div', string=re.compile(label_name, re.IGNORECASE))
            if label_div:
                row_div = label_div.find_parent('div', class_='row')
                if row_div:
                    value_div = row_div.find('div', class_=lambda c: c and 'text-end' in c)
                    if value_div:
                        raw_text = value_div.get_text(separator=' ', strip=True)
                        clean_text = ' '.join(raw_text.split())
                        return clean_text
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy {label_name}: {e}")
        return None

def extract_paragraph_content(soup, heading_keyword):
    """Hàm đa năng xử lý trích xuất văn bản từ một đề mục H2 bất kỳ."""
    try:
        h2_tag = soup.find('h2', string=re.compile(heading_keyword, re.IGNORECASE))
        if h2_tag:
            content_parts = []
            for sibling in h2_tag.find_next_siblings():
                text = sibling.get_text(separator=' ', strip=True)
                if text:
                    content_parts.append(text)
            raw_text = ' '.join(content_parts)
            clean_text = re.sub(r'[•\-\*·]', '', raw_text)
            clean_text = clean_text.replace('\xa0', ' ')
            final_text = ' '.join(clean_text.split())
            if final_text.startswith(('-', '=', '+', '@')):
                final_text = "'" + final_text
            return final_text
        return None
    except Exception as e:
        logging.error(f"Lỗi khi lấy {heading_keyword}: {e}")
        return None

def get_job_description(soup):
    """Lấy thẻ Mô tả công việc."""
    return extract_paragraph_content(soup, "Job description")

def get_job_requirements(soup):
    """Lấy thẻ Yêu cầu công việc."""
    return extract_paragraph_content(soup, "Your skills and experience")

def get_benefits(soup):
    """Lấy thẻ Thông tin phúc lợi dành cho bạn."""
    return extract_paragraph_content(soup, "Why you'll love working here")


# ── 5. VÒNG LẶP CHÍNH ────────────────────────────────────────────────────────────

def login_itviec(driver):
    if not MY_EMAIL or not MY_PASSWORD:
        logging.error("Chưa cấu hình ITVIEC_EMAIL hoặc ITVIEC_PASS trong file .env!")
        print("Lỗi: Không tìm thấy tài khoản để đăng nhập ở file .env.")
        return False

    try:
        print("Đang tiến hành đăng nhập ITviec...")
        driver.get("https://itviec.com/sign_in")
        wait = WebDriverWait(driver, 15)

        # Điền Email
        email_input = wait.until(EC.presence_of_element_located((By.ID, "user_email")))
        email_input.send_keys(MY_EMAIL)
        
        # Điền Password
        pass_input = driver.find_element(By.ID, "user_password")
        pass_input.send_keys(MY_PASSWORD)
        
        # Bấm nút Sign In with Email
        submit_btn = driver.find_element(
            By.XPATH, 
            "//button[@type='submit' and .//span[text()='Sign In with Email']]"
        )
        submit_btn.click()
        
        print("Đăng nhập thành công! Chờ 5s để web ổn định...")
        time.sleep(5)
        
        # Tắt popup tạo CV nếu có
        try:
            close_popup_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Remind me later')]")
            driver.execute_script("arguments[0].click();", close_popup_btn)
            logging.info("Đã đóng popup yêu cầu tạo CV!")
            time.sleep(1)
        except NoSuchElementException:
            pass
            
        return True
    except TimeoutException:
        logging.error("Lỗi Timeout khi cố gắng đăng nhập ITviec!")
        print("Lỗi: Phản hồi quá chậm. Không thể đăng nhập.")
        return False
    except Exception as e:
        logging.error(f"Lỗi khi đăng nhập ITviec: {e}")
        print(f"Lỗi hệ thống khi đăng nhập: {e}")
        return False


def main():
    options = uc.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Khởi tạo Undetected Chromedriver để vượt cơ chế chống bot của ITviec
    # Thêm version_main=148 vì Chrome của bạn đang ở phiên bản 148
    driver = uc.Chrome(options=options, version_main=148) 
    driver.set_window_size(900, 1080)
    driver.set_window_position(900, 0)
    
    # Thực hiện đăng nhập trước
    if not login_itviec(driver):
        print("Hủy cào dữ liệu vì đăng nhập thất bại.")
        driver.quit()
        return

    csv_columns = [
        "index", "job_url", "search_keyword", "job_title", "company_name", 
        "location", "salary", "is_fresher", "job_type", "date_post", 
        "job_skills", "job_expertise", "job_domain", "company_industry", 
        "company_type", "company_country", "job_description", "requirements", 
        "benefits", "source_site"
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


    # ── CRAWL JOB CHI TIẾT ────────────────────────────────────────────────────
    
    for raw_keyword in KEYWORDS:
        # Chuẩn hóa keyword cho URL của ITviec ('Data Analyst' -> 'data-analyst')
        formatted_keyword = raw_keyword.lower().replace(' ', '-')
        
        logging.info(f"==> BẮT ĐẦU CÀO KEYWORD: '{raw_keyword}' (URL: {formatted_keyword})")
        print(f"\n{'='*60}")
        print(f"BẮT ĐẦU QUÉT KEYWORD: {raw_keyword.upper()}")
        print(f"{'='*60}\n")
        
        for page in range(1, MAX_PAGES + 1):
            logging.info(f"keyword '{raw_keyword}' - Cào page {page} ===")
            print(f"keyword '{raw_keyword}' - Cào page {page} ===")
            
            target_url = BASE_URL_TEMPLATE.format(keyword=formatted_keyword, page=page)
            driver.get(target_url)
            time.sleep(3)
            
            # Cuộn trang xuống cuối để load jobList
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_data = soup.find("div", attrs={"data-search--pagination-target": "jobList"})
            
            if not job_data:
                logging.info(f"Không tìm thấy job list ở trang {page} cho '{raw_keyword}'. Dừng cào từ khóa này.")
                print(f"[THÔNG BÁO] Trang {page} không chứa job nào, hoặc đã hết. Chuyển sang từ khóa khác.")
                break
                
            job_tab = job_data.find_all('h3', attrs={'data-search--job-selection-target': 'jobTitle'})
            if len(job_tab) == 0:
                logging.info(f"Trang {page} rỗng cho '{raw_keyword}'. Dừng.")
                print(f"[THÔNG BÁO] Trang {page} rỗng. Chuyển.")
                break
                
            links = []
            for tag in job_tab:
                link = tag.get('data-url')
                if link:
                    clean_href = link.split('?')[0]
                    links.append(clean_href)

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
                    time.sleep(3)
                    
                    # Cuộn trang vài lần để load toàn bộ element ẩn
                    last_inner = driver.execute_script("return document.body.scrollHeight")
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1.5)
                        new_inner = driver.execute_script("return document.body.scrollHeight")
                        if new_inner == last_inner:
                            break
                        last_inner = new_inner
                    
                    new_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # Cào các trường dữ liệu
                    company_type = get_employer_info(new_soup, "Company type")
                    company_industry = get_employer_info(new_soup, "Company industry")
                    company_country = get_employer_info(new_soup, "Country")
                    
                    job_data_dict = {
                        "index":              global_index,
                        "job_url":            job_link,
                        "search_keyword":     raw_keyword,
                        "job_title":          get_title(new_soup),
                        "company_name":       get_company(new_soup),
                        "location":           get_location(new_soup),
                        "salary":             get_salary(new_soup),
                        "is_fresher":         get_is_fresher(new_soup),
                        "job_type":           get_job_type(new_soup),
                        "date_post":          get_date_posted(new_soup),
                        "job_skills":         get_skills(new_soup),
                        "job_expertise":      get_job_expertise(new_soup),
                        "job_domain":         get_job_domain(new_soup),
                        "company_industry":   company_industry,
                        "company_type":       company_type,
                        "company_country":    company_country,
                        "job_description":    get_job_description(new_soup),
                        "requirements":       get_job_requirements(new_soup),
                        "benefits":           get_benefits(new_soup),
                        "source_site":        "itviec.com"
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
    print("\n[HOÀN THÀNH] Đã cào xong dữ liệu ITviec!")


# ── 6. ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
