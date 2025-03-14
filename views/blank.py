# import asyncio
import packages.flet_easy as fs
import flet as ft


# blank = fs.AddPagesy()


# # We add a second page
# @blank.page(route="/blank", title="空白页")
def blank(data: fs.Datasy):
    # data.go_back()
    return ft.View(
        controls=[
            ft.Stack(
                [
                    ft.Text("空白页，仅用于刷新\n点击或放置指针以返回上一页",size=40,style=ft.TextStyle(weight="bold"),text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        on_click=data.go_back(),
                        on_hover=data.go_back(),
                        expand=True,
                    ),
                ],
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
    )
