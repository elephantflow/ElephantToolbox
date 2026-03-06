#!/usr/bin/env bash
# Usage: bash download_m3u8.sh <m3u8_url> <output_mp4>

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <m3u8_url> <output_mp4>"
  exit 1
fi

ffmpeg -i "$1" -bsf:a aac_adtstoasc -c copy "$2" -http_persistent 0
