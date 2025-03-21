import flet as ft
import core.methods as mt
import sys

import flet_easy as fs

# welcome = fs.AddPagesy()


# We add a page
# @welcome.page(route="/welcome", title="Qviewer | 欢迎")
async def welcome(data: fs.Datasy):
    view = data.view
    page = data.page

    # 清空已导入的数据（初始化）
    for key in ["json","dict","group"]:
        if await mt.storage(page, key, sub_prefix="import_file_", mode="s",type="s"):
            try:
                (
                    await mt.storage(page, key, "", sub_prefix="import_file_", mode="w",type="s")
                    if await mt.storage(page, key, sub_prefix="import_file_",type="s")
                    else None
                )
            except:
                await mt.log(f"清空已导入的数据失败：{key}")

    # 页面布局
    return ft.View(
        controls=[
            ft.Stack(
                [
                    ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Image("icon.png", width=70, height=70),
                                            ft.Text(
                                                "欢迎！",
                                                theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10,
                                    ),
                                    ft.ElevatedButton(
                                        icon=ft.Icons.MENU_BOOK,
                                        text="查阅教程与文档",
                                        on_click=lambda _: page.launch_url(
                                            "https://bing.com"
                                        ),
                                    ),
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=40,
                            ),
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.SETTINGS,
                                            icon_size=28,
                                            style=ft.ButtonStyle(
                                                color=ft.Colors.BLUE,
                                                bgcolor=ft.Colors.BLUE_50,
                                                padding=ft.padding.all(15),
                                                side=ft.BorderSide(
                                                    width=2, color=ft.Colors.BLUE_300
                                                ),
                                            ),
                                            on_click=data.go("/set"),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                            icon_size=28,
                                            style=ft.ButtonStyle(
                                                color=ft.Colors.BLUE,
                                                bgcolor=ft.Colors.BLUE_50,
                                                padding=ft.padding.all(15),
                                                side=ft.BorderSide(
                                                    width=2, color=ft.Colors.BLUE_300
                                                ),
                                            ),
                                            on_click=(
                                                data.go("/import/choose")
                                                if not page.web
                                                else data.go("/import/import_web")
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.only(
                                    left=10, right=10, top=0, bottom=10
                                ),
                            ),
                        ],
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # drawer=view.appbar,
    )
