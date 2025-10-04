from flask import Flask, render_template, request, jsonify
import base64
import io
from PIL import Image, ImageOps
import sympy as sp
import shutil
import pytesseract
import os
import re

app = Flask(__name__)

# Detect Tesseract OCR

def detect_tesseract():
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    path_in_env = shutil.which("tesseract")
    if path_in_env:
        return path_in_env
    return None

TESSERACT_PATH = detect_tesseract()
if TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    print("⚠️ Warning: Tesseract OCR not found. Install it to enable OCR functionality.")

# Clean and normalize OCR text

def clean_expression(text):
    text = text.replace(" ", "").replace("\n", "")
    replacements = {
        '−': '-', '×': '*', '÷': '/', '^': '**',
        '|': '1', 'I': '1', 'l': '1',
        'O': '0', 'o': '0', '—': '-', '–': '-'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Allow only valid chars
    text = re.sub(r"[^0-9a-zA-Z\+\-\*/\(\)\.=]", "", text)

    # Insert missing '*' between:
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)   # 2x → 2*x
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)   # x2 → x*2
    text = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', text)  # xy → x*y
    text = re.sub(r'\)(\d)', r')*\1', text)             # )(2 → )*2
    text = re.sub(r'\)([a-zA-Z])', r')*\1', text)       # )(x → )*x

    return text


# Routes

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    if not TESSERACT_PATH:
        return jsonify({
            "expression": "",
            "result": "Tesseract OCR is not installed or not found. Please install it."
        })

    try:
        data = request.json.get("image", "")
        if not data:
            return jsonify({"expression": "", "result": "No image received"})

        # Decode image
        image_data = base64.b64decode(data.split(",")[1])
        image = Image.open(io.BytesIO(image_data))

        # Preprocess image
        image = ImageOps.grayscale(image)
        image = image.resize((image.width * 3, image.height * 3))  # upscale for better OCR
        image = ImageOps.autocontrast(image)
        image = image.point(lambda p: 255 if p > 180 else 0)  # binarize (pure black-white)

        # OCR extraction
        extracted_text = pytesseract.image_to_string(
            image,
            config="--psm 6 -c tessedit_char_whitelist=0123456789+-*/().=xyzXYZ^"
        )

        print("Extracted text:", extracted_text)
        cleaned_expr = clean_expression(extracted_text)
        print("Cleaned expression:", cleaned_expr)

        if not cleaned_expr:
            return jsonify({"expression": "", "result": "Could not detect valid expression"})

        
        # Detect and Solve
        
        if '=' in cleaned_expr:
            try:
                lhs, rhs = cleaned_expr.split('=')
                lhs = sp.sympify(lhs)
                rhs = sp.sympify(rhs)

                # Detect variables dynamically
                symbols = list(lhs.free_symbols.union(rhs.free_symbols))
                if not symbols:
                    symbols = sp.symbols('x')

                equation = sp.Eq(lhs, rhs)
                solutions = sp.solve(equation, symbols)
                result = f"Solutions: {solutions}"
            except Exception as e:
                result = f"Could not solve equation: {e}"

        else:
            try:
                expr = sp.sympify(cleaned_expr)
                result = expr.evalf()
            except Exception:
                result = "Invalid expression"

        return jsonify({
            "expression": cleaned_expr,
            "result": str(result)
        })

    except Exception as e:
        print("Server error:", e)
        return jsonify({"expression": "", "result": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
