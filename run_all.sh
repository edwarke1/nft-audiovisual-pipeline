#!/bin/bash

echo "🚀 Running full NFT audio-visual pipeline..."

# Activate virtual environment
source venv/bin/activate

# Step 1: Analyze audio
echo "🎶 Analyzing audio..."
python analyze_audio.py

# Step 2: Analyze images
echo "🖼 Analyzing images..."
python analyze_images.py

# Step 3: Match and render videos
echo "🎬 Matching and rendering..."
python run_matching_and_render.py

echo "✅ Pipeline complete! Check the output folder."


