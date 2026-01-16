import os

base = "data"
for split in ["train", "val"]:
    print(f"\n(split.upper())")
    for cls in os.listdir(os.path.join(base, split)):
        count=len(os.listdir(os.path.join(base, split, cls)))
        print(cls, ":", count)
