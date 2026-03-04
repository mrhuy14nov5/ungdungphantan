import random
import time
from protocol import send_msg
from config import NODES

def send(cmd):
    """
    Gửi lệnh đến một node ngẫu nhiên. 
    Nếu node đó sập, thử chọn một node khác trong danh sách.
    """
    # Tạo danh sách các node để thử dần nếu có node bị sập
    available_nodes = list(NODES)
    random.shuffle(available_nodes)

    for node in available_nodes:
        try:
            response = send_msg(node, cmd)
            return response
        except (ConnectionRefusedError, OSError):
            print(f"[!] Node {node} không phản hồi, đang thử node khác...")
            continue
    
    return {"status": "ERROR", "message": "Toàn bộ cụm node không thể kết nối."}

def print_help():
    print("\n--- Hệ thống lưu trữ Phân tán ---")
    print("Các lệnh hỗ trợ:")
    print("  put <key> <value>    : Lưu trữ dữ liệu")
    print("  get <key>            : Lấy dữ liệu")
    print("  delete <key>         : Xóa dữ liệu")
    print("  exit                 : Thoát chương trình")
    print("---------------------------------\n")

if __name__ == "__main__":
    print_help()
    while True:
        try:
            user_input = input(">>> ").strip().split()
            if not user_input:
                continue

            cmd_type = user_input[0].lower()

            if cmd_type == "exit":
                break
            
            if cmd_type == "put":
                if len(user_input) < 3:
                    print("Lỗi: Thiếu key hoặc value. Cú pháp: put <key> <value>")
                    continue
                res = send({"type": "PUT", "key": user_input[1], "value": user_input[2]})
                print(f"Kết quả: {res}")

            elif cmd_type == "get":
                if len(user_input) < 2:
                    print("Lỗi: Thiếu key. Cú pháp: get <key>")
                    continue
                res = send({"type": "GET", "key": user_input[1]})
                print(f"Kết quả: {res}")

            elif cmd_type == "delete":
                if len(user_input) < 2:
                    print("Lỗi: Thiếu key. Cú pháp: delete <key>")
                    continue
                # Gửi lệnh DELETE tương tự như PUT (cần Quorum Write)
                res = send({"type": "DELETE", "key": user_input[1]})
                print(f"Kết quả: {res}")

            else:
                print("Lệnh không hợp lệ.")
                print_help()

        except KeyboardInterrupt:
            print("\nĐang thoát...")
            break
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")