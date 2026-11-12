# IPv4 头部解析示例

最小、无第三方依赖的 C++17 示例，用于演示构建、测试和边界验证。只读取 IPv4 固定头中的版本、IHL 和 total length，并验证输入含有完整头及 IP 数据报；不验证校验和、分片语义或传输层协议，不适合作为生产解析器。

从仓库根目录执行：

```sh
cmake -S examples/packet-parser -B build/packet-parser -DCMAKE_BUILD_TYPE=Debug
cmake --build build/packet-parser
ctest --test-dir build/packet-parser --output-on-failure
```

要求 CMake >= 3.20 与 C++17 编译器。支持直接编译测试：

```sh
g++ -std=c++17 -Wall -Wextra -Wpedantic -Iexamples/packet-parser/include examples/packet-parser/src/ipv4.cpp examples/packet-parser/tests/ipv4_test.cpp -o /tmp/ipv4_test
/tmp/ipv4_test
```

验证包括合法报文、空/截断输入、版本错误、头长度错误、total length 小于头长、数据报截断和字节序。函数读取调用者拥有的 buffer，不保留指针，也不修改输入。
