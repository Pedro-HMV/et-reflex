"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import typing
from typing import Union

import reflex as rx

from rxconfig import config


class Expense:
    def __init__(
        self, title: str = "", price: float = 0.0, due: int = 0, paid: bool = False
    ):
        self.title: str = title
        self.price: float = price
        self.due: int = due
        self.paid: bool = False

    def update(self, **kwargs):
        self.title = kwargs.get("title", self.title or "")
        self.price = kwargs.get("price", self.price or 0.0)
        self.due = kwargs.get("due", self.due or 0)

    def toggle_paid(self):
        self.paid = not self.paid


class State(rx.State):
    """The app state."""

    expenses: list[Expense] = []
    income: float = 0.0

    @rx.var
    def last(self) -> int:
        return len(self.expenses) - 1

    def add_expense(self, expense: Expense = Expense()):
        self.expenses.append(expense)

    def update_income(self, income: float):
        self.income = income

    def update_expense(self, index: int, value: typing.Union[str, float, int]):
        title = value if isinstance(value, str) else None
        price = value if isinstance(value, float) else None
        due = value if isinstance(value, int) else None
        self.expenses[index].update(title=title, price=price, due=due)

    def delete_expense(self, index):
        self.expenses.pop(index)

    def toggle_paid(self, index: int):
        self.expenses[index].toggle_paid()

    @rx.var
    def balance(self) -> float:
        return sum(e.price for e in self.expenses)


def expense_row(expense: Expense, i: int) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.input(
                value=expense.title,
                on_change=lambda v: State.update_expense(i, v),
            ),
            rx.input(
                value=expense.price,
                on_change=lambda v: State.update_expense(i, v),
            ),
            rx.input(
                value=expense.due,
                on_change=lambda v: State.update_expense(i, v),
            ),
            rx.checkbox(default_checked=expense.paid, on_click=State.toggle_paid(i)),
        ),
        rx.button(label="Add expense", on_click=new_row),
    )


def new_row() -> rx.Component:
    State.add_expense()
    index = State.last
    return rx.hstack(
        rx.input(value="", on_change=lambda v: State.update_expense(index, v)),
        rx.input(value=0.0, on_change=lambda v: State.update_expense(index, v)),
        rx.input(value=0, on_change=lambda v: State.update_expense(index, v)),
        rx.checkbox(default_checked=False, on_click=lambda: State.toggle_paid(index)),
    )


def new_expense():
    State.add_expense()


def index() -> rx.Component:
    # Welcome Page (Index)

    return (
        rx.container(
            rx.color_mode.button(position="top-right"),
            rx.heading("Expenses Tracker", size="9"),
            rx.text(
                "Manage income, fixed expenses and due dates with ease",
                size="5",
            ),
            rx.foreach(State.expenses, expense_row),
            rx.button(on_click=new_expense(), label="Add Expense"),
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
