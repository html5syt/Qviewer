import flet as ft
import core.methods as mt
import core.controls as ct
import json
import traceback
import sys

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
    import flet_easy as fs
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

    async def temporary_storage(e=ft.TapEvent):
        """
        如果存储中已有的JSON文本存在并且以用户新输入的内容结尾，则直接使用已有的JSON文本；否则将已有的JSON文本与用户新输入的内容拼接起来，然后写入存储。
        """
        # await mt.storage(
        #     page=page,
        #     sub_prefix="import_file_",
        #     key="json",
        #     mode="w",
        #     value=(
        #         str(
        #             await mt.storage(
        #                 page=page, sub_prefix="import_file_", key="json", mode="r"
        #             )
        #             if await mt.storage(
        #                 page=page, sub_prefix="import_file_", key="json", mode="s"
        #             )
        #             else ""
        #         )
        #         + json_input.value
        #         if str(
        #             await mt.storage(
        #                 page=page, sub_prefix="import_file_", key="json", mode="r"
        #             )
        #             if await mt.storage(
        #                 page=page, sub_prefix="import_file_", key="json", mode="s"
        #             )
        #             else ""
        #         ).endswith(json_input.value)
        #         else str(
        #             await mt.storage(
        #                 page=page, sub_prefix="import_file_", key="json", mode="r"
        #             )
        #             if await mt.storage(
        #                 page=page, sub_prefix="import_file_", key="json", mode="s"
        #             )
        #             else ""
        #         )
        #     ),
        # )
        # 获取当前存储中的 JSON 数据
        current_json = (
            await mt.storage(
                page=page, sub_prefix="import_file_", key="json", mode="r", type="s"
            )
            if await mt.storage(
                page=page, sub_prefix="import_file_", key="json", mode="s", type="s"
            )
            else ""
        )

        # 确定新的 JSON 数据
        if current_json.endswith(json_input.value):
            new_json = current_json
        else:
            new_json = current_json + json_input.value

        await mt.storage(
            page=page,
            sub_prefix="import_file_",
            key="json",
            mode="w",
            value=new_json,
            type="s",
        )

        # await mt.log(f"Temporary storage json complete!", page=page)

    async def import_json(e):
        # await mt.log(f"Importing json...", page=page)
        # await mt.log(f"Temporary storage json: {await mt.storage(page=page, sub_prefix='import_file_', key='json', mode='r')}", page=page)
        dialog = ct.Loading(text="正在转换JSON为字典...")
        try:
            await temporary_storage()
            if (
                await mt.storage(
                    page=page, sub_prefix="import_file_", key="json", mode="s", type="s"
                )
                and json_input.value
                and await mt.storage(
                    page=page, sub_prefix="import_file_", key="json", mode="r", type="s"
                )
            ):
                page.open(dialog)
                page.update()
                json_data = json.loads(
                    await mt.storage(
                        page=page,
                        sub_prefix="import_file_",
                        key="json",
                        mode="r",
                        type="s",
                    )
                )
                await mt.storage(
                    page=page,
                    mode="w",
                    sub_prefix="import_file_",
                    key="dict",
                    value=json_data,
                    type="s",
                )
            else:
                raise ValueError("请先输入JSON文件内容！")
        except Exception as err:
            page.close(dialog) if dialog in page.overlay else None
            await mt.error(f"JSON转换失败：{traceback.format_exc()}", page=page)
        else:
            page.close(dialog)
            await mt.log(f"JSON转换成功！", page=page)
            page.update()
            data.page.go("/")

    json_input = ft.TextField(
        label="复制JSON文件的所有内容到此处",
        hint_text="Tips：不建议一次性复制过多内容，否则可能造成卡顿\n建议对JSON内容进行反格式化后输入以提高效率\n长按上方备注栏可暂存当前输入的所有内容",
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
                                    json_input,
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
                                            on_click=import_json,
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
