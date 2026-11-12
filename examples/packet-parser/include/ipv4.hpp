#pragma once
#include <cstddef>
#include <cstdint>
#include <optional>

struct Ipv4Header {
  std::uint8_t header_length;
  std::uint16_t total_length;
};
// The caller owns data. The input must contain the entire IPv4 datagram.
std::optional<Ipv4Header> parse_ipv4(const std::uint8_t* data, std::size_t size);
