import tkinter as tk
import pickle
global canvas, rectlist,startx,starty, create,sym,killer,mirror
rectlist=[]
savelist=[]
create=True
sym=True
killer=False
mirror=False

def createBlockP(event):
    global startx,starty,f,canvas,create,killer,mirror
    create=False
    if len(canvas.find_overlapping(event.x, event.y, event.x, event.y))==0:
        if not killer:
            f=canvas.create_rectangle(event.x,event.y,event.x+1,event.y+1, fill="white",outline="white",tags="normal")
            if mirror:
                k=canvas.create_rectangle(event.x,event.y,event.x+1,event.y+1, fill="white",outline="white",tags="normal")
        elif killer:
            f=canvas.create_rectangle(event.x,event.y,event.x+1,event.y+1, fill="grey",outline="red",tags="killer")
        print(f)
        startx=event.x
        starty=event.y
        canvas.tag_raise("symline")
        create=True
def createBlockM(event):
    global startx,rectlist,starty,f,canvas,create
    if create:
        canvas.coords(f, (startx,starty,event.x,event.y))
        canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
def createBlockR(event):
    global f,rectlist,listb,create,killer
    if create:
        rectlist.append(f)
        listb.insert("end",f)
        listb.selection_clear(0,"end")
        listb.select_set("end")
        listb.activate("end")
        updateI(0)
        listb.focus_set()
def clear():
    global f,canvas,listb,sym,symLineH,symLineV,create
    create=True
    canvas.delete("all")
    listb.delete(0,"end")
    f=canvas.create_rectangle(0,480,700,500, fill="white",outline="white",tags="normal")
    canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
    createBlockR(2)
    if sym:
        symLineV=canvas.create_line(350,0,350,500,fill="white")
        symLineH=canvas.create_line(0,250,700,250,fill="white")
    elif not sym:
        symLineV=canvas.create_line(5350,5000,5350,5500,fill="white")
        symLineH=canvas.create_line(5000,5250,5700,5250,fill="white")
    drawSpawn()
    canvas.tag_raise("symline")
def clickBlock(event):
    global listb,canvas
    liss=listb.get(0,"end")
    print(liss)
    print(canvas.coords("current"))
    ind=liss.index(canvas.find_closest(event.x, event.y)[0])
    listb.selection_clear(0,"end")
    listb.select_set(ind)
    listb.activate(ind)
    listb.focus_set()
    updateI(0)
    pass

def updateI(event):
    global listb,canvas,rectlist,rsize,rcord
    for i in rectlist:
        if canvas.itemcget(i,"tags")=="normal":
            canvas.itemconfig(i,fill="white",outline="white")
        elif canvas.itemcget(i,"tags")=="killer":
            canvas.itemconfig(i,fill="grey",outline="red")
    #UPDATERAR ENTRIES
    try:
        cords=canvas.coords(listb.get(listb.curselection()))
        canvas.itemconfig(listb.get(listb.curselection()),fill="red",outline="red")
    except:cords=[0,0,0,0]
    rsize.delete(0,"end")
    rsize.insert("end",str(int(cords[2]-cords[0]))+","+str(int(cords[3]-cords[1])))
    rcord.delete(0,"end")
    rcord.insert(0,str(int(cords[0]))+","+str(int(cords[1])))

def setSize(event):
    global listb,rsize,canvas
    x=canvas.coords(listb.get(listb.curselection()))[0]
    y=canvas.coords(listb.get(listb.curselection()))[1]
    sizelist=rsize.get().split(",")
    xsize,ysize=int(sizelist[0]),int(sizelist[1])
    canvas.coords(listb.get(listb.curselection()),(x,y,x+xsize,y+ysize))
def setCord(event):
    global listb,rcord,canvas
    coords=canvas.coords(listb.get(listb.curselection()))
    newcoords=rcord.get().split(",")
    xadd=int(coords[2]-coords[0]+0.5)
    yadd=int(coords[3]-coords[1]+0.5)
    x=int(newcoords[0])
    y=int(newcoords[1])
    canvas.coords(listb.get(listb.curselection()),(x,y,x+xadd,y+yadd))
def delRect(*args):
    try:
        oldSel=listb.curselection()
        canvas.delete(listb.get(listb.curselection()))
        listb.delete(listb.curselection())
        print(len(listb.get(0,"end")),oldSel[0])
        if len(listb.get(0,"end"))>int(oldSel[0]):
            print("1")
            listb.select_set(oldSel)
        elif len(listb.get(0,"end"))<=int(oldSel[0]):
            oldSel=int(oldSel[0])-1
            listb.select_set(oldSel)
            print("2")
    except:pass
    updateI(0)
def save():
    global canvas,listb,fnameE,spawnCord
    savelist=[]
    savelist.append(spawnCord.get().split(",")[:4])
    savelist[0].append(canvas.winfo_width())
    savelist[0].append(canvas.winfo_height())
    print(canvas.winfo_width(),canvas.winfo_height())
    for i in listb.get(0,"end"):
        coords=canvas.coords(i)
        if canvas.itemcget(i,"tags")=="normal":
            canvas.itemconfig(i,fill="white",outline="white")
        elif canvas.itemcget(i,"tags")=="killer":
            canvas.itemconfig(i,fill="grey",outline="red")
        savelist.append([canvas.itemcget(i,"fill"),int(coords[0]),int(coords[1]),int(coords[2]-coords[0]),int(coords[3]-coords[1]),False,canvas.itemcget(i,"tags")])
    print(savelist)
    filename=fnameE.get()
    pickle.dump(savelist,open(filename+".p","wb"))
def load():
    global fnameE,f,canvas,listb,spawnCord,sym
    canvas.delete("all")
    listb.delete(0,"end")
    filename=fnameE.get()
    loadlist=pickle.load(open(filename+".p","rb"))
    spawnCord.delete(0,"end")
    spawnCord.insert(0,str(loadlist[0][0])+","+str(loadlist[0][1])+","+str(loadlist[0][2])+","+str(loadlist[0][3]))
    drawSpawn(0)
    for i in range(1,len(loadlist)):
        f=canvas.create_rectangle(loadlist[i][1],loadlist[i][2],loadlist[i][1]+loadlist[i][3],loadlist[i][2]+loadlist[i][4], fill=loadlist[i][0],outline=loadlist[i][0],tags=loadlist[i][6])
        if canvas.itemcget(f,"tags")=="killer":canvas.itemconfig(f,outline="red")
        canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
        createBlockR(2)
    if sym:
        symLineV=canvas.create_line(350,0,350,500,fill="white",tags="symline")
        symLineH=canvas.create_line(0,250,700,250,fill="white",tags="symline")
        canvas.tag_raise("symlines")
def moveL():
    canvas.move(listb.get(listb.curselection()),-1,0)
    updateI(0)
def moveR():
    canvas.move(listb.get(listb.curselection()),1,0)
    updateI(0)
def moveU():
    canvas.move(listb.get(listb.curselection()),0,-1)
    updateI(0)
def moveD():
    canvas.move(listb.get(listb.curselection()),0,1)
    updateI(0)
def drawSpawn(*args):
    global canvas,spawnCord
    canvas.delete("spawn")
    canvas.create_rectangle(int(spawnCord.get().split(",")[0]),int(spawnCord.get().split(",")[1]),int(spawnCord.get().split(",")[0])+20,int(spawnCord.get().split(",")[1])+40,tags="spawn",fill="red",outline="red")
    canvas.create_rectangle(int(spawnCord.get().split(",")[2]),int(spawnCord.get().split(",")[3]),int(spawnCord.get().split(",")[2])+20,int(spawnCord.get().split(",")[3])+40,tags="spawn",fill="blue",outline="blue")

def toggSym():
    global canvas,symLineV,symLineH,sym
    if sym:
        canvas.delete("symline")
        sym=False
    elif not sym:
        symLineV=canvas.create_line(350,0,350,500,fill="white",tags="symline")
        symLineH=canvas.create_line(0,250,700,250,fill="white",tags="symline")
        sym=True
def toggKiller():
    global killer,killBut
    if killer:
        killBut.config(text="Normal",bg="white",fg="black")
        killer=False
    elif not killer:
        killBut.config(text="Killer",bg="black",fg="white")
        killer=True
def toggMirrorM():
    global mirror
    if mirror:
        mirror=False
    elif not mirror:
        mirror=True

def test():
    print("Hiho")

def main():
    global canvas,listb,rsize,rcord,fnameE,f,symLineH,symLineV,spawnCord,killBut
    root=tk.Tk()
    root.geometry("941x503")
    root.resizable(0,0)
    fr=tk.LabelFrame(root,relief="groove")
    fr.pack(side="right",expand=1,fill="both",pady=1,padx=1)
    listb=tk.Listbox(fr)
    listb.pack_propagate(0)
    listb.pack(side="top",fill="x",pady=3)
    canvas=tk.Canvas(root, width=700,height=500,bg="black")
    canvas.pack(side="left",expand=1,fill="both")
    symLineV=canvas.create_line(350,0,350,500,fill="white",tags="symline")
    symLineH=canvas.create_line(0,250,700,250,fill="white",tags="symline")
    butF=tk.Frame(fr)
    delBut=tk.Button(butF,text="Del",command=delRect).pack(side="left")
    addBut=tk.Button(butF,text="Save",command=save).pack(side="left")
    loadBut=tk.Button(butF,text="Load",command=load).pack(side="left")
    fnameE=tk.Entry(butF)
    fnameE.pack(side="left",padx=4)
    fnameE.insert(0,"Filename")
    butF.pack(side="top")
    rsizef=tk.Frame(fr)
    rsizef.pack(side="top",fill="x",padx=1)
    rsize=tk.Entry(rsizef)
    rsize.pack(side="left",fill="x")
    rsizel=tk.Label(rsizef,text="Size")
    rsizel.pack(side="left")
    rcordf=tk.Frame(fr)
    rcordf.pack(side="top",fill="x",padx=1)
    rcord=tk.Entry(rcordf)
    rcord.pack(side="left",fill="x")
    rcordl=tk.Label(rcordf,text="XY")
    rcordl.pack(side="left")
    clkFr=tk.Frame(fr)
    clkFr.pack(fill="x")
    clBut=tk.Button(clkFr,text="Clear",command=clear).pack(side="left")
    killBut=tk.Button(clkFr,text="Normal",command=toggKiller,bg="white",width=10)
    killBut.pack(side="left")
    chkFr=tk.Frame(fr)
    chkFr.pack(side="top")
    toggleSym=tk.Checkbutton(chkFr,text="Symmetry lines",command=toggSym)
    toggleSym.select()
    toggleSym.pack(side="left")
    toggleMirr=tk.Checkbutton(chkFr,text="Mirror Mode",command=toggMirrorM)
    toggleMirr.select()
    toggleMirr.pack(side="right")
    upBut=tk.Button(fr,text="^",command=moveU,bg="grey").pack(side="top",fill="x")
    difr=tk.Frame(fr,bg="black")
    difr.pack(side="top",fill="x")
    rightBut=tk.Button(difr,text="->",command=moveR,bg="grey").pack(side="right",fill="x",expand=1)
    leftBut=tk.Button(difr,text="<-",command=moveL,bg="grey").pack(side="left",expand=1,fill="x")
    downBut=tk.Button(fr,text="v",command=moveD,bg="grey").pack(side="top",fill="x")
    spawnFr=tk.Frame(fr)
    spawnFr.pack(side="top",fill="x")
    spawnCord=tk.Entry(spawnFr)
    spawnCord.insert(0,"650,10,30,10")
    spawnCord.pack(side="left")
    spawnLbl=tk.Label(spawnFr,text="Spawn XY").pack(side="left")
    spawnM=tk.Button(spawnFr,text="Sel").pack(side="left",expand=1,fill="x")
    drawSpawn(0)
    listb.focus_set()
    scrollbar=tk.Scrollbar(listb,command=listb.yview)
    listb.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    f=canvas.create_rectangle(0,480,700,500, fill="white",outline="white",tags="normal")
    createBlockR(2)
    #BINDINGS
    canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
    canvas.bind("<ButtonPress-1>",createBlockP)
    canvas.bind("<B1-Motion>",createBlockM)
    canvas.bind("<ButtonRelease-1>",createBlockR)
    listb.bind("<ButtonPress-1>",updateI)
    listb.bind("<ButtonRelease-1>",updateI)
    listb.bind("<KeyPress-Down>",updateI)
    listb.bind("<KeyPress-Up>",updateI)
    listb.bind("<KeyRelease-Down>",updateI)
    listb.bind("<KeyRelease-Up>",updateI)
    listb.bind("<Delete>",delRect)
    rsize.bind("<Return>",setSize)
    rcord.bind("<Return>",setCord)
    spawnCord.bind("<Return>",drawSpawn)
    root.mainloop()

if __name__=="__main__":
    main()