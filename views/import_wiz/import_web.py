import flet as ft
import flet_easy as fs
import core.methods as mt

# welcome = fs.AddPagesy()


# We add a page
# @welcome.page(route="/welcome", title="Qviewer | 欢迎")
async def choose(data: fs.Datasy):
    view = data.view
    page = data.page

    # def pick_files_result(e: ft.FilePickerResultEvent):
    #     await mt.log(
    #         f"Files selected: {", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"}"
    #     )
    #     await mt.log(f"File picker result: {e}")

    # pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    # page.overlay.extend([pick_files_dialog])

    async def temporary_storage(e):
        await mt.storage(
            page=page,
            sub_prefix="import_file_",
            key="json",
            mode="w",
            value=str(
                await mt.storage(
                    page=page, sub_prefix="import_file_", key="json", mode="r"
                )
                if await mt.storage(
                    page=page, sub_prefix="import_file_", key="json", mode="s"
                )
                else ""
            )
            + json.value,
        )
        # await mt.log(f"Temporary storage json complete!", page=page)
        

    json = ft.TextField(
        label="复制JSON文件的所有内容到此处",
        hint_text="Tips：不建议一次性复制过多内容，否则可能造成卡顿\n长按上方备注栏可暂存当前输入的所有内容",
        multiline=True,
        min_lines=5,
        max_lines=10,
    )

    return ft.View(
        controls=[
            ft.Stack(
                [
                    ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "手动导入 JSON",
                                        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            "注：web版无法获取上传的文件内容\n请复制JSON文件的所有内容到下方文本框中。",
                                            color=ft.Colors.GREY,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        on_long_press=temporary_storage,
                                    ),
                                    json,
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
