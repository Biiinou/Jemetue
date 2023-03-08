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






def rotationcyl(objet,nb,axe): #Permet de rencre le cylindre rond
    for i in range (nb):
        c=rotation(objet,np.pi*i/nb,axe) #fait la rotation autour de l'axe
        if i == 0:
            objet2=c
        else:
            objet2=Fusion(objet2,c)
    return objet2

#=========builiding centraux======

def dupliquer(objet):
    f1,v1,n1=objet
    f,v,n=np.array(f1),np.array(v1),np.array(n1)
    return f,v,n

rotonde=grandeurobjet(300, 300, 150, cylindre)
rotonde=emplacementobjet(000, 000, 75, rotonde)
batisse=grandeurobjet(200, 600, 100, cube)
batisse=emplacementobjet(0, -300, 50, batisse)
petit=grandeurobjet(300, 300, 60, cube)
petit=emplacementobjet(50, 100, 30, petit)
#petit=acote_planobjet(petit, 'yz')


toit1=grandeurobjet(100, 300, 174, cube)
toit1=emplacementobjet(100, 0, 0, toit1)
toit2=dupliquer(toit1)
toit1=rotationobjet(toit1, np.pi/3,'y')
toit2=rotationobjet(toit2, 2*np.pi/3,'y')

toit=Fusion(toit1,toit2)
toit=emplacementobjet(50, 100, 60, toit)

bordure1=rotationobjet(cylindre, np.pi/2, 'x')
bordure1=grandeurobjet(10, 610, 10, bordure1)
bordure1=emplacementobjet(-100, -300, 50, bordure1)

bordure2=dupliquer(bordure1)
bordure2=emplacementobjet(100, -300, 50, bordure2)

bordure3=rotationobjet(cylindre, np.pi/2, 'y')
bordure3=grandeurobjet(200, 10, 10, bordure3)
bordure3=emplacementobjet(0, -605, 50, bordure3)

bordure4=grandeurobjet(10, 10, 105, cylindre)
bordure4=emplacementobjet(100, -605, 53, bordure4)
bordure5=dupliquer(bordure4)
bordure5=emplacementobjet(-100, -605, 53, bordure5)

bordure123=Fusion(bordure1,bordure2,bordure3)
bordure6=dupliquer(bordure123)
bordure6=emplacementobjet(0, -300, 100, bordure6)

bordure=Fusion(bordure1,bordure2,bordure3,bordure4,bordure5,bordure6)

bloc=grandeurobjet(1, 1, 1, cube)
base=rotationobjet(triangle, np.pi/2, 'y')
base=grandeurobjet(5, 5, 5, base)
base=rotationobjet(triangle, 3*np.pi/2, 'z')

airvent=Fusion(bloc,base)
airvent=rotationobjet(airvent, np.pi/2, 'y')
airvent=grandeurobjet(10, 20, 10, airvent)
airvent=emplacementobjet(-50, -500, 105, airvent)
airvent=reprect3D(airvent, 3, 4, 1, 50, 100, 1)

porte=grandeurobjet(5, 10, 20, cube)
porte=reprect3D(porte, 2, 5, 1, 200, 160, 1)
porte=emplacementobjet(0, -150, 10, porte)

building=Fusion(batisse,rotonde,petit,toit,bordure,airvent,porte)


#========helipad======

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


#===============================================================================

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



#========================================================================================

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




