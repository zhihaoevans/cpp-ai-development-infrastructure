# 开发环境与构建

## 为什么影响 AI 自动化

代理需要明确编译器、构建选项和依赖；同一变更如果在本地与 CI 使用不同配置，验证结果难以复现。

## 最小清单

- 记录支持的操作系统、架构、C++ 标准、编译器和构建工具版本。
- 依赖使用可追溯的版本或锁文件；写明镜像、缓存和离线限制。
- 统一配置、构建与测试入口；支持干净构建和增量构建。
- CMake 项目可开启 `CMAKE_EXPORT_COMPILE_COMMANDS` 以支持 clangd 和静态分析。
- 容器镜像、系统软件源和编译器都需要版本管理；仅写容器名称不等于环境完全可复现。
- 本地与 CI 尽可能执行相同命令，记录平台和工具版本，升级时做兼容性验证。

## CMake 示例

本仓库示例在 `examples/packet-parser`。从仓库根目录执行：

```sh
cmake -S examples/packet-parser -B build/packet-parser -DCMAKE_BUILD_TYPE=Debug
cmake --build build/packet-parser
ctest --test-dir build/packet-parser --output-on-failure
```

大型项目可增加 CMake Presets，描述构建类型、生成器、编译器和 sanitizer；具体编译器路径不要写死到共享配置。不同平台和 ABI 应分开构建目录。失败先保存完整命令、版本和日志，再决定是否清理缓存。

## 依赖管理选择

根据项目使用系统包、vcpkg、Conan 或已固定版本的源码依赖；确认许可、来源、升级策略和安全维护责任。不要把临时下载的未校验脚本或机密凭据写入仓库。
