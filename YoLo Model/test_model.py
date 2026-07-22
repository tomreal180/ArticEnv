from ultralytics import YOLO

# Load a trained YOLOv8 model
model = YOLO('runs/detect/arctic_bear_model/weights/best.pt')

# Run inference on an image
# for i in range(1, 6):
#     results = model(f'test_image{i}.png', save=True, conf=0.5)
results = model('test_real7.png', save=True, conf=0.5)
print("Done detecting, please go to the directory 'runs/detect/predict' to view the results!")