from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

app = Flask(__name__)
OUTPUT = Path("generated_document.pdf")

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        document_type = request.form.get("document_type", "Legal Document")
        name = request.form.get("name", "")
        details = request.form.get("details", "")

        c = canvas.Canvas(str(OUTPUT), pagesize=A4)
        width, height = A4
        y = height - 70
        c.setFont("Helvetica-Bold", 18)
        c.drawString(60, y, "LegalEase - AI-Powered Legal Document")
        y -= 45
        c.setFont("Helvetica-Bold", 13)
        c.drawString(60, y, document_type)
        y -= 35
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"Name: {name}")
        y -= 25

        for line in details.splitlines():
            if y < 70:
                c.showPage()
                y = height - 70
                c.setFont("Helvetica", 11)
            c.drawString(60, y, line[:100])
            y -= 20

        y -= 20
        c.drawString(60, y, "Generated using LegalEase. This is a sample document and")
        y -= 18
        c.drawString(60, y, "should be reviewed by a qualified legal professional.")
        c.save()
        message = "Document generated successfully."

    return render_template("index.html", message=message)

@app.route("/download")
def download():
    return send_file(OUTPUT, as_attachment=True, download_name="LegalEase_Document.pdf")

if __name__ == "__main__":
    app.run(debug=True)
