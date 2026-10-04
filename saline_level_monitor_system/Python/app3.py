import tkinter as tk
import serial
import threading
import time
from collections import deque


# ==========================================
# SERIAL SETTINGS
# ==========================================

SERIAL_PORT = "COM8"   # CHANGE THIS
BAUD_RATE = 9600


# ==========================================
# SALINE CALIBRATION
# ==========================================

FULL_DISTANCE = 5.0
EMPTY_DISTANCE = 20.0


# ==========================================
# GRAPH DATA
# ==========================================

saline_history = deque(maxlen=40)
distance_history = deque(maxlen=40)


# ==========================================
# SERIAL CONNECTION
# ==========================================

try:
    ser = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    time.sleep(2)

    connection_status = "CONNECTED"

except Exception:
    ser = None
    connection_status = "DISCONNECTED"


# ==========================================
# COLORS
# ==========================================

BG = "#07111F"
HEADER = "#0D1B2A"
CARD = "#102236"
CARD2 = "#132A40"

WHITE = "#F8FAFC"
TEXT = "#CBD5E1"
MUTED = "#7890A8"

CYAN = "#22D3EE"
GREEN = "#22C55E"
YELLOW = "#F59E0B"
RED = "#EF4444"

GRID = "#213B52"


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Smart Hospital - IV Monitoring System")

root.geometry("1200x760")

root.minsize(1100, 700)

root.configure(bg=BG)


# ==========================================
# HEADER
# ==========================================

header = tk.Frame(
    root,
    bg=HEADER,
    height=90
)

header.pack(
    fill="x",
    padx=18,
    pady=(18, 10)
)

header.pack_propagate(False)


header_left = tk.Frame(
    header,
    bg=HEADER
)

header_left.pack(
    side="left",
    padx=25
)


title = tk.Label(
    header_left,
    text="SMART HOSPITAL",
    font=("Arial", 27, "bold"),
    fg=WHITE,
    bg=HEADER
)

title.pack(
    anchor="w",
    pady=(12, 0)
)


subtitle = tk.Label(
    header_left,
    text="SMART IV / SALINE MONITORING SYSTEM",
    font=("Arial", 11, "bold"),
    fg=MUTED,
    bg=HEADER
)

subtitle.pack(
    anchor="w"
)


# ==========================================
# LIVE INDICATOR
# ==========================================

live_frame = tk.Frame(
    header,
    bg=HEADER
)

live_frame.pack(
    side="right",
    padx=25
)


live_dot = tk.Label(
    live_frame,
    text="●",
    font=("Arial", 18),
    fg=GREEN,
    bg=HEADER
)

live_dot.pack(
    side="left",
    padx=(0, 7)
)


live_text = tk.Label(
    live_frame,
    text="LIVE MONITORING",
    font=("Arial", 11, "bold"),
    fg=WHITE,
    bg=HEADER
)

live_text.pack(
    side="left"
)


# ==========================================
# PATIENT INFORMATION
# ==========================================

patient_frame = tk.Frame(
    root,
    bg=CARD
)

patient_frame.pack(
    fill="x",
    padx=18,
    pady=5
)


patient = tk.Label(
    patient_frame,
    text="PATIENT ID   P-001",
    font=("Arial", 12, "bold"),
    fg=WHITE,
    bg=CARD
)

patient.pack(
    side="left",
    padx=22,
    pady=12
)


bed = tk.Label(
    patient_frame,
    text="BED NO.   B-12",
    font=("Arial", 12, "bold"),
    fg=WHITE,
    bg=CARD
)

bed.pack(
    side="left",
    padx=22,
    pady=12
)


sensor_name = tk.Label(
    patient_frame,
    text="HC-SR04 ULTRASONIC MONITOR",
    font=("Arial", 11, "bold"),
    fg=CYAN,
    bg=CARD
)

sensor_name.pack(
    side="right",
    padx=22
)


# ==========================================
# MAIN CONTENT
# ==========================================

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=12
)


# ==========================================
# LEFT COLUMN
# ==========================================

left_column = tk.Frame(
    content,
    bg=BG
)

left_column.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 7)
)


# ==========================================
# SALINE LEVEL CARD
# ==========================================

saline_card = tk.Frame(
    left_column,
    bg=CARD
)

saline_card.pack(
    fill="x",
    pady=(0, 10)
)


saline_title = tk.Label(
    saline_card,
    text="SALINE LEVEL",
    font=("Arial", 14, "bold"),
    fg=TEXT,
    bg=CARD
)

saline_title.pack(
    anchor="w",
    padx=22,
    pady=(18, 0)
)


saline_value = tk.Label(
    saline_card,
    text="-- %",
    font=("Arial", 42, "bold"),
    fg=WHITE,
    bg=CARD
)

saline_value.pack(
    pady=(5, 0)
)


# ==========================================
# PROGRESS BAR
# ==========================================

progress_background = tk.Canvas(
    saline_card,
    height=18,
    bg="#1B3045",
    highlightthickness=0
)

progress_background.pack(
    fill="x",
    padx=22,
    pady=15
)


def update_progress(value):

    progress_background.delete("all")

    width = progress_background.winfo_width()

    if width <= 1:
        return

    filled_width = (
        width * value / 100
    )

    if value > 50:
        progress_color = GREEN

    elif value > 20:
        progress_color = YELLOW

    else:
        progress_color = RED

    progress_background.create_rectangle(
        0,
        0,
        filled_width,
        18,
        fill=progress_color,
        outline=""
    )


# ==========================================
# STATUS
# ==========================================

status_value = tk.Label(
    saline_card,
    text="WAITING",
    font=("Arial", 18, "bold"),
    fg=WHITE,
    bg=CARD
)

status_value.pack(
    pady=(0, 18)
)


# ==========================================
# SENSOR CARD
# ==========================================

sensor_card = tk.Frame(
    left_column,
    bg=CARD
)

sensor_card.pack(
    fill="both",
    expand=True
)


sensor_title = tk.Label(
    sensor_card,
    text="SENSOR INFORMATION",
    font=("Arial", 14, "bold"),
    fg=TEXT,
    bg=CARD
)

sensor_title.pack(
    anchor="w",
    padx=22,
    pady=(18, 15)
)


distance_value = tk.Label(
    sensor_card,
    text="-- cm",
    font=("Arial", 32, "bold"),
    fg=CYAN,
    bg=CARD
)

distance_value.pack(
    pady=(5, 2)
)


distance_label = tk.Label(
    sensor_card,
    text="CURRENT DISTANCE",
    font=("Arial", 9, "bold"),
    fg=MUTED,
    bg=CARD
)

distance_label.pack()


sensor_line = tk.Frame(
    sensor_card,
    bg=GRID,
    height=1
)

sensor_line.pack(
    fill="x",
    padx=22,
    pady=20
)


sensor_info = tk.Label(
    sensor_card,
    text="HC-SR04 Ultrasonic Sensor",
    font=("Arial", 13, "bold"),
    fg=WHITE,
    bg=CARD
)

sensor_info.pack(
    pady=5
)


monitoring_info = tk.Label(
    sensor_card,
    text="Real-Time Distance Monitoring",
    font=("Arial", 11),
    fg=MUTED,
    bg=CARD
)

monitoring_info.pack(
    pady=5
)


# ==========================================
# RIGHT COLUMN
# ==========================================

right_column = tk.Frame(
    content,
    bg=BG
)

right_column.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(7, 0)
)


# ==========================================
# SALINE GRAPH CARD
# ==========================================

saline_graph_card = tk.Frame(
    right_column,
    bg=CARD
)

saline_graph_card.pack(
    fill="both",
    expand=True,
    pady=(0, 7)
)


saline_graph_title = tk.Label(
    saline_graph_card,
    text="SALINE LEVEL TREND",
    font=("Arial", 13, "bold"),
    fg=TEXT,
    bg=CARD
)

saline_graph_title.pack(
    anchor="w",
    padx=18,
    pady=(15, 5)
)


saline_graph = tk.Canvas(
    saline_graph_card,
    bg=CARD,
    highlightthickness=0
)

saline_graph.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


# ==========================================
# DISTANCE GRAPH CARD
# ==========================================

distance_graph_card = tk.Frame(
    right_column,
    bg=CARD
)

distance_graph_card.pack(
    fill="both",
    expand=True,
    pady=(7, 0)
)


distance_graph_title = tk.Label(
    distance_graph_card,
    text="ULTRASONIC DISTANCE TREND",
    font=("Arial", 13, "bold"),
    fg=TEXT,
    bg=CARD
)

distance_graph_title.pack(
    anchor="w",
    padx=18,
    pady=(15, 5)
)


distance_graph = tk.Canvas(
    distance_graph_card,
    bg=CARD,
    highlightthickness=0
)

distance_graph.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


# ==========================================
# CONNECTION STATUS
# ==========================================

connection_frame = tk.Frame(
    root,
    bg=BG
)

connection_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 12)
)


connection_label = tk.Label(
    connection_frame,
    text=f"●  Arduino: {connection_status}",
    font=("Arial", 11, "bold"),
    fg=GREEN if ser else RED,
    bg=BG
)

connection_label.pack(
    side="left"
)


system_label = tk.Label(
    connection_frame,
    text="SYSTEM STATUS: ACTIVE",
    font=("Arial", 10, "bold"),
    fg=MUTED,
    bg=BG
)

system_label.pack(
    side="right"
)


# ==========================================
# SALINE CALCULATION
# ==========================================

def calculate_saline(distance):

    percentage = (
        (EMPTY_DISTANCE - distance)
        /
        (EMPTY_DISTANCE - FULL_DISTANCE)
    ) * 100

    percentage = max(
        0,
        min(100, percentage)
    )

    return percentage


# ==========================================
# DRAW SALINE GRAPH
# ==========================================

def draw_saline_graph():

    saline_graph.delete("all")

    width = saline_graph.winfo_width()
    height = saline_graph.winfo_height()

    if width <= 20 or height <= 20:
        return

    left = 40
    right = width - 15
    top = 15
    bottom = height - 30

    # Grid
    for i in range(6):

        y = bottom - (
            (bottom - top) * i / 5
        )

        saline_graph.create_line(
            left,
            y,
            right,
            y,
            fill=GRID
        )

        value = i * 20

        saline_graph.create_text(
            25,
            y,
            text=str(value),
            fill=MUTED,
            font=("Arial", 8)
        )

    if len(saline_history) < 2:
        return

    points = []

    for i, value in enumerate(saline_history):

        x = left + (
            (right - left)
            * i
            /
            max(1, len(saline_history) - 1)
        )

        y = bottom - (
            (bottom - top)
            * value
            /
            100
        )

        points.extend([x, y])

    saline_graph.create_line(
        points,
        fill=CYAN,
        width=3,
        smooth=True
    )

    # Current point
    if len(points) >= 2:

        x = points[-2]
        y = points[-1]

        saline_graph.create_oval(
            x - 5,
            y - 5,
            x + 5,
            y + 5,
            fill=CYAN,
            outline=""
        )


# ==========================================
# DRAW DISTANCE GRAPH
# ==========================================

def draw_distance_graph():

    distance_graph.delete("all")

    width = distance_graph.winfo_width()
    height = distance_graph.winfo_height()

    if width <= 20 or height <= 20:
        return

    left = 40
    right = width - 15
    top = 15
    bottom = height - 30

    if len(distance_history) < 2:
        return

    minimum = min(distance_history)
    maximum = max(distance_history)

    if maximum == minimum:
        maximum += 1
        minimum -= 1

    # Grid
    for i in range(5):

        y = top + (
            (bottom - top) * i / 4
        )

        distance_graph.create_line(
            left,
            y,
            right,
            y,
            fill=GRID
        )

    distance_graph.create_text(
        25,
        top,
        text=f"{maximum:.0f}",
        fill=MUTED,
        font=("Arial", 8)
    )

    distance_graph.create_text(
        25,
        bottom,
        text=f"{minimum:.0f}",
        fill=MUTED,
        font=("Arial", 8)
    )

    points = []

    for i, value in enumerate(distance_history):

        x = left + (
            (right - left)
            * i
            /
            max(1, len(distance_history) - 1)
        )

        y = bottom - (
            (bottom - top)
            *
            (value - minimum)
            /
            (maximum - minimum)
        )

        points.extend([x, y])

    distance_graph.create_line(
        points,
        fill=GREEN,
        width=3,
        smooth=True
    )

    if len(points) >= 2:

        x = points[-2]
        y = points[-1]

        distance_graph.create_oval(
            x - 5,
            y - 5,
            x + 5,
            y + 5,
            fill=GREEN,
            outline=""
        )


# ==========================================
# UPDATE GRAPHS
# ==========================================

def refresh_graphs():

    draw_saline_graph()

    draw_distance_graph()

    root.after(
        500,
        refresh_graphs
    )


# ==========================================
# UPDATE UI
# ==========================================

def update_ui(saline, distance):

    saline_value.config(
        text=f"{saline:.0f}%"
    )

    distance_value.config(
        text=f"{distance:.1f} cm"
    )

    # Store graph data
    saline_history.append(saline)
    distance_history.append(distance)

    update_progress(saline)

    if saline > 50:

        status_value.config(
            text="NORMAL",
            fg=GREEN
        )

    elif saline > 20:

        status_value.config(
            text="WARNING",
            fg=YELLOW
        )

    else:

        status_value.config(
            text="CRITICAL",
            fg=RED
        )


# ==========================================
# READ ARDUINO SERIAL DATA
# ==========================================

def read_serial():

    while True:

        if ser is None:

            time.sleep(1)

            continue

        try:

            data = ser.readline().decode(
                "utf-8"
            ).strip()

            if not data:
                continue

            distance = float(data)

            saline = calculate_saline(
                distance
            )

            root.after(
                0,
                update_ui,
                saline,
                distance
            )

        except Exception as e:

            print(
                "Serial Error:",
                e
            )

            time.sleep(1)


# ==========================================
# LIVE INDICATOR ANIMATION
# ==========================================

def animate_live():

    current_color = live_dot.cget("fg")

    if current_color == GREEN:
        live_dot.config(fg="#14532D")
    else:
        live_dot.config(fg=GREEN)

    root.after(
        700,
        animate_live
    )


# ==========================================
# START SERIAL THREAD
# ==========================================

if ser:

    serial_thread = threading.Thread(
        target=read_serial,
        daemon=True
    )

    serial_thread.start()


# ==========================================
# START UI ANIMATIONS
# ==========================================

root.after(
    500,
    refresh_graphs
)

root.after(
    700,
    animate_live
)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()


# ==========================================
# CLOSE SERIAL
# ==========================================

if ser:

    ser.close()

