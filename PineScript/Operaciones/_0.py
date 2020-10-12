# el comando print imprime 
print(2+2)
hola=1

print('hola')

print(type('hola'))
print(type(hola))

x=1
y='1'

print(x)
print(y)

print(type(x))
print(type(y))

print(x + int(y))
print(str(x) + y)
# se usa int y str para transformar textos y numeros
print('x' + y)

z = float(x)
print(type(z))

print(x)
x =  2  
print(x)

day = 28
month = 'September'
year = 2020

print('hoy es ' + str(day) + 'de' + month + 'del' + str(year))
print('hoy es {} de {} del {}'. format(day, month, year))
# la segunda opcion es mas general si se usa format es mejor 

lista=[1,'dos',3,['a','b','c'],'hola']

print(len(lista))
print(lista[4])

x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

y=range(5, 10, 2 )

for indice in y:
    print("Esta es la ireación: {}".format(indice))
    print(indice)
    
a=0
b=1

a,b=1,2

if a<b:
    print("{} es menor que {}".format (a,b))
elif a==b:
    print("{} es igual que {}".format(a,b))
elif a > b:
    print("{} es mayor que {}". format(a,b))
