from flask import Flask, render_template, request, send_file, redirect, url_for
from rembg import remove
import os
from io import BytesIO

app = Flask(__name__)

# Ensure the folder exists for saving images temporarily
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            # Read the file and remove the background
            input_image = file.read()
            output_image = remove(input_image)

            # Save the processed image to a temporary location
            filename = file.filename
            output_path = os.path.join('static/uploads', filename)
            with open(output_path, "wb") as f:
                f.write(output_image)

            # Return the file path for the preview
            return render_template("index.html", preview_image=filename)

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    # Provide the processed image for download
    return send_file(os.path.join('static/uploads', filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
