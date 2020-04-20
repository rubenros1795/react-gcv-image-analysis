
for n in [1,2,3,4]:
    print("photo = ",n)
    for c in ["a","b","c","d"]:
        
        print("-- iteration = ", c)
        if c == "c":
            print("breaking out of {}{}".format(n,c))
            break