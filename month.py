from block import Block
from select_field import SelectField
from datetime import datetime
import flet as ft
import calendar



class Month(ft.GridView):
    def __init__(self, year: int, month: int, target: SelectField):
        super().__init__()

        self.year = year
        self.month = month
        self.target = target

        self.expand = True
        self.width = 90 * 7
        self.max_extent = 80
        self.spacing = 10
        self.run_spacing = 10

        self.update()


    def update(self):
        self.controls.clear()

        date_obj = datetime(year=self.year, month=self.month, day=1)
        day_number = date_obj.isoweekday()
        for _ in range(day_number - 1):
            self.controls.append(ft.Container())

        for d in range(1, calendar.monthrange(self.year, self.month)[1] + 1):
            self.controls.append(Block(d, self.month, self.year, self.target))


    def set_month(self, e):
        self.month = int(e.control.value)
        Block.clear_all()
        self.update()


    def set_year(self, e):
        self.year = int(e.control.value)
        Block.clear_all()
        self.update()




