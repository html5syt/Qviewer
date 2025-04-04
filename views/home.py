import flet as ft
import core.methods as mt
import core.controls as ct
from core.load import *
import traceback
import sys
import asyncio

import flet_easy as fs


async def home(data: fs.Datasy):
    page = data.page

    async def navbar_click(e: ft.ControlEvent):
        if e.data == "0":
            data.page.go("/")
        else:
            list = await mt.storage(
                page=page, mode="r", sub_prefix="group_", key="list"
            )
            data.page.go(f"/group/{list[int(e.data)-1]}") if list else None

    mainview = ft.ElevatedButton(
        icon=ft.Icons.LOGIN,
        text=f"\n     导入向导     \n",
        on_click=data.go("/welcome"),
        style=ft.ButtonStyle(
            padding=ft.padding.all(15),
            side=ft.BorderSide(width=2, color=ft.Colors.BLUE_300),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )
    dialog = ct.Loading(text="正在加载字典聊天数据...")
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


    return ft.View(
        controls=[mainview],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
        # start_handler=mt.run_task(load_msg(data, page, mainview, dialog, drawer, appbar))
    )



