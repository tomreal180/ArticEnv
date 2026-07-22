from ultralytics import YOLO
import cv2

from PIL import Image
from IPython.display import display

def main():
    model = YOLO("yolov8n.pt") # Load a pretrained YOLOv8n model

    print("Starting training...")
    results = model.train(
        data='dataset.yaml',   # Point to configuration file for your dataset
        epochs=50,           # Number of training epochs
        imgsz=640,             # Input image size (YOLO will automatically resize your images to 640x640)
        batch=16,              # Number of images sent to the GPU at once. Reduce to 8 or 4 if you encounter out-of-memory errors.
        name='arctic_bear_model', # Name of the directory to save results
        device='cpu'             # Train on CPU
    )
    print("Training completed. Results are saved in the directory 'runs/train/arctic_bear_model'.")

if __name__ == "__main__":
    main()