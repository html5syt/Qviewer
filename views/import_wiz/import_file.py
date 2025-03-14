import flet as ft
import packages.flet_easy as fs
import core.methods as mt
import json
import packages.aiofiles as aiofiles
# TODO: Android上无法导入，待解决

# welcome = fs.AddPagesy()


# We add a page
# @welcome.page(route="/welcome", title="Qviewer | 欢迎")
async def choose(data: fs.Datasy):
    view = data.view
    page = data.page

    choose_button = ft.ElevatedButton(
        icon=ft.Icons.UPLOAD_FILE,
        text=f"\n     Tap to choose file     \n",
        on_click=lambda _: pick_files_dialog.pick_files(
            # allow_multiple=True
            allowed_extensions=["json", "db", "qvw"]
        ),
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            side=ft.BorderSide(width=2, color=ft.Colors.BLUE_300),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
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
        # on_click=data.go("/import/choose"),
        disabled=True,
    )

    async def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal choose_button
        if e.files[0].name.endswith(".json"):
            dialog = ft.AlertDialog(
                modal=True,
                content=ft.Row(
                    [
                        ft.ProgressRing(),
                        ft.Text("Converting JSON to dict..."),
                    ]
                ),
            )
            if e.files:
                await mt.log(f"File picker result: {e}", page=page)
                try:
                    page.open(dialog)
                    async with aiofiles.open(
                        e.files[0].path, "r", encoding="utf-8"
                    ) as f:
                        json_data = await f.read()
                        json_data = json.loads(json_data)
                        await mt.storage(
                            page=page,
                            mode="w",
                            sub_prefix="import_file_",
                            key="dict",
                            value=json_data,
                            force_out_to_log=True,
                        )
                except Exception as err:
                    page.close(dialog)
                    await mt.error(f"JSON convert error：{err}", page=page)
                else:
                    choose_button.text = "choosed：" + e.files[0].name
                    next_step.disabled = False
                    next_step.style = ft.ButtonStyle(
                        color=ft.Colors.BLUE,
                        bgcolor=ft.Colors.BLUE_50,
                        padding=ft.padding.all(15),
                        side=ft.BorderSide(width=2, color=ft.Colors.BLUE_300),
                    )
                    page.close(dialog)
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
                                        "Choose a file to import",
                                        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                    ),
                                    ft.Text(
                                        "Supported file formats: \nJSON file",
                                        color=ft.Colors.GREY,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    choose_button,
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
