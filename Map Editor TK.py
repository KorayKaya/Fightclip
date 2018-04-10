import tkinter as tk
import pickle, os
global canvas, rectlist,startx,starty, create,sym,blockType,mirror,follow,selSpawn
rectlist=[]
savelist=[]
create=True
sym=True
blockType=0
mirror=False
follow = False
selSpawn = 2
tpSet = 0

def createBlockP(event):
    global startx,starty,blueSpawnDoll,redSpawnDoll,tpDest,f,canvas,create,tpSet,tpDoll,blockType,mirror,k,follow,selSpawn,spawnCord,spawnM,currentWeapon
    graphics_dir= os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
    follow=True
    create=False
    if selSpawn==0:
        oldSpawnCords=spawnCord.get().split(",")
        newSpawnCords=[event.x,event.y]+oldSpawnCords[2:]
        newSpawnCordsStr=",".join(map(str,newSpawnCords))
        spawnCord.delete(0,"end")
        spawnCord.insert(0,newSpawnCordsStr)
        drawSpawn()
        spawnM.config(bg="blue")
        canvas.delete(redSpawnDoll)
        blueSpawnDoll = canvas.create_rectangle(-100,-100,-80,-60,fill="blue",outline="blue")
        selSpawn=1
    elif selSpawn==1:
        oldSpawnCords=spawnCord.get().split(",")
        newSpawnCords=oldSpawnCords[:2]+[event.x,event.y]
        newSpawnCordsStr=",".join(map(str,newSpawnCords))
        spawnCord.delete(0,"end")
        spawnCord.insert(0,newSpawnCordsStr)
        drawSpawn()
        spawnM.config(bg="white")
        canvas.delete(blueSpawnDoll)
        selSpawn=2
    elif tpSet == 1:
        tpDest.delete(0,"end")
        tpDest.insert(0,str(event.x)+","+str(event.y))
        teleDest()
        tpSet = 0
        canvas.delete(tpDoll)
    elif len(canvas.find_overlapping(event.x, event.y, event.x, event.y))==0:
        if blockType==1:
            f=canvas.create_rectangle(event.x,event.y,event.x+20,event.y+20, fill="black",outline="red",tags="killer")
            if mirror:
                print(canvas.winfo_width())
                k=canvas.create_rectangle(canvas.winfo_width()-event.x,event.y,canvas.winfo_width()-event.x-10,event.y+10, fill="black",outline="red",tags="killer")
        elif blockType==2:
            if tpDest.get()!="":
                f=canvas.create_rectangle(event.x,event.y,event.x+20,event.y+20, fill="yellow",outline="yellow",tags=("teleporter",tpDest.get()))
                if mirror:
                    k=canvas.create_rectangle(canvas.winfo_width()-event.x,event.y,canvas.winfo_width()-event.x-20,event.y+20, fill="yellow",outline="yellow",tags=("teleporter",tpDest.get()))
            else:
                f=canvas.create_rectangle(event.x,event.y,event.x+20,event.y+20, fill="yellow",outline="yellow",tags=("teleporter","spawn"))
                if mirror:
                    k=canvas.create_rectangle(canvas.winfo_width()-event.x,event.y,canvas.winfo_width()-event.x-20,event.y+20, fill="yellow",outline="yellow",tags=("teleporter","spawn"))
        elif blockType==3:
            f=canvas.create_rectangle(event.x,event.y,event.x+20,event.y+20, fill="green",outline="green",tags=("healer","2"))
            if mirror:
                k=canvas.create_rectangle(canvas.winfo_width()-event.x,event.y,canvas.winfo_width()-event.x-20,event.y+20, fill="green",outline="green",tags=("healer","2"))
        elif blockType==4:
            f=canvas.create_rectangle(event.x,event.y,event.x+20,event.y+20, fill="grey",outline="red",tags=("weapon","10","handGun"))
            try:
                if currentWeapon.get()!="":
                    tags=canvas.gettags(f)
                    canvas.itemconfig(f,tags=(tags[0],tags[1],currentWeapon.get()))
            except:pass
            #photo=tk.PhotoImage(file=graphics_dir+canvas.gettags(f)[2]+".gif")
            #canvas.create_image(event.x, event.y, image=photo, anchor="nw")
            print(canvas.gettags(f),event.x,event.y)
            if mirror:
                k=canvas.create_rectangle(canvas.winfo_width()-event.x,event.y,canvas.winfo_width()-event.x-20,event.y+20, fill="grey",outline="red",tags=("weapon","10","handGun"))
                try:
                    if currentWeapon.get()!="":
                        tags=canvas.gettags(k)
                        canvas.itemconfig(k,tags=(tags[0],tags[1],currentWeapon.get()))
                except:pass
                canvas.create_image(canvas.winfo_width()-event.x, event.y, image=photo, anchor="ne")
        else:
            f=canvas.create_rectangle(event.x,event.y,event.x+40,event.y+20, fill="white",outline="white",tags="normal")
            if mirror:
                k=canvas.create_rectangle(canvas.winfo_width()-event.x,event.y,canvas.winfo_width()-event.x-10,event.y+10, fill="white",outline="white",tags="normal")
        startx=event.x
        starty=event.y
        canvas.tag_raise("symline")
        create=True
def createBlockM(event):
    global startx,rectlist,starty,f,canvas,create,k
    if create:
        canvas.coords(f, (startx,starty,event.x,event.y))
        if mirror:
            canvas.coords(k, (canvas.winfo_width()-startx,starty,canvas.winfo_width()-event.x,event.y))
def createBlockR(event):
    global f,rectlist,listb,create,k,mirror,follow
    if create:
        if mirror and follow:
            canvas.tag_bind(k,"<ButtonPress-1>",clickBlock)
            rectlist.append(k)
            listb.insert("end",k)
        canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
        rectlist.append(f)
        print("5")
        listb.insert("end",f)
        listb.selection_clear(0,"end")
        listb.select_set("end")
        listb.activate("end")
        print("6")
        updateI(0)
        listb.focus_set()
        follow=False
        create=False
def mouseMotion(event):
    global tpSet,tpDoll,canvas,selSpawn,redSpawnDoll,blueSpawnDoll
    if tpSet==1:
        canvas.coords(tpDoll,event.x,event.y,event.x+20,event.y+40)
    elif selSpawn == 0:
        canvas.coords(redSpawnDoll,event.x,event.y,event.x+20,event.y+40)
    elif selSpawn == 1:
        canvas.coords(blueSpawnDoll,event.x,event.y,event.x+20,event.y+40)

def clear():
    global f,canvas,listb,sym,symLineH,symLineV,create
    create=True
    canvas.delete("all")
    listb.delete(0,"end")
    f=canvas.create_rectangle(0,canvas.winfo_height()-20,canvas.winfo_width(),canvas.winfo_height(), fill="white",outline="white",tags="normal")
    canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
    createBlockR(2)
    toggSym()
    toggSym()
    drawSpawn()
    canvas.tag_raise("symline")

def clickBlock(event):
    global listb,canvas
    liss=listb.get(0,"end")
    ind=liss.index(canvas.find_closest(event.x, event.y)[0])
    listb.selection_clear(0,"end")
    listb.select_set(ind)
    listb.activate(ind)
    listb.focus_set()
    updateI(0)

def updateI(event):
    global listb,canvas,rectlist,rsize,rcord,tpDest,TimeEn
    canvas.itemconfig("normal",fill="white",outline="white")
    canvas.itemconfig("killer",fill="black",outline="red")
    canvas.itemconfig("teleporter",fill="yellow",outline="yellow")
    canvas.itemconfig("healer",fill="green",outline="green")
    canvas.itemconfig("weapon",fill="grey",outline="red")
    try:
        cords=canvas.coords(listb.get(listb.curselection()))
        canvas.itemconfig(listb.get(listb.curselection()),fill="red",outline="red")
    except:cords=[0,0,0,0]
    #UPDATERAR ENTRIES
    rsize.delete(0,"end")
    rsize.insert(0,str(int(cords[2]-cords[0]))+","+str(int(cords[3]-cords[1])))
    rcord.delete(0,"end")
    rcord.insert(0,str(int(cords[0]))+","+str(int(cords[1])))
    try:
        tpDest.delete(0,"end")
        if canvas.gettags(listb.get(listb.curselection()))[0]=="teleporter":
            tpDest.insert(0,canvas.gettags(listb.get(listb.curselection()))[1])
        else:
            tpDest.insert(0,"")
    except:pass
    try:
        TimeEn.delete(0,"end")
        if canvas.gettags(listb.get(listb.curselection()))[0]=="healer" or canvas.gettags(listb.get(listb.curselection()))[0]=="weapon":
            TimeEn.insert(0,canvas.gettags(listb.get(listb.curselection()))[1])
        else:
            TimeEn.insert(0,"")
    except:pass

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
    global canvas,listb,fnameE,spawnCord,gunsVar
    savelist=[]
    savelist.append(spawnCord.get().split(",")[:4])
    if gunsVar.get()==0:
        savelist[0].append(False)
    elif gunsVar.get()==1:
        savelist[0].append(True)
    savelist[0].append((canvas.winfo_width(),canvas.winfo_height()))
    print(savelist[0])
    print(canvas.winfo_width(),canvas.winfo_height())
    listb.selection_clear(0,"end")
    for i in listb.get(0,"end"):
        coords=canvas.coords(i)
        print(canvas.gettags(i))
        if canvas.gettags(i)[0]=="normal":
            canvas.itemconfig(i,fill="white",outline="white")
        elif canvas.gettags(i)[0]=="killer":
            canvas.itemconfig(i,fill="black",outline="red")
        if canvas.gettags(i)[0]=="teleporter":
            canvas.itemconfig(i,fill="yellow",outline="yellow")
            savelist.append([canvas.itemcget(i,"fill"),int(coords[0]),int(coords[1]),int(coords[2]-coords[0]),int(coords[3]-coords[1]),canvas.gettags(i)[0],canvas.gettags(i)[1]])
        elif canvas.gettags(i)[0]=="healer":
            canvas.itemconfig(i,fill="green",outline="green")
            savelist.append([canvas.itemcget(i,"fill"),int(coords[0]),int(coords[1]),int(coords[2]-coords[0]),int(coords[3]-coords[1]),canvas.gettags(i)[0],canvas.gettags(i)[1]])
        elif canvas.gettags(i)[0]=="weapon":
            canvas.itemconfig(i,fill="grey",outline="red")
            savelist.append([canvas.itemcget(i,"fill"),int(coords[0]),int(coords[1]),20,20,canvas.gettags(i)[0],canvas.gettags(i)[1],canvas.gettags(i)[2]])
        else:
            savelist.append([canvas.itemcget(i,"fill"),int(coords[0]),int(coords[1]),int(coords[2]-coords[0]),int(coords[3]-coords[1]),canvas.gettags(i)[0]])
    print(savelist)
    filename=fnameE.get()
    pickle.dump(savelist,open(os.path.dirname(os.path.realpath(__file__))+"\\MAPS\\"+filename+".p","wb"))
def load():
    global fnameE,f,canvas,listb,spawnCord,sym,create,guns_chkbutt,gunsVar
    canvas.delete("all")
    listb.delete(0,"end")
    filename=fnameE.get()
    loadlist=pickle.load(open(os.path.dirname(os.path.realpath(__file__))+"\\MAPS\\"+filename+".p","rb"))
    print(loadlist)
    spawnCord.delete(0,"end")
    spawnCord.insert(0,str(loadlist[0][0])+","+str(loadlist[0][1])+","+str(loadlist[0][2])+","+str(loadlist[0][3]))
    drawSpawn(0)
    try:
        if int(loadlist[0][4])==0 or int(loadlist[0][4])==1:
            while int(loadlist[0][4])!=gunsVar.get():
                guns_chkbutt.toggle()
    except:pass
    for i in range(1,len(loadlist)):
        print(loadlist[i])
        f=canvas.create_rectangle(loadlist[i][1],loadlist[i][2],loadlist[i][1]+loadlist[i][3],loadlist[i][2]+loadlist[i][4], fill=loadlist[i][0],outline=loadlist[i][0],tags=loadlist[i][5])
        if canvas.itemcget(f,"tags")=="killer":canvas.itemconfig(f,outline="red")
        elif canvas.gettags(f)[0]=="teleporter":
            print(loadlist[i],i,f)
            try:canvas.itemconfig(f,tags=("teleporter",loadlist[i][6]))
            except:canvas.itemconfig(f,tags=("teleporter","spawn"))
        elif canvas.gettags(f)[0]=="healer":canvas.itemconfig(f,tags=("healer",loadlist[i][6]))
        elif canvas.gettags(f)[0]=="weapon":canvas.itemconfig(f,tags=("weapon",loadlist[i][6],loadlist[i][7]))
        canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
        create=True
        createBlockR(0)
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
def raiseItem():
    global listb,canvas
    item = listb.get(listb.curselection())
    canvas.tag_raise(item)
def lowerItem():
    global listb,canvas
    item = listb.get(listb.curselection())
    canvas.lower(item)
def spawnSelect(*args):
    global selSpawn,spawnM,canvas,redSpawnDoll
    if tpSet == 0:
        selSpawn=0
        spawnM.config(bg="red")
        redSpawnDoll = canvas.create_rectangle(-100,-100,-80,-60,fill="red",outline="red")
def drawSpawn(*args):
    global canvas,spawnCord,redSpawn,blueSpawn
    canvas.delete("spawnDolls")
    redSpawn=canvas.create_rectangle(int(spawnCord.get().split(",")[0]),int(spawnCord.get().split(",")[1]),int(spawnCord.get().split(",")[0])+20,int(spawnCord.get().split(",")[1])+40,tags="spawnDolls",fill="red",outline="red")
    blueSpawn=canvas.create_rectangle(int(spawnCord.get().split(",")[2]),int(spawnCord.get().split(",")[3]),int(spawnCord.get().split(",")[2])+20,int(spawnCord.get().split(",")[3])+40,tags="spawnDolls",fill="blue",outline="blue")

def toggSym():
    global canvas,symLineV,symLineH,sym
    if sym:
        canvas.delete("symline")
        sym=False
    elif not sym:
        symLineV=canvas.create_line(canvas.winfo_width()/2,0,canvas.winfo_width()/2,canvas.winfo_height(),fill="white",tags="symline")
        symLineH=canvas.create_line(0,canvas.winfo_height()/2,canvas.winfo_width(),canvas.winfo_height()/2,fill="white",tags="symline")
        sym=True
def toggBlockType():
    global blockType,blockTypeBut,rcordf,tpDest,rcordl,clkFr,setTpBut,TimeEn,weaponMenu,currentWeapon
    if blockType==1:
        blockTypeBut.config(text="Teleporter",bg="yellow",fg="black")
        blockType=2
        tpDest=tk.Entry(rcordf,width=7)
        tpDest.bind("<Return>",teleDest)
        tpDest.pack(side="left")
        rcordl.config(text="XY TO")
        setTpBut=tk.Button(clkFr,text="Set TP",bg="purple",command=tpSetFunc)
        setTpBut.pack(side="right",padx=22)
        updateI(0)
    elif blockType==2:
        blockTypeBut.config(text="Healer",bg="green",fg="black")
        blockType=3
        tpDest.destroy()
        rcordl.config(text="XY T:")
        TimeEn=tk.Entry(rcordf,width=7)
        TimeEn.bind("<Return>",TimeSet)
        TimeEn.pack(side="left")
        setTpBut.destroy()
    elif blockType==3:
        blockTypeBut.config(text="Weapon",bg="red",fg="black")
        weapons = ["handGun","assaultRifle","shotgun","lazerRifle","lazerPistol","adminGun","grenadeLauncher","katana"]
        currentWeapon=tk.StringVar()
        weaponMenu=tk.OptionMenu(clkFr,currentWeapon,*weapons,command = weaponSet)
        weaponMenu.pack(side="left")
        blockType=4
    elif blockType==4:
        blockTypeBut.config(text="Normal",bg="white",fg="black")
        weaponMenu.destroy()
        TimeEn.destroy()
        blockType=0
    elif blockType==0:
        blockTypeBut.config(text="Killer",bg="black",fg="white")
        blockType=1
def toggMirrorM():
    global mirror
    if mirror:
        mirror=False
    elif not mirror:
        mirror=True
def teleDest(*args):
    global listb,canvas,tpDest
    item = listb.get(listb.curselection())
    if canvas.gettags(item)[0]=="teleporter":
        canvas.itemconfig(item,tags=("teleporter",tpDest.get()))
        print(canvas.gettags(item))
def TimeSet(*args):
    global listb,canvas,TimeEn
    item = listb.get(listb.curselection())
    tags = canvas.gettags(item)
    if canvas.gettags(item)[0]=="healer":
        canvas.itemconfig(item,tags=(tags[0],TimeEn.get()))
        print(canvas.gettags(item))
    elif canvas.gettags(item)[0]=="weapon":
        canvas.itemconfig(item,tags=(tags[0],TimeEn.get(),tags[2]))
        print(canvas.gettags(item))
def weaponSet(*args):
    global listb,canvas,weaponMenu,currentWeapon
    item = listb.get(listb.curselection())
    tags = canvas.gettags(item)
    if tags[0]=="weapon":
        canvas.itemconfig(item,tags=(tags[0],tags[1],currentWeapon.get()))
        print(canvas.gettags(item))
def tpSetFunc(*args):
    global tpSet,canvas,tpDoll,selSpawn
    if selSpawn == 2:
        tpSet=1
        tpDoll = canvas.create_rectangle(-100,-100,-80,-60,fill="purple",outline="purple")

def test():
    print("Hiho")

def main():
    global canvas,clkFr,listb,rcordf,rsize,rcord,rcordl,guns_chkbutt,fnameE,f,symLineH,symLineV,gunsVar,spawnCord,blockTypeBut,spawnM
    root=tk.Tk()
    root.wm_title("FC Map Editor")
    root.iconbitmap(os.path.dirname(os.path.realpath(__file__))+'\\GRAPHICS\\mapeditoricon.ico')
    root.geometry("943x503")
    fr=tk.LabelFrame(root,relief="groove")
    fr.pack(side="right",fill="both",pady=1,padx=1)
    listb=tk.Listbox(fr)
    listb.pack_propagate(0)
    listb.pack(side="top",fill="x",pady=3)
    canvas=tk.Canvas(root, width=702,height=500,bg="black")
    canvas.pack(side="left",fill="both",expand=1)
    canvas.xview_moveto(0)
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
    rcord.pack(side="left",anchor="n",fill="x")
    rcordl=tk.Label(rcordf,text="XY")
    rcordl.pack(side="left",anchor="n")
    clkFr=tk.Frame(fr)
    clkFr.pack(fill="x")
    clBut=tk.Button(clkFr,text="Clear",command=clear).pack(side="left")
    blockTypeBut=tk.Button(clkFr,text="Normal",command=toggBlockType,bg="white",width=10)
    blockTypeBut.pack(side="left")
    chkFr=tk.Frame(fr)
    chkFr.pack(side="top")
    toggleSym=tk.Checkbutton(chkFr,text="Symmetry lines",command=toggSym)
    toggleSym.select()
    toggleSym.pack(side="left")
    toggleMirr=tk.Checkbutton(chkFr,text="Mirror Mode",command=toggMirrorM)
    toggleMirr.pack(side="right")
    raiseBut=tk.Button(fr,text="^",height=1,command=raiseItem,bg="black",fg="white").pack(side="top",fill="x")
    upBut=tk.Button(fr,text="^",command=moveU,bg="grey").pack(side="top",fill="x")
    difr=tk.Frame(fr,bg="black")
    difr.pack(side="top",fill="x")
    rightBut=tk.Button(difr,text="->",command=moveR,bg="grey").pack(side="right",fill="x",expand=1)
    leftBut=tk.Button(difr,text="<-",command=moveL,bg="grey").pack(side="left",expand=1,fill="x")
    downBut=tk.Button(fr,text="v",command=moveD,bg="grey").pack(side="top",fill="x")
    lowerBut=tk.Button(fr,text="v",height=1,command=lowerItem,bg="black",fg="white").pack(side="top",fill="x")
    spawnFr=tk.Frame(fr)
    spawnFr.pack(side="top",fill="x")
    spawnCord=tk.Entry(spawnFr)
    spawnCord.insert(0,"650,10,30,10")
    spawnCord.pack(side="left")
    spawnLbl=tk.Label(spawnFr,text="Spawn XY").pack(side="left")
    spawnM=tk.Button(spawnFr,text="Sel",command=spawnSelect)
    spawnM.pack(side="left",expand=1,fill="x")
    drawSpawn(0)
    listb.focus_set()
    scrollbar=tk.Scrollbar(listb,command=listb.yview)
    listb.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    gunsVar=tk.IntVar()
    guns_chkbutt= tk.Checkbutton(fr,variable=gunsVar,onvalue=1,offvalue=0,text="Guns allowed")
    guns_chkbutt.pack(side="top",anchor="w")
    guns_chkbutt.select()
    f=canvas.create_rectangle(0,480,700,500, fill="white",outline="white",tags="normal")
    createBlockR(2)
    graphics_dir=os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
    #photo=tk.PhotoImage(file=graphics_dir+"handGun.gif")
    #canvas.create_image(100, 100, image=photo, anchor="nw")
    #BINDINGS
    canvas.tag_bind(f,"<ButtonPress-1>",clickBlock)
    canvas.bind("<ButtonPress-1>",createBlockP)
    canvas.bind("<B1-Motion>",createBlockM)
    canvas.bind("<ButtonRelease-1>",createBlockR)
    canvas.bind("<Motion>",mouseMotion)
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
