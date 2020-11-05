#Operaciones + Lab
#12-10-2020

def Media(x):
    y = len(x)
    z = 0
    for indice in x:
        z = z + indice 
    r = z/y    
    r_ = 0
    for desv in x:
        r_ = ((desv - r)**2) + r_
    des  = (r_ / (y - 1))
    des_ = (des**(0.5))
    
    return z, y, r, des, des_
    
anderson = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

z, y, r, des, des_ = Media(anderson)
print("Suma De Todos Los Datos : {} \nNumero De Datos : {}\nPromedio : {}\nVarianza : {} \nDesviación : {}"
      .format(z, y, r, des, des_))
