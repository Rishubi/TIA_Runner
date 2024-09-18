# TIA_Runner
本仓库包含[生成式 AI 应用竞赛：面向工业软件的代码生成](https://www.biendata.xyz/competition/siemens-ai/)的自动评测代码。SCL 代码示例为示例15题。

## 代码说明
- `test.py`: 程序入口，指定待测试代码的名称与路径
- `auto_test.py`: 自动操作 TIA Portal 软件并返回测试结果
- `problems.py`: 题目的基本信息
- `check.py`: 从软件输出中提取编译/运行信息
- `locator`: TIA Portal 软件不同运行阶段的显示内容，供`auto_test.py`识别
- `cases`: 示例 SCL 代码

## 准备
- 将`TIA Portal`目录下的项目文件导入 TIA Portal 软件
- 将`locator`目录下所有图片替换为软件每个阶段在自己电脑上的显示内容（可以参考`auto_test.py`中的测试流程）

## 运行
- 在 TIA Portal 中打开项目，**手动展开左侧菜单的“TestProject->PLC_3->外部源文件”项**（否则无法导入外部文件），保持软件启动
- 在`test.py`中设置待测 SCL 代码的名称与路径
- 运行`test.py`以评测代码
