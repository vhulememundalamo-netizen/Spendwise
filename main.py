
import flet as ft
from datetime import date
from expense import Expense
from expense_manager import ExpenseManager


def main(page: ft.Page):
    manager = ExpenseManager()

    page.title = "SpendWise - Personal Expense Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 0

    status_text = ft.Text(
        "",
        color=ft.Colors.GREEN_700,
        size=13,
    )

    def money(value):
        return f"R {value:,.2f}"

    def show_message(message, error=False):
        status_text.value = message
        status_text.color = (
            ft.Colors.RED_700 if error
            else ft.Colors.GREEN_700
        )
        page.update()

    # -------------------------
    # NAVIGATION
    # -------------------------

    def navigate(route):
        page.route = route
        render_page()

    def nav_button(label, route):
        return ft.TextButton(
            content=label,
            on_click=lambda e: navigate(route),
        )

    # -------------------------
    # HEADER
    # -------------------------

    def app_header():
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=18,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.ACCOUNT_BALANCE_WALLET,
                                color=ft.Colors.BLUE_700,
                                size=30,
                            ),
                            ft.Text(
                                "SpendWise",
                                size=25,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_GREY_900,
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=8,
                        controls=[
                            nav_button("Dashboard", "/"),
                            nav_button("Add expense", "/add"),
                            nav_button("History", "/history"),
                            nav_button("Reports", "/reports"),
                        ],
                    ),
                ],
            ),
        )

    # -------------------------
    # COMMON PAGE LAYOUT
    # -------------------------

    def page_shell(content):
        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                app_header(),

                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.GREY_100,
                    padding=20,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=16,
                        controls=[
                            status_text,
                            content,
                            ft.Text(
                                "SpendWise | Personal Expense Tracker",
                                size=11,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
            ],
        )

    # -------------------------
    # SECTION TITLE
    # -------------------------

    def section_title(title, subtitle):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Text(
                    title,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_900,
                ),
                ft.Text(
                    subtitle,
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
            ],
        )

    # -------------------------
    # STATISTICS CARD
    # -------------------------

    def stat_card(title, value, icon, color):
        return ft.Container(
            width=300,
            height=115,
            padding=18,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                title,
                                size=13,
                                color=ft.Colors.GREY_700,
                            ),
                            ft.Icon(
                                icon,
                                color=color,
                                size=23,
                            ),
                        ],
                    ),
                    ft.Text(
                        value,
                        size=23,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_900,
                    ),
                ],
            ),
        )

    # -------------------------
    # DASHBOARD
    # -------------------------

    def dashboard_view():
        expenses = manager.get_all()

        total = sum(
            item.amount for item in expenses
        )

        categories = {
            item.category for item in expenses
        }

        recent = sorted(
            expenses,
            key=lambda item: item.date,
            reverse=True,
        )[:5]

        recent_rows = []

        for item in recent:
            recent_rows.append(
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=3,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        item.description,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"{item.category} | {item.date}",
                                        size=12,
                                        color=ft.Colors.GREY_700,
                                    ),
                                ],
                            ),
                            ft.Text(
                                money(item.amount),
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                )
            )

        if not recent_rows:
            recent_rows.append(
                ft.Text(
                    "No expenses recorded yet.",
                    color=ft.Colors.GREY_700,
                )
            )

        content = ft.Column(
            spacing=18,
            controls=[
                section_title(
                    "Your dashboard",
                    "A simple overview of where your money is going.",
                ),

                ft.Row(
                    wrap=True,
                    spacing=12,
                    controls=[
                        stat_card(
                            "Total expenses",
                            money(total),
                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                            ft.Colors.BLUE_700,
                        ),
                        stat_card(
                            "Transactions",
                            str(len(expenses)),
                            ft.Icons.RECEIPT_LONG,
                            ft.Colors.ORANGE_700,
                        ),
                        stat_card(
                            "Categories used",
                            str(len(categories)),
                            ft.Icons.CATEGORY,
                            ft.Colors.GREEN_700,
                        ),
                    ],
                ),

                ft.Container(
                    padding=18,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                "Recent expenses",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            *recent_rows,
                            ft.TextButton(
                                content="View all transactions",
                                on_click=lambda e: navigate("/history"),
                            ),
                        ],
                    ),
                ),

                ft.Row(
                    wrap=True,
                    controls=[
                        ft.Button(
                            content="Add an expense",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: navigate("/add"),
                        ),
                        ft.OutlinedButton(
                            content="View reports",
                            icon=ft.Icons.BAR_CHART,
                            on_click=lambda e: navigate("/reports"),
                        ),
                    ],
                ),
            ],
        )

        return page_shell(content)

    # -------------------------
    # ADD EXPENSE
    # -------------------------

    def add_view():
        description = ft.TextField(
            label="Description",
            hint_text="e.g. Lunch or transport",
        )

        amount = ft.TextField(
            label="Amount (R)",
            hint_text="e.g. 85.50",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        category = ft.Dropdown(
            label="Category",
            value="Food",
            options=[
                ft.DropdownOption("Food"),
                ft.DropdownOption("Transport"),
                ft.DropdownOption("Education"),
                ft.DropdownOption("Entertainment"),
                ft.DropdownOption("Shopping"),
                ft.DropdownOption("Bills"),
                ft.DropdownOption("Health"),
                ft.DropdownOption("Other"),
            ],
        )

        expense_date = ft.TextField(
            label="Date (YYYY-MM-DD)",
            value=date.today().isoformat(),
        )

        def save_expense(e):
            try:
                clean_description = (
                    description.value or ""
                ).strip()

                if not clean_description:
                    raise ValueError(
                        "Please enter a description."
                    )

                if not amount.value:
                    raise ValueError(
                        "Please enter an amount."
                    )

                amount_value = float(amount.value)

                if amount_value <= 0:
                    raise ValueError(
                        "Amount must be greater than zero."
                    )

                if not category.value:
                    raise ValueError(
                        "Please select a category."
                    )

                clean_date = (
                    expense_date.value or ""
                ).strip()

                date.fromisoformat(clean_date)

                new_expense = Expense(
                    description=clean_description,
                    amount=amount_value,
                    category=category.value,
                    date=clean_date,
                )

                manager.add(new_expense)

                show_message(
                    "Expense saved successfully."
                )

                navigate("/history")

            except ValueError as error:
                show_message(str(error), error=True)

            except OSError:
                show_message(
                    "Could not save the expense file.",
                    error=True,
                )

        content = ft.Column(
            spacing=16,
            controls=[
                section_title(
                    "Add an expense",
                    "Enter the details below to record a transaction.",
                ),

                ft.Container(
                    width=650,
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            description,
                            amount,
                            category,
                            expense_date,

                            ft.Row(
                                wrap=True,
                                controls=[
                                    ft.Button(
                                        content="Save expense",
                                        icon=ft.Icons.SAVE,
                                        on_click=save_expense,
                                    ),
                                    ft.OutlinedButton(
                                        content="Cancel",
                                        on_click=lambda e: navigate("/"),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )

        return page_shell(content)

    # -------------------------
    # TRANSACTION HISTORY
    # -------------------------

    def history_view():
        expenses = sorted(
            manager.get_all(),
            key=lambda item: item.date,
            reverse=True,
        )

        rows = []

        def delete_expense(expense_id):
            try:
                manager.delete(expense_id)
                show_message("Expense deleted.")
                navigate("/history")

            except OSError:
                show_message(
                    "Could not update the expense file.",
                    error=True,
                )

        for item in expenses:
            rows.append(
                ft.Container(
                    padding=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                expand=True,
                                spacing=3,
                                controls=[
                                    ft.Text(
                                        item.description,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"{item.category} | {item.date}",
                                        size=12,
                                        color=ft.Colors.GREY_700,
                                    ),
                                ],
                            ),

                            ft.Text(
                                money(item.amount),
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_600,
                                tooltip="Delete expense",
                                on_click=lambda e, expense_id=item.id: (
                                    delete_expense(expense_id)
                                ),
                            ),
                        ],
                    ),
                )
            )

        if not rows:
            rows.append(
                ft.Text(
                    "Your transaction history is empty.",
                    color=ft.Colors.GREY_700,
                )
            )

        content = ft.Column(
            spacing=16,
            controls=[
                section_title(
                    "Transaction history",
                    "View and manage your recorded expenses.",
                ),

                ft.Container(
                    padding=18,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    content=ft.Column(
                        spacing=5,
                        controls=rows,
                    ),
                ),

                ft.Text(
                    f"Number of transactions: {len(expenses)}",
                    color=ft.Colors.GREY_700,
                ),
            ],
        )

        return page_shell(content)

    # -------------------------
    # REPORTS
    # -------------------------

    def reports_view():
        expenses = manager.get_all()
        totals = {}

        for item in expenses:
            totals[item.category] = (
                totals.get(item.category, 0)
                + item.amount
            )

        total_spent = sum(totals.values())
        report_rows = []

        for category_name, category_total in sorted(
            totals.items(),
            key=lambda pair: pair[1],
            reverse=True,
        ):
            share = (
                category_total / total_spent * 100
                if total_spent > 0
                else 0
            )

            report_rows.append(
                ft.Container(
                    padding=12,
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        category_name,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        money(category_total),
                                    ),
                                ],
                            ),

                            ft.ProgressBar(
                                value=share / 100,
                                bar_height=8,
                            ),

                            ft.Text(
                                f"{share:.1f}% of total spending",
                                size=12,
                                color=ft.Colors.GREY_700,
                            ),
                        ],
                    ),
                )
            )

        if not report_rows:
            report_rows.append(
                ft.Text(
                    "Add expenses to see your spending report.",
                    color=ft.Colors.GREY_700,
                )
            )

        content = ft.Column(
            spacing=16,
            controls=[
                section_title(
                    "Spending reports",
                    "Understand how your money is distributed.",
                ),

                stat_card(
                    "Total recorded spending",
                    money(total_spent),
                    ft.Icons.BAR_CHART,
                    ft.Colors.BLUE_700,
                ),

                ft.Container(
                    padding=18,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                "Spending by category",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            *report_rows,
                        ],
                    ),
                ),
            ],
        )

        return page_shell(content)

    # -------------------------
    # PAGE RENDERING
    # -------------------------

    def render_page():
        route = page.route or "/"

        if route == "/":
            content = dashboard_view()

        elif route == "/add":
            content = add_view()

        elif route == "/history":
            content = history_view()

        elif route == "/reports":
            content = reports_view()

        else:
            page.route = "/"
            content = dashboard_view()

        page.controls.clear()
        page.add(content)
        page.update()

    # -------------------------
    # ROUTE CHANGES
    # -------------------------

    page.on_route_change = lambda e: render_page()

    # Initial screen
    page.add(dashboard_view())


if __name__ == "__main__":
    ft.run(main)
