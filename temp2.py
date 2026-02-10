from pathlib import Path

directory = Path("tesseract_training/ground_truth_flies")

for file_path in directory.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")
    if text.startswith("Total Pot : ") and text.endswith(" BB"):
        # text = text.replace("TotalPot:", "Total Pot : ")
        # text = text.replace("BB", " BB")
        pass
    else:
        if text.endswith(" BB") and not text.startswith("T"):
            pass
        # text = text.replace("BB", " BB")
        else:
            print("ALARM: text does not start with Total Pot: "+text + "|TEXT_END|")
            if text.endswith("BB "):
                text = text[:-1] # remove the extra space at the end
                file_path.write_text(text, encoding="utf-8")      
                  

    # file_path.write_text(text, encoding="utf-8")
