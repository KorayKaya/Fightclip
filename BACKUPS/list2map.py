import pickle
mlist=[['650', '10', '30', '10', 703, 503], ['white', 0, 480, 700, 20, False,"normal"], ['white', 157, 432, 67, 4, False,"normal"], ['white', 318, 428, 83, 5, False,"normal"], ['white', 471, 426, 91, 6, False,"normal"], ['white', 592, 425, 75, 7, False,"normal"]]
filename=input("Map name?")
pickle.dump(mlist,open(filename+".p","wb"))