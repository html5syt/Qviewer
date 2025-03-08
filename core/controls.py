import flet as ft
import flet_easy as fs
from datetime import datetime
from . import methods as mt
import asyncio


class Base(ft.Container):
    def __init__(self, name=None, timestamp=0, avatar=None, **kwargs):
        super().__init__(**kwargs)
        self.avatar = (
            avatar or "https://q.qlogo.cn/headimg_dl?dst_uin=0&spec=640&img_type=jpg"
        )
        self.name = name or "QQ用户"
        self.timestamp = datetime.fromtimestamp(timestamp + 8 * 60 * 60)
        # UTC+8
        self.expanded = True
        self.padding = 0
        self.margin = 0
        try:
            type(self.control)
        except AttributeError:
            self.control = ft.Text(
                r"""错误：未能解析消息""",
                color=ft.Colors.RED,
                # width=100,
                # no_wrap=True,
                # expand=1,
                # width=800,
            )
        self.content = ft.Row(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src=self.avatar,
                    radius=18,
                    # offset=ft.Offset(x=0, y=0.2),
                ),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    self.name,
                                    size=15,
                                ),
                                ft.Text(
                                    str(self.timestamp),
                                    size=12,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=self.control,
                            padding=10,
                            border_radius=ft.border_radius.all(10),
                            bgcolor=ft.Colors.BLUE_100,
                            expand=False,
                            expand_loose=False,
                        ),
                    ]
                ),
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            # scroll=True,
        )
        # self.content = ft.ListTile(
        #     leading=ft.CircleAvatar(
        #         foreground_image_src=self.avatar,
        #         radius=20,
        #         # offset=ft.Offset(x=0, y=0.2),
        #     ),
        #     title=ft.Row(
        #         [
        #             ft.Text(
        #                 self.name,
        #                 size=18,
        #             ),
        #             ft.Text(
        #                 str(self.timestamp),
        #                 size=15,
        #                 color=ft.Colors.GREY,
        #             ),
        #         ],
        #         alignment=ft.alignment.center,
        #     ),
        #     subtitle=ft.Container(
        #         content=self.control,
        #         padding=10,
        #         border_radius=ft.border_radius.all(10),
        #         bgcolor=ft.Colors.BLUE_100,
        #         expand=False,
        #         expand_loose=False,
        #     ),
        #     title_alignment=ft.ListTileTitleAlignment.TOP,
        # )


class TextMessage(Base):
    def __init__(self, text: str, data: fs.Datasy, **kwargs):
        self.data = data
        self.text = text
        self.control = ft.Text(
            self.text,
            color=ft.Colors.BLACK,
            selectable=True,
            size=14,
        )
        if len(self.text)*14 >= data.page.width/0.78:
            self.control.width = data.page.width*0.78
        # data.page.on_resized = self.on_resize(data)
        # data.page.run_task(self.on_resize, data)
        qqnum = 10001
        super().__init__(
            avatar=f"https://q.qlogo.cn/headimg_dl?dst_uin={qqnum}&spec=640&img_type=jpg"
        )
    # async def on_resize(self, data: fs.Datasy):
    #     # mt.log("on_resize")
    #     while True:
    #         mt.log(data.page.width)
    #         mt.log(self.control.width)
    #         if len(max((line.strip() for line in self.text)))*14 >= data.page.width/0.78:
    #             self.control.width = data.page.width*0.77
    #         else:
    #             self.control.width = None
    #         await asyncio.sleep(0.01)
