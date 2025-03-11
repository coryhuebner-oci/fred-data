# Ensure the src directory is in the path

import os
import sys


def ensure_src_in_path():
    src_path = os.path.abspath("../src")
    existing_path_entries = sys.path
    if src_path in existing_path_entries:
        print(f"{src_path} already in path")
    else:
        sys.path.append(src_path)
