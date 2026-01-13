# Automated Least-Squares Solutions Finder

## Installation

### Option A: Simple Installation (Recommended)

This is the fastest way to get the application running without any technical setup.

#### macOS

1. **Download & Open**
   Download the `.dmg` file from the provided drive or the GitHub Releases section, then double-click to open it.
2. **Install**
   When the window appears, drag the app icon into the **Applications** folder.
3. **Launch**
   Open **Applications** and double-click the app to start.

> **Note:**
> If you see *“Apple could not verify Least Squares Solver is free of malware”*:
> Go to **System Settings → Privacy & Security**, scroll down, and click **Open Anyway**.

#### Windows

1. **Download & Open**
   Download the `.exe` file from the provided drive or the GitHub Releases section.
2. **Launch**
   Double-click the file to run the application.

---

### Option B: Run from Source Code

Follow these steps if you want to run the application using Python and the raw source files.

#### 1. Prerequisites

Ensure you have **Python 3.x** installed:

```
python3 --version
```

#### 2. System Dependency (Tcl/Tk)

The GUI is built using **Tkinter**, which requires Tcl/Tk.

* **macOS**:

```
brew install tcl-tk
```

* **Windows/Linux**:
  Usually included with Python. If the app fails to open, reinstall Python and ensure **“tcl/tk and IDLE”** is checked.

#### 3. Environment Setup

It is recommended to use a virtual environment.

Create the environment:

```
python3 -m venv venv
```

Activate the environment:

* **macOS/Linux**:

```
source venv/bin/activate
```

* **Windows**:

```
.\venv\Scripts\activate
```

#### 4. Install Libraries

With the virtual environment active:

```
pip install -r requirements.txt
```

> **Note:**
> This installs **NumPy** and **tkmacosx** (for macOS button styling).

#### 5. Launch

Run the main script:

```
python3 main.py
```

---

## Getting Started

### Launch the Application

Choose an input mode:

* **Linear System Mode**
  Displays equations with variables and operators (e.g., `x₁ + x₂ = b`).

* **Augmented Matrix Mode**
  Displays a clean grid for entering raw coefficients, visually separating matrix **A** and vector **b**.

---

## How to Use the Solver

### Step 1: Define Dimensions

* Enter the **Number of Equations (m)** – number of rows
* Enter the **Number of Unknowns (n)** – number of variables (columns of matrix **A**)
* Click **Confirm Size**

> **Note:**
> If you enter dimensions larger than **5×5**, a warning prompt will appear asking you to confirm proceeding.

### Step 2: Input Data

After the grid appears, enter numeric values:

* **Coefficient Matrix (A)**: dark gray boxes
* **Constant Vector (b)**: dark blue boxes on the far right

### Step 3: Solve

Click the **Solve** button at the bottom of the window.

---

## Interpreting Results

After clicking **Solve**, the application displays:

* **Least Squares Solution Vector**
  The calculated ( \hat{x} ) values minimizing the sum of squared residuals.
* **Least Squares Error**
  The residual norm. An error of `0.000000` indicates a consistent system with an exact solution.

---

## Errors and Warnings

* **Input Error**
  Occurs if a field is empty or contains non-numeric characters.
* **Solver Error**
  May occur if matrix **A** is singular or if there is an issue in `solver.py`.
* **Grid Overlap Warning**
  For large matrices (m, n ≥ 5), you must manually confirm by clicking **Yes**.
