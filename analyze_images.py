import os
import pandas as pd
from colorthief import ColorThief
from PIL import Image
from collections import Counter

IMAGE_FOLDER = 'images'
OUTPUT_CSV = 'image_palette_traits.csv'

def classify_color(rgb):
    r, g, b = rgb
    r /= 255; g /= 255; b /= 255
    max_val = max(r, g, b); min_val = min(r, g, b)
    if max_val == min_val:
        hue = 0
    elif max_val == r:
        hue = (60 * ((g - b) / (max_val - min_val)) + 360) % 360
    elif max_val == g:
        hue = (60 * ((b - r) / (max_val - min_val)) + 120) % 360
    else:
        hue = (60 * ((r - g) / (max_val - min_val)) + 240) % 360

    if (0 <= hue <= 60) or (300 <= hue <= 360):
        return 'warm'
    elif 120 <= hue <= 240:
        return 'cool'
    else:
        return 'neutral'

image_data = []

for file in os.listdir(IMAGE_FOLDER):
    if file.endswith('.png'):
        filepath = os.path.join(IMAGE_FOLDER, file)
        ct = ColorThief(filepath)
        palette = ct.get_palette(color_count=5)
        bucket_counts = Counter([classify_color(rgb) for rgb in palette])
        total = sum(bucket_counts.values())
        warm_pct = (bucket_counts['warm'] / total) * 100
        cool_pct = (bucket_counts['cool'] / total) * 100
        neutral_pct = (bucket_counts['neutral'] / total) * 100
        dominant_bucket = max(bucket_counts, key=bucket_counts.get)
        img = Image.open(filepath).convert('L')
        stat = img.getextrema()
        brightness = (stat[1] + stat[0]) / 2
        brightness_tag = 'dark' if brightness < 85 else 'medium' if brightness < 170 else 'bright'

        image_data.append({
            'filename': file,
            'warm_pct': round(warm_pct, 2),
            'cool_pct': round(cool_pct, 2),
            'neutral_pct': round(neutral_pct, 2),
            'dominant_bucket': dominant_bucket,
            'brightness': round(brightness, 2),
            'brightness_tag': brightness_tag
        })

df = pd.DataFrame(image_data)
df.to_csv(OUTPUT_CSV, index=False)
print(f'Image analysis complete! Results saved to {OUTPUT_CSV}')