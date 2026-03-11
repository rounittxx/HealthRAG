"""
Entry point for Hugging Face Spaces deployment.
HF Spaces looks for app.py at root, so this just boots the Streamlit frontend.
"""

# HF Spaces runs: streamlit run app.py
# So we import and re-run the actual frontend from here

import os
import sys

# make sure imports from project root work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# the real app lives in frontend/app.py
exec(open("frontend/app.py").read())
