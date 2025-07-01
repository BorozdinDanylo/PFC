import flet as ft
from blinker import Signal
import json
import copy



class Template:
    standart_content = [
            ft.TextField(label="Name"),
            ft.TextField(label="P", value="0", width=100, ),
            ft.TextField(label="F", value="0", width=100),
            ft.TextField(label="C", value="0", width=100),
            ft.TextField(label="X", value="1", width=100),
        ]



    def __init__(self, page: ft.Page):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Template"),
            content=ft.Column(controls=self.standart_content.copy()),
            actions=[
                ft.TextButton("Yes", on_click=self.__save),
                ft.TextButton("No", on_click=self.__close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            alignment=ft.alignment.center,

        )

        self.page = page

        self._save = Signal("close")
        self._save.connect(self.__save, "save")


    def open(self):
        self.page.open(self.dialog)


    def __close(self, *_):
        # self.dialog.content = ft.Column(controls=copy.deepcopy(self.standart_content))
        # self.dialog.update()

        self.page.close(self.dialog)


    def __save(self, *_):
        # noinspection PyTypeChecker
        column: ft.Column = self.dialog.content
        with open(f"templates\\{column.controls[0].value}.json", "w") as f:
            json.dump({field.label: field.value for field in column.controls[1:]}, f)

        self.__close()
