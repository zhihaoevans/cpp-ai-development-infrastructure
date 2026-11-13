#pragma once
#include <cstddef>
#include <cstdint>
#include <optional>

struct Ipv4Header {
  std::uint8_t header_length;
  std::uint16_t total_length;
};
// The caller owns data and guarantees size readable bytes; input is never modified or retained.
// Requires the entire IPv4 datagram; trailing bytes are allowed. Invalid/truncated input returns
// nullopt. Does not validate checksum, fragmentation semantics, or transport-layer contents.
std::optional<Ipv4Header> parse_ipv4(const std::uint8_t* data, std::size_t size);
