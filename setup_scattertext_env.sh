#!/bin/bash
# Clean, safe setup for Scattertext + SpaCy + Gensim + Pandas

# 1. Remove old virtual environment (if it exists)
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# 2. Create a new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# 3. Activate the environment
source venv/bin/activate

# 4. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# 5. Install compatible packages
echo "Installing packages..."
pip install numpy==1.25.2 \
            scikit-learn==1.3.2 \
            scattertext==0.1.19 \
            spacy==3.8.7 \
            gensim==4.3.3 \
            pandas==2.3.1

# 6. Download SpaCy English model
echo "Downloading SpaCy English model..."
python -m spacy download en_core_web_sm

# 7. Confirm versions
echo "Installed package versions:"
python -c "import numpy, sklearn, scattertext, spacy, gensim, pandas; \
           print('numpy:', numpy.__version__); \
           print('scikit-learn:', sklearn.__version__); \
           print('scattertext:', scattertext.__version__); \
           print('spacy:', spacy.__version__); \
           print('gensim:', gensim.__version__); \
           print('pandas:', pandas.__version__)"
