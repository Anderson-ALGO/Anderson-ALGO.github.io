#Operaciones + Lab

#07-10-2020

#Variables

x = [1, 3, 2, 7, 6, 19]

#Numero de Datos Total

y = len(x)

#La suma de todos los valores

z = 0

for indice in x:
    z = z + indice
   
r = z/y   
 
print("Suma De Todos Los Datos : {} \nNumero De Datos : {}\nPromedio : {} " .format(z, y, r))

#12-10-2020


    
r_ = 0

for desv in x:
    r_ = ((desv - r)**2) + r_

des  = (r_ / (y - 1))
des_ = (des**(0.5))

print("Varianza : {} \nDesviación : {}".format(des,des_))

#END
