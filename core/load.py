import flet as ft
import core.methods as mt
import core.controls as ct


async def load_group(page: ft.Page):
    dict = await mt.storage(
        page=page,
        mode="r",
        type="s",
        sub_prefix="import_file_",
        key="dict",
        force_out_to_log=False,
    )
    group_list = []
    group_msg_ctrls = {}
    for msg in dict:
        if msg["40027"] not in group_list:
            group_list.append(msg["40027"])
            group_msg_ctrls[msg["40027"]] = []
        msg_type = (
            [msg_segment["45002"] for msg_segment in msg["40800"]["40800"]]
            if isinstance(msg["40800"]["40800"], list)
            else [msg["40800"]["40800"]["45002"]]
        )
        # await mt.log(f"msg_type:{msg_type}")

        # ——判断+渲染逻辑开始——
        if msg_type[0] == 1 and len(msg_type) == 1:
            # 文本消息
            group_msg_ctrls[msg["40027"]].append(
                ct.TextMessage(
                    text=msg["40800"]["40800"]["45101"],
                    page=page,
                    timestamp=msg["40050"],
                    qqnum=msg["40033"],
                    name=msg["40090"] if msg["40090"] else msg["40093"],
                )
            )
        else:
            # 其他消息类型
            group_msg_ctrls[msg["40027"]].append(
                ct.Base(
                    page=page,
                    timestamp=msg["40050"],
                    qqnum=msg["40033"],
                    name=msg["40090"] if msg["40090"] else msg["40093"],
                )
            )

    await mt.log(f"group_list:{group_list}")
    await mt.storage(
        page=page,
        mode="w",
        sub_prefix="group_",
        key="list",
        value=group_list,
    )
    await mt.storage(
        page=page,
        mode="w",
        sub_prefix="group_",
        key="ctrls",
        value=group_msg_ctrls,
    )
