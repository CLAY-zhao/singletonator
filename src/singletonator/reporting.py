import json
import webbrowser

from .color_util import COLOR


def generate_html_report(json_data, output_file="crash_report.html", do_open=True):
    """
    将 JSON 数据中的 stack_trace 转换为 ElementUI 表格，并生成静态 HTML 文件。
    
    :param json_data: 包含 stack_trace 的 JSON 数据
    :param output_file: 输出的 HTML 文件名
    """
    # 提取 stack_trace 数据
    stack_trace = json_data.get("stack_trace", [])
    exception = json_data.get("exception", "Unknown error")

    # 构建 ElementUI 表格数据
    table_data = []
    for frame in stack_trace:
        table_data.append({
            "filename": frame.get("filename", ""),
            "lineno": frame.get("lineno", ""),
            "function": frame.get("function", ""),
            "code": frame.get("code", ""),
            "is_exception_frame": frame.get("is_exception_frame", False)
        })

    # 构建完整的 HTML 页面
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crash Report</title>
        <!-- 引入 ElementUI 样式 -->
        <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                color: #d32f2f;
            }}
            .el-table .highlight-row {{
                background-color: #fff3e0; /* 高亮橙色 */
            }}
            .el-table .light-row {{
                background-color: #f5f5f5; /* 淡灰色 */
            }}
            .icon-true {{
                color: #409EFF; /* 蓝色 */
            }}
            .icon-false {{
                color: #F56C6C; /* 红色 */
            }}
        </style>
    </head>
    <body>
        <div id="app">
            <h1>Crash Report</h1>
            <h2>Exception: {exception}</h2>
            <el-table
                :data="tableData"
                style="width: 100%"
                :row-class-name="tableRowClassName"
                border
            >
                <el-table-column type="index" width="50"></el-table-column>
                <el-table-column prop="filename" label="Filename"></el-table-column>
                <el-table-column prop="lineno" label="Line Number" width="120"></el-table-column>
                <el-table-column prop="function" label="Function" width="200"></el-table-column>
                <el-table-column prop="code" label="Code"></el-table-column>
                <el-table-column label="Is Exception Frame" width="150">
                    <template slot-scope="scope">
                        <i
                            :class="scope.row.is_exception_frame ? 'el-icon-success icon-true' : 'el-icon-error icon-false'"
                        ></i>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 引入 Vue.js -->
        <script src="https://unpkg.com/vue@2.6.14/dist/vue.min.js"></script>
        <!-- 引入 ElementUI -->
        <script src="https://unpkg.com/element-ui/lib/index.js"></script>
        <script>
            new Vue({{
                el: '#app',
                data() {{
                    return {{
                        tableData: {json.dumps(table_data)}
                    }};
                }},
                methods: {{
                    tableRowClassName({{ row }}) {{
                        return row.is_exception_frame ? 'highlight-row' : 'light-row';
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    # 将 HTML 内容写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    COLOR.green(f"HTML report generated: {output_file}")

    if do_open:
        webbrowser.open(output_file)
