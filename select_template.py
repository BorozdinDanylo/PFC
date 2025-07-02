import flet as ft
from blinker import signal
import os



class SelectTemplate:
    def __init__(self, page: ft.Page):
        self.page = page
        self.window = ft.AlertDialog(
            title=ft.Text("Template"),
            content=ft.Dropdown(
                label="Select",
                options=[
                    ft.DropdownOption(key=name[:-5], content=ft.Text(value=name[:-5])) for name in os.listdir("templates") if name != "README.md"
                ],
                width=200,
            ),
            actions=[
                ft.TextButton("Ok", on_click=self._select),
                ft.TextButton("Censel", on_click=self._close),
            ],
        )

        self.load_template_event = signal("load_template")

        self._open()


    def _open(self):
        self.page.open(self.window)


    def _close(self, *_):
        self.page.close(self.window)


    def _select(self, *_):
        # noinspection PyTypeChecker
        selection: ft.Dropdown = self.window.content

        self.load_template_event.send(name=selection.value)

        self._close()

