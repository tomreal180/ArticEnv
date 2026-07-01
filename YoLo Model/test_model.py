from ultralytics import YOLO

# Tải bộ não AI bạn vừa train xong
model = YOLO('runs/detect/arctic_bear_model/weights/best.pt')

# Dự đoán trên một bức ảnh hoặc video mới
# Tham số save=True sẽ tự động vẽ khung Bounding Box và lưu thành ảnh mới
# for i in range(1, 6):
#     results = model(f'test_image{i}.png', save=True, conf=0.5)
results = model('test_real7.png', save=True, conf=0.5)
print("Đã nhận diện xong, hãy vào thư mục 'runs/detect/predict' để xem kết quả!")