import flet as ft

def main(page: ft.Page):
    page.title = "View Test"

    def route_change(e=None):
        page.views.clear()

        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.Text(
                        "VIEW CONTENT IS WORKING",
                        size=30,
                        color=ft.Colors.BLUE,
                    ),
                    ft.Text("This is a page view."),
                    ft.Button(
                        content="Test button",
                        on_click=lambda e: page.add(
                            ft.Text("Button clicked!")
                        ),
                    ),
                ],
            )
        )

        page.update()

    page.on_route_change = route_change
    route_change()

ft.run(main)