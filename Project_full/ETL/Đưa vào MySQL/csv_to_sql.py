import pandas as pd
import numpy as np

csv_path = 'Project_full/ETL/GHÉP_FILE/data_merged_2.csv'
sql_path = 'Project_full/ETL/Đưa vào MySQL/2. import_data_test.sql'

df = pd.read_csv(csv_path)

# Định nghĩa chính xác Datatype cho từng nhóm cột
cols = []
for col in df.columns:
    if col in ['date_posted', 'date_deadline']:
        cols.append(f'`{col}` DATE')
    elif col in ['mean_salary_fix', 'min_experience_fix']:
        cols.append(f'`{col}` DOUBLE')
    elif col.startswith('req_') or col.startswith('related_') or col.endswith('_benefits'):
        cols.append(f'`{col}` BOOLEAN')
    else:
        # Dùng TEXT cho các cột dạng chữ để tránh bị lỗi giới hạn 255 ký tự của VARCHAR
        cols.append(f'`{col}` TEXT')

# Xử lý dữ liệu rỗng
df = df.replace({np.nan: None})

create_stmt = "CREATE TABLE IF NOT EXISTS `raw_data` (\n" + ",\n".join(cols) + "\n);\n"
create_stmt += "TRUNCATE TABLE `raw_data`;\n"

with open(sql_path, 'w', encoding='utf-8') as f:
    f.write(create_stmt)
    
    batch_size = 500
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        values_list = []
        for _, row in batch.iterrows():
            row_vals = []
            for col_name, val in row.items():
                if val is None or val == "" or pd.isna(val):
                    row_vals.append("NULL")
                elif col_name in ['date_posted', 'date_deadline']:
                    row_vals.append(f"'{val}'")
                elif col_name in ['mean_salary_fix', 'min_experience_fix']:
                    row_vals.append(str(val))
                elif col_name.startswith('req_') or col_name.startswith('related_') or col_name.endswith('_benefits'):
                    if isinstance(val, str):
                        row_vals.append('1' if val.lower() == 'true' else '0')
                    else:
                        row_vals.append(str(int(bool(val))))
                else:
                    val_str = str(val).replace("'", "''").replace("\\", "\\\\")
                    row_vals.append(f"'{val_str}'")
            values_list.append("(" + ",".join(row_vals) + ")")
        
        insert_stmt = "INSERT INTO `raw_data` (" + ",".join([f"`{c}`" for c in df.columns]) + ") VALUES \n"
        insert_stmt += ",\n".join(values_list) + ";\n"
        f.write(insert_stmt)
