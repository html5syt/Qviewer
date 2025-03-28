import sys

# from core.config import ConfigApp
import flet as ft

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
    import flet_easy as fs
app = fs.FletEasy(route_init="/")

# # 导入view，用于注册路由
# import views.home
# import views.set

# # 导入向导
# import views.viewer
# import views.viewer.group
# import views.welcome
# import views.import_wiz.import_web

# if not sys.platform == "emscripten":
#     import views.import_wiz.import_file

#     app.add_routes(
#         [
#             fs.Pagesy(
#                 "/import/choose",
#                 views.import_wiz.import_file.choose,
#                 title="Qviewer | 导入向导-选择文件",
#             ),
#         ]
#     )

async def home(data: fs.Datasy):
    page = data.page

    async def navbar_click(e: ft.ControlEvent):
        print("navbar_click")

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="首页",
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME_FILLED,
            ),
            ft.Divider(),
        ],
        on_change=navbar_click,
    )
    page.drawer = drawer
    appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_size=27,
            on_click=lambda _: page.open(drawer),
            offset=ft.Offset(x=0.1, y=0),
        ),
        leading_width=30,
        title=ft.Text("首页"),
        center_title=False,
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.IconButton(ft.Icons.SEARCH, tooltip="搜索"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="导入向导", on_click=data.go("/welcome")),
                    ft.PopupMenuItem(),  # divider
                ],
                tooltip="选项",
            ),
        ],
    )

    # async def load_msg(page: ft.Page):
        

    # await load_msg(data, page, mainview, dialog, drawer, appbar)

    return ft.View(
        appbar=appbar,
        drawer=drawer,
    )
# We define the routes of the application.
app.add_routes(
    [
        fs.Pagesy("/", home, title="Qviewer | 首页"),
        # fs.Pagesy("/welcome", views.welcome.welcome, title="Qviewer | 欢迎"),
        # fs.Pagesy(
        #     "/import/import_web",
        #     views.import_wiz.import_web.choose,
        #     title="Qviewer | 导入向导-手动导入JSON",
        # ),
        # fs.Pagesy("/set", views.set.set_page, title="Qviewer | 设置"),
        # fs.Pagesy("/group/{group_id}", views.viewer.group.group),
    ]
)


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


# We load the application configuration.
ConfigApp(app)

# We run the application
app.run()
