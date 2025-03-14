import flet as ft
import packages.flet_easy as fs
import core.controls as ct
import core.methods as mt


# home = fs.AddPagesy(
#     # route_prefix="/counter",
# )


# We add a second page
# @home.page(route="/", title="Home")
def home(data: fs.Datasy):
    page = data.page

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.Icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.Icons.PHONE,
            ),
        ],
    )
    appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_size=25,
            on_click=lambda _: page.open(drawer),
        ),
        leading_width=30,
        title=ft.Text("首页"),
        center_title=False,
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.IconButton(ft.Icons.REFRESH, on_click=data.go("/blank"),tooltip="刷新布局"),
            ft.IconButton(ft.Icons.SEARCH,tooltip="搜索"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        text="导入向导(欢迎)", on_click=data.go("/welcome")
                    ),
                    # ft.PopupMenuItem(),  # divider
                    # ft.PopupMenuItem(text="Checked item",on_click=data.go("/blank")),
                ],
                tooltip="选项",
            ),
        ],
    )
    mainview = ft.ListView(
        expand=True,
        spacing=10,
    )
    # mainview = ft.Text("Hello world")
    # #     border=ft.border.all(1, ft.Colors.RED),
    # # )
    for i in range(10):
        # mainview.controls.append(ct.Base(timestamp=1738918858))
        mainview.controls.append(
            ct.TextMessage(
                text="Hello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello world\nHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello world",
                timestamp=1738918858,
                name=f"message{i}",
                data=data,
            )
        )
        mainview.controls.append(
            ct.Base(
                timestamp=1738918858,
                name=f"base{i}",
                data=data,
            )
        )
    # page.add(mainview)
    # def fab_pressed(e):
    #     page.floating_action_button = None
    #     data.go("/blank")



    # data.page.on_resized = on_resized
    return ft.View(
        controls=[mainview],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
    )
