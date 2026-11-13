# C/C++ 编码规范与检查

本规范适用于仓库自有的 C/C++ 示例代码。当前可运行示例使用 C++17；[C 规范](c-coding-guidelines.md)是供 C 项目采用的建议，尚无纯 C 构建或 CI 验证。C++ 规则见 [C++ 规范](cpp-coding-guidelines.md)。移植到其他项目时先确认平台和已有约定。

## 规则等级与例外

- **必须**：新代码及本次修改涉及的代码应满足；不以“工具通过”代替接口正确性。
- **建议**：默认采用；与兼容性或实测性能冲突时，在 PR 中说明取舍。
- **例外**：仅针对具体位置说明原因、影响和验证。不得为消除告警整体关闭检查。必要的 `NOLINTNEXTLINE(check-name)` 应附原因；格式豁免使用成对的 `clang-format off/on` 并说明用途。

本仓库只选取少量静态检查，不宣称完整符合 CERT、MISRA 或 C++ Core Guidelines。

## 公共约定

| 项目 | 约定 | 验证方式 |
|---|---|---|
| 排版 | 必须采用根目录 `.clang-format`；2 空格、100 列目标、左侧指针对齐、控制语句使用大括号 | clang-format 18；大括号另由 clang-tidy 检查 |
| 命名 | 函数、变量、字段用 `snake_case`，C++ 类型用 `PascalCase`，宏用带模块前缀的 `UPPER_SNAKE_CASE` | 审查；暂未启用命名检查 |
| 文件 | C 使用 `.c/.h`，C++ 使用 `.cpp/.hpp`；文件名用 `snake_case` | 审查 |
| 头文件 | 必须可独立包含，直接包含所需声明；实现文件先包含自己的头文件；C 用 include guard，C++ 示例使用 `#pragma once` | 编译与审查 |
| 接口 | 必须说明输入范围、空指针、长度单位、所有权、生命周期、失败及输出状态 | 审查与边界测试 |
| 转换 | 必须检查窄化、符号转换、长度加乘溢出；不能依赖强转使不合法数据变合法 | 审查、警告和测试 |
| 注释 | 解释原因和约束，避免重复代码；协议常量注明单位及来源含义 | 审查 |

```cpp
// 错误：无大括号，后续增添语句容易改变控制流。
if (size < 20) return std::nullopt;

// 正确：先判断可读范围，再访问输入。
if (size < 20) {
  return std::nullopt;
}
```

## 本地与 CI 共用的入口

需要 Python >= 3.9、Git、CMake >= 3.20、C++17 编译器，以及 clang-format **18.x** 和 clang-tidy **18.x**。脚本检查主版本，补丁版本未锁定；升级主版本时单独审查格式差异和诊断变化。

Ubuntu 24.04 安装检查工具：

```sh
sudo apt-get update
sudo apt-get install --yes clang-format-18 clang-tidy-18
```

其他平台安装 LLVM 18，并在需要时指定可执行文件：

```sh
export CLANG_FORMAT=/path/to/llvm18/bin/clang-format
export CLANG_TIDY=/path/to/llvm18/bin/clang-tidy
```

从仓库根目录运行：

```sh
python3 scripts/check_quality.py format
# 仅在需要修改排版时运行：
python3 scripts/check_quality.py format --fix
cmake -S examples/packet-parser -B build/packet-parser -DCMAKE_BUILD_TYPE=Debug
cmake --build build/packet-parser
ctest --test-dir build/packet-parser --output-on-failure
python3 scripts/check_quality.py tidy --build-dir build/packet-parser
```

脚本扫描 `examples/` 下 Git 已跟踪和未忽略的新 C/C++ 文件；格式检查包含头文件，静态分析逐个检查源文件及其包含的项目头文件。新增源文件必须同时加入构建目标；缺失编译数据库条目会失败。独立且未被包含的头文件不会获得静态分析覆盖。数据库生成需要 Makefiles 或 Ninja，其他生成器应另建检查目录。检查失败、工具缺失、版本错误均返回非零状态。

`.clang-tidy` 仅启用分析器、部分高风险错误检查、空指针现代化和控制语句大括号规则，诊断作为错误处理。CI 复用上述脚本；它不会自动修复、证明线程安全或验证真实网卡性能。Sanitizer、纯 C 编译和完整平台矩阵仍属于后续建设。

工具语义参考：[LLVM 18 clang-format](https://releases.llvm.org/18.1.8/tools/clang/docs/ClangFormatStyleOptions.html)、[LLVM 18 clang-tidy](https://releases.llvm.org/18.1.8/tools/clang/tools/extra/docs/clang-tidy/index.html)。

macOS 上独立安装的 clang-tidy 18 可能无法定位 Apple 工具链的标准库，或无法解析较新 SDK 使用的编译器内建函数。请使用与 LLVM 18 兼容的 SDK/标准库，或在 Ubuntu 24.04 环境执行检查；不要通过屏蔽编译错误获得“通过”。
