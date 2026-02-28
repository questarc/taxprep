from __future__ import annotations
from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from . import storage
from core.models import BalanceSheet, IncomeStatement, CashFlowStatement

def _draw_header(c: canvas.Canvas, title: str, y: int = 760) -> int:
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, title)
    return y - 30

def balance_sheet_pdf(bs: BalanceSheet) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    y = _draw_header(c, f"Balance Sheet - {bs.business.legal_name}")
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"As of: {bs.as_of.isoformat()}")
    y -= 20
    for line in bs.lines:
        c.drawString(40, y, f"{line.label}")
        c.drawRightString(550, y, f"{line.amount:,.2f}")
        y -= 15
        if y < 60:
            c.showPage()
            y = 760
    y -= 20
    c.drawString(40, y, f"Total Assets: {bs.total_assets:,.2f}")
    y -= 15
    c.drawString(40, y, f"Total Liabilities: {bs.total_liabilities:,.2f}")
    y -= 15
    c.drawString(40, y, f"Total Equity: {bs.total_equity:,.2f}")
    c.showPage()
    c.save()
    return buffer.getvalue()

def income_statement_pdf(is_stmt: IncomeStatement) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    y = _draw_header(c, f"Income Statement - {is_stmt.business.legal_name}")
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Period: {is_stmt.period_start.isoformat()} to {is_stmt.period_end.isoformat()}")
    y -= 20
    c.drawString(40, y, "Revenue")
    y -= 15
    for line in is_stmt.lines:
        if line.category != "revenue":
            continue
        c.drawString(60, y, line.label)
        c.drawRightString(550, y, f"{line.amount:,.2f}")
        y -= 15
    y -= 10
    c.drawString(40, y, "Expenses")
    y -= 15
    for line in is_stmt.lines:
        if line.category != "expense":
            continue
        c.drawString(60, y, line.label)
        c.drawRightString(550, y, f"{line.amount:,.2f}")
        y -= 15
    y -= 20
    c.drawString(40, y, f"Net Income: {is_stmt.net_income:,.2f}")
    c.showPage()
    c.save()
    return buffer.getvalue()

def cash_flow_pdf(cf: CashFlowStatement) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    y = _draw_header(c, f"Cash Flow Statement - {cf.business.legal_name}")
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Period: {cf.period_start.isoformat()} to {cf.period_end.isoformat()}")
    y -= 20

    def section(title: str, items, total: float, y: int) -> int:
        c.drawString(40, y, title)
        y -= 15
        for s in items:
            c.drawString(60, y, s.label)
            c.drawRightString(550, y, f"{s.amount:,.2f}")
            y -= 15
        y -= 10
        c.drawString(60, y, f"Net {title}: {total:,.2f}")
        return y - 25

    y = section("Operating Activities", cf.operating, cf.net_cash_operating, y)
    y = section("Investing Activities", cf.investing, cf.net_cash_investing, y)
    y = section("Financing Activities", cf.financing, cf.net_cash_financing, y)
    c.drawString(40, y, f"Net Change in Cash: {cf.net_change_in_cash:,.2f}")
    c.showPage()
    c.save()
    return buffer.getvalue()
