\# Drone Intrusion Detection System (DIDS)



\## Overview



The \*\*Drone Intrusion Detection System (DIDS)\*\* is an AI-based computer vision system designed to detect unauthorized drones in real time using a camera feed. The system uses a trained \*\*YOLOv8s object detection model\*\* to identify drones, display bounding boxes and confidence scores, and provide visual and audible intrusion alerts.



The project combines real-time object detection with a professional monitoring dashboard and optional SMS notification support.



\## Key Features



\- Real-time drone detection using YOLOv8s

\- Live camera monitoring

\- Bounding boxes around detected drones

\- Detection confidence display

\- Current-frame drone count

\- Audible siren alert on detection

\- Evidence image capture

\- Optional SMS alerts using Twilio

\- Professional fullscreen monitoring dashboard

\- Automatic camera detection

\- Configurable detection confidence threshold

\- Secure environment-variable based configuration for SMS credentials



\## System Workflow



```text

Camera Feed

&#x20;    ↓

Frame Capture

&#x20;    ↓

YOLOv8s Detection Model

&#x20;    ↓

Drone Detection

&#x20;    ↓

Bounding Box + Confidence + Drone Count

&#x20;    ↓

Intrusion Alert

&#x20;    ↓

Siren + Evidence Capture

&#x20;    ↓

Optional SMS Notification





Technology Stack

Programming Language: Python

Computer Vision: OpenCV

Object Detection: Ultralytics YOLOv8

Deep Learning: PyTorch

GUI: Tkinter

Image Processing: Pillow

SMS Notification: Twilio

Audio Alert: WAV audio

Version Control: Git and GitHub

Model Performance



The final YOLOv8s model was trained for 100 epochs and evaluated on the cleaned validation dataset.



Metric	Result

Precision	92.3%

Recall	94.3%

mAP@50	96.8%

mAP@50–95	64.1%



Validation was performed on 3,223 images containing 3,014 annotated drone instances.



Model Configuration

Model: YOLOv8s

Training: 100 epochs

Confidence threshold in GUI: 0.50

Number of classes: 1

Class: drone

Project Structure

DIDS/

│

├── best.pt

├── gui\_dids.py

├── logo.png

├── siren.wav

├── README.md

├── .gitignore

│

├── test\_images/

│   ├── test.jpg

│   └── test2.jpg

│

└── dataset\_raw/

&#x20;   └── drone\_dataset2/

&#x20;       ├── data.yaml

&#x20;       ├── yolo11n.pt

&#x20;       ├── yolov8n.pt

&#x20;       └── yolov8s.pt



Training images, labels, runtime evidence, virtual environments, and training outputs are intentionally excluded from version control.



Requirements



Recommended:



Python 3.9+

PyTorch

Ultralytics

OpenCV

Pillow

NumPy

Tkinter

Twilio (only if SMS notification is required)



Install dependencies:



pip install ultralytics opencv-python pillow numpy twilio

Installation

1\. Clone the repository

git clone https://github.com/pushpakgavande/DIDS-Drone-Intrusion-Detection-System.git

cd DIDS-Drone-Intrusion-Detection-System

2\. Create and activate a virtual environment

python -m venv dids\_env

.\\dids\_env\\Scripts\\Activate.ps1

3\. Install dependencies

pip install ultralytics opencv-python pillow numpy twilio

Running the Application



Make sure best.pt, gui\_dids.py, logo.png, and siren.wav are in the project root.



Run:



python gui\_dids.py



The application automatically searches available camera indexes and starts the monitoring interface.



Controls

START MONITORING — begins real-time detection

STOP — stops monitoring

EXIT — closes the application

Esc — exits fullscreen

Z — exits the application with confirmation

SMS Alert Configuration



SMS notifications are optional. The application reads Twilio credentials from environment variables instead of storing credentials directly in the source code.



$env:TWILIO\_ACCOUNT\_SID="your\_account\_sid"

$env:TWILIO\_AUTH\_TOKEN="your\_auth\_token"

$env:TWILIO\_PHONE\_NUMBER="your\_twilio\_number"

$env:TARGET\_PHONE\_NUMBER="your\_target\_number"



Then run:



python gui\_dids.py



If SMS credentials are not configured, the system continues operating with local detection, siren, and evidence capture.



Never commit real API credentials, authentication tokens, passwords, or .env files to GitHub.



Evidence Capture



When an intrusion is detected, the system can save evidence frames for later inspection. Runtime evidence is excluded from the Git repository through .gitignore.



Dataset



The dataset configuration is stored in:



dataset\_raw/drone\_dataset2/data.yaml



The dataset was cleaned before final training by removing duplicate images, invalid label/script files, and a corrupt validation image.



The training and validation image/label directories are intentionally not included in the public repository.



Challenges and Solutions

Duplicate and invalid dataset files



Duplicate images and an invalid Python file were identified during dataset inspection.



Solution: The dataset was cleaned before final training.



Corrupt validation image



A corrupt validation image was identified during validation.



Solution: The corrupt image and its corresponding label were removed and the validation cache was rebuilt.



Real-time detection performance



The system needed good detection accuracy while remaining practical for real-time inference.



Solution: YOLOv8s was trained for 100 epochs to provide a strong balance between accuracy and performance.



Secure SMS integration



Hardcoding Twilio credentials could expose sensitive information.



Solution: Credentials are read from environment variables and are not stored in the source code.



Repository organization



Including the complete dataset and training outputs would make the repository unnecessarily large.



Solution: Dataset images, labels, runtime evidence, virtual environments, and training outputs are excluded using .gitignore, while the final trained model is included.



Applications

Restricted airspace monitoring

Industrial and infrastructure security

Campus and institutional security

Perimeter surveillance

Critical facility monitoring

Event and temporary restricted-zone monitoring

Limitations

Performance depends on camera quality, lighting, distance, and viewing angle.

A single camera provides limited coverage.

Very small or heavily occluded drones may be harder to detect.

Real-world deployment requires testing under different environmental conditions.

SMS notification requires valid Twilio configuration and network connectivity.

Future Scope

Multi-camera monitoring

Drone tracking across consecutive frames

Improved detection of very small drones

Night-time and low-light detection

Additional object classes

Web-based remote monitoring

Database-backed incident logging

Cloud-based alerting

Edge-device deployment

Integration with security and surveillance infrastructure

Security Notes

Do not commit API keys, authentication tokens, passwords, or other secrets.

Keep Twilio credentials in environment variables or a secure secret-management system.

Keep runtime evidence and local configuration files outside version control.

