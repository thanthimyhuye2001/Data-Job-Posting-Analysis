# Báo Cáo Thị Trường Tuyển Dụng Ngành Data Tại Việt Nam

## Góc nhìn từ dữ liệu tuyển dụng thực tế

*Dự án cá nhân: thu thập, xử lý và trực quan hóa dữ liệu tuyển dụng ngành Data từ 4 nền tảng tuyển dụng việc làm IT tại Việt Nam*

---

## Lời mở đầu

Báo cáo "Vietnam IT & Tech Talent Landscape 2024-2025" của TopDev cho một bức tranh tổng quan về toàn ngành IT Việt Nam, nhưng chưa đi sâu vào riêng mảng **Data** — nhóm ngành đang có tốc độ tăng trưởng nhu cầu nhanh nhất trong các vai trò kỹ thuật, đặc biệt là AI/Machine Learning.

Với mục tiêu hiểu rõ hơn thị trường việc làm Data trước khi ứng tuyển, mình đã tự thu thập dữ liệu tuyển dụng từ 4 nền tảng tuyển dụng việc làm IT phổ biến tại Việt Nam *(ghi rõ tên 4 nguồn ở đây)*, xây dựng mô hình dữ liệu và dashboard Power BI để phân tích. Báo cáo này tổng hợp lại những insight chính rút ra được.

---

## 1. Phương pháp thực hiện

|  |  |
| --- | --- |
| **Nguồn dữ liệu** | 4 nền tảng tuyển dụng việc làm IT tại Việt Nam |
| **Phạm vi thời gian thu thập** | \~12/02/2026 – 30/09/2026 |
| **Quy mô dữ liệu** | 2.803 tin tuyển dụng hợp lệ từ 1.093 công ty (trong khung phân tích chính) |
| **Pipeline** | Web scraping → Làm sạch/ETL → Data modeling (Star Schema: 1 Fact table `fact_job` + các Dimension: vị trí, kỹ năng, lương, địa điểm, ngành, phúc lợi...) → Trực quan hóa Power BI |

**Giới hạn dữ liệu cần lưu ý khi đọc báo cáo:**

- Phân tích lương chỉ dựa trên tập con các tin **có công bố mức lương công khai**, không đại diện 100% thị trường.
- 4 nhóm vai trò (Data Analyst/BI, Data Engineer, Data Science, AI/ML) được gắn nhãn dựa trên từ khóa trong JD nên có thể chồng lấp giữa các nhóm.
- Dữ liệu phản ánh "nguồn cung tin tuyển dụng công khai", chưa bao gồm các vị trí tuyển qua headhunter/referral nội bộ.

---

## 2. Tổng quan thị trường

| Việc làm | Công ty | Full-time | Nguồn |
| --- | --- | --- | --- |
| **2.803** | **1.093** | **93%** | **4** |

Lượng tin đăng mới mỗi ngày dao động trong khoảng 693 – 1.287 tin, đạt đỉnh vào đầu tháng 5/2026 rồi hạ nhiệt dần về cuối giai đoạn quan sát (\~1.057 vào giữa tháng 6).

**Nhu cầu theo 4 nhóm vai trò chính:**

| Vai trò | Số tin | Tỷ trọng tương đối |
| --- | --- | --- |
| AI / Machine Learning | 598 | Cao nhất |
| Data Analyst / BI | 569 |  |
| Data Engineer | 453 |  |
| Data Science | 99 | Thấp nhất rõ rệt |

> **Insight:** AI/Machine Learning hiện là nhóm có nhu cầu tuyển dụng cao nhất, vượt qua cả Data Analyst/BI — vai trò vốn thường được xem là cửa vào phổ biến nhất ngành Data. Điều này khớp với xu hướng dòng vốn đầu tư AI tại Việt Nam tăng mạnh được ghi nhận trong báo cáo TopDev. Ngược lại, "Data Science" thuần túy có số tin thấp nhất — nhiều khả năng do phần lớn vị trí dạng này đã được gộp vào nhóm AI/ML trong thực tế tuyển dụng.

**Top 5 ngành khát nhân lực Data nhất:**

1. Tài chính – Ngân hàng: 799 tin
2. Công nghệ – Phần mềm: 674 tin
3. Thương mại điện tử – Bán lẻ: 377 tin
4. Dịch vụ – Truyền thông: 316 tin
5. Sản xuất – Logistics: 312 tin

> **Insight:** Tài chính – Ngân hàng là "khách hàng" lớn nhất của nhân sự Data, đúng với nhận định về Banking & Fintech dẫn đầu chuyển đổi số trong báo cáo ngành IT của TopDev.

**Nhu cầu theo cấp bậc:**

Nhân viên (1.639 tin, \~58%) áp đảo hoàn toàn so với các cấp còn lại — Trưởng nhóm (432), Intern/Fresher chỉ **150 tin (\~5%)**, Trưởng phòng (146), Lãnh đạo/Quản lý rất ít.

> **Insight:** Thị trường ưu tiên tuyển người đã có kinh nghiệm hơn là fresher. Sinh viên mới ra trường nên chủ động tích lũy project/thực tập trước khi apply, vì cơ hội entry-level khá hạn chế so với tổng nhu cầu.

---

## 3. Phân bố địa lý

Hồ Chí Minh (1.668 tin) và Hà Nội (1.552 tin) chiếm hơn **94% tổng số tin tuyển dụng Data toàn quốc**. Các địa phương khác (Đà Nẵng, Đồng Nai, Bình Dương...) chỉ chiếm phần rất nhỏ, dưới 40 tin mỗi nơi.

> **Insight:** Nếu không ở HCM hoặc Hà Nội, cơ hội làm remote hoặc sẵn sàng chuyển đến 1 trong 2 thành phố này gần như là điều kiện bắt buộc để có nhiều lựa chọn việc làm Data.

---

## 4. Kỹ năng & yêu cầu

**Top kỹ năng được yêu cầu nhiều nhất** (tỷ lệ % tin có đề cập):

| Kỹ năng | Tỷ lệ |
| --- | --- |
| SQL | 51% |
| Python | 39% |
| BI / Visualization | 31% |
| AI / Machine Learning | 28% |
| Excel | 26% |
| Cloud / Modern Stack | 25% |
| DevOps / MLOps | 24% |
| Java/C++/R... | 18% |
| Big Data | 18% |

> **Insight:** SQL vẫn là kỹ năng "must-have" số 1, xuất hiện trong hơn một nửa số tin — bất kể vai trò nào. Đáng chú ý, AI/ML (28%) đã vượt Excel ở vị trí top 4, cho thấy với các vai trò Data chuyên sâu, Excel không còn là công cụ trung tâm.

**Yêu cầu học vấn:** Đại học (49%) và "Không yêu cầu" (15%) là hai nhóm lớn nhất — tức khoảng **36%** JD không đòi hỏi cụ thể bằng đại học, cho thấy ngành Data khá cởi mở về bằng cấp nếu ứng viên chứng minh được kỹ năng thực tế.

**Yêu cầu tiếng Anh tăng dần theo thời gian:** từ 46% (tháng 3) lên 51% (tháng 6) — tăng 5 điểm phần trăm chỉ trong 4 tháng quan sát. Tiếng Anh đang dần trở thành yêu cầu bắt buộc hơn là một điểm cộng.

**Ranh giới vai trò đang mờ dần:** trong ma trận chồng lấp, cặp **Data Engineer – AI/ML** có số lượng job yêu cầu cả 2 kỹ năng cao nhất (42 tin), cho thấy nhiều công ty tìm Data Engineer có khả năng hỗ trợ pipeline cho các hệ thống AI/ML.

---

## 5. Mức lương phổ biến

*(Lưu ý: số liệu dựa trên tập con tin có công bố lương, chỉ mang tính tham khảo)*

**Theo nhóm ngành** (khoảng phân vị 25%–75%):

| Nhóm ngành | Khoảng lương phổ biến |
| --- | --- |
| Data Analyst / BI | 15 – 30 triệu |
| AI / Machine Learning | 20 – 40 triệu |
| Data Engineer | 23 – 39 triệu |
| Data Science | 24 – 37 triệu |

> **Insight:** Data Analyst/BI có mức sàn thấp nhất — phù hợp làm điểm khởi đầu sự nghiệp. Ba nhóm còn lại có mặt bằng lương tương đương và cao hơn đáng kể, phản ánh độ khan hiếm của kỹ năng kỹ thuật chuyên sâu (pipeline, mô hình hóa, MLOps...).

**Theo địa điểm:** Hà Nội có trần lương nhỉnh hơn HCM (37 triệu so với 35 triệu), dù sàn lương bằng nhau (18 triệu). Đà Nẵng thấp hơn cả hai (17–30 triệu).

**Theo cấp bậc:**

| Cấp bậc | Khoảng lương |
| --- | --- |
| Intern / Fresher | \~12 triệu |
| Nhân viên | 17 – 30 triệu |
| Trưởng nhóm | 25 – 47 triệu |
| Trưởng phòng | 28 – 48 triệu |
| Lãnh đạo / Quản lý | 31 – 77 triệu |

Lương tăng rõ rệt theo số năm kinh nghiệm, có thể vượt mốc 70–100 triệu ở nhóm 5–10 năm kinh nghiệm, dù độ phân tán khá lớn ở mốc 3–6 năm (do khác biệt về vai trò và quy mô công ty).

---

## 6. Tổng hợp insight dành cho người tìm việc Data

- **SQL + Python** là 2 kỹ năng bắt buộc phải có trước khi ứng tuyển bất kỳ vai trò Data nào.
- **Data Analyst/BI** vẫn là cửa vào dễ nhất: lương sàn thấp nhất, nhu cầu cao thứ 2 toàn thị trường.
- **AI/ML** đang có nhu cầu tuyển cao nhất và lương hấp dẫn, nhưng đòi hỏi kỹ năng chuyên sâu hơn — phù hợp làm mục tiêu dài hạn sau khi có nền tảng vững.
- Ưu tiên ứng tuyển vào ngành **Tài chính – Ngân hàng** và **Công nghệ – Phần mềm** — hai ngành có nhu cầu tuyển Data lớn nhất.
- Nên chủ động cải thiện **tiếng Anh** — tỷ lệ yêu cầu đang tăng dần qua từng tháng.
- Ưu tiên tìm việc tại **TP.HCM hoặc Hà Nội** để tối đa hóa cơ hội (hai thành phố chiếm hơn 94% tổng tin).
- Cơ hội intern/fresher khá hạn chế (\~5% tổng tin) — nên chủ động làm project cá nhân hoặc thực tập để tăng sức cạnh tranh khi ứng tuyển vị trí "Nhân viên".

---

## 7. Hạn chế & hướng phát triển tiếp theo

- Dữ liệu lương chỉ dựa trên tập con tin công khai mức lương, có thể thiên lệch về nhóm công ty minh bạch hơn.
- Phân loại vai trò dựa trên từ khóa trong JD, chưa phản ánh hoàn toàn chính xác bản chất công việc thực tế.
- Hướng mở rộng tiếp theo: thu thập liên tục để có chuỗi thời gian dài hơn, bổ sung phân tích theo quy mô công ty và loại hình công ty (product/outsourcing).

---

## Về dự án này

Báo cáo này là sản phẩm của một dự án cá nhân nhằm thực hành toàn bộ quy trình của một Data Analyst: thu thập dữ liệu (web scraping), làm sạch và xử lý dữ liệu (ETL), thiết kế mô hình dữ liệu (Star Schema), và trực quan hóa (Power BI dashboard gồm 4 trang: Tổng quan, Địa lý, Kỹ năng & Yêu cầu, Mức lương).

Dự án được thực hiện sau khi tham khảo báo cáo "Vietnam IT & Tech Talent Landscape 2024-2025" của TopDev, với mong muốn đào sâu hơn vào phân khúc Data — vốn chưa được phân tích riêng trong các báo cáo ngành IT nói chung.

*\[Ghi thêm tại đây: tên, liên hệ, link dashboard Power BI/GitHub nếu muốn đính kèm vào hồ sơ xin việc\]*