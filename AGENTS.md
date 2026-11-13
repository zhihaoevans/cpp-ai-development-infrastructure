# 仓库协作指南

本仓库是 C++ AI 开发基础设施的中文指南，`docs/` 存放说明，`examples/packet-parser/` 存放演示项目。

修改指南时，区分已实现的能力与建议配置；示例中的命令须与实际文件保持一致。不得将本仓库说明性的配置当作已启用的 GitHub 分支保护或真实硬件测试。

示例验证（需要 CMake >= 3.20 和 C++17 编译器）：

```sh
cmake -S examples/packet-parser -B build/packet-parser -DCMAKE_BUILD_TYPE=Debug
cmake --build build/packet-parser
ctest --test-dir build/packet-parser --output-on-failure
```

修改解析器时关注截断、输入边界及字节序；必要时增加回归测试。反馈说明执行过的命令、结果及无法验证的部分。

编码前阅读 [公共规范](docs/coding-standards.md) 及对应语言指南。当前示例为 C++17；C 指南尚无纯 C 编译验证。

质量检查需要 Python >= 3.9、clang-format 18 和 clang-tidy 18（可通过 `CLANG_FORMAT` / `CLANG_TIDY` 指定路径）：

```sh
python3 scripts/check_quality.py format
python3 scripts/check_quality.py tidy --build-dir build/packet-parser
```

静态分析需要先按上述 CMake 命令生成编译数据库。格式修复使用 `python3 scripts/check_quality.py format --fix`，随后重新构建并测试；不要关闭规则来掩盖错误。命名、所有权和错误语义仍需人工审查。
