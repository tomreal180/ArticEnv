# Arctic Environment Simulator

This project is a 3D application built with the Panda3D engine. It simulates an arctic environment featuring an animated polar bear, dynamic weather effects (blizzard and sunny), a particle-based snow system, and multiple camera controls.

A key feature of this application is its ability to generate synthetic data for machine learning. It can calculate the 2D bounding box of the 3D polar bear model in real-time and save screenshots paired with YOLO-formatted label files.

## Features

- **Modular System Design**: The application is broken down into clear, manageable systems (Environment, Snow, Camera, Actor, Recording).
- **Dynamic Environment**: Switch between a dense blizzard and a clear, sunny day. Lighting, fog, and background color adjust accordingly.
- **Particle Snow System**: A procedural snow system with adjustable flake count and wind effects.
- **Animated Actor**: An animated polar bear that walks along a predefined path.
- **Advanced Camera Controls**: Multiple camera presets (top-down, side views, etc.) and runtime adjustments for height and distance.
- **Synthetic Data Generation**:
    - Automatically records image frames and corresponding YOLO `.txt` label files.
    - Renders a real-time 2D bounding box overlay for visualization.
    - Renders a wireframe overlay on the 3D model for debugging.
- **Configurable**: Most initial parameters are controlled via a `config.json` file.

## Project Structure

```
ArticEnv/
├── assets/
│   ├── models/
│   │   ├── polar_bear2.glb
│   │   └── snow_mountain/
│   │       └── scene.gltf
│   └── textures/
│       └── snowflake.png
├── YOLO Model/
│   ├── dataset.yaml
│   ├── train_model.py
│   └── test_model.py
├── src/
│   ├── __init__.py
│   ├── camera_system.py
│   ├── enviroment_system.py
│   ├── Polar_bears.py
│   ├── record_system.py
│   └── snow_system.py
├── output/
│   ├── images/
│   └── labels/
├── config.json
└── main.py
```

- **`main.py`**: The main entry point of the application. It initializes all systems and handles user input.
- **`config.json`**: A configuration file to set initial values for the scene, actor, camera, snow, and recording systems.
- **`src/`**: Contains the core logic, broken down into different modules.
    - `enviroment_system.py`: Manages the 3D scene, lighting, and fog effects.
    - `snow_system.py`: Manages the creation and movement of snow particles.
    - `Polar_bears.py`: Defines the Polar Bear actor, its animations, movement, and debug overlays.
    - `camera_system.py`: Controls camera movement, positioning, and targeting.
    - `record_system.py`: Handles saving screenshots and YOLO label data.
- **`assets/`**: Stores all 3D models and textures.
- **`output/`**: The default directory where generated images and labels are saved.

## Setup and Installation

1.  **Prerequisites**:
    - Python 3.14.10

2.  **Clone the repository** (or ensure all files are in the same directory structure as above).

3.  **Install dependencies**:
    The primary dependency is Panda3D. You can install it using pip.
    For training and testing the YOLO model, you will also need `ultralytics`
    ```bash
    pip install -r requirements.txt
    ```
    It is recommended to do this in a virtual environment.

4.  **Assets**:
    Make sure the `assets` folder with the required models and textures is present in the project's root directory.

## How to Run

Navigate to the project's root directory in your terminal and run the main script:

```bash
python main.py
```

The application window will appear, displaying the simulation.

## Controls

| Key             | Action                                           |
|-----------------|--------------------------------------------------|
| **Recording**   |                                                  |
| `r`             | Toggle continuous recording of images and labels.|
| `f`             | Take a single screenshot and its label.          |
| `w`             | Toggle the green 2D YOLO bounding box overlay.   |
| **Environment** |                                                  |
| `d`             | Toggle between Blizzard and Sunny weather.       |
| `s` / `a`       | Increase / Decrease fog density.                 |
| `z` / `x`       | Increase / Decrease the entire scene's scale.    |
| **Snow**        |                                                  |
| `k` / `j`       | Increase / Decrease the number of snowflakes.    |
| `l`             | Update the snow area to follow the camera.       |
| **Camera**      |                                                  |
| `u` / `y`       | Increase / Decrease camera height.               |
| `o` / `i`       | Zoom Out / Zoom In (increase/decrease distance). |
| `t`             | Set camera to "main" view.                       |
| `Arrow Up`      | Set camera to "topdown" view.                    |
| `Arrow Down`    | Set camera to "behind" view.                     |
| `Arrow Left`    | Set camera to "left" view.                       |
| `Arrow Right`   | Set camera to "right" view.                      |
| **Actor (Bear)**|                                                  |
| `e`             | Toggle the red wireframe outline on the bear.    |
| `b` / `v`       | Increase / Decrease the bear's height (Z-axis).  |
| `n` / `m`       | Increase / Decrease the bear's scale.            |
| **Debug**       |                                                  |
| `p`             | Print current camera, actor, and scene values to the console. |

## Training and Using the YOLO Model

This project can generate a synthetic dataset to train a YOLOv8 object detection model to recognize the polar bear.

### 1. Generate the Dataset

1.  Run the main application: `python main.py`.
2.  Use the `r` key to start/stop automatic data recording or the `f` key to capture single frames.
3.  The images and YOLO-formatted labels will be saved into a directory specified in `config.json` (default is `polar_bear_dataset`). This directory will contain `images` and `labels` subdirectories, already split into `train` and `val` sets.

### 2. Prepare for Training

The YOLO training script expects a specific folder structure and a `dataset.yaml` file.

1.  **Navigate to the YOLO folder**:
    ```bash
    cd "YoLo Model"
    ```
2.  **Link the dataset**: The training script looks for a folder named `dataset`. Create a symbolic link (or simply copy/rename the generated folder `polar_bear_dataset` to `dataset`) inside the `YoLo Model` directory.
    - **Windows (as Admin)**:
      ```cmd
      mklink /D dataset "..\polar_bear_dataset"
      ```
    - **macOS / Linux**:
      ```bash
      ln -s ../polar_bear_dataset dataset
      ```
3.  **Verify `dataset.yaml`**: Ensure the `dataset.yaml` file inside the `YoLo Model` directory is configured correctly. The default file should work if you followed the step above.

### 3. Train the Model

Run the training script from within the `YoLo Model` directory:

```bash
python train_model.py
```

The training process will begin, and the results, including the trained model weights (`best.pt`), will be saved in the `runs/detect/arctic_bear_model/` directory.

### 4. Test the Model

1.  Place a test image (e.g., `test_image.png`) in the `YoLo Model` directory.
2.  Edit `test_model.py` to point to your test image.
3.  Run the script:
    ```bash
    python test_model.py
    ```
The script will perform inference, draw a bounding box on the detected bear, and save the result in the `runs/detect/predict/` directory.

---

*This README was generated by Gemini Code Assist.*
