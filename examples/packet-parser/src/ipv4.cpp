#include "ipv4.hpp"

std::optional<Ipv4Header> parse_ipv4(const std::uint8_t* data, std::size_t size) {
  if (data == nullptr || size < 20 || (data[0] >> 4) != 4) {
    return std::nullopt;
  }
  const auto header_length = static_cast<std::uint8_t>((data[0] & 0x0f) * 4);
  if (header_length < 20 || size < header_length) {
    return std::nullopt;
  }
  const auto total_length =
      static_cast<std::uint16_t>((static_cast<std::uint16_t>(data[2]) << 8) | data[3]);
  if (total_length < header_length || size < total_length) {
    return std::nullopt;
  }
  return Ipv4Header{header_length, total_length};
}
