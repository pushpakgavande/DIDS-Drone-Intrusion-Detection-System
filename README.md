# Drone Intrusion Detection System (DIDS)

> **AI-powered real-time drone detection, monitoring, and intrusion alert system.**

## Overview

The **Drone Intrusion Detection System (DIDS)** is an AI-based computer vision application developed to detect drones in real time using a camera feed. It uses a trained **YOLOv8s object detection model** to identify drones and provides a monitoring dashboard with detection information, audible alerts, evidence capture, and optional SMS notification support.

## Key Features

- Real-time drone detection using YOLOv8s
- Live camera monitoring
- Bounding boxes around detected drones
- Detection confidence display
- Current-frame drone count
- Audible siren alert when a drone is detected
- Evidence image capture
- Optional SMS alerts using Twilio
- Professional fullscreen monitoring dashboard
- Automatic camera detection
- Configurable confidence threshold
- Secure environment-variable based SMS configuration

## System Workflow

```text
Camera Feed
    |
    v
Frame Capture
    |
    v
YOLOv8s Detection Model
    |
    v
Drone Detection
    |
    v
Bounding Box + Confidence + Drone Count
    |
    v
Intrusion Alert
    |
    +-------------------+
    |                   |
    v                   v
Siren Alert       Evidence Capture
                        |
                        v
                Optional SMS Alert
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| OpenCV | Camera capture and computer vision |
| Ultralytics YOLOv8 | Drone object detection |
| PyTorch | Deep learning framework |
| Tkinter | Graphical user interface |
| Pillow | Image processing and display |
| Twilio | Optional SMS notification |
| Git & GitHub | Version control and project hosting |

## Model Performance

The final YOLOv8s model was trained for **100 epochs** and evaluated on the cleaned validation dataset.

| Metric | Performance |
|---|---:|
| Precision | **92.3%** |
| Recall | **94.3%** |
| mAP@50 | **96.8%** |
| mAP@50-95 | **64.1%** |

The final validation evaluation used **3,223 images** containing **3,014 annotated drone instances**.

## Model Configuration

| Parameter | Value |
|---|---|
| Model | YOLOv8s |
| Training epochs | 100 |
| Confidence threshold | 0.50 |
| Number of classes | 1 |
| Detection class | `drone` |

## Project Structure

```text
DIDS/
|
+-- best.pt                         # Final trained YOLOv8s model
+-- gui_dids.py                     # Main DIDS monitoring application
+-- logo.png                        # Application logo
+-- siren.wav                       # Intrusion alert sound
+-- README.md                       # Project documentation
+-- .gitignore                      # Git exclusion rules
|
+-- test_images/
|   +-- test.jpg                    # Sample test image
|   +-- test2.jpg                   # Sample test image
|
+-- dataset_raw/
    +-- drone_dataset2/
        +-- data.yaml               # Dataset configuration
        +-- yolo11n.pt              # Reference pretrained model
        +-- yolov8n.pt              # Reference pretrained model
        +-- yolov8s.pt              # Reference pretrained model
```

> Training images, labels, runtime evidence, virtual environments, and training outputs are intentionally excluded from version control.

## Requirements

- Python 3.9 or newer
- PyTorch
- Ultralytics
- OpenCV
- Pillow
- NumPy
- Tkinter
- Twilio (only when SMS notification is required)

Install the required Python packages with:

```powershell
pip install ultralytics opencv-python pillow numpy twilio
```

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/pushpakgavande/DIDS-Drone-Intrusion-Detection-System.git
cd DIDS-Drone-Intrusion-Detection-System
```

### 2. Create a virtual environment

```powershell
python -m venv dids_env
```

Activate it on Windows PowerShell:

```powershell
.\dids_env\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install ultralytics opencv-python pillow numpy twilio
```

## Running the Application

Make sure the following files are available in the project root:

- `best.pt`
- `gui_dids.py`
- `logo.png`
- `siren.wav`

Start the application with:

```powershell
python gui_dids.py
```

The application automatically searches available camera indexes and opens the DIDS monitoring dashboard.

### Controls

| Control | Function |
|---|---|
| START MONITORING | Starts real-time drone detection |
| STOP | Stops monitoring |
| EXIT | Closes the application |
| Esc | Exits fullscreen |
| Z | Exits the application with confirmation |

## SMS Alert Configuration

SMS notifications are optional. The application reads Twilio credentials from environment variables instead of storing them directly in the source code.

Set the following variables in PowerShell:

```powershell
$env:TWILIO_ACCOUNT_SID="your_account_sid"
$env:TWILIO_AUTH_TOKEN="your_auth_token"
$env:TWILIO_PHONE_NUMBER="your_twilio_number"
$env:TARGET_PHONE_NUMBER="your_target_number"
```

Then run the application normally:

```powershell
python gui_dids.py
```

If SMS credentials are not configured, the system continues to operate with local detection, siren, and evidence capture.

**Never commit real API credentials, authentication tokens, passwords, or `.env` files to GitHub.**

## Evidence Capture

When an intrusion is detected, the system can capture evidence frames for later inspection. Runtime evidence is excluded from the Git repository through `.gitignore`.

## Dataset

The dataset configuration is stored in:

```text
dataset_raw/drone_dataset2/data.yaml
```

The dataset was cleaned before final training. Duplicate images, invalid files, and a corrupt validation image were removed before the final model evaluation.

The training and validation image/label directories are intentionally not included in the public repository.

## Challenges and Solutions

### 1. Dataset duplicates and invalid files

Duplicate images and an invalid Python file were identified during dataset inspection.

**Solution:** The dataset was cleaned before final training.

### 2. Corrupt validation image

A corrupt validation image was identified during validation.

**Solution:** The corrupt image and its corresponding label were removed and the validation cache was rebuilt.

### 3. Real-time detection performance

The system needed strong detection accuracy while remaining practical for real-time inference.

**Solution:** YOLOv8s was trained for 100 epochs to provide a strong balance between detection accuracy and practical performance.

### 4. Secure SMS integration

Hardcoding Twilio credentials could expose sensitive information in source control.

**Solution:** Credentials are read from environment variables and are not stored in the application source code.

### 5. Repository organization

Including the complete dataset and training outputs would make the repository unnecessarily large.

**Solution:** Dataset images, labels, runtime evidence, virtual environments, and training outputs are excluded using `.gitignore`, while the final trained model is included.

## Applications

- Restricted airspace monitoring
- Industrial and infrastructure security
- Campus and institutional security
- Perimeter surveillance
- Critical facility monitoring
- Event and temporary restricted-zone monitoring

## Limitations

- Performance depends on camera quality, lighting, distance, and viewing angle.
- A single camera provides limited coverage.
- Very small or heavily occluded drones may be harder to detect.
- Real-world deployment requires additional testing under different environmental conditions.
- SMS notification requires valid Twilio configuration and network connectivity.

## Future Scope

- Multi-camera monitoring
- Drone tracking across consecutive frames
- Improved detection of very small drones
- Night-time and low-light detection
- Additional object classes
- Web-based remote monitoring
- Database-backed incident logging
- Cloud-based alerting
- Edge-device deployment
- Integration with security and surveillance infrastructure

## Security Notes

- Do not commit API keys, authentication tokens, passwords, or other secrets.
- Keep Twilio credentials in environment variables or a secure secret-management system.
- Keep runtime evidence and local configuration files outside version control.

## Author

**Pushpak Gavande**  
**Ayan Sawant**
Parul Institute of Technology, Parul University

## Repository

[GitHub Repository](https://github.com/pushpakgavande/DIDS-Drone-Intrusion-Detection-System)

---

**Drone Intrusion Detection System (DIDS)** — AI-powered real-time drone monitoring and intrusion alert system.
