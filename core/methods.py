import flet as ft
import datetime
import asyncio
import traceback
from os import getenv, path


async def log(msg, page=ft.Page):
    print(f"[Log-{datetime.datetime.now()}]{msg}")
    try:

        if (
                await storage(
                    page=page,
                    sub_prefix="settings_",
                    key="debug_mode",
                    mode="r",
                    type="c",
                )
                == "true"
            ):
            try:
                if len(msg if msg else "") <= 500:
                    page.open(
                            ft.SnackBar(
                                ft.ListView(
                                    [ft.Text(f"[Log-{datetime.datetime.now()}]{msg}")]
                                ),
                                duration=60000,
                                dismiss_direction=ft.DismissDirection.END_TO_START,
                            )
                        )
                else:
                    await info(f"[Log-{datetime.datetime.now()}]{msg}", page=page)
            except:
                await info(f"[Log-{datetime.datetime.now()}]{msg}", page=page)
    except Exception as e:
        # print(f"[Error-{datetime.datetime.now()}]{traceback.format_exc()}")
        # print(f"[Error-{datetime.datetime.now()}]页面可能未初始化")
        pass


async def error(message: str, on_close=None, page=ft.Page) -> ft.AlertDialog:
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
                ft.Text("错误", color=ft.Colors.RED),
            ]
        ),
        content=ft.Column([ft.Text(message)], scroll="auto"),
        on_dismiss=on_close,
    )

    def on_close_default(e):
        page.close(dialog)

    dialog.actions = [
        ft.TextButton("关闭", on_click=on_close or on_close_default),
    ]
    page.open(dialog)
    return dialog


async def info(message: str, on_close=None, page=ft.Page) -> ft.AlertDialog:
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE),
                ft.Text("提示", color=ft.Colors.BLUE),
            ]
        ),
        content=ft.Column([ft.Text(message)], scroll="auto"),
        on_dismiss=on_close,
    )

    def on_close_default(e):
        page.close(dialog)

    dialog.actions = [
        ft.TextButton("关闭", on_click=on_close or on_close_default),
    ]
    page.open(dialog)
    return dialog


async def storage(
    page: ft.Page,
    key="",
    value=None,
    type="s",
    mode="r",
    prefix="qviewer_",
    sub_prefix="storage_",
    force_out_to_log=False,
):
    """存储数据，默认使用 session 存储，模式为读取，前缀为 qviewer_
    Args:
        key (str): 键
        value (_type_): 值
        type (str, optional): c为持久缓存，s为session缓存，DEL为清空（仅用于调试！），默认c.
        mode (str, optional): r为读取，w为写入，d为删除,s为查询是否存在，默认r.
        prefix (str, optional): 前缀.
        sub_prefix (str, optional): 子前缀.
    """

    key = prefix + sub_prefix + key
    if type == "s":
        if mode == "r":
            if page.session.contains_key(key):
                return page.session.get(key)
            else:
                return None
        elif mode == "w":
            page.session.set(key, value)
        elif mode == "d":
            if page.session.contains_key(key):
                page.session.remove(key)
            else:
                return None
        elif mode == "s":
            if page.session.contains_key(key):
                return True
            else:
                return False
        (
            await log(f"{key}值为: {page.session.get(key)}", page=page)
            if len(str(page.session.get(key))) <= 500 or force_out_to_log
            else await log(
                f"{key}值有: {len(str(page.session.get(key)))}个字符", page=page
            )
        )
    elif type == "c":
        if mode == "r":
            if await page.client_storage.contains_key_async(key):
                temp = await page.client_storage.get_async(key)
                return temp
            else:
                raise LookupError("Key not found in client storage")
        elif mode == "w":
            await page.client_storage.set_async(key, value)
        elif mode == "d":
            if await page.client_storage.contains_key_async(key):
                page.client_storage.remove(key)
            else:
                raise LookupError("Key not found in client storage")
            (
                await log(
                    f"{key}值为: {await page.client_storage.get_async(key)}", page=page
                )
                if len(str(await page.client_storage.get_async(key))) <= 500
                or force_out_to_log
                else await log(
                    f"{key}值有: {len(str(await page.client_storage.get_async(key)))}个字符",
                    page=page,
                )
            )
        elif mode == "s":
            if await page.client_storage.contains_key_async(key):
                return True
            else:
                return False
    elif type == "DEL":
        await page.client_storage.clear_async()
        page.session.clear()


class GetEnv:
    def get_env(name) -> str:
        """获取环境变量"""
        try:
            return getenv(name)
        except:
            raise ValueError(f"环境变量{name}不存在")

    def get_app_data_path() -> str:
        """获取应用数据目录"""
        return getenv("FLET_APP_STORAGE_DATA")

    def get_app_temp_path() -> str:
        """获取本地应用数据目录"""
        return getenv("FLET_APP_STORAGE_TEMP")


def path_process(is_stroage: bool, filename: str) -> str:
    if is_stroage:
        return path.join(GetEnv.get_app_data_path(), filename)
    else:
        return path.join(GetEnv.get_app_temp_path(), filename)


def run_task(func):
    return asyncio.get_running_loop().create_task(func)
