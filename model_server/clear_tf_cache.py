from transformers import TRANSFORMERS_CACHE 
import shutil 
print(TRANSFORMERS_CACHE)
shutil.rmtree(TRANSFORMERS_CACHE)