from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date

class BusinessProfile(BaseModel):
    legal_name: str
    ein: str
    state: str
    address: str
    naics_code: Optional[str] = None
    accounting_method: str = Field(default="Cash")  # Cash or Accrual
    tax_year_start: date
    tax_year_end: date

class BalanceSheetLine(BaseModel):
    label: str
    amount: float = 0.0
    category: str  # "current_asset", "noncurrent_asset", "current_liability", "noncurrent_liability", "equity"

class BalanceSheet(BaseModel):
    business: BusinessProfile
    as_of: date
    lines: List[BalanceSheetLine]

    @property
    def total_assets(self) -> float:
        return sum(l.amount for l in self.lines if "asset" in l.category)

    @property
    def total_liabilities(self) -> float:
        return sum(l.amount for l in self.lines if "liability" in l.category)

    @property
    def total_equity(self) -> float:
        return sum(l.amount for l in self.lines if l.category == "equity")

    @property
    def is_balanced(self) -> bool:
        return round(self.total_assets, 2) == round(self.total_liabilities + self.total_equity, 2)

class IncomeStatementLine(BaseModel):
    label: str
    amount: float
    category: str  # "revenue" or "expense"

class IncomeStatement(BaseModel):
    business: BusinessProfile
    period_start: date
    period_end: date
    lines: List[IncomeStatementLine]

    @property
    def total_revenue(self) -> float:
        return sum(l.amount for l in self.lines if l.category == "revenue")

    @property
    def total_expenses(self) -> float:
        return sum(l.amount for l in self.lines if l.category == "expense")

    @property
    def net_income(self) -> float:
        return self.total_revenue - self.total_expenses

class CashFlowSection(BaseModel):
    label: str
    amount: float

class CashFlowStatement(BaseModel):
    business: BusinessProfile
    period_start: date
    period_end: date
    operating: List[CashFlowSection] = []
    investing: List[CashFlowSection] = []
    financing: List[CashFlowSection] = []

    @property
    def net_cash_operating(self) -> float:
        return sum(s.amount for s in self.operating)

    @property
    def net_cash_investing(self) -> float:
        return sum(s.amount for s in self.investing)

    @property
    def net_cash_financing(self) -> float:
        return sum(s.amount for s in self.financing)

    @property
    def net_change_in_cash(self) -> float:
        return self.net_cash_operating + self.net_cash_investing + self.net_cash_financing
