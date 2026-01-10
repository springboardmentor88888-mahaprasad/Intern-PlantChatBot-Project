import os

base = "data"
for split in ["train", "val"]:
    print(f"\n{split.upper()}")
    for cls in os.listdir(f"{base}/{split}"):
        count=len(os.listdir(f" {base}/{split}/{cls}"))
        print(cls, ":", count)
