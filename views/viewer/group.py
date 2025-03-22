import flet as ft
import flet_easy as fs
import core.controls as ct
import core.methods as mt
import asyncio
import sys


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

    # msg_ctrls = await mt.storage(
    #     page=page,
    #     mode="r",
    #     sub_prefix="group_",
    #     key="ctrls",
    # )
    # # mainview.controls = msg_ctrls[int(group_id)]
    # async def load_progressly():
    #     nonlocal mainview
    #     for i,ctrls in enumerate(msg_ctrls[int(group_id)]):
    #         mainview.controls.append(ctrls)
    #         # send page to a page
    #         if i % 500 == 0:
    #             page.update()
    #     # send the rest to a page
    #     page.update()
    #     mainview.auto_scroll=False
    # load_task=mt.run_task(load_progressly())

    # await load_messang(group_id, page, mainview)


    return ct.ViewWithStartHandler(
        controls=[mainview],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
        start_handler=mt.run_task(load_message(group_id, page, mainview))
    )

async def load_message(group_id, page, mainview):
    msg_ctrls = await mt.storage(
        page=page,
        mode="r",
        sub_prefix="group_",
        key="ctrls",
    )

    async def load_progressly():
        nonlocal mainview
        group = msg_ctrls[int(group_id)]
        batch_size = 1500  # 推荐初始值
        total = len(group)
        
        for start in range(0, total, batch_size):
            # 批量扩展控件
            mainview.controls.extend(group[start:start + batch_size])
            
            # 非阻塞更新并让出事件循环
            await page.update_async()
            if start % (batch_size * 3) == 0:  # 每3批次主动让出
                await asyncio.sleep(0)
        
        # 最终设置
        mainview.auto_scroll = False
        await page.update_async()

    if sys.platform != "emscripten":
        from concurrent.futures import ThreadPoolExecutor

        async def threaded_loader():
            loop = asyncio.get_running_loop()
            executor = ThreadPoolExecutor()
            group = msg_ctrls[int(group_id)]
            batch_size = 3000
            
            # 生成批次索引
            batches = range(0, len(group), batch_size)
            
            # 并行处理数据分片
            futures = [
                loop.run_in_executor(
                    executor,
                    lambda s=start: group[s:s + batch_size]
                ) for start in batches
            ]
            
            # 异步获取并更新UI
            for future in asyncio.as_completed(futures):
                batch = await future
                # 通过线程安全方式更新控件
                def update_ui(batch):
                    mainview.controls.extend(batch)
                    page.update()
                
                # 将UI操作提交到主线程事件循环
                await loop.run_in_executor(
                    None, 
                    lambda: loop.call_soon_threadsafe(
                        lambda: update_ui(batch)
                ))
                
                # 轻量级更新触发
                try:await page.update_async()
                except:pass
            
            # 最终设置
            def final_update():
                mainview.auto_scroll = False
                page.update()
            await loop.run_in_executor(None, final_update)

        load_task = mt.run_task(threaded_loader())
    else:
        load_task = mt.run_task(load_progressly())
