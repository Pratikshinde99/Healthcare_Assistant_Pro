import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import transformers
try:
    pipe = transformers.pipeline("text2text-generation", model="t5-small")
    print("Success")
except Exception as e:
    print(f"Error: {e}")
