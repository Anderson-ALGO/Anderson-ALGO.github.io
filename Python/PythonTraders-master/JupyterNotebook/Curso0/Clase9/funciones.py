
CLAVE_BROOKER = 'EL_TACO_NO'

def prepararTrade(t):
    '''

    Parameters
    ----------
    t : TYPE: Diccionario
        Debe contener al menos la clave Precio 

    Returns
    -------
    t : TYPE
        Devuelve el mismo diccionario modificado ya que agrega las claves:
            stopLoss
            takeProfit
        Ambas variables están en función del la clave Precio que supone el precio de entrada al trade
        

    '''
    import datetime as dt
    
    try:
        t['fecha'] = dt.datetime.now().ctime()
        try:
            t['stopLoss'] = t['Precio'] * 0.95
            t['takeProfit'] = t['Precio'] * 1.1                
        except:
            print('El trade debe contener la clave "Precio"  y eso debe ser un numero')
    except:
        print('El trade debe ser un diccionario')
    
    return t


def bajarYPF():
    import yfinance as yf
    data = yf.download('YPF')
    return data
    
    
def banda_porcentual(precio,porcentaje):
    '''
    

    Parameters
    ----------
    precio : poner si o si un flotante porque si no se rompe todo
        El precio es el precio  .
    porcentaje : TYPE
        DESCRIPTION.

    Returns
    -------
    float
        DESCRIPTION.
    sup : TYPE
        DESCRIPTION.

    '''

    inf = precio * (1-(porcentaje/100))
    sup = precio * (1+(porcentaje/100))
    return inf,sup


def sumar(a,b):
    '''
    Sumar dos números: a y b
    Parámetros: a y b
    
    Si los argumentos pasados no son flotantes, devuelve mensaje de error
    '''
    try:
        suma = a+b
    except:
        suma = 'No se pueden sumar los valores ingresados'
    return suma


def restar(a,b):
    '''
    Restar dos números: a - b
    Parámetros: a y b
    
    Si los argumentos pasados no son flotantes, devuelve mensaje de error
    '''
    try:
        resta = a-b
    except:
        resta = 'No se pueden restar los valores ingresados'
    return resta

