import flet as ft
import sys

import flet_easy as fs

class ConfigApp:
    def __init__(self, app: fs.FletEasy):
        self.app = app
        self.start()

    def start(self):
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
