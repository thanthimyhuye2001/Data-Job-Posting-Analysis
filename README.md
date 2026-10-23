# [POWER BI] Phân tích tuyển dụng ngành Data ở Việt Nam 

## [I. GIỚI THIỆU](https://)
### 1.1. Về báo cáo
Trước khi ứng tuyển vào ngành Data, mình muốn tự trả lời cho chính bản thân những câu hỏi bên dưới, thay vì chỉ dựa vào cảm nhận chủ quan hay những lời khuyên chung chung trên mạng:
1. Mình nên theo hướng nào DA ? DE ? DS ? AI ? 
2. Kỹ năng nào cần học? Tiếng Anh có quan trọng không?
3. Intern / Fresher, sinh viên mới ra trường, nên kỳ vọng mức lương bao nhiêu?

Vì vậy, mình đã tự thu thập dữ liệu tuyển dụng từ 4 nền tảng tuyển dụng việc làm phổ biến tại Việt Nam (Vietnamworks, TopCV, ITviec, CareerViet) thực hiện từ ngày **26/03/2026 – 13/06/2026**. Từ đó xây dựng mô hình dữ liệu và dashboard để phân tích.

### 1.2. Phương pháp thực hiện
 - **Nguồn dữ liệu**:  Cào 4 website tuyển dụng Vietnamworks, TopCV, ITviec, CareerViet dựa trên list từ khóa các ngành nghề trong lĩnh vực data.
 - **Phạm vi thời gian thu thập**: 30/03/2026 – 13/06/2026
 - **Quy mô dữ liệu**: 3,489 tin tuyển dụng trong lĩnh vực data từ 1,273 công ty (trong khung phân tích chính)
 - **Quy trình**: 
    <br>1. Python: Web scraping --> Explore data --> ETL  (lưu dữ liệu dạng CSV)<br>2. MySQL: Xác định Dim Fact --> Xây dựng Modeling dạng Star Schema<br>3. Power BI: Phân tích insights --> Xây dựng Dahsboard


**Data Modeling**
![**Data Modeling**](https://github.com/thanthimyhuye2001/Data-Job-Posting-Analysis/blob/main/Project_full/%E1%BA%A3nh/Modeling.png)

### 1.3. Lưu ý
- Phân tích lương chỉ dựa trên tập con các tin có công bố mức lương công khai, không đại diện 100% thị trường. Cụ thể là 885 job công bố lương, ứng với 25.4% tập dữ liệu.
- 4 nhóm vai trò (`Data Analyst / BI`, `Data Engineer`, `Data Science`, `AI / Machine Learning`) được gắn nhãn dựa trên từ khóa trong tên vị trí job, nên có thể chồng lấp giữa các nhóm, và không bao quát hết tập dữ liệu.
- Về thông tin địa điểm tỉnh thành, trường hợp tin tuyển dụng có hiển thị làm việc nhiều nơi, thì chỉ lấy thông tin tỉnh thành hợp lệ đầu tiên được nhắc tới.
- Dữ liệu phản ánh "nguồn cung tin tuyển dụng công khai", chưa bao gồm các vị trí tuyển qua headhunter / referral nội bộ.
### 1.4. Kết quả phân tích
- [Báo cáo phân tích thị trường tuyển dụng Data ở Việt Nam 2026 Q2](https://drive.google.com/file/d/1i0vdUc2pHrUWyC2YnwgQ-bANUDVWhyQ8/view?usp=drive_link)
- [Dashboard phân tích POWER BI](https://github.com/thanthimyhuye2001/Data-Job-Posting-Analysis/blob/main/Project_full/dashboard/Dashboard%20Job%20Posting%20Analyst.pbix)


---
## II. DASHBOARD  [POWER BI]
### 2.1. Phân tích tổng quan
Hướng phân tích:
- Cơ hội việc làm tăng trưởng mỗi ngày ra sao?
- Nhu cầu tuyển dụng đối với từng vai trò như thế nào?
- Cơ hội việc làm data tập trung ở lĩnh vực nào?
- Trong nội bộ từng lĩnh vực, họ ưu tiên tuyển ngành nghề nào nhất?
  
![](https://github.com/thanthimyhuye2001/Data-Job-Posting-Analysis/blob/main/Project_full/dashboard/1.Overview.png)

### 2.2. Phân tích thị trường làm việc theo khu vực
Hướng phân tích:
- Cơ hội việc làm Data tập trung ở đâu?
- Doanh nghiệp ở Hà Nội và TP.HCM đang kiếm tìm những vai trò nào?
- Mỗi khu vực thì mạnh ở những domain nào?
- Kiếm việc Remote/Hybrid/Part-time ở đâu?
  
![](https://github.com/thanthimyhuye2001/Data-Job-Posting-Analysis/blob/main/Project_full/dashboard/2.Location.png)


### 2.3. Phân tích các kỹ năng và yêu cầu
Hướng phân tích:
- Muốn vào ngành Data, nên theo hướng nào, học gì trước?
- Mỗi vai trò trong Data có “đóng khung” hay làm nhiều việc cùng lúc?
- Không có bằng Đại học có sao không?
- Kỹ năng tiếng Anh có bắt buộc phải có không?
  
![](https://github.com/thanthimyhuye2001/Data-Job-Posting-Analysis/blob/main/Project_full/dashboard/3.Skill%20%26%20Require.png)

### 2.4. Phân tích mức lương phổ biến
Hướng phân tích:
- Tiếng Anh có giúp tăng lương không?
- Lương bao nhiêu là hợp lý ở từng cấp bậc?
- Số năm kinh nghiệm ảnh hưởng tới mức lương như thế nào?
  
![](https://github.com/thanthimyhuye2001/Data-Job-Posting-Analysis/blob/main/Project_full/dashboard/4.Salary.png)

---
## III. INSIGHTS CHÍNH
#### 3.1. Nhu cầu theo vai trò và cấp bậc
- Thị trường do bộ ba **AI/Machine Learning, Data Analyst/BI và Data Engineer** dẫn dắt, còn Data Science rất ít và chỉ tập trung ở các tổ chức lớn có Big Data.
- Cấp **Nhân viên** chiếm 66% tin tuyển dụng, và ở cấp này **nhu cầu tuyển Data Analyst/ BI nhiều nhất**.
- Nhiều tin yêu cầu **một người kiêm nhiều vai trò** (Data Engineer x AI/Machine Learning, Data Analyst/BI x Data Engineer), và những vị trí lai này có mức lương cao hơn vai trò thuần.

#### 3.2. Nhu cầu theo lĩnh vực
- **Tài chính - Ngân hàng và Công nghệ** chiếm tới 55% tổng nhu cầu
- 5 lĩnh vực chiếm gần 90% thị trường: 
  <br>1. Tài chính - Ngân hàng
  <br>2. Công nghệ - Phần mềm
  <br>3. Thương mại điện tử - Bán lẻ
  <br>4. Sản xuất - Logistics
  <br>5. Dịch vụ - Truyền thông
   
- **Công nghệ - Phần mềm** nghiêng về kỹ thuật (AI/Machine Learning, Data Engineer), trong khi **TMĐT - Bán lẻ** thiên về Data Analyst/ BI .
- **Game** là lĩnh vực nghiêng về Data Analyst/ BI nhất, vì vận hành game dựa vào phân tích hành vi người chơi hằng ngày.
- **Tài chính - Ngân hàng** phân bổ đều giữa các vai trò và có tỷ lệ Data Science cao nhất, nhưng rào cản thuật ngữ và pháp lý khiến đây là nhóm khó vào nhất.

#### 3.3. Khu vực và hình thức làm việc
- Cơ hội gần như chỉ nằm ở 2 thành phố lớn **Hà Nội** và **Hồ Chí Minh**.
- Hà Nội mạnh ở Tài chính - Công nghệ, còn TP.HCM mạnh ở TMĐT, Dịch vụ - Truyền thông và Logistics.
- Job  Remote / Hybrid ở **Hồ Chí Minh** nhiều hơn.

#### 3.4. Kỹ năng và học vấn
- **SQL**  là kỹ năng phổ biến nhất.
- Kỹ năng tiếng Anh là rào cản lớn đối với Intern / Fresher, đặc biệt là ngành Sản xuất - Logistics. Nhưng đây cũng là yếu tố giúp đàm phán lương ở mức cao hơn.
- **21% tin không yêu cầu bằng cấp**, tập trung nhiều nhất ở Dịch vụ - Truyền thông.
- Xu hướng tuyển dụng đang dịch chuyển sang **kỹ năng và portfolio** thay vì bằng cấp.

#### 3.5. Mức lương
-	Lương Intern/Fresher khoảng 5-12 triệu, nhảy vọt lên 17-30 triệu khi thành Nhân viên chính thức.
-	Sau 5 năm, dải lương mở rộng rất rộng, nghĩa là kinh nghiệm chỉ quyết định “mức sàn”, còn lương thực tế phụ thuộc cấp bậc, vai trò và kỹ năng.
-	**Tỷ lệ tin công khai lương giảm dần khi yêu cầu số năm kinh nghiệm tăng lên**, và chỉ có 25% tổng dữ liệu thu được là công khai mức lương.

---
## IV. ĐỀ XUẤT

#### 4.1. Chọn hướng đi

- Chọn **Data Analyst / BI** làm vai trò khởi đầu, vì đây là vị trí có nhu cầu lớn nhất ở cấp nhân viên.
- Chưa nên nhắm Data Science làm vị trí đầu tiên, vì số tin ít và tập trung ở các tổ chức lớn.
- Ưu tiên lĩnh vực có rào cản thấp như **TMĐT - Bán lẻ, Truyền thông và Game**, nơi nghiệp vụ dễ hình dung và nhu cầu DA/BI cao.
- Tài chính - Ngân hàng nên để sau, bắt đầu từ các ngách như fintech hoặc số hóa.

#### 4.2. Chuẩn bị hồ sơ và kỹ năng

- Học **SQL trước tiên**, sau đó theo lộ trình Excel, Power BI/Tableau rồi Python.
- Xây **2-3 project portfolio** bằng dữ liệu thực, có dashboard hoàn chỉnh, để bù cho thiếu kinh nghiệm và bằng cấp.
- Cải thiện tiếng Anh song song với kỹ năng, bắt đầu từ đọc hiểu tài liệu kỹ thuật và viết CV, email.
- Chỉ nộp vào công ty Global / Outsourcing khi đã đủ tự tin về tiếng Anh, trước đó ưu tiên các lĩnh vực yêu cầu tiếng Anh thấp.

##### 4.3. Tìm việc và đặt kỳ vọng

- Tập trung tìm việc ở **Hà Nội và TP.HCM**, và chuẩn bị tâm lý làm Onsite/Full-time vì hình thức linh hoạt rất hiếm.
- Xem vị trí intern là bước đệm lấy kinh nghiệm, vì lương tăng rõ rệt khi lên nhân viên chính thức.
- Về dài hạn, tăng giá trị bằng **kỹ năng lai** (ví dụ DA/BI biết thêm kỹ năng DE) thay vì chỉ chờ thêm năm kinh nghiệm.
- Dùng mốc 3-5 năm để nhảy việc hoặc thăng tiến, và tham chiếu lương theo cấp bậc thay vì theo số năm khi đàm phán.
