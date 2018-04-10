import pickle
filename="tpfight"
loadlist=pickle.load(open("C:\\Users\\ab43324\\Desktop\\FunktionellaProjekt\\FightClip\\MAPS\\"+filename+".p","rb"))
for i in loadlist[1:]:
    i.pop(5)
print("NEW!!!!!!!!!!!!!!!!!",loadlist)
pickle.dump(loadlist,open("C:\\Users\\ab43324\\Desktop\\FunktionellaProjekt\\FightClip\\MAPS\\"+filename+".p","wb"))

