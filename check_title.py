import glob

files = glob.glob("./dataset/with_title/*")
for file in files:
    with open(file) as f:
        t = f.readlines()[0].strip()
        print(file)
        print(t)
        print('---------')
    
