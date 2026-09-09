from datetime import datetime

from fpdf import FPDF


class NewsPDF(FPDF):

    def header(self):

        self.set_font(
            "Helvetica",
            "B",
            16
        )

        self.cell(
            0,
            10,
            "AI News Research Digest",
            ln=True,
            align="C"
        )

        self.ln(5)


    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "I",
            8
        )

        self.cell(
            0,
            10,
            f"Page {self.page_no()}",
            align="C"
        )


def generate_pdf(
    topic,
    report
):
    """
    Generate a PDF version of the
    AI news report.
    """

    pdf = NewsPDF()


    pdf.set_auto_page_break(
        auto=True,
        margin=20
    )


    pdf.add_page()


    # ========================================================
    # TITLE
    # ========================================================

    pdf.set_font(
        "Helvetica",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        f"Topic: {topic}",
        ln=True
    )


    # ========================================================
    # DATE
    # ========================================================

    pdf.set_font(
        "Helvetica",
        size=10
    )

    pdf.cell(
        0,
        8,
        "Generated: "
        + datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
        ln=True
    )


    pdf.ln(5)


    # ========================================================
    # REPORT
    # ========================================================

    pdf.set_font(
        "Helvetica",
        size=10
    )


    safe_report = (
        report
        .encode(
            "latin-1",
            "replace"
        )
        .decode(
            "latin-1"
        )
    )


    pdf.multi_cell(
        0,
        7,
        safe_report
    )


    return bytes(
        pdf.output()
    )