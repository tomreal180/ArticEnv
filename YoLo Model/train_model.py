from ultralytics import YOLO
import cv2

from PIL import Image
from IPython.display import display

def main():
    model = YOLO("yolov8n.pt")

    print("Starting training...")
    results = model.train(
        data='dataset.yaml',   # Trỏ tới file cấu hình vừa tạo
        epochs=50,           # Số vòng lặp qua toàn bộ dataset. Bắt đầu với 50-100 vòng.
        imgsz=640,             # Kích thước ảnh đầu vào (YOLO sẽ tự resize ảnh của bạn về 640x640)
        batch=16,              # Số lượng ảnh đưa vào GPU cùng lúc. Giảm xuống 8 hoặc 4 nếu bị lỗi hết RAM.
        name='arctic_bear_model', # Tên thư mục lưu kết quả
        device='cpu'             # Sử dụng GPU đầu tiên. Đổi thành 'cpu' nếu máy không có card rời.
    )
    print("Training completed. Results are saved in the directory 'runs/train/arctic_bear_model'.")

if __name__ == "__main__":
    main()

    