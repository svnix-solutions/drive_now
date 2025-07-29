#!/bin/bash

# Create public directory if it doesn't exist
mkdir -p public

# Create a simple SVG icon
cat > public/icon.svg << 'EOF'
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <rect width="512" height="512" fill="#2563eb"/>
  <g transform="translate(256, 256)">
    <circle cx="0" cy="-50" r="30" fill="white"/>
    <path d="M -70 20 Q 0 -30 70 20 Q 0 70 -70 20" fill="white" stroke="none"/>
    <rect x="-80" y="20" width="160" height="60" rx="10" fill="white"/>
    <circle cx="-50" cy="80" r="15" fill="#2563eb"/>
    <circle cx="50" cy="80" r="15" fill="#2563eb"/>
  </g>
  <text x="256" y="400" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="white">DRIVE NOW</text>
</svg>
EOF

echo "✅ Created icon.svg"

# Note: For actual PNG generation, you would need ImageMagick or similar tools
# For now, we'll create placeholder files
echo "📌 Note: PNG icons need to be generated from the SVG using a tool like ImageMagick"
echo "📌 Install ImageMagick and run:"
echo "   convert -background none public/icon.svg -resize 192x192 public/icon-192x192.png"
echo "   convert -background none public/icon.svg -resize 256x256 public/icon-256x256.png"
echo "   convert -background none public/icon.svg -resize 384x384 public/icon-384x384.png"
echo "   convert -background none public/icon.svg -resize 512x512 public/icon-512x512.png"

# Create placeholder PNG files (empty for now)
touch public/icon-192x192.png
touch public/icon-256x256.png
touch public/icon-384x384.png
touch public/icon-512x512.png
touch public/book-icon.png
touch public/history-icon.png
touch public/screenshot1.png
touch public/screenshot2.png

echo "✅ Created placeholder PNG files"