# import asyncio
import flet as ft
import core.methods as mt
import sys

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
    import flet_easy as fs

# set = fs.AddPagesy()


# # We add a second page
# @set.page(route="/set", title="设置")
async def set_page(data: fs.Datasy):
    # data.go_back()
    page = data.page

    async def debug_switch(e):
        await mt.storage(
            page=page,
            sub_prefix="settings_",
            key="debug_mode",
            value=e.data,
            mode="w",
            type="c",
        )
        await mt.log(e, page=page)
    async def dynamic_load_switch(e):
        await mt.storage(
            page=page,
            sub_prefix="settings_",
            key="dynamic_load",
            value=e.data,
            mode="w",
            type="c",
        )
        await mt.log(e, page=page)
        # page.open(ft.SnackBar(ft.Text(f"Counter value at")))

    async def handle_data_path(e):
        await mt.log(
            mt.GetEnv.get_app_data_path(),
            page=page,
        )

    async def handle_temp_path(e):
        await mt.log(
            mt.GetEnv.get_app_temp_path(),
            page=page,
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
                                        "TODO: 设置页面",
                                        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                    ),
                                    ft.Text(
                                        f"on {sys.platform}",
                                        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                    ),
                                    ft.Switch(
                                        label="DEBUG MODE",
                                        on_change=debug_switch,
                                        value=(
                                            await mt.storage(
                                                page=page,
                                                sub_prefix="settings_",
                                                key="debug_mode",
                                                mode="r",
                                                type="c",
                                            )
                                            if await mt.storage(
                                                page=page,
                                                sub_prefix="settings_",
                                                key="debug_mode",
                                                mode="s",
                                                type="c",
                                            )
                                            else "false"
                                        ),
                                    ),
                                    ft.Switch(
                                        label="动态加载",
                                        on_change=dynamic_load_switch,
                                        value=(
                                            await mt.storage(
                                                page=page,
                                                sub_prefix="settings_",
                                                key="dynamic_load",
                                                mode="r",
                                                type="c",
                                            )
                                            if await mt.storage(
                                                page=page,
                                                sub_prefix="settings_",
                                                key="dynamic_load",
                                                mode="s",
                                                type="c",
                                            )
                                            else "false"
                                        ),
                                    ),
                                    ft.Button(
                                        "get data path", on_click=handle_data_path
                                    ),
                                    ft.Button(
                                        "get temp path", on_click=handle_temp_path
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
                                            on_click=data.go_back(),
                                        ),
                                        # ft.IconButton(
                                        #     icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                        #     icon_size=28,
                                        #     style=ft.ButtonStyle(
                                        #         color=ft.Colors.BLUE,
                                        #         bgcolor=ft.Colors.BLUE_50,
                                        #         padding=ft.padding.all(15),
                                        #         side=ft.BorderSide(
                                        #             width=2, color=ft.Colors.BLUE_300
                                        #         ),
                                        #     ),
                                        #     on_click=data.go("/import/choose"),
                                        # ),
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
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
    )
