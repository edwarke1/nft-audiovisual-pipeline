all: setup analyze_audio analyze_images match_render

setup:
	@echo "🔧 Activating virtual environment"
	source venv/bin/activate

analyze_audio:
	@echo "🎶 Running audio analysis"
	python analyze_audio.py

analyze_images:
	@echo "🖼 Running image analysis"
	python analyze_images.py

match_render:
	@echo "🎬 Running match and render"
	python run_matching_and_render.py

clean:
	@echo "🧹 Cleaning output folder"
	rm -rf output/* matched_pairs.csv summary_report.txt

