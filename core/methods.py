import flet as ft
import datetime
from os import getenv, path


async def log(msg, page=ft.Page):
    print(f"[Log-{datetime.datetime.now()}]{msg}")
    if await storage(
        page=page, sub_prefix="settings_", key="debug_mode", mode="s", type="c"
    ):
        if (
            await storage(
                page=page, sub_prefix="settings_", key="debug_mode", mode="r", type="c"
            )
            == "true"
        ):
            page.open(ft.SnackBar(ft.Text(f"[Log-{datetime.datetime.now()}]{msg}"),duration=2**30))


async def storage(
    page: ft.Page,
    key="",
    value=None,
    type="s",
    mode="r",
    prefix="qviewer_",
    sub_prefix="storage_",
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
                raise LookupError("Key not found in session storage")
        elif mode == "w":
            page.session.set(key, value)
        elif mode == "d":
            if page.session.contains_key(key):
                page.session.remove(key)
            else:
                raise LookupError("Key not found in session storage")
        elif mode == "s":
            if page.session.contains_key(key):
                return True
            else:
                return False
        await log(f"{key}值为: {page.session.get(key)}", page=page)
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
            await log(f"{key}值为: {page.session.get(key)}", page=page)
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
