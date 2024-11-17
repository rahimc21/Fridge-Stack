from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import cv2
from pytesseract import image_to_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create an uploads folder if it doesn't exist


# Stack class to handle items and expiration dates
class ExpirationStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        if not isinstance(item['expiration_date'], datetime):
            raise ValueError("expiration_date must be a datetime object")
        inserted = False
        for i in range(len(self.stack)):
            if item['expiration_date'] < self.stack[i]['expiration_date']:
                self.stack.insert(i, item)
                inserted = True
                break
        if not inserted:
            self.stack.append(item)

    def get_stack(self):
        return self.stack


stack = ExpirationStack()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        expiration_date_str = request.form["expiration_date"]
        try:
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")
            stack.push({"name": name, "expiration_date": expiration_date})
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        return redirect(url_for("home"))

    return render_template("index.html", stack=stack.get_stack())


@app.route("/extract-text", methods=["GET", "POST"])
def extract_text():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in the request"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if file:
            # Save the file to the uploads folder
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Perform OCR on the image
            image = cv2.imread(file_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
            cv2.imwrite(f"{UPLOAD_FOLDER}/preprocessed_{file.filename}", thresh_image)
            extracted_text = image_to_string(thresh_image)

            return render_template("extract_text.html", text=extracted_text)

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
