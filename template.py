import flet as ft
import json



class Template:
    def __init__(self, page: ft.Page):
        self.page = page
        self._clean_dialog()


    def open(self):
        self.page.open(self.dialog)


    def _close(self, *_):
        self.page.close(self.dialog)
        self._clean_dialog()


    def _save(self, *_):
        # noinspection PyTypeChecker
        column: ft.Column = self.dialog.content

        data = {field.label: field.value for field in column.controls[1:]}
        print(data)
        if len(data) == 4 and "" not in data.values():
            with open(f"templates\\{column.controls[0].value}.json", "w") as f:
                json.dump(data, f)
        else:
            self.page.open(ft.SnackBar(ft.Text("Error")))

        self._close()


    @property
    def _dialog(self):
        return ft.AlertDialog(
            title=ft.Text("Template"),
            content=ft.Column(
                controls=[
                    ft.TextField(label="Name"),
                    ft.TextField(label="P", value="0", width=100),
                    ft.TextField(label="F", value="0", width=100),
                    ft.TextField(label="C", value="0", width=100),
                    ft.TextField(label="X", value="1", width=100),
                ]
            ),
            actions=[
                ft.TextButton("Save", on_click=self._save),
                ft.TextButton("Censel", on_click=self._close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            alignment=ft.alignment.center,
            # on_dismiss=self._clean_dialog,
        )

    def _clean_dialog(self, *_):
        self.dialog = self._dialog
