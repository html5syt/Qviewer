import flet as ft
import flet_easy as fs
import core.controls as ct
import core.methods as mt


async def group(data: fs.Datasy, group_id: str):
    page = data.page

    async def navbar_click(e: ft.ControlEvent):
        if e.data == "0":
            data.page.go("/")
        else:
            list = await mt.storage(
                page=page, mode="r", sub_prefix="group_", key="list"
            )
            data.page.go(f"/group/{list[int(e.data)-1]}") if list else None

    page.title = "Qviewer | 群: " + group_id

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

    appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_size=27,
            on_click=lambda _: page.open(drawer),
            offset=ft.Offset(x=0.1, y=0),
        ),
        leading_width=30,
        title=ft.Text("群: " + group_id),
        center_title=False,
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.IconButton(ft.Icons.SEARCH, tooltip="搜索"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="导入向导", on_click=data.go("/welcome")),
                ],
                tooltip="选项",
            ),
        ],
    )
    if await mt.storage(page=page, mode="s", sub_prefix="group_", key="list"):
        for group_id_temp in await mt.storage(
            page=page, mode="r", sub_prefix="group_", key="list"
        ):
            drawer.controls.append(
                ft.NavigationDrawerDestination(
                    label=group_id_temp,
                )
            )
            if group_id_temp == int(group_id):

                drawer.selected_index = len(drawer.controls) - 3
            appbar.actions[1].items.append(
                ft.PopupMenuItem(
                    text=group_id_temp, on_click=data.go(f"/group/{group_id_temp}")
                )
            )
        page.update()

    mainview = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    msg_ctrls = await mt.storage(
        page=page,
        mode="r",
        sub_prefix="group_",
        key="ctrls",
    )
    # mainview.controls = msg_ctrls[int(group_id)]
    async def load_progressly():
        nonlocal mainview
        for i,ctrls in enumerate(msg_ctrls[int(group_id)]):
            mainview.controls.append(ctrls)
            # send page to a page
            if i % 500 == 0:
                page.update()
        # send the rest to a page
        page.update()
        mainview.auto_scroll=False
    load_task=mt.run_task(load_progressly())

    return ft.View(
        controls=[mainview],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
    )
