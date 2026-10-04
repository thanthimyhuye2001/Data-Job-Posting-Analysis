import subprocess
import sys
import time
import os

def cleanup_chrome_processes():
    """Đóng các tiến trình chromedriver bị treo để giải phóng RAM và Port"""
    try:
        # Xóa dòng kill chrome.exe để không tắt nhầm trình duyệt chính của bạn
        subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe", "/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    # Thư mục chứa file crawl_all.py
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Danh sách các file crawl cần chạy lần lượt (dùng đường dẫn tuyệt đối)
    scripts = [
        os.path.join(base_dir, "crawl_vietnamworks.py"),
        os.path.join(base_dir, "crawl_itviec.py"),
        os.path.join(base_dir, "crawl_topcv_3_groups.py"),
        os.path.join(base_dir, "crawl_careerviet_2_group.py")
    ]

    print("=========================================================")
    print(" BẮT ĐẦU CHƯƠNG TRÌNH CRAWL JOB TỰ ĐỘNG ")
    print("=========================================================")

    # Dọn dẹp trước khi bắt đầu
    cleanup_chrome_processes()

    for script in scripts:
        print(f"\n{'='*57}")
        script_name = os.path.basename(script)
        print(f" ĐANG CHẠY: {script_name}")
        print(f"{'='*57}\n")
        
        try:
            # sys.executable chứa đường dẫn tới python.exe đang chạy
            # Giúp đảm bảo file con chạy bằng đúng môi trường Python hiện tại
            subprocess.run([sys.executable, script], check=True)
            
            print(f"\n[THÀNH CÔNG] Đã chạy xong {script}")
            
            # Tạm nghỉ 5 giây giữa 2 script
            print("[HỆ THỐNG] Đang dọn dẹp RAM & Driver chờ script tiếp theo...")
            time.sleep(5)
            
            # Dọn dẹp tiến trình rác của script vừa xong
            cleanup_chrome_processes()
            time.sleep(2)
            
        except subprocess.CalledProcessError as e:
            print(f"\n[LỖI] {script} gặp lỗi (Mã thoát: {e.returncode}).")
            print("-> Tạm dừng chương trình.")
            break
        except KeyboardInterrupt:
            print("\n[THÔNG BÁO] Người dùng ngắt chương trình (Ctrl+C).")
            break
        except Exception as e:
            print(f"\n[LỖI CHƯA RÕ] Lỗi khi chạy {script}: {e}")
            break

    print("\n=========================================================")
    print(" HOÀN TẤT TOÀN BỘ QUÁ TRÌNH CRAWL ")
    print("=========================================================\n")

if __name__ == "__main__":
    main()
