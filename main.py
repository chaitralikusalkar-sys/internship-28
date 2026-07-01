from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Daily Expense Tracker")


# ===========================
# Initial Balance APIs
# ===========================

@app.post("/balance", response_model=schemas.BalanceResponse)
def create_balance(balance: schemas.BalanceCreate, db: Session = Depends(get_db)):
    new_balance = models.InitialBalance(total_amount=balance.total_amount)
    db.add(new_balance)
    db.commit()
    db.refresh(new_balance)
    return new_balance


@app.get("/balance", response_model=list[schemas.BalanceResponse])
def get_balance(db: Session = Depends(get_db)):
    return db.query(models.InitialBalance).all()


@app.put("/balance/{id}", response_model=schemas.BalanceResponse)
def update_balance(id: int, balance: schemas.BalanceCreate, db: Session = Depends(get_db)):
    bal = db.query(models.InitialBalance).filter(models.InitialBalance.id == id).first()

    if not bal:
        raise HTTPException(status_code=404, detail="Balance not found")

    bal.total_amount = balance.total_amount
    db.commit()
    db.refresh(bal)

    return bal


# ===========================
# Expense APIs
# ===========================

@app.post("/expenses", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = models.Expense(
        expense_for=expense.expense_for,
        amount=expense.amount
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()


@app.get("/expenses/{id}", response_model=schemas.ExpenseResponse)
def get_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@app.put("/expenses/{id}", response_model=schemas.ExpenseResponse)
def update_expense(id: int, data: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.expense_for = data.expense_for
    expense.amount = data.amount

    db.commit()
    db.refresh(expense)

    return expense


@app.delete("/expenses/{id}")
def delete_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


# ===========================
# Saving Goal APIs
# ===========================

@app.post("/goals", response_model=schemas.GoalResponse)
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    new_goal = models.SavingGoal(
        monthly_goal=goal.monthly_goal,
        weekly_goal=goal.weekly_goal,
        daily_goal=goal.daily_goal
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


@app.get("/goals", response_model=list[schemas.GoalResponse])
def get_goals(db: Session = Depends(get_db)):
    return db.query(models.SavingGoal).all()


@app.put("/goals/{id}", response_model=schemas.GoalResponse)
def update_goal(id: int, goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    g = db.query(models.SavingGoal).filter(models.SavingGoal.id == id).first()

    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")

    g.monthly_goal = goal.monthly_goal
    g.weekly_goal = goal.weekly_goal
    g.daily_goal = goal.daily_goal

    db.commit()
    db.refresh(g)

    return g