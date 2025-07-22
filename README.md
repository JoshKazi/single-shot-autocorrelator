# Single-Shot Autocorrelator for Ultrafast Laser Diagnostics

This project implements a real-time, single-shot autocorrelator (SSA) to characterize femtosecond laser pulses using noncollinear second-harmonic generation (SHG) in a nonlinear BBO crystal. It integrates a CCD camera, Python-based data acquisition, and real-time Gaussian fitting to extract pulse durations with sub-100 fs resolution.

---

## 📄 Project Overview

- **Field**: Ultrafast optics, femtosecond metrology
- **Pulse Measurement Method**: Spatial SHG fringe analysis
- **Software Stack**: Python, OpenCV, SciPy, Matplotlib, Tkinter
- **Hardware**: BBO crystal, CCD camera, optical delay stage, beam splitter, grating compressor

---

## 🔬 How It Works

1. A femtosecond pulse is split into two replicas via a beam splitter.
2. The two beams are directed to intersect at a nonlinear crystal (BBO).
3. When spatially and temporally overlapped, they generate a second-harmonic fringe pattern.
4. A CCD camera captures the SHG signal.
5. A Python script processes the intensity profile, fits a Gaussian curve, and calculates the full width at half maximum (FWHM) in femtoseconds.

---

## ⚙️ Calibration & Results

### ✅ Updated Calibration

- Delay Stage Movement: 19 × 20 µm = **380 µm**, doubled = **760 µm**
- Pixel Displacement: ~640 pixels
- 1 µm of light travel = **3.33 fs**
- ➤ **Calibration Factor** = `3.95 fs/pixel`

### 📉 Pulse Duration Observations

| Condition                      | Result         |
|-------------------------------|----------------|
| Before grating optimization   | ~746 fs        |
| After motor adjustment (5585 → 4886) | Much narrower spatial fringe and reduced pulse width |
| Expected benchmark            | ~30 fs         |

---

## 💡 Autocorrelation Notes

- The spatial SHG fringe should be **symmetric**. Any **asymmetry** indicates **stray light interference**.
- SHG is a second-order nonlinear process: \( \omega + \omega = 2\omega \), conserving energy.
- Temporal FWHM is extracted from spatial FWHM using Gaussian fit and the calibration factor.

---

## 🛠 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
