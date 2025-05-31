import flet as ft
from month import Month
from select_field import SelectField
from datetime import datetime



def main(page: ft.Page):
    def chenge_month(e):
        try:
            calender.set_month(e)
        except ValueError:
            pass
        else:
            page.update()


    def chenge_year(e):
        try:
            calender.set_year(e)
        except ValueError:
            pass
        else:
            page.update()


    page.theme_mode = ft.ThemeMode.LIGHT

    date = datetime.now()

    sf = SelectField()

    m = date.month
    y = date.year

    calender = Month(y, m, sf)

    month = ft.TextField(
        value=str(m),
        label="Month",
        on_change=chenge_month
    )
    year = ft.TextField(
        value=str(y),
        label="Year",
        on_change=chenge_year
    )

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                month,
                                year,
                            ]
                        ),
                        calender,
                    ]
                ),
                sf,
            ],
            spacing=100,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
    )

    calender.select_today()



if __name__ == '__main__':
    ft.app(target=main)
