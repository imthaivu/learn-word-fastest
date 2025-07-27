from fpdf import FPDF

def txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            pdf.multi_cell(0, 10, txt=line.strip())

    pdf.output(pdf_path)

# Dùng ví dụ:
txt_to_pdf("input.txt", "output.pdf")
