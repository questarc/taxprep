from __future__ import annotations
from .models import BalanceSheet, IncomeStatement, CashFlowStatement

def compute_retained_earnings(is_stmt: IncomeStatement) -> float:
    # For now, assume retained earnings = net income (no prior-year RE tracking)
    return is_stmt.net_income

def sync_equity_with_income(bs: BalanceSheet, is_stmt: IncomeStatement) -> BalanceSheet:
    retained = compute_retained_earnings(is_stmt)
    # naive: add/update a "Retained Earnings" equity line
    found = False
    for line in bs.lines:
        if line.label.lower() == "retained earnings":
            line.amount = retained
            found = True
            break
    if not found:
        from .models import BalanceSheetLine
        bs.lines.append(
            BalanceSheetLine(label="Retained Earnings", amount=retained, category="equity")
        )
    return bs
