# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 19:34:33 2023

@author: samue
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:44:50 2023

@author: samue
"""
import numpy as np
from MEC1315_STL import *

#Lire les différents fichiers
diamant = LireSTL("Diamant.stl")
cylindre = LireSTL("Cylindre.stl")
triangle = LireSTL("Triangle.stl")
cube = LireSTL("Cube.stl")
f18=LireSTL('fighter_jet_f18.stl')

def acote_plan(objet,plan): #Perment de déposer le stl sur un plan
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    if plan =="xy": #Sur plan XY
        v[:,2]=v[:,2]-min(v[:,2])
    if plan =="xz": #Sur plan XZ
        v[:,1]=v[:,1]-min(v[:,1])
    if plan =="yz": #Sur plan YZ
        v[:,0]=v[:,0]-min(v[:,0])
    return f,v,n
    
def emplacement(x,y,z,objet): #Permet de déplacer le stl
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    v[:,0]=v[:,0]-(max(v[:,0])+min(v[:,0]))/2+x #déplacement en x
    v[:,1]=v[:,1]-(max(v[:,1])+min(v[:,1]))/2+y #déplacement en y
    v[:,2]=v[:,2]-(max(v[:,2])+min(v[:,2]))/2+z #déplacement en z
    
    return f,v,n
    
def grandeur(x,y,z,objet): #Permet de changer l'échelle du stl (homothétie), Dois utiliser centrer avant
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    v[:,0]=v[:,0]/(max(v[:,0])-min(v[:,0]))*x #mise à l'échelle composant x
    v[:,1]=v[:,1]/(max(v[:,1])-min(v[:,1]))*y #mise à l'échelle composant y
    v[:,2]=v[:,2]/(max(v[:,2])-min(v[:,2]))*z #mise à l'échelle composant z
    return f,v,n

def rotation(objet,angle,axe): #Permet de tourner le stl
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    if axe =="z": #Tourne sur l'axe z
        v=v.dot(np.array([[np.cos(angle),np.sin(angle),0],[-np.sin(angle),np.cos(angle),0],[0,0,1]]))
    elif axe == "y": #Tourne sur l'axe y
        v=v.dot(np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]]))
    elif axe == "x": #Tourne sur l'axe x
        v=v.dot(np.array([[1,0,0],[0,np.cos(angle),np.sin(angle)],[0,-np.sin(angle),np.cos(angle)]]))
    return f,v,n

def copycentre(nom):
    f,v,n = nom
    fc = np.array(f)
    vc = np.array(v)
    nc = np.array(n)
    vc[:,0]=vc[:,0]-(max(vc[:,0])+min(vc[:,0]))/2 #centre axe x
    vc[:,1]=vc[:,1]-(max(vc[:,1])+min(vc[:,1]))/2 #centre axe y
    vc[:,2]=vc[:,2]-(max(vc[:,2])+min(vc[:,2]))/2 #centre axe z 
    objet=fc,vc,nc
    return objet        
    
def RepCirculaire(nom,nb,r,a,axe):                 
    f1,v1,n1=nom
    nv1=len(v1)    
    t=np.linspace(0,a,nb+1)
    t=t[:-1]
    if axe=="z":            
        x,y=r*np.cos(t),r*np.sin(t)
    if axe=="y":            
        x,z=r*np.cos(t),r*np.sin(t)
    if axe=="x":            
        y,z=r*np.cos(t),r*np.sin(t)   
    for i in range(len(t)):
        if i != 0:          # ne pas augmenter le f si c'est le premier objet
            f1=np.array(f1+nv1)
        objet2=rotation(nom,t[i],axe)
        f2,v2,n2=objet2
        if axe=="z":
            v2=v2+[x[i],y[i],0] 
        if axe=="y":
            v2=v2+[x[i],0,z[i]] 
        if axe=="x":
            v2=v2+[0,y[i],z[i]]
        if i ==0:               # pas faire le vstack si c'est le premier objet
            ft=np.array(f1)
            nt=np.array(n1)
            vt=np.array(v2)
        else:
            ft=np.vstack((ft,f1))
            nt=np.vstack((nt,n1))
            vt=np.vstack((vt,v2))
        objet=ft,vt,nt
    return objet

def Fusion(*args):
    l = len(args) 
    for i in range(l):
        if i == 0:            
            f,v,n = args[i]
            nv = len(v)
        else:
            f2,v2,n2 = args[i]
            f = np.vstack((f,f2+nv))
            v = np.vstack((v,v2))
            n = np.vstack((n,n2))
            nv = len(v)
        objet=f,v,n
    return objet     

def copieob(objet):
    f,v,n = objet
    fc = np.array(f)
    vc = np.array(v)
    nc = np.array(n)
    objet = fc,vc,nc
    return objet

def dupliquer(objet):
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    return f,v,n

def translation(objet, dep):#Déplacement donné sous la forme d'une matrice [dx,dy,dz]
    f,v,n = objet
    v = v + dep
    objet = f,v,n
    return objet

def reprect3D(objet,nbx,nby,nbz,dx,dy,dz): #Si l'instance est 0, mettre 1
    rep = np.empty((3,3))
    for i in range(nbx):
        for j in range(nby):
            for k in range(nbz):
                copie = copieob(objet)
                copie = translation(objet, [i*dx,j*dy,k*dz])
                rep = Fusion(copie,rep)         
    return rep

def rotationcyl(objet,nb,axe): #Permet de rendre le cylindre rond
    for i in range (nb):
        c=rotation(objet,np.pi*i/nb,axe) #fait la rotation autour de l'axe
        if i == 0:
            objet2=c
        else:
            objet2=Fusion(objet2,c)
    return objet2
    
def gazon(x,y,z): #Permet de créer les tas de gazon
    pel=grandeur(20, 10, 1, triangle) #création de 5 gazon
    pel=rotation(pel, np.pi/2, "y")
    pel2=copycentre(pel)
    pel2=emplacement(5, 20, 5, pel2)
    pel3=copycentre(pel)
    pel3=emplacement(-5, 15, 7, pel3)
    pel4=copycentre(pel)
    pel4=emplacement(-5, -8, 2, pel4)
    pelgr1=Fusion(pel,pel2,pel3,pel4) #création de 4 tas de gazon
    pelgr2=copycentre(pelgr1)
    pelgr2=emplacement(0, 0, 8, pelgr2)
    pelgr2=rotation(pelgr2, np.pi/3, 'z')
    pelgr3=copycentre(pelgr1)
    pelgr3=emplacement(-15, 20, 10, pelgr3)
    pelgr3=rotation(pelgr3, 5*np.pi/3, 'z')
    pelgr4=copycentre(pelgr1)
    pelgr4=emplacement(-15, -20, 12, pelgr4)
    pelgr4=rotation(pelgr4, 5*np.pi/6, 'z')
    gazon=Fusion(pelgr1,pelgr2,pelgr3,pelgr4)
    gazon=emplacement(x, y, z, gazon)
    return gazon


#tour de contrôle
cylindre1=copycentre(cylindre)
cylindre1=grandeur(160,160,400,cylindre1)
cylindre1=acote_plan(cylindre1,"xy")
cylindre1=rotationcyl(cylindre1,8,"z")

diamant1=copycentre(diamant)
diamant1=grandeur(300,300,240,diamant1)
diamant1=emplacement(0,0,max(cylindre1[1][:,2]),diamant1)

diamant2=copycentre(diamant)
diamant2=grandeur(240,240,180,diamant2)
diamant2=emplacement(0,0,max(diamant1[1][:,2])-20,diamant2)
        
base=copycentre(cube)
base=grandeur(3200,7000,50,base)
base=emplacement(0,250,-20,base)

antenne1 = copycentre(cylindre)
antenne1 = rotationcyl(antenne1,9,'z')
antenne1 = grandeur(7, 7, 50, antenne1)
antenne1 = acote_plan(antenne1,'xy')

antenne2 = copycentre(cylindre)
antenne2 = rotationcyl(antenne2,9,'z')
antenne2 = grandeur(5, 5, 50, antenne2)
antenne2 = emplacement(0,0,75,antenne2)

boutantenne = copycentre(diamant)
boutantenne = grandeur(8,8,8,boutantenne)
boutantenne = emplacement(0,0,100,boutantenne)

antenne = Fusion(antenne1,antenne2,boutantenne)
antenne = translation(antenne,[55,55,0])

plaque = copycentre(cylindre)
plaque = grandeur(160,160,8,plaque)
plaque = rotationcyl(plaque,9,"z")

radarbarre = copycentre(cylindre)
radarbarre = rotationcyl(radarbarre,9,'z')
radarbarre = acote_plan(radarbarre,'xy')
radarbarre = grandeur(14,14,60,radarbarre)

#pr = piece radar

pr1=copycentre(cube)
pr1=grandeur(100, 2, 20, pr1)
prcentre=RepCirculaire(pr1, 25, 150, 1.05*np.pi, 'x')
prcentre=RepCirculaire(pr1, 25, 150, 1.05*np.pi, 'x')
pr=acote_plan(prcentre,"yz")

devant=copycentre(cube)
devant=grandeur(2, 162, 10,devant)
devant=emplacement(0,0,0,devant)
devant=RepCirculaire(devant, 50, 70, np.pi, 'x')

derriere=copycentre(cube)
derriere=grandeur(2, 152, 10,derriere)
derriere=emplacement(100, 75, 0, derriere)
derriere=RepCirculaire(derriere, 50, 0, np.pi, 'x')

pr2 = copycentre(cube)
pr2 = grandeur(100,300,5,pr2)
pr2 = acote_plan(pr2,'yz')

radar = Fusion(pr,devant,derriere,pr2)
radar = rotation(radar,0.5*np.pi,'x')
radar = grandeur(120,30,25,radar)
radar = emplacement(0,0,60,radar)

plateforme = Fusion(plaque,antenne,radarbarre,radar)
plateforme=grandeur(260,260,200,plateforme)
plateforme=emplacement(0,0,980,plateforme)

tour = Fusion(diamant1,diamant2, cylindre1)
tour = Fusion((tour[0],tour[1]*1.5,tour[2]),base,plateforme)


#dogfight
f18a=copycentre(f18)
f18a=grandeur(250,250,90,f18a)
f18a=rotation(f18a,0.75*np.pi/2,"y")
f18a=emplacement(0,0,max(tour[1][:,2]+200),f18a)
dogfight=RepCirculaire(f18a, 3, 700, 2*np.pi, 'z')
tour=Fusion(tour,dogfight)


#Hangar
mur=copycentre(cube)
mur=grandeur(400, 2, 20, mur)
toit_centre=RepCirculaire(mur, 25, 150, 1.05*np.pi, 'x')
toit=acote_plan(toit_centre,"yz")

devant=copycentre(cube)
devant=grandeur(10, 55, 10,devant)
devant=emplacement(0,28,0,devant)
devant=RepCirculaire(devant, 50, 95, np.pi, 'x')

derriere=copycentre(cube)
derriere=grandeur(2, 152, 10,derriere)
derriere=emplacement(400, 75, 0, derriere)
derriere=RepCirculaire(derriere, 50, 0, np.pi, 'x')

Hangar=Fusion(toit,devant,derriere)
Hangar=emplacement(1300,1000,70,Hangar)
Hangar=reprect3D(Hangar,1,6,1,1,-400,1)


#piste
cube1=copycentre(cube)
cube1=grandeur(30,200,40,cube1)

triangle1=copycentre(triangle)
triangle1=grandeur(50,180,40,triangle1)
triangle1=acote_plan(acote_plan(triangle1,"xz"),"yz")
fleche=Fusion(cube1,triangle1)
fleche=RepCirculaire(fleche,2,0,2*np.pi,"y")
fleche=emplacement(-950,-1000,0,fleche)
fleche=reprect3D(fleche,1,3,1,1,350,1)

ligne1=copycentre(cube)
ligne1=grandeur(250,20,40,ligne1)
ligne1=emplacement(-950,-150,0,ligne1)

ligne2=copycentre(cube)
ligne2=grandeur(20,150,40,ligne2)
ligne2=emplacement(-875,0,0,ligne2)
ligne2=reprect3D(ligne2,2,1,1,-150,1,1)

ligne3=copycentre(cube)
ligne3=grandeur(20,150,40,ligne3)
ligne3=emplacement(-950,400,0,ligne3)
ligne3=reprect3D(ligne3,1,9,1,1,400,1)

piste=copycentre(cube)
piste=grandeur(250,5000,30,piste)
piste=emplacement(-950,1250,0,piste)

f18b=copycentre(f18)
f18b=grandeur(250,250,90,f18b)
f18b=rotation(rotation(f18b,-0.15*np.pi/2,"x"),np.pi,"z")
f18b=emplacement(-950,3500,100,f18b)

piste=Fusion(cube1,fleche,ligne1,ligne2,ligne3,piste,f18b)

piste2=copycentre(piste)
piste2=rotation(piste2,-np.pi/5,"z")
piste2=emplacement(0,1450,60,piste2)
piste=Fusion(piste,piste2)


#building
rotonde=grandeur(300, 300, 150, cylindre)
rotonde=emplacement(000, 000, 75, rotonde)
batisse=grandeur(200, 600, 100, cube)
batisse=emplacement(0, -300, 50, batisse)
petit=grandeur(300, 300, 60, cube)
petit=emplacement(50, 100, 30, petit)

toit1=grandeur(100, 300, 174, cube)
toit1=emplacement(100, 0, 0, toit1)
toit2=dupliquer(toit1)
toit1=rotation(toit1, np.pi/3,'y')
toit2=rotation(toit2, 2*np.pi/3,'y')

toit=Fusion(toit1,toit2)
toit=emplacement(50, 100, 60, toit)

bordure1=rotation(cylindre, np.pi/2, 'x')
bordure1=grandeur(10, 610, 10, bordure1)
bordure1=emplacement(-100, -300, 50, bordure1)

bordure2=dupliquer(bordure1)
bordure2=emplacement(100, -300, 50, bordure2)

bordure3=rotation(cylindre, np.pi/2, 'y')
bordure3=grandeur(200, 10, 10, bordure3)
bordure3=emplacement(0, -605, 50, bordure3)

bordure4=grandeur(10, 10, 105, cylindre)
bordure4=emplacement(100, -605, 53, bordure4)
bordure5=dupliquer(bordure4)
bordure5=emplacement(-100, -605, 53, bordure5)

bordure123=Fusion(bordure1,bordure2,bordure3)
bordure6=dupliquer(bordure123)
bordure6=emplacement(0, -300, 100, bordure6)

bordure=Fusion(bordure1,bordure2,bordure3,bordure4,bordure5,bordure6)

bloc=grandeur(1, 1, 1, cube)
base=rotation(triangle, np.pi/2, 'y')
base=grandeur(5, 5, 5, base)
base=rotation(triangle, 3*np.pi/2, 'z')

airvent=Fusion(bloc,base)
airvent=rotation(airvent, np.pi/2, 'y')
airvent=grandeur(10, 20, 10, airvent)
airvent=emplacement(-50, -500, 105, airvent)
airvent=reprect3D(airvent, 3, 4, 1, 50, 100, 1)

porte=grandeur(5, 10, 20, cube)
porte=reprect3D(porte, 2, 5, 1, 200, 160, 1)
porte=emplacement(0, -150, 10, porte)

building=Fusion(batisse,rotonde,petit,toit,bordure,airvent,porte)
building=building[0],building[1]*1.5,building[2]


#taxiway
taxiway=copycentre(cube)
taxiway=grandeur(250,2570,20,taxiway)
taxiway=emplacement(900,70,0,taxiway)

taxiway2=copycentre(cube)
taxiway2=grandeur(250,940,20,taxiway2)
taxiway2=rotation(taxiway2,np.pi/4,"z")
taxiway2=emplacement(600,1600,0,taxiway2)

f18c=copycentre(f18)
f18c=grandeur(250,250,90,f18c)
f18c=rotation(f18c,1.2*np.pi,"z")
f18c=emplacement(900,-800,65,f18c)
f18c=reprect3D(f18c,1,3,1,1,500,1)

taxiway=Fusion(taxiway,taxiway2,f18c)


#helipad
cote=grandeur(6, 40, 10, cube)
cote=emplacement(0, 0, 20, cote)
cote=RepCirculaire(cote, 33, 200, 2*np.pi, 'z')
cote=emplacement(0, 3000, 20, cote)

H=grandeur(180, 10, 15, cube)
H=reprect3D(H, 1, 2, 1, 1, 130, 1)
H=emplacement(0, 3000, 20, H)

bar=grandeur(10, 130, 15, cube)
bar=emplacement(0, 3000, 20, bar)

base=grandeur(500, 500, 20, cube)
base=emplacement(0, 3000, 6, base)

marche=grandeur(20, 20, 100, triangle)
marche=rotation(marche, np.pi/2, 'y')
marche=rotation(marche, 3*np.pi/2, 'z')
marche=emplacement(10, 0,6 , marche)
marche=RepCirculaire(marche, 4, 250, 2*np.pi, 'z')
marche=emplacement(0, 3000, 6, marche)

helipad=Fusion(cote,H,bar,base,marche)
helipad=emplacement(0, 3000, 20, helipad)


#gazon
gazon1=gazon(550, 1200, 10)
gazon2=gazon(350, 650, 10)
gazon3=gazon(-100, 900, 10)
gazon4=gazon(1200, 1400, 10)
gazon5=gazon(950, 1950, 10)
gazon6=gazon(1450, 2500, 10)
gazon7=gazon(800, 3400, 10)
gazon8=gazon(-500, 3000, 10)
gazon9=gazon(150, 2200, 10)
gazon10=gazon(-650, 1400, 10)
gazon11=gazon(-1300, 3500, 10)
gazon12=gazon(-1200, 850, 10)
gazon13=gazon(-1500, 2100, 10)
gazon14=gazon(-400, -100, 10)
gazon15=gazon(500, -400, 10)
gazonfin=Fusion(gazon1,gazon2,gazon3,gazon4,gazon5,gazon6,gazon7,gazon8,gazon9,gazon10,gazon11,gazon12,gazon13,gazon14,gazon15)

f,v,n=Fusion(dogfight,tour,piste,Hangar,building,taxiway,helipad,gazonfin)
EcrireSTLASCII("test.stl", f, v, n)
