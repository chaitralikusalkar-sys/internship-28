from pydantic import BaseModel
from datetime import datetime


# ---------- Initial Balance ----------

class BalanceCreate(BaseModel):
    total_amount: float


class BalanceResponse(BalanceCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Expenses ----------

class ExpenseCreate(BaseModel):
    expense_for: str
    amount: float


class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Saving Goals ----------

class GoalCreate(BaseModel):
    monthly_goal: float
    weekly_goal: float
    daily_goal: float


class GoalResponse(GoalCreate):
    id: int

    class Config:
        from_attributes = True