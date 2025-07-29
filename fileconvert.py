import os
import cairosvg

svg_folder = 'images/svg'
png_folder = 'images/png'
os.makedirs(png_folder, exist_ok=True)

for filename in os.listdir(svg_folder):
    if filename.endswith('.svg'):
        svg_path = os.path.join(svg_folder, filename)
        png_path = os.path.join(png_folder, filename.replace('.svg', '.png'))
        
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=64, output_height=64)
        print(f"Converted {filename} -> {png_path}")