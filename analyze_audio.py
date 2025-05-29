import librosa
import pandas as pd
import numpy as np
import os

audio_folder = 'audio'
output_csv = 'audio_traits.csv'

audio_data = []

for file in os.listdir(audio_folder):
    if file.endswith('.mp3') or file.endswith('.wav'):
        filepath = os.path.join(audio_folder, file)
        y, sr = librosa.load(filepath)
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = np.mean(librosa.feature.rms(y=y))
        mood = 'calm' if tempo < 80 else 'high-energy' if tempo > 120 else 'moderate'

        audio_data.append({
            'filename': file,
            'duration_sec': round(duration, 2),
            'tempo_bpm': round(tempo, 2),
            'energy_rms': round(rms, 4),
            'mood_tag': mood
        })

df = pd.DataFrame(audio_data)
df.to_csv(output_csv, index=False)
print(f'Audio analysis complete! Results saved to {output_csv}')