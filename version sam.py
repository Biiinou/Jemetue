# Jemetue
Jemetue
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
diamant2 = LireSTL("Diamant.stl")
cube = LireSTL("Cube.stl")
f18=LireSTL('fighter_jet_f18.stl')

def centrer(v):
    v[:,0]=v[:,0]-(max(v[:,0])+min(v[:,0]))/2
    v[:,1]=v[:,1]-(max(v[:,1])+min(v[:,1]))/2
    v[:,2]=v[:,2]-(max(v[:,2])+min(v[:,2]))/2
    return v

def grandeur(x,y,z,v):
    v[:,0]=v[:,0]/(max(v[:,0])-min(v[:,0]))*x
    v[:,1]=v[:,1]/(max(v[:,1])-min(v[:,1]))*y
    v[:,2]=v[:,2]/(max(v[:,2])-min(v[:,2]))*z
    return v

def emplacement(x,y,z,v):
    v[:,0]=v[:,0]-(max(v[:,0])+min(v[:,0]))/2+x
    v[:,1]=v[:,1]-(max(v[:,1])+min(v[:,1]))/2+y
    v[:,2]=v[:,2]-(max(v[:,2])+min(v[:,2]))/2+z
    return v

def rotation(v,angle,axe):
    if axe =="z":
        v=v.dot(np.array([[np.cos(angle),np.sin(angle),0],[-np.sin(angle),np.cos(angle),0],[0,0,1]]))
    elif axe == "y":
        v=v.dot(np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]]))
    elif axe == "x":
        v=v.dot(np.array([[1,0,0],[0,np.cos(angle),np.sin(angle)],[0,-np.sin(angle),np.cos(angle)]]))
    return v

def acote_plan(v,plan):
    if plan =="xy":
        v[:,2]=v[:,2]-min(v[:,2])
    if plan =="xz":
        v[:,1]=v[:,1]-min(v[:,1])
    if plan =="yz":
        v[:,0]=v[:,0]-min(v[:,0])
    return v

def copycentre(nom):
    f,v,n = nom
    fc = np.array(f)
    vc = np.array(v)
    nc = np.array(n)
    vc[:,0]=vc[:,0]-(max(vc[:,0])+min(vc[:,0]))/2 #centre axe x
    vc[:,1]=vc[:,1]-(max(vc[:,1])+min(vc[:,1]))/2 #centre axe y
    vc[:,2]=vc[:,2]-(max(vc[:,2])+min(vc[:,2]))/2 #centre axe z 
    return fc,vc,nc

def sym(nom,axe):
    f,v,n=nom
    if axe=="x":
        v[:,0]=-v[:,0]
    if axe=="y":
        v[:,1]=-v[:,1]
    if axe=="z":
        v[:,2]=-v[:,2]
    f[0],f[1],f[2]=f[2],f[1],f[0]
    return f,v,n

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
        v2=rotation(v1,t[i],axe)
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
    return ft,vt,nt

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
    return f,v,n     



def reprect(nom,nbx,nby,nbz,dx,dy,dz):
    f,v,n = nom
    nv = len(v)
    for i in range(nbx):
        if i == 0 :
            f = np.array(f)
        else:
            f = np.array(f+nv)
        v2 = np.array(v)       
        n2 = np.array(n)
        v = v + [dx,0,0]
        if i == 0:
            fx = np.array(f)
            vx = np.array(v2)
            nx = np.array(n2)
        else:
            fx = np.vstack((fx,f))
            vx = np.vstack((vx,v2))
            nx = np.vstack((nx,n2))
            
    for i in range(nby):
        if i == 0 :
            f = np.array(f)
        else:
            f = np.array(f+nv)
        v2 = np.array(v)       
        n2 = np.array(n)
        v = v + [0,dy,0]
        if i == 0:
            fx = np.array(f)
            vx = np.array(v2)
            nx = np.array(n2)
        else:
            fx = np.vstack((fx,f))
            vx = np.vstack((vx,v2))
            nx = np.vstack((nx,n2))
          
        for i in range(nbz):
            if i == 0 :
                f = np.array(f)
            else:
                f = np.array(f+nv)
            v2 = np.array(v)       
            n2 = np.array(n)
            v = v + [dx,0,0]
            if i == 0:
                fx = np.array(f)
                vx = np.array(v2)
                nx = np.array(n2)
            else:
                fx = np.vstack((fx,f))
                vx = np.vstack((vx,v2))
                nx = np.vstack((nx,n2))
            for i in range(nbz):
                if i == 0 :
                    f = np.array(f)
                else:
                    f = np.array(f+nv)
                v2 = np.array(v)       
                n2 = np.array(n)
                v = v + [0,0,dz]
                if i == 0:
                    fx = np.array(f)
                    vx = np.array(v2)
                    nx = np.array(n2)
                else:
                    fx = np.vstack((fx,f))
                    vx = np.vstack((vx,v2))
                    nx = np.vstack((nx,n2))
                              
        
    return fx,vx,nx
    



cylindre=cylindre[0],acote_plan(grandeur(160,160,400,centrer(cylindre[1])),"xy"),cylindre[2]
diamant=diamant[0],emplacement(0,0,max(cylindre[1][:,2]),grandeur(300,300,240,centrer(diamant[1]))),diamant[2]
diamant2=diamant2[0],emplacement(0,0,max(diamant[1][:,2])-20,grandeur(240,240,180,centrer(diamant2[1]))),diamant2[2]
for i in range (8):
    c=cylindre[0],rotation(cylindre[1],np.pi*i/8,"z"),cylindre[2]
    if i == 0:
        cylindre2=c
    else:
        cylindre2=Fusion(cylindre2,c)
base=cube[0],emplacement(0,1250,0,grandeur(2500,5000,10,centrer(cube[1]))),cube[2]
tour = Fusion(diamant,diamant2, cylindre, cylindre2)
tour = Fusion((tour[0],tour[1]*1.5,tour[2]),base)

f18a=copycentre(f18)
f18a=cylindre=f18a[0],emplacement(0,0,max(tour[1][:,2]),rotation((grandeur(250,250,90,centrer(f18a[1]))),0.75*np.pi/2,"y")),f18a[2]
dogfight=RepCirculaire(f18a, 3, 700, 2*np.pi, 'z')

mur=cube[0],grandeur(400, 2, 20, cube[1]),cube[2]
toit_centre=RepCirculaire(mur, 25, 150, 1.05*np.pi, 'x')
toit=toit_centre[0],acote_plan(toit_centre[1],"yz"),toit_centre[2]
devant=cube[0],emplacement(0,28,0,grandeur(10, 55, 10, cube[1])),cube[2]
devant=RepCirculaire(devant, 50, 95, np.pi, 'x')
derriere=cube[0],grandeur(2, 152, 10, cube[1]),cube[2]
derriere=derriere[0],emplacement(400, 75, 0, derriere[1]),derriere[2]
derriere=RepCirculaire(derriere, 50, 0, np.pi, 'x')
Hangar=Fusion(toit,devant,derriere)
Hangar=Hangar[0],emplacement(950,1000,70,Hangar[1]),Hangar[2]
Hangar=reprect(Hangar,0,6,0,0,-400,0)

cube=cube[0],grandeur(30,200,40,centrer(cube[1])),cube[2]
triangle1=Fusion(cube,(triangle[0],acote_plan(acote_plan(grandeur(50,180,40,centrer(triangle[1])),"xz"),"yz"),triangle[2]))
fleche=Fusion(triangle1,(RepCirculaire(triangle,2,0,2*np.pi,"y")))
fleche=fleche[0],emplacement(-950,-1000,0,fleche[1]),fleche[2]
fleche=reprect(fleche,0,3,0,0,350,0)
ligne=cube[0],emplacement(-950,-150,0,grandeur(250,20,40,centrer(cube[1]))),cube[2]
fleche=Fusion(fleche,ligne)
ligne=cube[0],emplacement(-875,0,0,grandeur(20,150,40,centrer(cube[1]))),cube[2]
ligne=reprect(ligne,2,0,0,-150,0,0)
fleche=Fusion(fleche,ligne)
ligne=cube[0],emplacement(-950,400,0,grandeur(20,150,40,centrer(cube[1]))),cube[2]
ligne=reprect(ligne,0,9,0,0,400,0)
fleche=Fusion(fleche,ligne)
piste=cube[0],emplacement(-950,1250,0,grandeur(250,5000,30,centrer(cube[1]))),cube[2]
f18b=copycentre(f18)
f18b=cylindre=f18b[0],emplacement(-950,3500,100,rotation(rotation((grandeur(250,250,90,centrer(f18b[1]))),-0.15*np.pi/2,"x"),np.pi,"z")),f18b[2]
piste=Fusion(piste,fleche,f18b)

f,v,n=Fusion(dogfight,tour,piste,Hangar)

EcrireSTLASCII("test.stl", f, v, n)
