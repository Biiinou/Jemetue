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
    rep = []
    for i in range(nbx):
        for j in range(nby):
            for k in range(nbz):
                copie = copieob(objet)
                copie = translation(objet, [i*dx,j*dy,k*dz])
                rep += [copie]
                
    for i in range(len(rep)):
        if i == 0:
            repet = rep[0]
        else:
            repet = Fusion(rep[i],repet)
            
    return repet

    
#tour de contrôle
cylindre1=copycentre(cylindre)
cylindre1=grandeur(160,160,400,cylindre1)
cylindre1=acote_plan(cylindre1,"xy")

diamant1=copycentre(diamant)
diamant1=grandeur(300,300,240,diamant1)
diamant1=emplacement(0,0,max(cylindre1[1][:,2]),diamant1)

diamant2=copycentre(diamant)
diamant2=grandeur(240,240,180,diamant2)
diamant2=emplacement(0,0,max(diamant1[1][:,2])-20,diamant2)


for i in range (8):
    c=rotation(cylindre1,np.pi*i/8,"z")
    if i == 0:
        cylindre2=c
    else:
        cylindre2=Fusion(cylindre2,c)
        
base=copycentre(cube)
base=grandeur(3200,7000,10,base)
base=emplacement(0,250,0,base)

tour = Fusion(diamant1,diamant2, cylindre1, cylindre2)
tour = Fusion((tour[0],tour[1]*1.5,tour[2]),base)


#dogfight
f18a=copycentre(f18)
f18a=grandeur(250,250,90,f18a)
f18a=rotation(f18a,0.75*np.pi/2,"y")
f18a=emplacement(0,0,max(tour[1][:,2]),f18a)
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
f18b=rotation(rotation((grandeur(250,250,90,f18b)),-0.15*np.pi/2,"x"),np.pi,"z")
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
#petit=acote_planobjet(petit, 'yz')


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
# taxiway=copycentre(cube)
# taxiway=grandeur

f,v,n=Fusion(dogfight,tour,piste,Hangar,building)

EcrireSTLASCII("test.stl", f, v, n)
