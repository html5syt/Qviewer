import sys
from core.config import ConfigApp

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
    import flet_easy as fs
app = fs.FletEasy(route_init="/")

# 导入view，用于注册路由
import views.home
import views.set

# 导入向导
import views.viewer
import views.viewer.group
import views.welcome
import views.import_wiz.import_web
if not sys.platform == "emscripten":
    import views.import_wiz.import_file

    app.add_routes(
        [
            fs.Pagesy(
                "/import/choose",
                views.import_wiz.import_file.choose,
                title="Qviewer | 导入向导-选择文件",
            ),
        ]
    )


# We define the routes of the application.
app.add_routes(
    [
        fs.Pagesy("/", views.home.home, title="Qviewer | 首页"),
        fs.Pagesy("/welcome", views.welcome.welcome, title="Qviewer | 欢迎"),
        fs.Pagesy(
            "/import/import_web",
            views.import_wiz.import_web.choose,
            title="Qviewer | 导入向导-手动导入JSON",
        ),
        fs.Pagesy("/set", views.set.set_page, title="Qviewer | 设置"),
        fs.Pagesy("/group/{group_id}", views.viewer.group.group),
    ]
)
# We load the application configuration.
ConfigApp(app)

# We run the application
app.run()
