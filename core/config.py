import flet as ft
import packages.flet_easy as fs


class ConfigApp:
    def __init__(self, app: fs.FletEasy):
        self.app = app
        self.start()

    def start(self):
        # @self.app.view
        # def view_config(data: fs.Datasy):
        #     #     """Adding an AppBar on all pages"""
        #     return fs.Viewsy(
        #         appbar=ft.AppBar(
        #             leading=ft.Container(
        #                 ft.Icon(ft.Icons.PALETTE),
        #                 on_click=lambda _: data.page.open(drawer),
        #                 alignment=ft.alignment.center,
        #             ),
        #             leading_width=40,
        #             title=ft.Text("R#Leak (1468)"),
        #             center_title=False,
        #             bgcolor=ft.Colors.BLUE,
        #             actions=[
        #                 ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
        #                 ft.IconButton(ft.Icons.FILTER_3),
        #                 ft.PopupMenuButton(
        #                     items=[
        #                         ft.PopupMenuItem(
        #                             text="Item 1",
        #                             on_click=lambda _: data.page.open(drawer),
        #                         ),
        #                         ft.PopupMenuItem(),  # divider
        #                         ft.PopupMenuItem(text="Checked item", checked=False),
        #                     ]
        #                 ),
        #             ],
        #         )
        #     )

        @self.app.config
        def page_config(page: ft.Page):
            """页面通用设置"""
            theme = ft.Theme()
            platforms = ["android", "ios", "macos", "linux", "windows"]
            for platform in platforms:
                setattr(
                    theme.page_transitions,
                    platform,
                    ft.PageTransitionTheme.CUPERTINO,
                )
            page.theme = theme
