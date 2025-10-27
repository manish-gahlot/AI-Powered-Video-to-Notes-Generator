# utils/pdf_utils.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

def create_pdf_from_notes(title: str, notes_text: str, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    flow = []

    title_style = styles["Title"]
    normal = styles["Normal"]
    bullet_style = ParagraphStyle('bullet', parent=normal, leftIndent=12, firstLineIndent=-6)
    small = ParagraphStyle('small', parent=normal, fontSize=10)

    flow.append(Paragraph(title, title_style))
    flow.append(Spacer(1, 6))

    # Break notes_text into paragraphs by blank lines
    parts = notes_text.split("\n\n")
    for p in parts:
        # try to detect bullets starting with "-" or "*"
        lines = p.splitlines()
        if all(line.strip().startswith("-") or line.strip().startswith("*") for line in lines if line.strip()):
            # multiple bullets
            for line in lines:
                if line.strip():
                    flow.append(Paragraph(line.strip().lstrip("-* ").strip(), bullet_style))
            flow.append(Spacer(1,6))
        else:
            flow.append(Paragraph(p.replace("\n", "<br/>"), normal))
            flow.append(Spacer(1,6))

    doc.build(flow)
    return output_path
