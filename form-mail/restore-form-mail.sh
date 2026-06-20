#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
site_dir="$(cd "$script_dir/../risbergetvaalerfinnskog.com" && pwd)"

cp "$script_dir/6b43a23c09.js" "$site_dir/onewebstatic/6b43a23c09.js"
cp "$script_dir/07e4829d26.js" "$site_dir/onewebstatic/07e4829d26.js"

echo "Restored One.com form mail files to onewebstatic/."
