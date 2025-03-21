import flet as ft
import core.methods as mt
import core.controls as ct
from core.load import *
import traceback
import sys

import flet_easy as fs

# home = fs.AddPagesy(
#     # route_prefix="/counter",
# )


# We add a second page
# @home.page(route="/", title="Home")
async def home(data: fs.Datasy):
    page = data.page

    mainview = ft.Text("Hello world")
    dialog = ft.AlertDialog(
        modal=True,
        content=ft.Row(
            [
                ft.ProgressRing(),
                ft.Text("正在加载字典聊天数据..."),
            ]
        ),
    )
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
        ],
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
                    ft.PopupMenuItem(
                        text="导入向导(欢迎)", on_click=data.go("/welcome")
                    ),
                    ft.PopupMenuItem(),  # divider
                    # ft.PopupMenuItem(text="Checked item",on_click=data.go("/blank")),
                ],
                tooltip="选项",
            ),
        ],
    )

    async def load_msg(page: ft.Page):
        if await mt.storage(
            page=page, mode="r", sub_prefix="import_file_", key="dict", type="s"
        ):
            await mt.log(page=page, msg="import_file_dict is not empty")
            try:
                await load_group(page=page)
                await mt.log(
                    page=page,
                    msg=f"加载字典聊天数据成功\ngroup_list:{await mt.storage(page=page,mode='r',sub_prefix='group_',key='list')}",
                )
                mainview.value += "\n加载字典聊天数据成功"
                page.close(dialog)
                page.update()
                for group_id in await mt.storage(
                    page=page, mode="r", sub_prefix="group_", key="list"
                ):
                    drawer.controls.append(
                        ft.TextButton(
                            text=group_id,
                            on_click=data.go(f"/group/{group_id}"),
                        )
                    )
                    appbar.actions[1].items.append(
                        ft.PopupMenuItem(
                            text=group_id, on_click=data.go(f"/group/{group_id}")
                        )
                    )
                    page.update()
            except Exception as e:
                await mt.error(
                    page=page,
                    message=f"加载字典聊天数据时出现问题: {traceback.format_exc()}",
                )
                page.close(dialog)
                mainview.value += "\n加载字典聊天数据时出现问题"
                page.update()

    if await mt.storage(
        page=page, mode="r", sub_prefix="import_file_", key="dict", type="s"
    ):
        mainview.value += "\n正在加载字典聊天数据..."
        page.open(dialog)
        page.update()
    load_task = mt.run_task(load_msg(page=page))

    # mainview = ft.ListView(
    #     expand=True,
    #     spacing=10,
    # )
    # if await mt.storage(page=page, mode="s", sub_prefix="group_", key="list"):
    #     for group_id in await mt.storage(
    #         page=page, mode="r", sub_prefix="group_", key="list"
    #     ):

    # mainview = ct.TextWithPreRun("Hello world", page=page,pre_run=load_msg())
    #     border=ft.border.all(1, ft.Colors.RED),
    # )
    # for i in range(10):
    #     # mainview.controls.append(ct.Base(timestamp=1738918858))
    #     mainview.controls.append(
    #         ft.Row(
    #             alignment=ft.MainAxisAlignment.START,
    #             controls=[
    #                 ct.TextMessage(
    #                     text="Hello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello world\nHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello worldHello world",
    #                     timestamp=1738918858,
    #                     name=f"message{i}",
    #                     data=data,
    #                 )
    #             ],
    #         ),
    #     )
    #     mainview.controls.append(
    #         ct.Base(
    #             timestamp=1738918858,
    #             name=f"base{i}",
    #             data=data,
    #         )
    #     )
    # page.add(mainview)

    return ft.View(
        controls=[mainview, drawer],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
    )
