const fs = require('fs');
const path = require('path');

// Create a simple SVG icon
const svgIcon = `
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
`;

// Ensure public directory exists
const publicDir = path.join(__dirname, 'public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir);
}

// Save the SVG
fs.writeFileSync(path.join(publicDir, 'icon.svg'), svgIcon);

console.log('✅ Generated placeholder SVG icon');
console.log('📌 Note: For production, replace these with professionally designed icons');
console.log('📌 You can use tools like:');
console.log('   - https://www.pwabuilder.com/imageGenerator');
console.log('   - https://maskable.app/');
console.log('   - https://realfavicongenerator.net/');