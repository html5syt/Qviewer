import flet as ft
import flet_easy as fs
import core.controls as ct
import core.methods as mt
import asyncio



class GroupState:
    loading = False
    loaded_count = 0
    all_loaded = False
    page_ready = False


async def group(data: fs.Datasy, group_id: str):
    page = data.page
    state = GroupState()

    async def navbar_click(e: ft.ControlEvent):
        if e.data == "0":
            data.page.go("/")
        else:
            group_list = await mt.storage(
                page=page, mode="r", sub_prefix="group_", key="list"
            )
            data.page.go(f"/group/{group_list[int(e.data)-1]}") if group_list else None

    page.title = "Qviewer | 群: " + group_id

    # 初始化UI组件
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

    # 加载群组列表到导航栏
    if await mt.storage(page=page, mode="s", sub_prefix="group_", key="list"):
        group_list = await mt.storage(
            page=page, mode="r", sub_prefix="group_", key="list"
        )
        for idx, group_id_temp in enumerate(group_list):
            drawer.controls.append(ft.NavigationDrawerDestination(label=group_id_temp))
            if group_id_temp == group_id:
                drawer.selected_index = idx + 1  # +1因为前面有首页和分隔线
            appbar.actions[1].items.append(
                ft.PopupMenuItem(
                    text=group_id_temp, on_click=data.go(f"/group/{group_id_temp}")
                )
            )
        page.update()

    # 主消息视图和进度条
    progress_bar = ft.ProgressBar(visible=False)
    mainview = ft.ListView(expand=True, spacing=10, reverse=True)

    # 获取消息数据
    msg_ctrls = await mt.storage(page=page, mode="r", sub_prefix="group_", key="ctrls")
    group_msgs = msg_ctrls.get(group_id, []) if msg_ctrls else []
    total_messages = len(group_msgs)
    batch_size = 100

    # 初始加载
    initial_batch = group_msgs[:batch_size]
    mainview.controls.extend(initial_batch)
    state.loaded_count = len(initial_batch)
    state.all_loaded = state.loaded_count >= total_messages

    async def load_messages():
        if state.loading or state.all_loaded or not state.page_ready:
            return

        state.loading = True
        progress_bar.visible = True
        progress_bar.value = 0
        page.update()

        current_batch = min(batch_size, total_messages - state.loaded_count)
        for i in range(current_batch):
            # 添加单条消息
            mainview.controls.append(group_msgs[state.loaded_count + i])

            # 更新进度条
            progress_bar.value = (i + 1) / current_batch
            if i % 10 == 0:  # 每10条更新一次UI以平衡性能
                page.update()

        state.loaded_count += current_batch
        state.all_loaded = state.loaded_count >= total_messages

        # 完成当前批次加载
        progress_bar.visible = False
        progress_bar.value = 0
        page.update()
        state.loading = False

    def on_scroll(e: ft.OnScrollEvent):
        if (
            e.pixels <= 100
            and not state.loading
            and not state.all_loaded
            and state.page_ready
        ):
            mt.run_task_ori(page.loop, load_messages())

    mainview.on_scroll = on_scroll

    # 页面布局
    view = ft.Column([progress_bar, mainview], expand=True)

    async def on_page_ready():
        state.page_ready = True
        page.update()

    return ct.ViewWithStartHandler(
        controls=[view],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
        start_handler=mt.run_task(on_page_ready()),
    )
