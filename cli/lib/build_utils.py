import os
from .search_utils import PROJECT_ROOT

CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")
CACHE_PATH_DOC = os.path.join(PROJECT_ROOT, "cache", "docmap.pkl")
CACHE_PATH_INDEX = os.path.join(PROJECT_ROOT, "cache", "index.pkl")

    
def create_cache():
    os.makedirs(CACHE_PATH, exist_ok=True)