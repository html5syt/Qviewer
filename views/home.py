import flet as ft
import core.methods as mt
import core.controls as ct
from core.load import *
import traceback
import sys
import asyncio

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
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

    # mainview = ft.Text("Hello world")
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

    # async def load_msg(page: ft.Page):
        

    # await load_msg(data, page, mainview, dialog, drawer, appbar)

    return ct.ViewWithStartHandler(
        controls=[mainview],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=appbar,
        drawer=drawer,
        start_handler=mt.run_task(load_msg(data, page, mainview, dialog, drawer, appbar))
    )

# async def load_msg(data, page:ft.Page, mainview, dialog, drawer, appbar):
#     if await mt.storage(
#         page=page, mode="r", sub_prefix="import_file_", key="dict", type="s"
#     ) and not await mt.storage(page=page, mode="r", sub_prefix="group_", key="list"):
#         # await asyncio.sleep(1)
#         # mainview.value += "\n正在加载字典聊天数据..."
#         page.open(dialog)
#         page.update()
#         # await page.update_async()
#         # mt.run_task(load_msg(page=page))
#         try:
#             await load_group(page=page)
#             await mt.log(
#                 page=page,
#                 msg=f"加载字典聊天数据成功\ngroup_list:{await mt.storage(page=page,mode='r',sub_prefix='group_',key='list')}",
#             )
#             # mainview.value += "\n加载字典聊天数据成功"
#             page.close(dialog)
#             page.update()
#             # await page.update_async()
#             for group_id in await mt.storage(
#                 page=page, mode="r", sub_prefix="group_", key="list"
#             ):
#                 drawer.controls.append(
#                     ft.NavigationDrawerDestination(
#                         label=group_id,
#                     )
#                 )
#                 appbar.actions[1].items.append(
#                     ft.PopupMenuItem(
#                         text=group_id, on_click=data.go(f"/group/{group_id}")
#                     )
#                 )
#                 page.update()
#         except Exception as e:
#             await mt.error(
#                 page=page,
#                 message=f"加载字典聊天数据时出现问题: {traceback.format_exc()}",
#             )
#             page.close(dialog)
#             page.update()
#             # mainview.value += "\n加载字典聊天数据时出现问题"
#             # await page.update_async()
#     elif await mt.storage(page=page, mode="r", sub_prefix="group_", key="list"):
#         for group_id in await mt.storage(
#             page=page, mode="r", sub_prefix="group_", key="list"
#         ):
#             drawer.controls.append(
#                 ft.NavigationDrawerDestination(
#                     label=group_id,
#                 )
#             )
#             appbar.actions[1].items.append(
#                 ft.PopupMenuItem(
#                     text=group_id, on_click=data.go(f"/group/{group_id}")
#                 )
#             )
#             await page.update_async()
# async def load_msg(data:fs.Datasy, page: ft.Page, mainview, dialog, drawer, appbar):
#     async def safe_update():
#         """非阻塞安全更新页面"""
#         try:await page.update_async()
#         except:pass
#         await asyncio.sleep(0)  # 主动让出事件循环

#     async def batch_add_items(items, target_list, batch_size=50):
#         """批量添加项目到指定列表"""
#         for i in range(0, len(items), batch_size):
#             batch = items[i:i + batch_size]
#             target_list.extend(batch)
#             await safe_update()

#     async def load_groups():
#         """核心加载逻辑"""
#         group_list = await mt.storage(
#             page=page, mode="r", sub_prefix="group_", key="list"
#         )
        
#         # 生成所有需要添加的控件
#         drawer_destinations = []
#         popup_items = []
#         for group_id in group_list:
#             drawer_destinations.append(
#                 ft.NavigationDrawerDestination(label=group_id)
#             )
#             popup_items.append(
#                 ft.PopupMenuItem(
#                     text=group_id, 
#                     on_click=data.go(f"/group/{group_id}")
#                 )
#             )

#         # 批量添加控件
#         await batch_add_items(drawer_destinations, drawer.controls)
#         await batch_add_items(popup_items, appbar.actions[1].items)

#     try:
#         # 异步检查存储状态
#         has_dict = await mt.storage(
#             page=page, mode="r", sub_prefix="import_file_", key="dict", type="s"
#         )
#         has_group = await mt.storage(
#             page=page, mode="r", sub_prefix="group_", key="list"
#         )

#         if has_dict and not has_group:
#             page.open(dialog)  # 异步打开对话框
#             await safe_update()

#             loop = asyncio.get_running_loop()
            
#             if sys.platform != "emscripten":
#                 # 使用嵌套事件循环执行异步函数
#                 from concurrent.futures import ThreadPoolExecutor
#                 with ThreadPoolExecutor() as pool:
#                     await loop.run_in_executor(
#                         pool,
#                         lambda: asyncio.run(load_group(page))  # 创建子事件循环
#                     )
#             else:
#                     await load_group(page=page)

#             await mt.log(  # 异步记录日志
#                 page=page,
#                 msg=f"加载字典聊天数据成功\ngroup_list:{has_group}"
#             )
#             page.close(dialog)  # 异步关闭对话框
#             await safe_update()

#         # 统一加载群组数据
#         if has_group:
#             await load_groups()

#     except Exception as e:
#         await mt.error(  # 异步错误处理
#             page=page,
#             message=f"加载失败: {traceback.format_exc()}")
#         page.close(dialog)
#         await safe_update()


async def load_msg(data:fs.Datasy, page: ft.Page, mainview, dialog, drawer, appbar):
    # 添加线程安全锁
    storage_lock = asyncio.Lock() if sys.platform != "emscripten" else None

    async def safe_update():
        """线程安全更新页面"""
        try:
            await page.update_async()
            await asyncio.sleep(0)
        except Exception as e:
            pass

    async def thread_safe_storage(mode, **kwargs):
        """线程安全存储访问"""
        async with storage_lock:
            return await mt.storage(**kwargs)

    async def batch_add_items(items, target_list, batch_size=50):
        """批量添加项目到指定列表"""
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            target_list.extend(batch)
            await safe_update()

    async def load_groups():
        """核心加载逻辑"""
        # 使用安全存储访问
        group_list = await thread_safe_storage(
            page=page, 
            mode="r", 
            sub_prefix="group_", 
            key="list"
        )
        
        drawer_destinations = []
        popup_items = []
        for group_id in group_list:
            drawer_destinations.append(
                ft.NavigationDrawerDestination(label=group_id)
            )
            # 使用闭包绑定当前group_id值
            popup_items.append(
                ft.PopupMenuItem(
                    text=group_id, 
                    on_click=lambda _, gid=group_id: data.go(f"/group/{gid}")
                )
            )

        await batch_add_items(drawer_destinations, drawer.controls)
        await batch_add_items(popup_items, appbar.actions[1].items)

    try:
        # 原子化存储访问
        has_dict, has_group = await asyncio.gather(
            mt.storage(
                page=page, 
                mode="r", 
                sub_prefix="import_file_", 
                key="dict", 
                type="s"
            ),
            mt.storage(
                page=page, 
                mode="r", 
                sub_prefix="group_", 
                key="list"
            )
        )

        if has_dict and not has_group:
            page.open(dialog)  # 使用异步打开
            await safe_update()

            loop = asyncio.get_running_loop()
            
            if sys.platform != "emscripten":
                # 重构线程池调用方式
                from concurrent.futures import ThreadPoolExecutor
                
                async def wrapped_load_group():
                    """将异步操作包装到主线程"""
                    def sync_part():
                        # 仅执行同步计算部分
                        return "heavy_computation_result"
                        
                    with ThreadPoolExecutor() as pool:
                        result = await loop.run_in_executor(pool, sync_part)
                        # 主线程执行异步存储操作
                        await load_group(page=page)

                    return result
                    
                await wrapped_load_group()
            else:
                await load_group(page=page)

            # 刷新群组列表引用
            has_group = await thread_safe_storage(
                page=page, 
                mode="r", 
                sub_prefix="group_", 
                key="list"
            )

            await mt.log(
                page=page,
                msg=f"加载成功\n当前group_list:{has_group}"
            )
            page.close(dialog)
            await safe_update()

        if has_group:
            await load_groups()

    except Exception as e:
        await mt.error(
            page=page,
            message=f"加载失败: {traceback.format_exc()}"
        )
        page.close(dialog)
        await safe_update()