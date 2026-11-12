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
