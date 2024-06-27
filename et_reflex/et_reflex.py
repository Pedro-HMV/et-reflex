import json
import typing

import reflex as rx

from rxconfig import config


class Expense(rx.Component):
    title: rx.Var[str]
    price: rx.Var[float]
    due: rx.Var[int]
    paid: rx.Var[bool]

    def __init__(self, title: str = "New expense", price: float = 100.0, due: int = 1, paid: bool = False):
        self.title = title
        self.price = price
        self.due = due
        self.paid = paid

    def update(self, **kwargs):
        self.title = kwargs.get("title", self.title or "")
        self.price = kwargs.get("price", self.price or 0.0)
        self.due = kwargs.get("due", self.due or 0)

    def toggle_paid(self):
        self.paid = not self.paid


@rx.serializer
def serialize_expense(expense: Expense) -> list:
    return json.dumps(str(expense))

class State(rx.State):
    """The app state."""

    expenses: typing.List[Expense] = [Expense()]
    income: float = 0.0

    @rx.var
    def last(self) -> int:
        return max(len(self.expenses) - 1, 0)

    def add_expense(self):
        self.expenses.append(Expense())

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
                value=State.expenses.title,
                on_change=lambda v: State.update_expense(i, v),
            ),
            rx.input(
                value=State.expenses[i].price,
                on_change=lambda v: State.update_expense(i, v),
            ),
            rx.input(
                value=State.expenses[i].due,
                on_change=lambda v: State.update_expense(i, v),
            ),
            rx.checkbox(default_checked=State.expenses[i].paid, on_click=State.toggle_paid(i)),
        ),
    )


def new_row() -> rx.Component:
    State.add_expense()
    index = State.last
    return rx.hstack(
        rx.input(value="New expense", on_change=lambda v: State.update_expense(index, v)),
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
            rx.button("Add expense", on_click=new_expense()),
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)

