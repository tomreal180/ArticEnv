import os
from panda3d.core import Filename
import random
import shutil

class Record_System:
    def __init__(self,win, taskMgr, config=None):
        self.win = win
        self.taskMgr = taskMgr
        self.yolo_coordinates = (0, 0, 0, 0)  # Khởi tạo với giá trị mặc định
        if config is None:
            config = {}
        self.frame_count = 0
        self.limit = config.get("limit", 10)
        self.validation_split = config.get("validation_split", 0.2)
        self.split_interval = config.get("split_interval", 10)
        self.is_recording = False
        # self.dataset_dir = config.get("dataset_dir", "polar_bear_dataset")
        self.session_files = []
        
        self.dataset_dir = None
        # for sub_dir in ["images/train", "images/val", "labels/train", "labels/val"]:
        #     os.makedirs(os.path.join(self.dataset_dir, sub_dir), exist_ok=True)

    # def scaler(self, number):
    #     return (number + 1) / 2

    # def yolo_normalize(self):
    #     min_x, max_x, min_y, max_y = self.get_Coordinates()
    #     min_yolo_y = 1 - self.scaler(max_y)
    #     max_yolo_y = 1 - self.scaler(min_y)
    #     return self.scaler(min_x), self.scaler(max_x), min_yolo_y, max_yolo_y

    # def get_yolo_coordinates(self):
    #     min_x, max_x, min_y, max_y = self.yolo_normalize()
    #     yolo_x_center = (min_x + max_x) / 2
    #     yolo_y_center = (min_y + max_y) / 2
    #     yolo_width = max_x - min_x
    #     yolo_height = max_y - min_y
    #     return yolo_x_center, yolo_y_center, yolo_width, yolo_height
    def set_yolo_coordinates(self,yolo_coordinates):
        self.yolo_coordinates = yolo_coordinates

    def get_dataset_name_from_keyboard(self):
        name = input("Enter a name for the dataset (or press Enter to use default): ")
        if name.strip() == "":
            name = "polar_bear_dataset"
        self.dataset_dir = name
        for sub_dir in ["images/train", "images/val", "labels/train", "labels/val"]:
            os.makedirs(os.path.join(self.dataset_dir, sub_dir), exist_ok=True)
    
    def togglerecording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            print("Started recording dataset.")
            self.session_files.clear()
            self.taskMgr.add(self.auto_capture_task, "auto_capture_task", delay=1)  # Capture every 1 second
        else:
            print("Stopped recording dataset.")
            self.taskMgr.remove("auto_capture_task")
            # self.split_val_train()
            self.session_files.clear()
        
    def auto_capture_task(self,task):
        if self.frame_count >= self.limit:  # Giới hạn số lượng ảnh chụp
            print("Reached maximum frame count. Stopping recording.")
            self.is_recording = False
            self.frame_count = 0
            self.dataset_dir = None
            return task.done
        self.take_single_photo()
        return task.again  # Schedule the task to run again after the specified interval

    def take_single_photo(self):
        if self.dataset_dir is None:
            self.get_dataset_name_from_keyboard()
        base_name = f"frame_{self.frame_count:04d}"
        filepath = f"{self.dataset_dir}/images/train/{base_name}.png"

        panda_filename = Filename.from_os_specific(filepath)

        self.win.saveScreenshot(panda_filename)
        txt_path = f"{self.dataset_dir}/labels/train/{base_name}.txt"

        yolo_x_center, yolo_y_center, yolo_width, yolo_height = self.yolo_coordinates
        with open(txt_path, 'w') as f:
            f.write(f"0 {yolo_x_center:.6f} {yolo_y_center:.6f} {yolo_width:.6f} {yolo_height:.6f}\n")

        self.session_files.append(base_name)
        print(f"Captured frame {self.frame_count} to {filepath}")
        self.frame_count += 1
        if self.frame_count > 0 and (self.frame_count % self.split_interval) == 0:
            self.split_val_train()

    def split_val_train(self):
        if not self.session_files:
            return
        
        num_val = self.validation_split  #int(len(self.session_files) * self.validation_split)

        if num_val == 0 and len(self.session_files) >= 5:
            num_val = 1
        
        if num_val == 0:
            print("Not enough files to split into validation set.")
            return
        
        val_files_basenames = random.sample(self.session_files, num_val)

        for basename in val_files_basenames:
            src_img = os.path.join(self.dataset_dir, 'images','train', f"{basename}.png")
            dst_img = os.path.join(self.dataset_dir, 'images','val', f"{basename}.png")
            src_label = os.path.join(self.dataset_dir, 'labels','train', f"{basename}.txt")
            dst_label = os.path.join(self.dataset_dir, 'labels','val', f"{basename}.txt")

            try:
                if os.path.exists(src_img):
                    shutil.move(src_img, dst_img)
                if os.path.exists(src_label):
                    shutil.move(src_label, dst_label)
            except Exception as e:
                raise Exception(f"Error moving files for {basename}: {e}")
            self.session_files.remove(basename)
        
        print(f" Moved {num_val} files to validation set.")
        # self.session_files.clear()
