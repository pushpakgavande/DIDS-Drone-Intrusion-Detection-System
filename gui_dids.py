import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
from datetime import datetime
import winsound
import time
import os

# ============================================================
# DIDS - DRONE INTRUSION DETECTION SYSTEM
# ============================================================

# ================= CONFIGURATION =================

MODEL_PATH = "best.pt"
CONF_THRESHOLD = 0.50

SIREN_DURATION = 10
SMS_COOLDOWN = 30
IMAGE_COOLDOWN = 5

# Optional Twilio configuration through environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TARGET_PHONE_NUMBER = os.getenv("TARGET_PHONE_NUMBER")

# ================= DIRECTORIES =================

os.makedirs("evidence", exist_ok=True)

# ================= MODEL =================

try:
    model = YOLO(MODEL_PATH)
    model_status = "READY"
except Exception as e:
    model = None
    model_status = "ERROR"
    print("Model loading error:", e)

# ================= TWILIO =================

twilio_client = None

if all([
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    TARGET_PHONE_NUMBER
]):
    try:
        from twilio.rest import Client

        twilio_client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

        sms_configured = True

    except Exception as e:
        print("Twilio initialization error:", e)
        sms_configured = False

else:
    sms_configured = False


# ================= CAMERA =================

def get_working_camera():

    print("Searching for camera...")

    for index in range(5):

        camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)

        if camera.isOpened():

            ret, frame = camera.read()

            if ret:
                print(f"Camera working at index {index}")
                return camera

            camera.release()

    print("No working camera detected!")
    return None


cap = get_working_camera()

if cap is not None:

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# ================= SYSTEM STATE =================

running = False

siren_on = False
siren_start_time = 0

last_sms_time = 0
last_image_time = 0

last_detection_time = "--"

# ============================================================
# GUI
# ============================================================

window = tk.Tk()

window.title("DIDS - Drone Intrusion Detection System")

window.geometry("1280x800")

window.configure(bg="#0b1220")

window.attributes("-fullscreen", True)


# ============================================================
# COLORS
# ============================================================

BG = "#0b1220"
CARD = "#111c2e"
CARD_LIGHT = "#17243a"

PRIMARY = "#38bdf8"
SUCCESS = "#22c55e"
DANGER = "#ef4444"
WARNING = "#f59e0b"

TEXT = "#f8fafc"
MUTED = "#94a3b8"


# ============================================================
# KEYBOARD CONTROLS
# ============================================================

def exit_fullscreen(event=None):

    window.attributes("-fullscreen", False)


def close_program(event=None):

    global running

    answer = messagebox.askyesno(
        "Exit DIDS",
        "Are you sure you want to exit the Drone Intrusion Detection System?"
    )

    if answer:

        running = False

        stop_siren()

        if cap is not None:
            cap.release()

        cv2.destroyAllWindows()

        window.destroy()


window.bind("<Escape>", exit_fullscreen)

window.bind("<z>", close_program)
window.bind("<Z>", close_program)

window.protocol("WM_DELETE_WINDOW", close_program)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    window,
    bg=BG,
    height=90
)

header.pack(fill="x", padx=30, pady=(20, 5))

header.pack_propagate(False)


# ================= LOGO =================

try:

    logo_img = Image.open("logo.png")

    logo_img.thumbnail((65, 65))

    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(
        header,
        image=logo_photo,
        bg=BG
    )

    logo_label.pack(
        side="left",
        padx=(5, 15)
    )

except Exception:

    logo_label = tk.Label(
        header,
        text="DIDS",
        font=("Arial", 24, "bold"),
        fg=PRIMARY,
        bg=BG
    )

    logo_label.pack(
        side="left",
        padx=15
    )


# ================= TITLE =================

title_frame = tk.Frame(
    header,
    bg=BG
)

title_frame.pack(
    side="left",
    fill="y"
)


title_label = tk.Label(
    title_frame,
    text="DRONE INTRUSION DETECTION SYSTEM",
    font=("Arial", 24, "bold"),
    fg=TEXT,
    bg=BG
)

title_label.pack(
    anchor="w",
    pady=(12, 0)
)


subtitle_label = tk.Label(
    title_frame,
    text="AI-Powered Real-Time Surveillance & Intrusion Alert Platform",
    font=("Arial", 11),
    fg=MUTED,
    bg=BG
)

subtitle_label.pack(
    anchor="w",
    pady=(3, 0)
)


# ================= SYSTEM INDICATOR =================

system_indicator = tk.Label(
    header,
    text="● SYSTEM READY",
    font=("Arial", 11, "bold"),
    fg=SUCCESS,
    bg=BG
)

system_indicator.pack(
    side="right",
    padx=15,
    pady=20
)


# ============================================================
# MAIN CONTENT
# ============================================================

main_frame = tk.Frame(
    window,
    bg=BG
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# ============================================================
# LEFT - CAMERA PANEL
# ============================================================

camera_panel = tk.Frame(
    main_frame,
    bg=CARD,
    bd=0
)

camera_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 12)
)


camera_title = tk.Label(
    camera_panel,
    text="LIVE SURVEILLANCE FEED",
    font=("Arial", 14, "bold"),
    fg=TEXT,
    bg=CARD
)

camera_title.pack(
    anchor="w",
    padx=20,
    pady=(15, 8)
)


camera_status = tk.Label(
    camera_panel,
    text="● CAMERA ONLINE",
    font=("Arial", 9, "bold"),
    fg=SUCCESS,
    bg=CARD
)

camera_status.pack(
    anchor="w",
    padx=20,
    pady=(0, 10)
)


# ================= CAMERA DISPLAY =================

camera_display = tk.Frame(
    camera_panel,
    bg="#020617"
)

camera_display.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0, 15)
)


camera_label = tk.Label(
    camera_display,
    text="Initializing camera...",
    font=("Arial", 16),
    fg=MUTED,
    bg="#020617"
)

camera_label.pack(
    fill="both",
    expand=True
)


# ============================================================
# RIGHT - INFORMATION PANEL
# ============================================================

info_panel = tk.Frame(
    main_frame,
    bg=BG,
    width=350
)

info_panel.pack(
    side="right",
    fill="y"
)

info_panel.pack_propagate(False)


# ============================================================
# DETECTION STATUS CARD
# ============================================================

detection_card = tk.Frame(
    info_panel,
    bg=CARD,
    height=180
)

detection_card.pack(
    fill="x",
    pady=(0, 10)
)

detection_card.pack_propagate(False)


tk.Label(
    detection_card,
    text="DETECTION STATUS",
    font=("Arial", 11, "bold"),
    fg=MUTED,
    bg=CARD
).pack(
    pady=(15, 2)
)


status_label = tk.Label(
    detection_card,
    text="SYSTEM STOPPED",
    font=("Arial", 19, "bold"),
    fg=DANGER,
    bg=CARD
)

status_label.pack(
    pady=5
)


counter_label = tk.Label(
    detection_card,
    text="0",
    font=("Arial", 42, "bold"),
    fg=PRIMARY,
    bg=CARD
)

counter_label.pack()


tk.Label(
    detection_card,
    text="DRONES DETECTED",
    font=("Arial", 9, "bold"),
    fg=MUTED,
    bg=CARD
).pack()


# ============================================================
# DETAILS CARD
# ============================================================

details_card = tk.Frame(
    info_panel,
    bg=CARD,
    height=150
)

details_card.pack(
    fill="x",
    pady=10
)

details_card.pack_propagate(False)


tk.Label(
    details_card,
    text="DETECTION INFORMATION",
    font=("Arial", 11, "bold"),
    fg=MUTED,
    bg=CARD
).pack(
    anchor="w",
    padx=15,
    pady=(15, 8)
)


confidence_label = tk.Label(
    details_card,
    text="Confidence: --",
    font=("Arial", 11),
    fg=TEXT,
    bg=CARD
)

confidence_label.pack(
    anchor="w",
    padx=15,
    pady=3
)


time_label = tk.Label(
    details_card,
    text="Last Detection: --",
    font=("Arial", 11),
    fg=TEXT,
    bg=CARD
)

time_label.pack(
    anchor="w",
    padx=15,
    pady=3
)


# ============================================================
# SYSTEM STATUS CARD
# ============================================================

system_card = tk.Frame(
    info_panel,
    bg=CARD,
    height=190
)

system_card.pack(
    fill="x",
    pady=10
)

system_card.pack_propagate(False)


tk.Label(
    system_card,
    text="SYSTEM STATUS",
    font=("Arial", 11, "bold"),
    fg=MUTED,
    bg=CARD
).pack(
    anchor="w",
    padx=15,
    pady=(15, 8)
)


model_status_label = tk.Label(
    system_card,
    text=f"● AI MODEL     {model_status}",
    font=("Arial", 10, "bold"),
    fg=SUCCESS if model_status == "READY" else DANGER,
    bg=CARD
)

model_status_label.pack(
    anchor="w",
    padx=15,
    pady=5
)


siren_status = tk.Label(
    system_card,
    text="● SIREN        OFF",
    font=("Arial", 10, "bold"),
    fg=SUCCESS,
    bg=CARD
)

siren_status.pack(
    anchor="w",
    padx=15,
    pady=5
)


sms_status = tk.Label(
    system_card,
    text="● SMS ALERT    " + ("READY" if sms_configured else "NOT CONFIGURED"),
    font=("Arial", 10, "bold"),
    fg=SUCCESS if sms_configured else WARNING,
    bg=CARD
)

sms_status.pack(
    anchor="w",
    padx=15,
    pady=5
)


# ============================================================
# ALERT CARD
# ============================================================

alert_card = tk.Frame(
    info_panel,
    bg="#132033",
    height=100
)

alert_card.pack(
    fill="x",
    pady=10
)

alert_card.pack_propagate(False)


alert_label = tk.Label(
    alert_card,
    text="✓ AREA SECURE\nNo drone detected",
    font=("Arial", 12, "bold"),
    fg=SUCCESS,
    bg="#132033",
    justify="center"
)

alert_label.pack(
    expand=True
)


# ============================================================
# BUTTON PANEL
# ============================================================

button_frame = tk.Frame(
    window,
    bg=BG
)

button_frame.pack(
    fill="x",
    padx=30,
    pady=(5, 20)
)


# ============================================================
# FUNCTIONS
# ============================================================

def start_detection():

    global running

    if model is None:

        messagebox.showerror(
            "Model Error",
            "The YOLO model could not be loaded."
        )

        return

    if cap is None:

        messagebox.showerror(
            "Camera Error",
            "No working camera was detected."
        )

        return

    running = True

    status_label.config(
        text="MONITORING",
        fg=PRIMARY
    )

    system_indicator.config(
        text="● SYSTEM ACTIVE",
        fg=SUCCESS
    )


def stop_detection():

    global running

    running = False

    stop_siren()

    counter_label.config(
        text="0"
    )

    confidence_label.config(
        text="Confidence: --"
    )

    status_label.config(
        text="SYSTEM STOPPED",
        fg=DANGER
    )

    alert_label.config(
        text="SYSTEM STOPPED\nMonitoring is inactive",
        fg=MUTED
    )

    system_indicator.config(
        text="● SYSTEM READY",
        fg=WARNING
    )

    window.configure(
        bg=BG
    )


def stop_siren():

    global siren_on

    if siren_on:

        winsound.PlaySound(
            None,
            winsound.SND_PURGE
        )

        siren_on = False

        siren_status.config(
            text="● SIREN        OFF",
            fg=SUCCESS
        )


# ============================================================
# BUTTONS
# ============================================================

start_btn = tk.Button(
    button_frame,
    text="▶  START MONITORING",
    font=("Arial", 12, "bold"),
    bg=SUCCESS,
    fg="white",
    activebackground="#16a34a",
    activeforeground="white",
    width=22,
    height=2,
    bd=0,
    cursor="hand2",
    command=start_detection
)

start_btn.pack(
    side="left",
    padx=8
)


stop_btn = tk.Button(
    button_frame,
    text="■  STOP",
    font=("Arial", 12, "bold"),
    bg=DANGER,
    fg="white",
    activebackground="#dc2626",
    activeforeground="white",
    width=14,
    height=2,
    bd=0,
    cursor="hand2",
    command=stop_detection
)

stop_btn.pack(
    side="left",
    padx=8
)


exit_btn = tk.Button(
    button_frame,
    text="✕  EXIT",
    font=("Arial", 12, "bold"),
    bg="#475569",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    width=14,
    height=2,
    bd=0,
    cursor="hand2",
    command=close_program
)

exit_btn.pack(
    side="right",
    padx=8
)


# ============================================================
# MAIN DETECTION LOOP
# ============================================================

def update_frame():

    global siren_on
    global siren_start_time
    global last_sms_time
    global last_image_time
    global last_detection_time

    if cap is None:

        camera_label.config(
            text="CAMERA NOT AVAILABLE",
            fg=DANGER
        )

        window.after(
            1000,
            update_frame
        )

        return


    ret, frame = cap.read()


    if not ret:

        camera_status.config(
            text="● CAMERA ERROR",
            fg=DANGER
        )

        window.after(
            100,
            update_frame
        )

        return


    annotated_frame = frame.copy()


    # ========================================================
    # DETECTION
    # ========================================================

    if running and model is not None:

        results = model(
            frame,
            conf=CONF_THRESHOLD,
            verbose=False
        )

        result = results[0]

        annotated_frame = result.plot()

        boxes = result.boxes

        current_drone_count = (
            len(boxes)
            if boxes is not None
            else 0
        )


        # ====================================================
        # DRONE DETECTED
        # ====================================================

        if current_drone_count > 0:

            current_time = time.time()

            window.configure(
                bg="#2a0d0d"
            )

            status_label.config(
                text="⚠ INTRUSION DETECTED",
                fg=DANGER
            )

            counter_label.config(
                text=str(current_drone_count),
                fg=DANGER
            )

            alert_label.config(
                text="⚠ INTRUSION DETECTED\nDrone detected in monitored area",
                fg=DANGER
            )


            # ================================================
            # CONFIDENCE
            # ================================================

            if boxes.conf is not None:

                confidence = float(
                    boxes.conf.max().item()
                ) * 100

                confidence_label.config(
                    text=f"Confidence: {confidence:.1f}%"
                )


            # ================================================
            # DETECTION TIME
            # ================================================

            last_detection_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            time_label.config(
                text=f"Last Detection: {last_detection_time}"
            )


            # ================================================
            # SIREN
            # ================================================

            if not siren_on:

                try:

                    winsound.PlaySound(
                        "siren.wav",
                        winsound.SND_ASYNC |
                        winsound.SND_LOOP
                    )

                    siren_on = True

                    siren_start_time = current_time

                    siren_status.config(
                        text="● SIREN        ACTIVE",
                        fg=DANGER
                    )

                except Exception as e:

                    print("Siren error:", e)


            # ================================================
            # SMS
            # ================================================

            if (
                sms_configured
                and twilio_client is not None
                and current_time - last_sms_time > SMS_COOLDOWN
            ):

                try:

                    twilio_client.messages.create(
                        body="🚨 ALERT: Drone detected by DIDS.",
                        from_=TWILIO_PHONE_NUMBER,
                        to=TARGET_PHONE_NUMBER
                    )

                    sms_status.config(
                        text="● SMS ALERT    SENT",
                        fg=SUCCESS
                    )

                    last_sms_time = current_time

                except Exception as e:

                    print("SMS error:", e)

                    sms_status.config(
                        text="● SMS ALERT    FAILED",
                        fg=DANGER
                    )


            # ================================================
            # SAVE EVIDENCE
            # ================================================

            if (
                current_time - last_image_time
                > IMAGE_COOLDOWN
            ):

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                cv2.rectangle(
                    annotated_frame,
                    (5, 5),
                    (430, 42),
                    (0, 0, 0),
                    -1
                )

                cv2.putText(
                    annotated_frame,
                    timestamp,
                    (10, 31),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

                filename = (
                    "evidence/drone_"
                    + datetime.now().strftime(
                        "%Y-%m-%d_%H-%M-%S"
                    )
                    + ".jpg"
                )

                cv2.imwrite(
                    filename,
                    annotated_frame
                )

                last_image_time = current_time


        # ====================================================
        # NO DRONE
        # ====================================================

        else:

            counter_label.config(
                text="0",
                fg=PRIMARY
            )

            confidence_label.config(
                text="Confidence: --"
            )

            status_label.config(
                text="MONITORING",
                fg=PRIMARY
            )

            alert_label.config(
                text="✓ AREA SECURE\nNo drone detected",
                fg=SUCCESS
            )

            window.configure(
                bg=BG
            )


    # ========================================================
    # STOP SIREN AFTER DURATION
    # ========================================================

    if (
        siren_on
        and time.time() - siren_start_time
        >= SIREN_DURATION
    ):

        stop_siren()


    # ========================================================
    # TIMESTAMP ON LIVE FEED
    # ========================================================

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cv2.rectangle(
        annotated_frame,
        (5, 5),
        (225, 35),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        annotated_frame,
        timestamp,
        (10, 27),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 0),
        2
    )


    # ========================================================
    # DISPLAY FRAME
    # ========================================================

    frame_rgb = cv2.cvtColor(
        annotated_frame,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(
        frame_rgb
    )

    # Fit camera image into available panel
    display_width = 850
    display_height = 620

    img.thumbnail(
        (display_width, display_height),
        Image.Resampling.LANCZOS
    )

    imgtk = ImageTk.PhotoImage(
        image=img
    )

    camera_label.imgtk = imgtk

    camera_label.configure(
        image=imgtk,
        text=""
    )


    window.after(
        20,
        update_frame
    )


# ============================================================
# START APPLICATION
# ============================================================

update_frame()

window.mainloop()


# ============================================================
# CLEANUP
# ============================================================

if cap is not None:

    cap.release()

cv2.destroyAllWindows()