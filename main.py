import sys

from core.config import ConfigApp
import flet as ft

import flet_easy as fs

app = fs.FletEasy(route_init="/")

# 导入view，用于注册路由
import views.home
import views.set

# 导入向导
import views.viewer
import views.viewer.group
import views.welcome
# import views.import_wiz.import_web
import views.import_wiz.choose
import views.import_wiz.db_config

app.add_routes(
    [
        fs.Pagesy(
            "/import/choose",
            views.import_wiz.choose.choose,
            title="Qviewer | 导入向导-选择文件",
        ),
        fs.Pagesy(
            "/import/db_config",
            views.import_wiz.db_config,
            title="Qviewer | 导入向导-数据库配置",
        ),
    ]
)


# We define the routes of the application.
app.add_routes(
    [
        fs.Pagesy("/", views.home.home, title="Qviewer | 首页"),
        fs.Pagesy("/welcome", views.welcome.welcome, title="Qviewer | 欢迎"),
        fs.Pagesy("/set", views.set.set_page, title="Qviewer | 设置"),
        fs.Pagesy("/group/{group_id}", views.viewer.group.group),
    ]
)




# We load the application configuration.
ConfigApp(app)

# We run the application
app.run()

# ft.app(app.get_app())

