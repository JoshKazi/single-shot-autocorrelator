# 📡 Single-Shot Autocorrelator for Ultrafast Laser Diagnostics  

This repository contains the software and analysis pipeline developed for my undergraduate thesis,  
**“Single-Shot Autocorrelator Design and Analysis for Ultrafast Laser Diagnostics”** (University of Waterloo, 2024).  

The project combines **experimental physics** and **software engineering** to measure femtosecond laser pulses in real time using:  
- Python-based data acquisition and signal processing  
- Gaussian curve fitting and calibration  
- Real-time visualization with Tkinter + Matplotlib  
- Automated data logging and reproducible analysis  

---

## 📄 Project Overview  

- **Field**: Ultrafast optics, signal processing, experimental physics  
- **Method**: Single-shot autocorrelation via noncollinear second-harmonic generation (SHG)  
- **Software Stack**: Python, OpenCV, NumPy, SciPy, Matplotlib, Tkinter  
- **Hardware**: BBO crystal, CCD camera, optical delay stage, beam splitter, grating compressor  

---

## 🔬 How It Works  

1. A femtosecond laser pulse is split into two replicas via a beam splitter.  
2. The beams overlap in a nonlinear BBO crystal, generating a **second-harmonic fringe pattern**.  
3. A CCD camera captures the SHG fringe in real time.  
4. The Python script:  
   - Extracts intensity profiles  
   - Applies Gaussian smoothing  
   - Fits a Gaussian curve to determine spatial FWHM  
5. Using a calibrated conversion factor, the spatial FWHM is converted into pulse duration (fs).  

---

## ⚙️ Calibration & Results  

### ✅ Temporal Calibration  

- Delay stage displacement: **380 µm**, doubled optical path = **760 µm**  
- Pixel shift observed: **640 px**  
- Conversion: 1 µm ↔ **3.33 fs**  
- ➤ **Calibration Factor** = `3.95 fs/pixel`  

### 📉 Pulse Duration Measurements  

| Condition                     | Result          |
|-------------------------------|-----------------|
| Initial measurement           | ~1.21 ps        |
| After compressor optimization | **90.75 fs**    |
| Expected benchmark            | ~30 fs          |  

---

## 💡 Key Insights  

- SHG fringe symmetry is essential; asymmetry often indicates **stray light or misalignment**.  
- Gaussian fitting provides robust and reproducible pulse width extraction.  
- Automated pipelines save **frames, plots, and CSV logs** for reproducibility and collaboration.  

---

## 🛠 Requirements  

Install dependencies with:  

```bash
pip install -r requirements.txt
