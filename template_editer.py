import flet as ft
from template import Template
import os



class TemplateEditer(Template):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.dialog = None

    def open(self):
        self.dialog = self._select_template
        self.page.open(self.dialog)


    @property
    def _select_template(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            title=ft.Text("Select template"),
            content=ft.Dropdown(
                options=[
                    ft.DropdownOption(key=name[:-5], content=ft.Text(value=name[:-5])) for name in os.listdir("templates") if name != "README.md"
                ]
            ),
            actions=[
                ft.TextButton("Edit", on_click=self._edit),
                ft.TextButton("Remvoe", on_click=self._remove),
                ft.TextButton("Censel", on_click=self._close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            alignment=ft.alignment.center,
        )


    def _edit(self, *_):
        ...


    def _remove(self, *_):
        # noinspection PyTypeChecker
        feld: ft.Dropdown = self.dialog.content

        name = feld.value
        if name == "":
            return

        os.remove(f"templates\\{name}.json")

        self._close()




