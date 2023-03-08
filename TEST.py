import numpy as np
import struct
from MEC1315_STL import *


def centrer(v): #Permet de centrer le stl en(0,0,0)
    v[:,0]=v[:,0]-(max(v[:,0])+min(v[:,0]))/2 #centre axe x
    v[:,1]=v[:,1]-(max(v[:,1])+min(v[:,1]))/2 #centre axe y
    v[:,2]=v[:,2]-(max(v[:,2])+min(v[:,2]))/2 #centre axe z
    return v

def grandeur(x,y,z,v): #Permet de changer l'échelle du stl (homothétie), Dois utiliser centrer avant
    v[:,0]=v[:,0]/(max(v[:,0])-min(v[:,0]))*x #mise à l'échelle composant x
    v[:,1]=v[:,1]/(max(v[:,1])-min(v[:,1]))*y #mise à l'échelle composant y
    v[:,2]=v[:,2]/(max(v[:,2])-min(v[:,2]))*z #mise à l'échelle composant z
    return v

def emplacement(x,y,z,v): #Permet de déplacer le stl
    v[:,0]=v[:,0]-(max(v[:,0])+min(v[:,0]))/2+x #déplacement en x
    v[:,1]=v[:,1]-(max(v[:,1])+min(v[:,1]))/2+y #déplacement en y
    v[:,2]=v[:,2]-(max(v[:,2])+min(v[:,2]))/2+z #déplacement en z
    return v
    
def rotation(v,angle,axe): #Permet de tourner le stl
    if axe =="z": #Tourne sur l'axe z
        v=v.dot(np.array([[np.cos(angle),np.sin(angle),0],[-np.sin(angle),np.cos(angle),0],[0,0,1]]))
    elif axe == "y": #Tourne sur l'axe y
        v=v.dot(np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]]))
    elif axe == "x": #Tourne sur l'axe x
        v=v.dot(np.array([[1,0,0],[0,np.cos(angle),np.sin(angle)],[0,-np.sin(angle),np.cos(angle)]]))
    return v

def acote_plan(v,plan): #Perment de déposer le stl sur un plan
    if plan =="xy": #Sur plan XY
        v[:,2]=v[:,2]-min(v[:,2])
    if plan =="xz": #Sur plan XZ
        v[:,1]=v[:,1]-min(v[:,1])
    if plan =="yz": #Sur plan YZ
        v[:,0]=v[:,0]-min(v[:,0])
    return v

def Fusion(*args): #Permet de fusionner tous les stl pour Meshlab
    l = len(args) #Nombre d'élément à fusionner
    
    for i in range(l): #Fusion des éléments
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

def RepCirculaire(nom,nb,r,a,axe): #Permet de faire une répétition circulaire selon un nombre d'élément, un rayon et un angle, sur un axe donné                 
    f1,v1,n1=nom
    nv1=len(v1)    
    t=np.linspace(0,a,nb+1) #Perment de répartir le nombre d'élément équitablement sur l'angle
    t=t[:-1]
    if axe=="z": #Pour l'axe Z            
        x,y=r*np.cos(t),r*np.sin(t)
    if axe=="y": #Pour l'axe Y            
        x,z=r*np.cos(t),r*np.sin(t)
    if axe=="x": #Pour l'axe X             
        y,z=r*np.cos(t),r*np.sin(t)   
    for i in range(len(t)):
        if i != 0: #Si f est le premier élément, ne pas prendre en compte nv1 
            f1=np.array(f1+nv1)
        v2=rotation(v1,t[i],axe)
        if axe=="z":
            v2=v2+[x[i],y[i],0] 
        if axe=="y":
            v2=v2+[x[i],0,z[i]] 
        if axe=="x":
            v2=v2+[0,y[i],z[i]]
        if i ==0: #Si f est le premier élément, ne pas prendre en compte ft,nt et vt 
            ft=np.array(f1)
            nt=np.array(n1)
            vt=np.array(v2)
        else:
            ft=np.vstack((ft,f1))
            nt=np.vstack((nt,n1))
            vt=np.vstack((vt,v2))
    return ft,vt,nt



   
   
   def sim(v,axe):
    if axe=="x":
        s=np.array([[-1,0,0],[0,1,0],[0,0,1]])
    if axe=="y":
        s=np.array([[1,0,0],[0,-1,0],[0,0,1]])
    if axe=="z":
        s=np.array([[1,0,0],[0,1,0],[0,0,-1]])
    if axe=="vertex":
        s=np.array([[-1,0,0],[0,1,0],[0,0,-1]])
    v=np.dot(v,s)
    return v

cube=cube[0],grandeur(200,50,20,centrer(cube[1])),cube[2]
triangle=Fusion((triangle[0],acote_plan(acote_plan(grandeur(180,80,20,centrer(triangle[1])),"xz"),"yz"),triangle[2]),(triangle[0],sim(acote_plan(acote_plan(grandeur(180,80,20,centrer(triangle[1])),"xz"),"yz"),"y"),sim(triangle[2],"vertex")))

#===========Hangar=============#
cube=LireSTL("Cube.stl")

mur=cube[0],grandeur(400, 2, 20, cube[1]),cube[2]
toit=RepCirculaire(mur, 25, 150, np.pi, 'x')

devant=cube[0],grandeur(2, 60, 10, cube[1]),cube[2]
devant=RepCirculaire(devant, 50, 95, np.pi, 'x')

derriere=cube[0],grandeur(2, 152, 10, cube[1]),cube[2]
derriere=derriere[0],emplacement(400, 75, 0, derriere[1]),derriere[2]
derriere=RepCirculaire(derriere, 50, 0, np.pi, 'x')

Hangar=Fusion(toit,devant,derriere)
ff,vf,nf = Hangar
nom_out='hangar.stl'
EcrireSTLASCII(nom_out, ff, vf, nf)







def copycentre(nom):
    f,v,n = nom
    
    fc = np.array(f)
    vc = np.array(v)
    nc = np.array(n)
    
    vc[:,0]=vc[:,0]-(max(vc[:,0])+min(vc[:,0]))/2 #centre axe x
    vc[:,1]=vc[:,1]-(max(vc[:,1])+min(vc[:,1]))/2 #centre axe y
    vc[:,2]=vc[:,2]-(max(vc[:,2])+min(vc[:,2]))/2 #centre axe z
    
    return fc,vc,nc
    
    
   #====meme fonction pour objet=========#
   
   def acote_planobjet(objet,plan): #Perment de déposer le stl sur un plan
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    if plan =="xy": #Sur plan XY
        v[:,2]=v[:,2]-min(v[:,2])
    if plan =="xz": #Sur plan XZ
        v[:,1]=v[:,1]-min(v[:,1])
    if plan =="yz": #Sur plan YZ
        v[:,0]=v[:,0]-min(v[:,0])
    return f,v,n
    
    def emplacementobjet(x,y,z,objet): #Permet de déplacer le stl
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    v[:,0]=v[:,0]-(max(v[:,0])+min(v[:,0]))/2+x #déplacement en x
    v[:,1]=v[:,1]-(max(v[:,1])+min(v[:,1]))/2+y #déplacement en y
    v[:,2]=v[:,2]-(max(v[:,2])+min(v[:,2]))/2+z #déplacement en z
    
    return f,v,n
    
def grandeurobjet(x,y,z,objet): #Permet de changer l'échelle du stl (homothétie), Dois utiliser centrer avant
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    v[:,0]=v[:,0]/(max(v[:,0])-min(v[:,0]))*x #mise à l'échelle composant x
    v[:,1]=v[:,1]/(max(v[:,1])-min(v[:,1]))*y #mise à l'échelle composant y
    v[:,2]=v[:,2]/(max(v[:,2])-min(v[:,2]))*z #mise à l'échelle composant z
    return f,v,n

    def rotationobjet(objet,angle,axe): #Permet de tourner le stl
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    if axe =="z": #Tourne sur l'axe z
        v=v.dot(np.array([[np.cos(angle),np.sin(angle),0],[-np.sin(angle),np.cos(angle),0],[0,0,1]]))
    elif axe == "y": #Tourne sur l'axe y
        v=v.dot(np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]]))
    elif axe == "x": #Tourne sur l'axe x
        v=v.dot(np.array([[1,0,0],[0,np.cos(angle),np.sin(angle)],[0,-np.sin(angle),np.cos(angle)]]))
    return f,v,n

#=============
    def translation(objet, dep):#Déplacement donné sous la forme d'une matrice [dx,dy,dz]
    f,v,n = objet
    v = v + dep
    objet = f,v,n
    return objet



#=====================================================================================================================
#Nouvelle fonction répétition a utiliser


def copieob(objet):
    f,v,n = objet
    fc = np.array(f)
    vc = np.array(v)
    nc = np.array(n)
    objet = fc,vc,nc
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






def rotationcyl(objet,nb,axe):
    for i in range (nb):
        c=objet[0],rotation(objet[1],np.pi*i/nb,axe),objet[2]
        if i == 0:
            objet2=c
        else:
            objet2=Fusion(objet2,c)
    return objet2

