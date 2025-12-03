#!/bin/bash
# Water Quality Analysis - Quick Start Script

echo "======================================================================"
echo "   Water Quality Classification & Prediction System"
echo "   Quick Start Script"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip is not installed"
    exit 1
fi

echo "✅ pip found"
echo ""

# Install requirements
echo "📦 Installing required packages..."
echo "This may take a few minutes..."
echo ""

pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully!"
else
    echo "⚠️  Some packages may have failed to install"
    echo "Please check the output above for errors"
fi

echo ""
echo "======================================================================"
echo "   Installation Complete!"
echo "======================================================================"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Open the analysis notebook:"
echo "   jupyter lab water_quality_analysis.ipynb"
echo ""
echo "   OR"
echo ""
echo "   jupyter notebook water_quality_analysis.ipynb"
echo ""
echo "2. Run all cells in the notebook (Cell -> Run All)"
echo "   Expected runtime: 5-15 minutes"
echo ""
echo "3. After training, make predictions:"
echo "   python3 predict_water_quality.py"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Project overview"
echo "   - USAGE_GUIDE.md - Detailed usage instructions"
echo "   - PROJECT_SUMMARY.md - Complete project summary"
echo ""
echo "======================================================================"
echo "✅ Ready to start! Good luck with your analysis!"
echo "======================================================================"

