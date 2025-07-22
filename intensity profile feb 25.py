import cv2
import numpy as np
import os
import csv
from datetime import datetime
from tkinter import Tk, Button, Frame, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit

# Calibration factor (fs/pixel)
CALIBRATION_FACTOR = 0.00373

# Camera setup
width, height, frame_rate = 1280, 720, 15
camera_index = 2  # Change if needed
vid_capture = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
vid_capture.set(3, width)
vid_capture.set(4, height)

# Recording setup
is_recording = False
output_dir = None
output_video = None
frame_dir = None
plots_dir = None
csv_file = None
frame_count = 0
update_after_id = None

# Tkinter setup
root = Tk()
root.title("Intensity Profile Analysis")
root.geometry("1360x800")  # Adjust window size

# Matplotlib figure for live intensity profile
fig, ax = plt.subplots(figsize=(6, 4))
line, = ax.plot([], [], lw=2)  # Line object for the intensity profile
fwhm_text = ax.text(0.5, 0.9, '', transform=ax.transAxes, fontsize=10, ha='center', color='red')
ax.set_xlim(0, width)
ax.set_ylim(0, 255)
ax.set_xlabel("Horizontal Pixel Position")
ax.set_ylabel("Intensity")
ax.set_title("Live Intensity Profile")

# Embed Matplotlib plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side="top", fill="both", expand=True)

# Intensity profile smoothing
def extract_intensity_profile(frame):
    center_row = frame.shape[0] // 2
    row_range = 20  # Number of rows to average
    channel_data = frame[:, :, 0]  # Extract Blue channel
    intensity_profile = np.mean(channel_data[center_row - row_range:center_row + row_range, :], axis=0)
    return gaussian_filter(intensity_profile, sigma=2)

# Create timestamped recording folder
def create_recording_folder():
    global output_dir, frame_dir, plots_dir, csv_file
    base_dir = filedialog.askdirectory(title="Select Save Directory")
    if not base_dir:
        print("No directory selected.")
        return None
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(base_dir, timestamp)
    frame_dir = os.path.join(output_dir, "Frames")
    plots_dir = os.path.join(output_dir, "Plots")
    os.makedirs(frame_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)
    csv_file = os.path.join(output_dir, "intensity_data.csv")
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "FWHM (px)", "Pulse Duration (fs)", "Peak Intensity"])
    return output_dir

# Gaussian fitting and data saving
def analyze_and_save_data(frame, frame_number):
    intensity_profile = extract_intensity_profile(frame)
    x_data = np.arange(len(intensity_profile))
    initial_guess = [intensity_profile.max(), len(intensity_profile) / 2, 10]
    try:
        popt, _ = curve_fit(lambda x, a, x0, sigma: a * np.exp(-(x - x0)**2 / (2 * sigma**2)), x_data, intensity_profile, p0=initial_guess)
        sigma_fit = popt[2]
        fwhm_pixels = 2 * np.sqrt(2 * np.log(2)) * sigma_fit
        pulse_duration = fwhm_pixels * CALIBRATION_FACTOR
        peak_intensity = popt[0]
        
        # Save data to CSV
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([frame_number, fwhm_pixels, pulse_duration, peak_intensity])
        
        # Save plot
        plt.figure()
        plt.plot(x_data, intensity_profile, label="Intensity Profile")
        plt.plot(x_data, popt[0] * np.exp(-(x_data - popt[1])**2 / (2 * sigma_fit**2)), label=f"Gaussian Fit (FWHM: {fwhm_pixels:.2f}px, Duration: {pulse_duration:.2f} fs)", linestyle="--", color="red")
        plt.xlabel("Pixel Position")
        plt.ylabel("Intensity")
        plt.title(f"Frame {frame_number} - Intensity Profile")
        plt.legend()
        plt.savefig(os.path.join(plots_dir, f"frame_{frame_number:05d}.png"))
        plt.close()
    except Exception as e:
        print(f"Error processing frame {frame_number}: {e}")

# Start/Stop recording
def toggle_recording():
    global is_recording, output_video, frame_count, output_dir
    if not is_recording:
        output_dir = create_recording_folder()
        if not output_dir:
            return
        video_file = os.path.join(output_dir, "Recorded_Video.mp4")
        output_video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))
        is_recording = True
        frame_count = 0
        print("Recording started.")
    else:
        is_recording = False
        if output_video:
            output_video.release()
            output_video = None
        print("Recording stopped.")

# Extract data from current frame
def extract_data():
    if not output_dir:
        print("No recording directory found. Start recording first.")
        return
    ret, frame = vid_capture.read()
    if ret:
        analyze_and_save_data(frame, frame_count)
        print("Data extracted and saved.")

# Update function
def update():
    global frame_count
    ret, frame = vid_capture.read()
    if not ret:
        return
    intensity_profile = extract_intensity_profile(frame)
    line.set_data(np.arange(len(intensity_profile)), intensity_profile)
    canvas.draw()
    cv2.imshow("Camera Feed", frame)
    if is_recording and output_video:
        output_video.write(frame)
        frame_path = os.path.join(frame_dir, f"frame_{frame_count:05d}.jpg")
        cv2.imwrite(frame_path, frame)
        analyze_and_save_data(frame, frame_count)
        frame_count += 1
    root.after(50, update)

# Exit function
def exit_program():
    vid_capture.release()
    cv2.destroyAllWindows()
    root.destroy()

# Toolbar buttons
toolbar = Frame(root)
toolbar.pack(side="bottom", fill="x")
Button(toolbar, text="Start/Stop Recording", command=toggle_recording, bg="green", fg="white").pack(side="left", padx=10, pady=5)
Button(toolbar, text="Extract Data", command=extract_data, bg="blue", fg="white").pack(side="left", padx=10, pady=5)
Button(toolbar, text="Exit", command=exit_program, bg="red", fg="white").pack(side="left", padx=10, pady=5)

# Start updating
update()
root.mainloop()
