import pandas as pd
import os
import subprocess

IMAGE_TRAITS_CSV = 'image_palette_traits.csv'
AUDIO_TRAITS_CSV = 'audio_traits.csv'
OUTPUT_MATCH_CSV = 'matched_pairs.csv'
AUDIO_FOLDER = 'audio'
IMAGE_FOLDER = 'images'
OUTPUT_FOLDER = 'output'

image_df = pd.read_csv(IMAGE_TRAITS_CSV)
audio_df = pd.read_csv(AUDIO_TRAITS_CSV)

mood_map = {'warm': 'high-energy', 'cool': 'calm', 'neutral': 'moderate'}
matches = []

for idx, row in image_df.iterrows():
    dominant_bucket = row['dominant_bucket']
    brightness_tag = row['brightness_tag']
    mapped_mood = mood_map.get(dominant_bucket, 'moderate')
    mood_group = audio_df[audio_df['mood_tag'] == mapped_mood]

    if brightness_tag == 'bright':
        filtered_audio = mood_group[mood_group['tempo_bpm'] > 100]
    elif brightness_tag == 'dark':
        filtered_audio = mood_group[mood_group['tempo_bpm'] < 90]
    else:
        filtered_audio = mood_group

    if not filtered_audio.empty:
        selected_audio = filtered_audio.sample(1).iloc[0]['filename']
        matches.append({
            'image_file': row['filename'],
            'dominant_visual_mood': dominant_bucket,
            'brightness': brightness_tag,
            'matched_audio_file': selected_audio,
            'audio_mood': mapped_mood
        })

df_matches = pd.DataFrame(matches)
df_matches.to_csv(OUTPUT_MATCH_CSV, index=False)
print(f'Matching complete! Results saved to {OUTPUT_MATCH_CSV}')

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for match in matches:
    image_path = os.path.join(IMAGE_FOLDER, match['image_file'])
    audio_path = os.path.join(AUDIO_FOLDER, match['matched_audio_file'])
    output_filename = f"{os.path.splitext(match['image_file'])[0]}_final.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    print(f'Creating video: {output_filename}')
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', image_path,
        '-i', audio_path, '-c:v', 'libx264', '-tune', 'stillimage',
        '-c:a', 'aac', '-b:a', '192k', '-shortest', output_path
    ]
    subprocess.run(cmd)

print('Batch rendering complete! Final MP4 files saved.')