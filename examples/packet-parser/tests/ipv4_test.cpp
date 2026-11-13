#include "ipv4.hpp"
#include <array>
#include <cstdint>
#include <iostream>

int main() {
  int failures = 0;
  auto check = [&](bool ok, const char* name) {
    if (!ok) {
      std::cerr << "FAIL: " << name << '\n';
      ++failures;
    }
  };
  std::array<std::uint8_t, 260> p{};
  p[0] = 0x45;
  p[2] = 1;
  p[3] = 4;
  auto h = parse_ipv4(p.data(), p.size());
  check(h && h->header_length == 20 && h->total_length == 260, "valid and byte order");
  check(!parse_ipv4(nullptr, p.size()), "null");
  check(!parse_ipv4(p.data(), 0), "empty");
  check(!parse_ipv4(p.data(), 19), "truncated fixed header");
  check(!parse_ipv4(p.data(), 259), "truncated datagram");
  p[0] = 0x65;
  check(!parse_ipv4(p.data(), p.size()), "wrong version");
  p[0] = 0x44;
  check(!parse_ipv4(p.data(), p.size()), "invalid IHL");
  p[0] = 0x4f;
  check(!parse_ipv4(p.data(), 20), "truncated options");
  p[0] = 0x46;
  p[2] = 0;
  p[3] = 20;
  check(!parse_ipv4(p.data(), p.size()), "total smaller than header");
  p[3] = 24;
  h = parse_ipv4(p.data(), p.size());
  check(h && h->header_length == 24 && h->total_length == 24, "valid options and trailing bytes");
  return failures == 0 ? 0 : 1;
}
