# 🖊️ Math Solver Web App

A **Flask web application** that allows users to draw mathematical expressions and equations on a canvas. The app uses **Tesseract OCR** to extract text from the image and **SymPy** to solve equations or evaluate arithmetic expressions.

---

## 🧩 Features

- Draw equations on a canvas.  
- Preprocesses the image for better OCR accuracy:
  - Grayscale conversion  
  - Upscaling  
  - Contrast enhancement  
  - Binarization  
- Supports **arithmetic expressions** and **algebraic equations**.  
- Cleans OCR output and inserts missing operators (e.g., `2x → 2*x`).  
- Solves equations and expressions using **SymPy**.  
- Returns **numeric results or symbolic solutions**.  

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML5, Canvas, JavaScript  
- **OCR:** Tesseract OCR  
- **Math Solver:** SymPy  
- **Libraries:** Pillow, pytesseract, sympy, requests  

---

## Screenshots
<img width="1899" height="853" alt="image" src="https://github.com/user-attachments/assets/a9b95c6e-0600-4e54-89e0-f1ee29c6198d" />
<img width="1867" height="850" alt="image" src="https://github.com/user-attachments/assets/29d3ab77-c206-4461-9a7b-bc35c6e08486" />


---

## ⚡ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/math-solver-webapp.git
cd math-solver-webapp


