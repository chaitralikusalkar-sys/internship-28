from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.sql import func

from database import Base


class InitialBalance(Base):
    __tablename__ = "initial_balance"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(DECIMAL(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    expense_for = Column(String(100))
    amount = Column(DECIMAL(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SavingGoal(Base):
    __tablename__ = "saving_goals"

    id = Column(Integer, primary_key=True, index=True)
    monthly_goal = Column(DECIMAL(10, 2))
    weekly_goal = Column(DECIMAL(10, 2))
    daily_goal = Column(DECIMAL(10, 2))