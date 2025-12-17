const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const svgContent = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0b0d17"/>
      <stop offset="100%" style="stop-color:#1a1f35"/>
    </linearGradient>
    <linearGradient id="starGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00d4ff"/>
      <stop offset="100%" style="stop-color:#00ff88"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <!-- Background -->
  <rect width="512" height="512" rx="100" fill="url(#bg)"/>
  <!-- Outer ring -->
  <circle cx="256" cy="256" r="200" fill="none" stroke="url(#starGrad)" stroke-width="8" opacity="0.3"/>
  <!-- Star -->
  <g filter="url(#glow)">
    <polygon points="256,80 290,190 408,190 312,260 346,370 256,300 166,370 200,260 104,190 222,190" fill="url(#starGrad)"/>
  </g>
  <!-- Small stars decoration -->
  <circle cx="100" cy="100" r="6" fill="#00d4ff" opacity="0.6"/>
  <circle cx="420" cy="120" r="4" fill="#00ff88" opacity="0.5"/>
  <circle cx="80" cy="380" r="5" fill="#00d4ff" opacity="0.4"/>
  <circle cx="440" cy="400" r="7" fill="#00ff88" opacity="0.6"/>
  <circle cx="380" cy="80" r="3" fill="#ffffff" opacity="0.5"/>
</svg>
`;

const sizes = [192, 512];

async function generateIcons() {
  const iconsDir = path.join(__dirname, 'public', 'icons');
  
  // Ensure directory exists
  if (!fs.existsSync(iconsDir)) {
    fs.mkdirSync(iconsDir, { recursive: true });
  }

  for (const size of sizes) {
    const outputPath = path.join(iconsDir, `icon-${size}.png`);
    
    await sharp(Buffer.from(svgContent))
      .resize(size, size)
      .png()
      .toFile(outputPath);
    
    console.log(`Generated: icon-${size}.png`);
  }
  
  // Also create favicon.ico (32x32)
  await sharp(Buffer.from(svgContent))
    .resize(32, 32)
    .png()
    .toFile(path.join(__dirname, 'public', 'favicon.png'));
  
  console.log('Generated: favicon.png');
  console.log('Done! Icons generated successfully.');
}

generateIcons().catch(console.error);

