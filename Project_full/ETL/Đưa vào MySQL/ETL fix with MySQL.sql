UPDATE dim_position
SET position = 'Intern/ Fresher'
WHERE position = 'Intern/ Mới tốt nghiệp';




/* 

ETL 1

*/

UPDATE fact_job
SET mean_salary_fix = 25600000.0
WHERE job_url = 'https://www.topcv.vn/viec-lam/giao-vien-day-mon-tri-tue-nhan-tao-part-time/2157892.html';




-- Thêm cột phân loại theo thành phố lớn
ALTER TABLE dim_location ADD COLUMN location_big VARCHAR(50);

UPDATE dim_location
SET location_big = CASE 
    WHEN location IN ('Hà Nội') THEN 'Hà Nội'
    WHEN location IN ('Hồ Chí Minh') THEN 'Hồ Chí Minh'
    WHEN location IN ('Đà Nẵng') THEN 'Đà Nẵng'
    ELSE 'Khác'
END;



/* 

ETL 2 fix Company

*/

SELECT * 
FROM `dim_company`
WHERE company_name LIKE '%bank%' 
   OR company_name LIKE '%ngân hàng%'
   OR company_name LIKE '%ngan hang%';


ALTER TABLE dim_company 
ADD COLUMN company_clean VARCHAR(255);


UPDATE dim_company c
LEFT JOIN company_mapping m ON c.company_name = m.company_name
SET c.company_clean = UPPER(TRIM(
    REGEXP_REPLACE(
        -- Bước 1: Loại bỏ ký tự thừa trước
        REGEXP_REPLACE(IF(m.company_name IS NOT NULL, m.company_group, c.company_name), '[\\(\\),\\.\\-\\–\\|\\"]+', ' '),

        -- Bước 2: Xóa đuôi Pro Company + Xóa tất cả các từ thừa
        'Pro Company$|\\b(TMCP|CTCP|TNHH|MTV|JSC|INC|Co\\s+Ltd\\s+Limited|Co\\s+Ltd|Pvt\\s+Ltd|Ltd|Private Limited Company|Limited Company|Limited|Thương mại cổ phần|Công ty Cổ phần|Trách nhiệm hữu hạn|Một thành viên|Chi nhánh|CP & DV|CP|Công ty|Việt nam|vietnam|viet nam|corp|Corporation)\\b|\\b(?!và\\s+)(?!&\\s+)công nghệ(?!\\s+và)(?!\\s+&)\\b', '', 1, 0, 'i'
    )
));


-- Bước phụ: Thu gọn các khoảng trắng kép ở giữa chuỗi thành 1 khoảng trắng đơn (nếu có)
UPDATE dim_company 
SET company_clean = REGEXP_REPLACE(company_clean, '[[:space:]]+', ' ')
WHERE company_clean IS NOT NULL;

-- ALTER TABLE dim_company DROP COLUMN company_clean;
