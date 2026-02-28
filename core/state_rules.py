from __future__ import annotations
from typing import Dict, List
from .models import BusinessProfile, BalanceSheet, IncomeStatement, CashFlowStatement

class StateRequirement:
    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description

STATE_RULES: Dict[str, List[StateRequirement]] = {
    "MA": [
        StateRequirement("MA-LLC-1", "Confirm Massachusetts annual report filed."),
        StateRequirement("MA-LLC-2", "Capture Massachusetts estimated tax payments for the year."),
    ],
    "CA": [
        StateRequirement("CA-LLC-1", "Include CA LLC franchise fee and LLC gross receipts fee if applicable."),
    ],
    # Extend for other states…
}

def get_state_requirements(state: str) -> List[StateRequirement]:
    return STATE_RULES.get(state.upper(), [])

def validate_state_compliance(
    profile: BusinessProfile,
    bs: BalanceSheet | None,
    is_stmt: IncomeStatement | None,
    cf: CashFlowStatement | None,
) -> List[str]:
    # Placeholder for richer validation logic
    messages: List[str] = []
    for req in get_state_requirements(profile.state):
        messages.append(f"[{req.code}] {req.description}")
    return messages
