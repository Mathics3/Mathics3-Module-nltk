#!/usr/bin/env python3
"""
Load bcp47 which is needed to support Mathics3 builtin-function WordTranslation.
"""
import os

import nltk

# choose a local data dir so we don't require system-wide write access
data_dir = os.environ.get("NLTK_DATA", os.path.join(os.getcwd(), ".nltk_data"))
os.makedirs(data_dir, exist_ok=True)

# ensure nltk knows about it
if data_dir not in nltk.data.path:
    nltk.data.path.append(data_dir)

# only download if missing
try:
    nltk.data.find("corpora/bcp47")
except LookupError:
    nltk.download("bcp47", download_dir=data_dir, quiet=False)
