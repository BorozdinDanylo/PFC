from select_template import SelectTemplate
from blinker import signal
import json
import flet as ft



PROTEIN = 191
FET = 61
CARBOHYDRATE = 219
KCAL = 2_188



def evaluation(normal, _is):
    percents = _is * 100 / normal - 100
    abs_percents = abs(percents)

    if percents == -100:
        return ft.Colors.BLACK
    if abs_percents <= 5:
        return ft.Colors.GREEN
    if abs_percents <= 10:
        return ft.Colors.YELLOW
    if percents > 10:
        return ft.Colors.RED
    if percents < -10:
        return ft.Colors.BLUE



class SelectField(ft.Column):
    count_of_felds = 0
    date: str = "2025_2_28"



    def __init__(self):
        super().__init__()

        load_template_event = signal("load_template")
        load_template_event.connect(self._load_template)

        self.alignment = ft.MainAxisAlignment.CENTER

        self.protein = ft.Text(value="P: 0")
        self.fet = ft.Text(value="F: 0")
        self.carbohydrate = ft.Text(value="C: 0")
        self.kcal = ft.Text(value="KK: 0")


    def add_feld(self, *_):
        self.count_of_felds += 1

        self.controls.append(
            ft.Row(
                controls=[
                    ft.TextField(label="Б", value="0", width=100, on_change=self.compute),
                    ft.TextField(label="Ж", value="0", width=100, on_change=self.compute),
                    ft.TextField(label="В", value="0", width=100, on_change=self.compute),
                    ft.TextField(label="X", value="1", width=100, on_change=self.compute),
                    ft.TextButton(text="Remove", data=self.count_of_felds, on_click=self.__remove_feld),
                ],
                data=self.count_of_felds,
            )
        )

        self.controls[-1], self.controls[-2] = self.controls[-2], self.controls[-1]

        self.update()


    def _open_template(self, *_):
        SelectTemplate(self.page)


    def _load_template(self, sender, **extra):
        name = extra.get("name", None)

        if not name:
            return

        with open(f"templates\\{name}.json", "r") as f:
            data: dict = json.load(f)

        self.controls.append(
            ft.Row(
                controls=[
                    ft.TextField(label="Б", value=data["P"], width=100, on_change=self.compute),
                    ft.TextField(label="Ж", value=data["F"], width=100, on_change=self.compute),
                    ft.TextField(label="В", value=data["C"], width=100, on_change=self.compute),
                    ft.TextField(label="X", value=data["X"], width=100, on_change=self.compute),
                    ft.TextButton(text="Remove", data=self.count_of_felds, on_click=self.__remove_feld),
                ],
                data=self.count_of_felds,
            )
        )

        self.count_of_felds += 1
        self.controls[-1], self.controls[-2] = self.controls[-2], self.controls[-1]
        self.compute()
        self.update()


    def compute(self, *_):
        p = f = c = 0

        try:
            for i in self.controls[1: -1]:
                p += float(i.controls[0].value) * float(i.controls[3].value)
                f += float(i.controls[1].value) * float(i.controls[3].value)
                c += float(i.controls[2].value) * float(i.controls[3].value)
        except ValueError:
            return

        kcal = (p + c) * 4 + f * 9

        self.protein.value = f"P: {p:.2f}"
        self.protein.color = evaluation(PROTEIN, p)

        self.fet.value = f"F: {f:.2f}"
        self.fet.color = evaluation(FET, f)

        self.carbohydrate.value = f"C: {c:.2f}"
        self.carbohydrate.color = evaluation(CARBOHYDRATE, c)

        self.kcal.value = f"kca: {kcal:.2f}"
        self.kcal.color = evaluation(KCAL, kcal)

        self.update()

        self.__save()


    def diactivate(self):
        self.controls.clear()
        self.update()


    def activate(self, day: int, month: int, year: int):
        self.__set_date(f"{year}_{month}_{day}")
        self.__load()


    def __set_date(self, date: str):
        self.date = date


    def __remove_feld(self, event: ft.ControlEvent):
        _id = event.control.data

        for i, tf in enumerate(self.controls):
            if tf.data == _id:
                self.controls.pop(i)
                self.update()
                break

        self.compute()


    def __save(self):
        import json

        data = []
        for i in self.controls[1: -1]:
            data.append(
                {
                    "P": i.controls[0].value,
                    "F": i.controls[1].value,
                    "C": i.controls[2].value,
                    "X": i.controls[3].value,
                }
            )

        with open(f"saves\\{self.date}.json", "w") as f:
            json.dump(data, f)


    def __load(self):
        from os.path import exists

        self.controls.clear()
        path = f"saves\\{self.date}.json"
        if exists(path):
            with open(path, "r") as f:
                data = json.load(f)
        else:
            data = [
                {
                    "P": "0",
                    "F": "0",
                    "C": "0",
                    "X": "1",
                }
            ]

        self.controls.append(
            ft.Row(
                controls=[
                    self.protein,
                    self.fet,
                    self.carbohydrate,
                    self.kcal,
                ],
                spacing=50,
                height=100,
            )
        )

        for i in data:
            self.controls.append(
                ft.Row(
                    controls=[
                        ft.TextField(label="Б", value=i["P"], width=100, on_change=self.compute),
                        ft.TextField(label="Ж", value=i["F"], width=100, on_change=self.compute),
                        ft.TextField(label="В", value=i["C"], width=100, on_change=self.compute),
                        ft.TextField(label="X", value=i["X"], width=100, on_change=self.compute),
                        ft.TextButton(text="Remove", data=self.count_of_felds, on_click=self.__remove_feld),
                    ],
                    data=self.count_of_felds,
                )
            )

            self.count_of_felds += 1

        self.controls.append(
            ft.Row(
                controls=[
                    ft.TextButton(
                        text="Create new",
                        on_click=self.add_feld,
                    ),
                    ft.TextButton(
                        text="Load template",
                        on_click=self._open_template,
                    ),
                ]
            )
        )

        self.compute()
        self.update()





