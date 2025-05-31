import flet as ft
from select_field import SelectField



class Block(ft.Container):
    _all_blocks = []



    def __new__(cls, *args, **kwargs):
        _instance = super().__new__(cls)
        cls._all_blocks.append(_instance)
        return _instance


    def __init__(self, day: int, month: int, year: int, target: SelectField, size=80):
        super().__init__()

        self.day = day
        self.month = month
        self.year = year
        self.target = target

        self.border_radius = ft.border_radius.all

        self.content = ft.Text(
            value=str(day),
            width=size,
            height=size,
            size=size / 2,
            text_align=ft.TextAlign.CENTER
        )

        self.bgcolor = ft.Colors.GREY_400
        self.border_radius = 10
        self.border = ft.border.all(2, ft.Colors.WHITE)

        self.on_click = self.chose
        self.is_chosed = False


    def chose(self, e=None):
        if self.is_chosed and e:
            Block.deactivate()
            return
        elif e:
            Block.deactivate()

        if self.is_chosed:
            self.border = ft.border.all(2, ft.Colors.WHITE)
            self.bgcolor = ft.Colors.GREY_400
            self.is_chosed = False
            self.target.diactivate()
        else:
            self.border = ft.border.all(2, ft.Colors.BLACK)
            self.bgcolor = ft.Colors.GREY_500
            self.is_chosed = True
            self.target.activate(self.day, self.month, self.year)

        self.update()


    def set_color(self, color=""):
        match color:
            case "black":
                self.content.color = ft.colors.BLACK
            case "red":
                self.content.color = ft.colors.RED
            case "green":
                self.content.color = "#10A83E"
            case "blue":
                self.content.color = ft.colors.BLUE


    @staticmethod
    def clear_all():
        Block.deactivate()
        Block._all_blocks.clear()


    @staticmethod
    def deactivate():
        for b in Block._all_blocks:
            if type(b) is Block and b.is_chosed:
                b.chose()
                break




