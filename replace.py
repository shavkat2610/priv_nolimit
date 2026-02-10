


import os
files = os.listdir("tesseract_training/ground_truth_flies")
for src in files:
    dst = src.replace(']', 'I').replace('[', 'I').replace('|', 'I')
    os.rename("tesseract_training/ground_truth_flies/"+src, "tesseract_training/ground_truth_flies/"+dst)
