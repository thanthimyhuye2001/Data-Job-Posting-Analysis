/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

PHẦN 1: TẠO DIM FACT
		1. TẠO BẢNG FACT JOB
		2. DIM COMPANY
		3. DIM LOCATION
		4. DIM INDUSTRY
		5. DIM EDU
		6. DIM WORK TYPE
		7. DIM POSITION
		8. DIM SOURCE
		9. DIM EXP YEARS RANGE  
		10. Dim tag nhóm ngành (ROLE DATA: DA, DS, DE, AI/ML) (BOOLEAN)
		11. Dim Benefit (BOOLEAN)
        FINAL: XÓA CỘT THỪA TRONG BẢNG FACT


PHẦN 2: TẠO CÁC BẢNG UNPIVOT cho các cột có giá trị BOOLEAN
		2.1. UNPIVOT ROLE DATA   (4 cột bảng dim_role_data)
        2.2. UNPIVOT BENEFITS    (4 cột bảng dim_benefits )
        2.3. UNPIVOT SKILLS TOOL (9 cột ở bảng FACT)
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */



/*=========================================================================
1. TẠO BẢNG FACT JOB
========================================================================= */
-- Sao chép y nguyên cấu trúc, kiểu dữ liệu, index của raw_data sang fact_job
CREATE TABLE fact_job LIKE raw_data;

-- Đổ toàn bộ dữ liệu từ raw_data sang fact_job
INSERT INTO fact_job 
SELECT * FROM raw_data;




/*=========================================================================
2. DIM COMPANY
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_company (
    id_company INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_company sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_company (company_name)
SELECT DISTINCT company_name 
FROM raw_data 
WHERE company_name IS NOT NULL AND company_name != ''
ORDER BY company_name ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_company INT;

-- Cập nhật id_company bằng cách JOIN với dim_company vừa tạo
UPDATE fact_job t
JOIN dim_company d ON t.company_name = d.company_name
SET t.id_company = d.id_company;


/*=========================================================================
3. DIM LOCATION
   chỉ cần tạo `id_location` trong `fact_job`
========================================================================= */

-- Bước 1: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_location INT;

-- Cập nhật id_location bằng cách JOIN với dim_location vừa tạo
UPDATE fact_job t
JOIN dim_location d ON t.location = d.location
SET t.id_location = d.id_location;


/*=========================================================================
4. DIM INDUSTRY
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_industry (
    id_industry INT AUTO_INCREMENT PRIMARY KEY,
    job_industry VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_industry sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_industry (job_industry)
SELECT DISTINCT job_industry 
FROM raw_data 
WHERE job_industry IS NOT NULL AND job_industry != ''
ORDER BY job_industry ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_industry INT;

-- Cập nhật id_industry bằng cách JOIN với dim_industry vừa tạo
UPDATE fact_job t
JOIN dim_industry d ON t.job_industry = d.job_industry
SET t.id_industry = d.id_industry;


/*=========================================================================
5. DIM EDU
   yêu cầu trình độ học vấn ở mức tối thiểu
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_edu (
    id_edu INT AUTO_INCREMENT PRIMARY KEY,
    edu VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_edu sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_edu (edu)
SELECT DISTINCT edu 
FROM raw_data 
WHERE edu IS NOT NULL AND edu != ''
ORDER BY edu ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_edu INT;

-- Cập nhật id_edu bằng cách JOIN với dim_edu vừa tạo
UPDATE fact_job t
JOIN dim_edu d ON t.edu = d.edu
SET t.id_edu = d.id_edu;


/*=========================================================================
6. DIM work_type WORK TYPE
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_work_type (
    id_work_type INT AUTO_INCREMENT PRIMARY KEY,
    work_type VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_work_type sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_work_type (work_type)
SELECT DISTINCT work_type 
FROM raw_data 
WHERE work_type IS NOT NULL AND work_type != ''
ORDER BY work_type ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_work_type INT;

-- Cập nhật id_work_type bằng cách JOIN với dim_work_type vừa tạo
UPDATE fact_job t
JOIN dim_work_type d ON t.work_type = d.work_type
SET t.id_work_type = d.id_work_type;




/*=========================================================================
7. DIM POSITION  job_position
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_position (
    id_position INT AUTO_INCREMENT PRIMARY KEY,
    job_position VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_position sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_position (job_position)
SELECT DISTINCT job_position 
FROM raw_data 
WHERE job_position IS NOT NULL AND job_position != ''
ORDER BY job_position ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_position INT;

-- Cập nhật id_position bằng cách JOIN với dim_position vừa tạo
UPDATE fact_job t
JOIN dim_position d ON t.job_position = d.job_position
SET t.id_position = d.id_position;



/*=========================================================================
8. DIM SOURCE  source
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_source (
    id_source INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_source sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_source (source)
SELECT DISTINCT source 
FROM raw_data 
WHERE source IS NOT NULL AND source != ''
ORDER BY source ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_source INT;

-- Cập nhật id_source bằng cách JOIN với dim_source vừa tạo
UPDATE fact_job t
JOIN dim_source d ON t.source = d.source
SET t.id_source = d.id_source;




/*=========================================================================
9. DIM EXP YEARS `exp_range`
   Phần ETL, cột này được tạo dựa trên số năm kinh nghiệm tối thiểu
========================================================================= */
-- Bước 1: Tạo cấu trúc bảng chuẩn với khóa chính tự tăng
CREATE TABLE dim_exp_range (
    id_exp_range INT AUTO_INCREMENT PRIMARY KEY,
    exp_range VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bước 2: Insert dữ liệu duy nhất vào (id_exp_range sẽ tự động nhảy 1, 2, 3...)
INSERT INTO dim_exp_range (exp_range)
SELECT DISTINCT exp_range 
FROM raw_data 
WHERE exp_range IS NOT NULL AND exp_range != ''
ORDER BY exp_range ASC;


-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE fact_job ADD COLUMN id_exp_range INT;

-- Cập nhật id_exp_range bằng cách JOIN với dim_exp_range vừa tạo
UPDATE fact_job t
JOIN dim_exp_range d ON t.exp_range = d.exp_range
SET t.id_exp_range = d.id_exp_range;




/*==========================================================================
10. DIM NHÓM ROLE trong lĩnh vực DATA `dim_role_data`
	các cột này có giá BOOLEAN
	`role_data_analyst_bi` 
	`role_data_engineer` 
	`role_data_science` 
	`role_ai_ml`
========================================================================== */

-- Bước 1: Tạo bảng DIM với khóa chính tự tăng
CREATE TABLE `dim_role_data` (
	`id_role_data` INT AUTO_INCREMENT PRIMARY KEY,
	`role_data_analyst_bi` 	TINYINT(1) NOT NULL,
	`role_data_engineer` 	TINYINT(1) NOT NULL,
	`role_data_science` 	TINYINT(1) NOT NULL,
	`role_ai_ml` 		    TINYINT(1) NOT NULL,

	UNIQUE KEY `uq_dim_role_data` (
        `role_data_analyst_bi`, 
        `role_data_engineer`, 
        `role_data_science`, 
        `role_ai_ml`
        )

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Bước 2: Insert các nhóm giá trị của ROLE DATA duy nhất vào bảng DIM
-- id_role_data sẽ tự động tăng từ 1, 2, 3...
INSERT INTO `dim_role_data` (`role_data_analyst_bi`, `role_data_engineer`, `role_data_science`, `role_ai_ml`)
SELECT DISTINCT `role_data_analyst_bi`, `role_data_engineer`, `role_data_science`, `role_ai_ml`
FROM `fact_job`
ORDER BY `role_data_analyst_bi`, `role_data_engineer`, `role_data_science`, `role_ai_ml`;



-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE `fact_job`
	ADD COLUMN `id_role_data` INT;

-- Cập nhật id_role_data bằng cách JOIN với bảng dim_role_data vừa tạo
UPDATE `fact_job` AS t
JOIN `dim_role_data` AS d
	ON  d.`role_data_analyst_bi`= t.`role_data_analyst_bi`
	AND d.`role_data_engineer` 	= t.`role_data_engineer`
	AND d.`role_data_science` 	= t.`role_data_science`
	AND d.`role_ai_ml` 		    = t.`role_ai_ml`

SET t.`id_role_data` = d.`id_role_data`;




/*==========================================================================
11. DIM NHÓM BENEFITS `dim_benefits`
	các cột này có giá BOOLEAN
	`financial_benefits`
	`health_benefits`
	`training_growth_benefits`
	`culture_benefits`
========================================================================== */

-- Bước 1: Tạo bảng DIM với khóa chính tự tăng
CREATE TABLE `dim_benefits` (
	`id_benefits` INT AUTO_INCREMENT PRIMARY KEY,
	`financial_benefits` 	TINYINT(1) NOT NULL,
	`health_benefits` 	TINYINT(1) NOT NULL,
	`training_growth_benefits` 	TINYINT(1) NOT NULL,
	`culture_benefits` 		    TINYINT(1) NOT NULL,

	UNIQUE KEY `uq_dim_benefits` (
        `financial_benefits`, 
        `health_benefits`, 
        `training_growth_benefits`, 
        `culture_benefits`
        )

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Bước 2: Insert các nhóm giá trị của BENEFITS duy nhất vào bảng DIM
-- id_benefits sẽ tự động tăng từ 1, 2, 3...
INSERT INTO `dim_benefits` (`financial_benefits`, `health_benefits`, `training_growth_benefits`, `culture_benefits`)
SELECT DISTINCT `financial_benefits`, `health_benefits`, `training_growth_benefits`, `culture_benefits`
FROM `fact_job`
ORDER BY `financial_benefits`, `health_benefits`, `training_growth_benefits`, `culture_benefits`;



-- Bước 3: Thêm cột mới vào bảng fact/data gốc
ALTER TABLE `fact_job`
	ADD COLUMN `id_benefits` INT;

-- Cập nhật id_benefits bằng cách JOIN với bảng dim_benefits vừa tạo
UPDATE `fact_job` AS t
JOIN `dim_benefits` AS d
	ON  d.`financial_benefits`= t.`financial_benefits`
	AND d.`health_benefits` 	= t.`health_benefits`
	AND d.`training_growth_benefits` 	= t.`training_growth_benefits`
	AND d.`culture_benefits` 		    = t.`culture_benefits`

SET t.`id_benefits` = d.`id_benefits`;



/*=========================================================================
FINAL: XÓA CỘT THỪA TRONG BẢNG FACT
==========================================================================*/
ALTER TABLE fact_job 
DROP COLUMN company_name,
DROP COLUMN location,
DROP COLUMN job_industry,
DROP COLUMN edu,
DROP COLUMN work_type,
DROP COLUMN job_position,
DROP COLUMN `source`,
DROP COLUMN exp_range,
DROP COLUMN `role_data_analyst_bi`, 
DROP COLUMN `role_data_engineer`,
DROP COLUMN `role_data_science`,  
DROP COLUMN `role_ai_ml`,
DROP COLUMN `financial_benefits`,
DROP COLUMN `health_benefits`,
DROP COLUMN `training_growth_benefits`,
DROP COLUMN `culture_benefits`
;
















/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

PHẦN 2: TẠO CÁC BẢNG UNPIVOT cho các cột có giá trị BOOLEAN
		2.1. UNPIVOT ROLE DATA   (4 cột bảng dim_role_data)
        2.2. UNPIVOT BENEFITS    (4 cột bảng dim_benefits )
        2.3. UNPIVOT SKILLS TOOL (9 cột ở bảng FACT)
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

/*==========================================================================
2.1. UNPIVOT ROLE DATA   (4 cột bảng dim_role_data + Description gọn)
     `unpivot_role_detail`
     Mục đích: Vẽ Bar chart so sánh lượng job từng role và Ma trận giao thoa
               Cung cấp mô tả tổng quan về vai trò phục vụ Tooltip/Popup
========================================================================== */

DROP TABLE IF EXISTS `unpivot_role_detail`;

CREATE TABLE `unpivot_role_detail` AS
	SELECT 
		`id_role_data`, 
		'Data Analyst / BI' AS `role_name`,
		'NHÓM PHÂN TÍCH DỮ LIỆU & BI (Thiên về phân tích, báo cáo, trực quan hóa dữ liệu).\nCác vị trí phổ biến: Data Analyst, Business Intelligence (BI) Analyst, Product Analyst, Marketing Analyst, Financial Analyst.' AS `description_role`
	FROM `dim_role_data`
	WHERE `role_data_analyst_bi` = 1

	UNION ALL

	SELECT 
		`id_role_data`, 
		'Data Engineer' AS `role_name`,
		'NHÓM XÂY DỰNG HỆ THỐNG & KỸ SƯ DỮ LIỆU (Thiên về xây dựng hạ tầng, thiết kế kho dữ liệu, tối ưu hóa các đường ống (pipelines))\nCác vị trí phổ biến: Data Engineer, Data Architect, Database Administrator (DBA), Analytics Engineer, Data Platform Specialist.' AS `description_role`
	FROM `dim_role_data`
	WHERE `role_data_engineer` = 1

	UNION ALL

	SELECT 
		`id_role_data`, 
		'Data Science' AS `role_name`,
		'NHÓM KHOA HỌC DỮ LIỆU (Thiên về toán, thống kê, mô hình kinh doanh)\nCác vị trí phổ biến: Data Scientist, Quantitative Analyst (Quant), Risk Modeler, Fraud Analyst, Statistical Research Analyst.' AS `description_role`
	FROM `dim_role_data`
	WHERE `role_data_science` = 1

	UNION ALL

	SELECT 
		`id_role_data`, 
		'AI / Machine Learning' AS `role_name`,
		'NHÓM TRÍ TUỆ NHÂN TẠO & HỌC MÁY (Thiên về nghiên cứu, huấn luyện các mô hình học máy, thị giác máy tính, xử lý ngôn ngữ tự nhiên (NLP))\nCác vị trí phổ biến: AI Engineer, Machine Learning Engineer, MLOps Engineer, NLP Developer, Computer Vision Specialist.' AS `description_role`
	FROM `dim_role_data`
	WHERE `role_ai_ml` = 1
	;

-- Thêm Index tối ưu tốc độ JOIN và Filter (Đã sửa lỗi 1089 bằng cách bỏ tiền tố độ dài cố định)
ALTER TABLE `unpivot_role_detail` ADD INDEX `idx_id_role_data` (`id_role_data`);




/*==========================================================================
2.2. UNPIVOT BENEFITS   (4 cột thuộc bảng dim_benefits + Description)
     `unpivot_benefits_detail`
     Mục đích: Vẽ bar chart so sánh mức độ phổ biến của các nhóm phúc lợi 
========================================================================== */


DROP TABLE IF EXISTS `unpivot_benefits_detail`;

CREATE TABLE `unpivot_benefits_detail` AS
	SELECT 
		`id_benefits`, 
		'Phúc lợi Tài chính' AS `benefit_name`,
		'Các chế độ đãi ngộ trực tiếp bằng tiền mặt hoặc lợi ích kinh tế tương đương. \nBao gồm: Lương, thưởng hiệu suất, lương tháng 13, phụ cấp, cổ phiếu (ESOP), ngày nghỉ phép có lương.' AS `description_benefits`
	FROM `dim_benefits`
	WHERE `financial_benefits` = 1

	UNION ALL

	SELECT 
		`id_benefits`, 
		'Sức khỏe & Bảo hiểm' AS `benefit_name`,
		'Các chương trình chăm sóc thể chất, tinh thần và bảo vệ an toàn cho người lao động. \nBao gồm: Bảo hiểm bắt buộc (BHXH, BHYT, BHTN), bảo hiểm tai nạn/y tế tư nhân, trợ cấp chăm sóc sức khỏe, Gym/Fitness.' AS `description_benefits`
	FROM `dim_benefits`
	WHERE `health_benefits` = 1

	UNION ALL

	SELECT 
		`id_benefits`, 
		'Đào tạo & Phát triển' AS `benefit_name`,
		'Các chương trình phát triển năng lực và kỹ năng, và lộ trình thăng tiến nghề nghiệp cho nhân viên. \nBao gồm: Khóa đào tạo, lộ trình thăng tiến rõ ràng, hỗ trợ chi phí thi chứng chỉ, học bổng, chương trình cố vấn (Mentorship).' AS `description_benefits`
	FROM `dim_benefits`
	WHERE `training_growth_benefits` = 1

	UNION ALL

	SELECT 
		`id_benefits`, 
		'Văn hóa & Môi trường' AS `benefit_name`,
		'Các yếu tố về không gian, công cụ làm việc và hoạt động gắn kết tinh thần tập thể. \nBao gồm: Du lịch, Team building, liên hoan, chế độ làm việc linh hoạt (Remote/WFH), cấp phát máy tính/Macbook.' AS `description_benefits`
	FROM `dim_benefits`
	WHERE `culture_benefits` = 1
	;

-- Thêm Index để tối ưu tốc độ JOIN và filter trong Power BI / MySQL
ALTER TABLE `unpivot_benefits_detail` ADD INDEX `idx_id_benefits` (`id_benefits`);







/*==========================================================================
2.3. UNPIVOT SKILLS DETAIL (9 cột kỹ năng từ bảng fact_job)
     `unpivot_skills_detail`
     Mục đích: Vẽ chart tính lương trung bình, range lương theo từng skill
               Vẽ ma trận/bar chart phân bố skill theo ngành nghề
========================================================================== */

DROP TABLE IF EXISTS `unpivot_skills_detail`;

CREATE TABLE `unpivot_skills_detail` AS
	SELECT 
		`id_job`, 
		'SQL' AS `skill_name`, 
		'Ngôn ngữ truy vấn và quản lý cơ sở dữ liệu.' AS `skill_display_vi`,
		'SQL, Oracle, MySQL, SQL Server, PostgreSQL, BigQuery, Database, Data Warehouse, Data Mart' AS `description_skills`
	FROM `fact_job`
	WHERE `req_sql` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'Python' AS `skill_name`, 
		'Ngôn ngữ lập trình Python và thư viện' AS `skill_display_vi`,
		'Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Scikit-Learn, PyTorch, TensorFlow, PySpark, ...' AS `description_skills`
	FROM `fact_job`
	WHERE `req_python` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'Excel' AS `skill_name`, 
		'Excel' AS `skill_display_vi`,
		'Excel, VBA, Google Sheets, Spreadsheet, Pivot Table, Power Query, Power Pivot, Macro' AS `description_skills`
	FROM `fact_job`
	WHERE `req_excel` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'Cloud / Modern Stack' AS `skill_name`, 
		'Hệ sinh thái công nghệ hiện đại vận hành trên nền tảng đám mây (Cloud)' AS `skill_display_vi`,
		'AWS, Azure, GCP, Snowflake, BigQuery, Databricks, Redshift, Athena, Microsoft Fabric, dbt (Data Build Tool), Airflow, SAP BW, ...' AS `description_skills`
	FROM `fact_job`
	WHERE `req_cloud_mordern_stack` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'Big Data' AS `skill_name`, 
		'Công nghệ xử lý luồng dữ liệu lớn (Big Data) theo thời gian thực (streaming).' AS `skill_display_vi`,
		'Spark, PySpark, Hadoop, Kafka, Lakehouse, Apache Superset, Databricks.' AS `description_skills`
	FROM `fact_job`
	WHERE `req_big_data` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'Java/C++/R...' AS `skill_name`, 
		'Các ngôn ngữ lập trình khác, bổ trợ hoặc chuyên dụng cho phần mềm và thống kê chuyên sâu.' AS `skill_display_vi`,
		'Java, JavaScript, TypeScript, Scala, Kotlin, Go, Ruby, PHP, C++, C#, SAS, R, ...' AS `description_skills`
	FROM `fact_job`
	WHERE `req_other_programming` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'AI / Machine Learning' AS `skill_name`, 
		'AI / Machine Learning: Trí tuệ nhân tạo & Học máy' AS `skill_display_vi`,
		'Machine Learning, Deep Learning, GenAI, LLM, Agentic AI, NLP, Computer Vision, PyTorch, TensorFlow, MLOps' AS `description_skills`
	FROM `fact_job`
	WHERE `req_ai_ml` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'DevOps / MLOps' AS `skill_name`, 
		'DevOps / MLOps: Vận hành hệ thống tự động hóa' AS `skill_display_vi`,
		'Git, Docker, CI/CD, Kubernetes, Jenkins, MLOps, DataOps, Power Automate, Automation Anywhere' AS `description_skills`
	FROM `fact_job`
	WHERE `req_devops` = 1

	UNION ALL

	SELECT 
		`id_job`, 
		'BI / Visualization' AS `skill_name`, 
		'Công cụ BI & Trực quan hóa dữ liệu' AS `skill_display_vi`,
		'Power BI, Tableau, Looker Studio, Metabase, QlikView, Google Analytics (GA4), Hotjar, Microsoft Clarity, Shopify Analytics, CDP' AS `description_skills`
	FROM `fact_job`
	WHERE `req_bi_viz` = 1
	;

-- Đánh Index tối ưu hiệu năng lọc và vẽ chart trên Power BI
ALTER TABLE `unpivot_skills_detail` ADD INDEX `idx_id_job` (`id_job`);
ALTER TABLE `unpivot_skills_detail` ADD INDEX `idx_skill_name` (`skill_name`);


