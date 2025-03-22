from datetime import datetime

import flet as ft
import sys
import asyncio

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
    import flet_easy as fs


class Base(ft.Container):
    def __init__(self, name=None, timestamp=0, avatar=None, qqnum=None, **kwargs):
        super().__init__()
        self.avatar = (
            avatar
            or f"https://q.qlogo.cn/headimg_dl?dst_uin={qqnum}&spec=640&img_type=jpg"
            if qqnum
            else "https://q.qlogo.cn/headimg_dl?dst_uin=0&spec=640&img_type=jpg"
        )
        self.name = name or "QQ用户"
        self.timestamp = datetime.fromtimestamp(timestamp + 8 * 60 * 60)
        # UTC+8
        self.expand = True
        self.expand_loose = True
        self.padding = 0
        self.margin = 0
        try:
            type(self.control)
        except AttributeError:
            self.control = ft.Text(
                r"""错误：未能解析消息""",
                color=ft.Colors.RED,
            )
        self.content = ft.Column(
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.CircleAvatar(
                                    foreground_image_src=self.avatar,
                                    radius=18,
                                    # offset=ft.Offset(x=0, y=0.2),
                                ),
                                ft.Text(
                                    self.name,
                                    size=16,
                                    offset=ft.Offset(x=0, y=-0.3),
                                ),
                                ft.Container(
                                    ft.Text(
                                        str(self.timestamp),
                                        size=12,
                                        color=ft.Colors.GREY,
                                    ),
                                    offset=ft.Offset(x=0, y=-0.3),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            content=self.control,
                            padding=10,
                            border_radius=ft.border_radius.all(10),
                            bgcolor=ft.Colors.BLUE_100,
                            expand=True,
                            expand_loose=True,
                            margin=ft.margin.only(left=45),
                        ),
                    ],
                ),
            ],
            expand=True,
            expand_loose=True,
        )

class TextMessage(Base):
    def __init__(self, text: str, qqnum=0, **kwargs):
        self.text = text
        self.control = ft.Text(
            self.text,
            color=ft.Colors.BLACK,
            selectable=True,
            size=14,
        )
        super().__init__(
            avatar=f"https://q.qlogo.cn/headimg_dl?dst_uin={qqnum}&spec=640&img_type=jpg",
            **kwargs,
        )
