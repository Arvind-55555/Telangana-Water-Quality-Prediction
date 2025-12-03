#!/bin/bash

echo "🔧 Organizing Project Structure..."

# Create new directory structure
mkdir -p docs/{css,js,images,data}
mkdir -p src/{models,utils,notebooks}
mkdir -p scripts
mkdir -p documentation

# Move files to appropriate directories
echo "📁 Moving files..."

# Move notebooks
mv water_quality_analysis.ipynb src/notebooks/ 2>/dev/null

# Move Python scripts
mv run_analysis.py scripts/ 2>/dev/null
mv predict_water_quality.py src/ 2>/dev/null

# Move documentation
mv README.md documentation/ 2>/dev/null
mv USAGE_GUIDE.md documentation/ 2>/dev/null
mv PROJECT_SUMMARY.md documentation/ 2>/dev/null
mv BUGFIX.md documentation/ 2>/dev/null
mv EXECUTION_SUMMARY.md documentation/ 2>/dev/null

# Move data
cp Water_Quality_Data_06_2025.csv docs/data/ 2>/dev/null

# Keep models in root for now
# mv models/ src/models/ 2>/dev/null

# Move quickstart script
mv quickstart.sh scripts/ 2>/dev/null

echo "✅ Project structure organized!"
echo ""
echo "New structure:"
tree -L 2 -I '__pycache__|*.pyc|.git' 2>/dev/null || ls -R
