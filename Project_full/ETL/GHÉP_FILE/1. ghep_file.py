import pandas as pd
import time
import os

start_time = time.time()

# Định nghĩa đường dẫn các file
vnw_path = r"Project_full/ETL/ETL_1_vietnamworks/data_vnw_5.csv"
itv_path = r"Project_full/ETL/ETL_2_ITviec/data_ITviec_10.csv"
top_path = r"Project_full/ETL/ETL_3_topcv/data_topcv_5.csv"
crv_path = r"Project_full/ETL/ETL_4_careerviet/data_crviet_4.csv"


print("Đang đọc các file dữ liệu...")
df_vnw = pd.read_csv(vnw_path)
df_itv = pd.read_csv(itv_path)
df_top = pd.read_csv(top_path)
df_crv = pd.read_csv(crv_path)

# Hàm làm sạch sơ bộ và đồng bộ các cột trước khi gộp
def clean_dataframe(df):
    # Loại bỏ các cột dư thừa
    cols_to_drop = ['index', 'source_site']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    return df

df_vnw = clean_dataframe(df_vnw)
df_itv = clean_dataframe(df_itv)
df_top = clean_dataframe(df_top)
df_crv = clean_dataframe(df_crv)

print(f"Kích thước VNW: {df_vnw.shape}")
print(f"Kích thước ITV: {df_itv.shape}")
print(f"Kích thước TOP: {df_top.shape}")
print(f"Kích thước CRV: {df_crv.shape}")

print("\nTiến hành gộp 4 file (Union)...")
# Khi dùng pd.concat, nếu dataframe nào thiếu cột (ví dụ TOP thiếu note_to_combine, 
# CRV thiếu company_field và note_to_combine), Pandas sẽ tự động điền NaN (None) vào cột đó.
df_merged = pd.concat([df_vnw, df_itv, df_top, df_crv], ignore_index=True)

print(f"✅ Gộp thành công! Kích thước file tổng: {df_merged.shape}")
print(f"Số lượng dòng: {df_merged.shape[0]}, Số lượng cột: {df_merged.shape[1]}")
print(f"Danh sách các cột trong file gộp:\n{list(df_merged.columns)}")

# Lưu ra file mới
output_path = "Project_full/ETL/GHÉP_FILE/data_merged.csv"
df_merged.to_csv(output_path, index=False)
print(f"\n✅ Đã lưu file tổng vào: {output_path}")
print(f"⏱ Thời gian chạy: {time.time() - start_time:.4f} giây")
