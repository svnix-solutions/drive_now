const fs = require('fs');
const path = require('path');

// This script updates the frontend.html template with the correct asset filenames after build

const assetsDir = path.join(__dirname, '../drive_now/public/frontend/assets');
const templatePath = path.join(__dirname, '../drive_now/templates/pages/frontend.html');

// Find the actual built files
const files = fs.readdirSync(assetsDir);

let mainJs = files.find(f => f.startsWith('main.') && f.endsWith('.js'));
let mainCss = files.find(f => f.startsWith('main.') && f.endsWith('.css'));
let vendorJs = files.find(f => f.startsWith('vendor.') && f.endsWith('.js'));
let vendorCss = files.find(f => f.startsWith('vendor.') && f.endsWith('.css'));

if (!mainJs || !mainCss || !vendorJs || !vendorCss) {
  console.error('❌ Could not find all required asset files');
  process.exit(1);
}

// Read the template
let template = fs.readFileSync(templatePath, 'utf8');

// Update asset references using regex
// Handle both old format and new standalone format
template = template.replace(
  /src="\/assets\/drive_now\/frontend\/assets\/main\.[^"]+\.js"/g,
  `src="/assets/drive_now/frontend/assets/${mainJs}"`
);

template = template.replace(
  /href="\/assets\/drive_now\/frontend\/assets\/vendor\.[^"]+\.js"/g,
  `href="/assets/drive_now/frontend/assets/${vendorJs}"`
);

template = template.replace(
  /href="\/assets\/drive_now\/frontend\/assets\/vendor\.[^"]+\.css"/g,
  `href="/assets/drive_now/frontend/assets/${vendorCss}"`
);

template = template.replace(
  /href="\/assets\/drive_now\/frontend\/assets\/main\.[^"]+\.css"/g,
  `href="/assets/drive_now/frontend/assets/${mainCss}"`
);

// Write the updated template
fs.writeFileSync(templatePath, template);

console.log('✅ Updated frontend.html with new asset filenames:');
console.log(`   - main.js: ${mainJs}`);
console.log(`   - main.css: ${mainCss}`);
console.log(`   - vendor.js: ${vendorJs}`);
console.log(`   - vendor.css: ${vendorCss}`);