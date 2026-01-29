# Sample Images Guide

This guide helps you create or find images for your Kids Schedule tasks.

## Image Specifications

### Recommended Settings
- **Size**: 512x512 pixels (minimum 256x256)
- **Aspect Ratio**: 1:1 (square)
- **Format**: PNG (recommended) or JPG
- **File Size**: Under 500KB for best performance
- **Background**: Transparent PNG or solid color

### File Naming
Use descriptive, lowercase names with hyphens:
- `brush-teeth.png`
- `get-dressed.png`
- `eat-breakfast.png`
- `pack-backpack.png`

## Where to Find Free Images

### Icon Sites (Best for Kids)
1. **Flaticon** (https://www.flaticon.com/)
   - Search: "kids routine", "morning routine", "tooth brush icon"
   - Free with attribution
   - Download as PNG, select 512px size

2. **Icons8** (https://icons8.com/)
   - Great kid-friendly style
   - Search by activity
   - Free tier available

3. **Freepik** (https://www.freepik.com/)
   - Vector illustrations
   - Many kid-themed graphics
   - Free with attribution

### Custom Creation Tools

1. **Canva** (https://www.canva.com/)
   - Free tier available
   - Templates for icons
   - Easy to customize colors
   - Export as PNG, 512x512

2. **Figma** (https://www.figma.com/)
   - Free for personal use
   - Professional design tool
   - Great for customization

### Take Your Own Photos
- Use your smartphone
- Take photos of actual items (toothbrush, shoes, etc.)
- Crop to square
- Use apps like:
  - **Remove.bg** - Remove background
  - **Canva** - Add borders/effects
  - **Photoshop Express** - Free mobile editing

## Sample Icon Collections

### Morning Routine Set
- ☀️ Wake up / Sun
- 🦷 Brush teeth / Toothbrush
- 👕 Get dressed / Clothes
- 🛏️ Make bed / Bed
- 🥣 Eat breakfast / Bowl/Food
- 🎒 Pack backpack / Backpack
- 👟 Put on shoes / Shoes

### After School Set
- 🎒 Put away backpack
- 🧼 Wash hands / Soap
- 🍎 Have snack / Apple
- 📚 Do homework / Books
- 🎮 Free play / Toys

### Bedtime Set
- 🧸 Put away toys / Toy box
- 🛁 Take bath / Bathtub
- 🦷 Brush teeth / Toothbrush
- 👕 Put on pajamas / PJs
- 📖 Read story / Book
- 😴 Sleep / Moon/Stars

## Creating Custom Icons

### Using Canva (Free)

1. Create new design: Custom size 512x512px
2. Search for elements (e.g., "toothbrush")
3. Drag onto canvas
4. Resize to fill space
5. Add background color or keep transparent
6. Download as PNG

### Using GIMP (Free Desktop App)

1. Download GIMP (https://www.gimp.org/)
2. New Image: 512x512px
3. Import photo or create from scratch
4. Add effects/filters
5. Export as PNG

### Using Smartphone Apps

**iOS:**
- **Procreate Pocket** ($5) - Professional drawing
- **Adobe Illustrator Draw** (Free) - Vector graphics
- **Canva** (Free) - Easy templates

**Android:**
- **Infinite Design** (Free) - Vector graphics
- **Pixel Studio** (Free) - Pixel art
- **Canva** (Free) - Easy templates

## Example: Creating a "Brush Teeth" Icon

### Method 1: Free Online (Flaticon)
1. Go to flaticon.com
2. Search "tooth brush kids"
3. Select a colorful icon
4. Download as PNG, 512px
5. Save to Home Assistant

### Method 2: Custom Photo
1. Take photo of your child's toothbrush
2. Open in photo editor
3. Crop to square
4. Use remove.bg to remove background
5. Add colorful border in Canva
6. Export 512x512

### Method 3: Canva Template
1. Open Canva
2. Create 512x512 design
3. Search "toothbrush icon"
4. Add to canvas
5. Customize colors
6. Add fun background
7. Download

## Directory Structure

Organize your images:

```
/config/www/images/
├── morning/
│   ├── wake-up.png
│   ├── brush-teeth.png
│   ├── get-dressed.png
│   └── breakfast.png
├── school/
│   ├── backpack.png
│   ├── homework.png
│   └── lunch.png
├── bedtime/
│   ├── bath.png
│   ├── pajamas.png
│   ├── book.png
│   └── sleep.png
└── chores/
    ├── cleanup.png
    ├── dishes.png
    └── laundry.png
```

Reference in calendar:
```yaml
image: /local/images/morning/brush-teeth.png
```

## Tips for Kid-Friendly Images

✅ **Use Bright Colors**: Kids respond to vibrant, cheerful colors  
✅ **Simple Design**: Avoid overly detailed or complex images  
✅ **Recognizable**: Use familiar objects/symbols  
✅ **Consistent Style**: Keep similar visual style across all icons  
✅ **Age Appropriate**: Match complexity to child's age  
✅ **High Contrast**: Ensure images are easy to see  

## Quick Image Processing

### Batch Resize (ImageMagick)
```bash
# Resize all images in directory to 512x512
mogrify -resize 512x512 *.png
```

### Remove Backgrounds (Python)
```python
# Using rembg library
from rembg import remove
from PIL import Image

input_path = 'input.png'
output_path = 'output.png'

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input_img = i.read()
        output_img = remove(input_img)
        o.write(output_img)
```

## Ready-to-Use Collections

Several projects offer free icon packs:

- **Material Design Icons** (https://pictogrammers.com/library/mdi/)
  - Search by activity
  - Download as PNG
  - Free, no attribution required

- **Font Awesome** (https://fontawesome.com/)
  - Convert icons to images
  - Free tier available

- **Noun Project** (https://thenounproject.com/)
  - Huge collection
  - Free with attribution

## Attribution

If using free resources that require attribution:

Create `/config/www/images/CREDITS.txt`:
```
Icons from Flaticon.com:
- brush-teeth.png: Created by Freepik
- backpack.png: Created by Smashicons
- breakfast.png: Created by photo3idea_studio
```

## Need Help?

- Can't find the right image? Try different search terms
- Need custom work? Consider commissioning on Fiverr ($5-20)
- Want to share your collection? Upload to GitHub!
