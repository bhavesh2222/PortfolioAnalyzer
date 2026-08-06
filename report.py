from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class Report:

    @staticmethod
    def export_pdf(rows, summary):

        doc = SimpleDocTemplate("Portfolio_Report.pdf")

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph("Portfolio Analysis Report", styles["Title"])
        )

        data = [[
            "Ticker",
            "Company",
            "Qty",
            "Buy",
            "Current",
            "Profit",
            "Return %"
        ]]

        for row in rows:

            data.append([
                row["ticker"],
                row["company"],
                row["quantity"],
                f"${row['buy_price']:.2f}",
                f"${row['current_price']:.2f}",
                f"${row['profit']:.2f}",
                f"{row['return_percent']:.2f}%"
            ])

        table = Table(data)

        table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("ALIGN", (0, 0), (-1, -1), "CENTER")

        ]))

        elements.append(table)

        elements.append(
            Paragraph("<br/><br/>", styles["Normal"])
        )

        elements.append(
            Paragraph(
                f"<b>Total Investment:</b> ${summary['investment']:.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Current Value:</b> ${summary['current_value']:.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Total Profit:</b> ${summary['profit']:.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Overall Return:</b> {summary['return']:.2f}%",
                styles["Normal"]
            )
        )

        doc.build(elements)

        print("\nPortfolio_Report.pdf created successfully!")