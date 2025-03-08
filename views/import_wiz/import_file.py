import flet as ft
import flet_easy as fs
import core.methods as mt

# welcome = fs.AddPagesy()


# We add a page
# @welcome.page(route="/welcome", title="Qviewer | 欢迎")
def choose(data: fs.Datasy):
    view = data.view
    page = data.page

    async def pick_files_result(e: ft.FilePickerResultEvent):

        await mt.log(f"File picker result: {e}", page=page)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.extend([pick_files_dialog])

    return ft.View(
        controls=[
            ft.Stack(
                [
                    ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "选择文件",
                                        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                    ),
                                    ft.Text(
                                        "支持的文件格式：\n①nt_msg.db文件 ②JSON文件 ③导出的预渲染文件",
                                        color=ft.Colors.GREY,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.ElevatedButton(
                                        icon=ft.Icons.UPLOAD_FILE,
                                        text="\n     点击此处上传文件     \n",
                                        on_click=lambda _: pick_files_dialog.pick_files(
                                            # allow_multiple=True
                                            allowed_extensions=["json"]
                                        ),
                                        style=ft.ButtonStyle(
                                            padding=ft.padding.all(26),
                                            side=ft.BorderSide(
                                                width=2, color=ft.Colors.BLUE_300
                                            ),
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=40,
                            ),
                            # 下方按钮
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.KEYBOARD_ARROW_LEFT,
                                            icon_size=28,
                                            style=ft.ButtonStyle(
                                                color=ft.Colors.BLUE,
                                                bgcolor=ft.Colors.BLUE_50,
                                                padding=ft.padding.all(26),
                                                side=ft.BorderSide(
                                                    width=2, color=ft.Colors.BLUE_300
                                                ),
                                            ),
                                            on_click=data.go("/welcome"),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                            icon_size=28,
                                            style=ft.ButtonStyle(
                                                color=ft.Colors.BLUE,
                                                bgcolor=ft.Colors.BLUE_50,
                                                padding=ft.padding.all(26),
                                                side=ft.BorderSide(
                                                    width=2, color=ft.Colors.BLUE_300
                                                ),
                                            ),
                                            on_click=data.go("/import/choose"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.only(
                                    left=20, right=20, top=0, bottom=20
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
