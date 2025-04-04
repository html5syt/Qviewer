import flet as ft
import flet_easy as fs
import core.methods as mt
import core.controls as ct
import traceback


async def choose(data: fs.Datasy):
    # view = data.view
    page = data.page

    choose_button_db_path = ft.ElevatedButton(
        icon=ft.Icons.FOLDER,
        text="\n【Tencent Files\\QQ号】文件夹\n",
        on_click=lambda _: pick_files_dialog.get_directory_path(
            # allowed_extensions=["db","qvw"]
        ),
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            side=ft.BorderSide(width=2, color=ft.Colors.BLUE_300),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        col={"sm": 6},
    )
    choose_button_db_file = ft.ElevatedButton(
        icon=ft.Icons.DATASET,
        text="\n   mt_msg.db文件   \n",
        on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["db"]),
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            side=ft.BorderSide(width=2, color=ft.Colors.BLUE_300),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        col={"sm": 6},
    )
    choose_button_qvw = ft.ElevatedButton(
        icon=ft.Icons.BACKUP_TABLE,
        text="\n     由本工具导出的qvw文件     \n",
        on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["qvw"]),
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            side=ft.BorderSide(width=2, color=ft.Colors.BLUE_300),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        # col={"sm": 6},
    )

    next_step = ft.IconButton(
        icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
        icon_size=28,
        style=ft.ButtonStyle(
            color=ft.Colors.GREY,
            bgcolor=ft.Colors.GREY_50,
            padding=ft.padding.all(15),
            side=ft.BorderSide(width=2, color=ft.Colors.GREY_300),
        ),
        # on_click=data.go("/"),
        disabled=True,
    )

    async def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal choose_button_qvw
        await mt.log(f"File picker result: {e}", page=page)
        if e.path:
            # TODO: 自动设置参数
            choose_button_db_file.visible = False
            choose_button_qvw.visible = False
            choose_button_db_path.text = f"\n     已选择目录：{e.path}     \n"
            choose_button_db_path.col = None
            next_step.disabled = False
            next_step.style.color = ft.Colors.BLUE
            next_step.style.bgcolor = ft.Colors.BLUE_50
            page.update()
        elif e.files[0].name.endswith(".db"):
            choose_button_db_path.visible = False
            choose_button_qvw.visible = False
            choose_button_db_file.text = f"\n     已选择文件：{e.files[0].name}     \n"
            choose_button_db_file.col = None
            next_step.disabled = False
            next_step.style.color = ft.Colors.BLUE
            next_step.style.bgcolor = ft.Colors.BLUE_50
            page.update()
        elif e.files[0].name.endswith(".qvw"):
            choose_button_db_path.visible = False
            choose_button_db_file.visible = False
            choose_button_qvw.text = f"\n     已选择文件：{e.files[0].name}     \n"
            choose_button_qvw.col = None
            next_step.disabled = False
            next_step.style.color = ft.Colors.BLUE
            next_step.style.bgcolor = ft.Colors.BLUE_50
            page.update()

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
                                        "Tips: 选择文件夹可自动填写相关参数，详情请查看文档",
                                        color=ft.Colors.GREY,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.ResponsiveRow(
                                        [
                                            choose_button_db_path,
                                            choose_button_db_file,
                                            choose_button_qvw,
                                        ],
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
                                                padding=ft.padding.all(15),
                                                side=ft.BorderSide(
                                                    width=2, color=ft.Colors.BLUE_300
                                                ),
                                            ),
                                            on_click=data.go("/welcome"),
                                        ),
                                        next_step,
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
