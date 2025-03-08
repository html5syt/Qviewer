# # from typing import Dict

# # import flet
# # from flet import (
# #     Column,
# #     ElevatedButton,
# #     FilePicker,
# #     FilePickerResultEvent,
# #     FilePickerUploadEvent,
# #     FilePickerUploadFile,
# #     Page,
# #     ProgressRing,
# #     Ref,
# #     Row,
# #     Text,
# #     icons,
# # )

# # secret_key = "secret_key"
# # def main(page: Page):
# #     prog_bars: Dict[str, ProgressRing] = {}
# #     files = Ref[Column]()
# #     upload_button = Ref[ElevatedButton]()

# #     def file_picker_result(e: FilePickerResultEvent):
# #         upload_button.current.disabled = True if e.files is None else False
# #         prog_bars.clear()
# #         files.current.controls.clear()
# #         if e.files is not None:
# #             for f in e.files:
# #                 prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
# #                 prog_bars[f.name] = prog
# #                 files.current.controls.append(Row([prog, Text(f.name)]))
# #         page.update()

# #     def on_upload_progress(e: FilePickerUploadEvent):
# #         prog_bars[e.file_name].value = e.progress
# #         prog_bars[e.file_name].update()

# #     file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

# #     def upload_files(e):
# #         uf = []
# #         if file_picker.result is not None and file_picker.result.files is not None:
# #             for f in file_picker.result.files:
# #                 uf.append(
# #                     FilePickerUploadFile(
# #                         f.name,
# #                         upload_url=page.get_upload_url(f.name, 600),
# #                     )
# #                 )
# #             file_picker.upload(uf)

# #     # hide dialog in a overlay
# #     page.overlay.append(file_picker)

# #     page.add(
# #         ElevatedButton(
# #             "Select files...",
# #             icon=icons.FOLDER_OPEN,
# #             on_click=lambda _: file_picker.pick_files(allow_multiple=True),
# #         ),
# #         Column(ref=files),
# #         ElevatedButton(
# #             "Upload",
# #             ref=upload_button,
# #             icon=icons.UPLOAD,
# #             on_click=upload_files,
# #             disabled=True,
# #         ),
# #     )


# # flet.app(target=main, upload_dir="uploads", view=flet.WEB_BROWSER)

# import flet as ft

# class Data:
#     def __init__(self) -> None:
#         self.counter = 0

# d = Data()

# def main(page):

#     page.snack_bar = ft.SnackBar(
#         content=ft.Text("Hello, world!"),
#         action="Alright!",
#     )

#     def on_click(e):
#         page.snack_bar = ft.SnackBar(ft.Text(f"Hello {d.counter}"))
#         page.snack_bar.open = True
#         d.counter += 1
#         page.update()

#     page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))

# ft.app(target=main)


import flet as ft


def main(page: ft.Page):
    counter = 0

    def on_click(e):
        # nonlocal counter
        # page.open(ft.SnackBar(ft.Text(f"CounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounter\nCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounterCounter value at")))
        # counter += 1
        # page.update()
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Row(
                [
                    ft.ProgressRing(),
                    ft.Text("正在转换JSON为字典..."),
                ]
            ),
        )
        page.open(dialog)

    page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))


ft.app(target=main)