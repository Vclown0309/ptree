# ptree - 目录树显示工具

一个简洁高效的目录树结构显示工具，支持自定义深度、排除文件、筛选类型及多语言切换，帮助你快速可视化目录结构。

## 功能特点

- **多语言支持**：内置中英文双语，可通过配置默认语言
- **颜色区分**：目录和文件以不同颜色显示（需安装colorama）
- **灵活筛选**：支持按文件类型筛选（如仅显示`.txt`、`.py`文件）
- **配置持久化**：保存默认颜色模式和语言设置到配置文件
- **友好交互**：Ctrl+C中断时可选择继续或终止，错误提示清晰
- **跨平台兼容**：自动适配Windows、Linux和macOS的控制台编码

## 安装说明

1. 克隆或下载本项目
2. 安装依赖（颜色显示需要）：
   ```bash
   pip install colorama
   ```
   
   > 或者直接 在项目目录下`pip install -r requirements`

## 使用方法

### 基本用法

```bash
# 显示当前目录的目录树（默认深度3）
python ptree.py

# 显示指定目录的目录树
python ptree.py /path/to/directory
```

### 常用参数

| 参数              | 说明                         | 示例                                            |
| ----------------- | ---------------------------- | ----------------------------------------------- |
| `-d, --depth`     | 设置最大遍历深度             | `python ptree.py -d 2`（只显示 2 层）           |
| `-e, --exclude`   | 排除指定名称的文件 / 目录    | `python ptree.py -e __pycache__ .git`           |
| `-t, --types`     | 只显示指定类型的文件         | `python ptree.py -t py txt`（只显示.py 和.txt） |
| `-n, --no-color`  | 禁用颜色显示（使用文本标识） | `python ptree.py -n`                            |
| `-c, --set-color` | 设置默认颜色模式（on/off）   | `python ptree.py -c off`（默认禁用颜色）        |
| `-l, --set-lang`  | 设置默认语言（zh/en）        | `python ptree.py -l en`（默认英文）             |
| `-v, --version`   | 显示版本信息                 | `python ptree.py -v`                            |

## 配置文件

配置文件位于 `~/.ptree/config.json`，内容示例：

```json
{
  "use_color": true,
  "language": "zh"
}
```

可通过`--set-color`和`--set-lang`参数修改，也可直接编辑该文件。

## 注意事项

- Windows 系统若颜色显示异常，可按程序提示修改注册表启用 ANSI 支持
- 无 colorama 库时会自动降级为文本标识模式（[目录]/[文件]）
- 目录遍历遇到权限问题时会显示`[权限不足]`提示，不中断程序