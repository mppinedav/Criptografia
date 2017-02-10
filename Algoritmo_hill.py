
import numpy as np
import re

def convert_to_mod26(message):
  """
  Funcion que convierte el texto ingresado a su valor correspondiente en entero
  segun el algoritmo de Hill
  
  Parameters
  ----------
  message : str
      Mensaje ingresado por el usuario
      
  Returns
  -------
  numpy.array
      Mensaje convertido a su valor correspondiente a enteros

  """
  message = re.sub("[^a-zA-z]", "", message)
  message=message.upper()
  arr = np.array([ord(i) - ord('A') for i in message], dtype=int)
  if len(arr)%2==1:
    arr= np.append(arr,[0])
  return arr
  
  
def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modular_inverse(a, m):
  """
  Funcion que calcula el inverso modular con el 
  algoritmo extendido de Euclides
  
  Parameters
  ----------
  a : int
      Numero al que se desea calcular el inverso modular
  m : int
      modulo sobre el que se va a trabajar
  Returns
  -------
  int
      El inverso de a mod m

  """
  g, x, y = egcd(a, m)
  if g != 1:
    raise Exception('El inverso modulo 26 para este valor no existe')
  else:
    return x % m


def encrypt(matrix, arr):
  """
  Funcion que decifra un mensaje segun el algoritmo de hill
  
  Parameters
  ----------
  matrix : numpy.matrix
      Matriz de 2x2 que representa la clave de cifrado
  array : numpy.array
      Array de enteros correspondiente al mensaje a cifrar
  Returns
  -------
  string
      El mensaje cifrado mod 26 correspondiente al algoritmo de Hill

  """
  cipher= ''
  for i in range(0,len(arr)-1,2):
    pair= np.array([arr[i], arr[i+1]])
    number= np.array( pair* matrix%26)
    cipher += chr(int(str(number[0][0])) + ord('a'))+chr(int(str(number[0][1])) + ord('a'))
  return cipher.upper()


def inverse_mod_26(matrix):
  """
  Funcion que calcula la matriz inversa modulo 26 de una matriz dada
  
  Parameters
  ----------
  matrix : numpy.matrix
      matriz que representa la llave de cifrado
  Returns
  -------
  numpy.matrix
      Matriz inversa calculada con la matriz de cofactores transpuesta y el determinante modulo 26 

  """
  ct= (np.linalg.inv(matrix).T * np.linalg.det(matrix)).T
  det= int(np.linalg.det(matrix)%26)
  invdet= modular_inverse(det,26)
  invermod26= np.matrix(ct*invdet%26)
  return invermod26
  
  
def decrypt(matrix, arr):
  """
  Funcion que decifra un mensaje cifrado con el algoritmo de Hill
  
  Parameters
  ----------
  matrix : numpy.matrix
      Matriz que corresponde a la llave de cifrado
  arr : numpy.array
      array que contiene el valor modulo 26 del mensaje cifrado
  Returns
  -------
  str
      Mensaje decifrado

  """
  message= ''
  minv = inverse_mod_26(matrix)
  for i in range(0,len(arr)-1,2):
    pair= np.array([arr[i], arr[i+1]])
    number= np.array( pair* minv%26, dtype='int')
    message += chr(int(str(number[0][0])) + ord('a'))+chr(int(str(number[0][1])) + ord('a'))
  return message.upper()
  

  
def main():
  
  task= int(input("Para cifrar ingrese 1, para decifrar ingrese 2:"))
  while (task != 1 and task != 2):
    task= int(input("El valor ingresado no es valido. Para cifrar ingrese 1, para decifrar ingrese 2:"))
  print (task)
  print("La llave es una matriz 2x2. Ingrese cada elemento de la matriz separado por enter.")
  print("Elementos de la fila 1")
  fila1 = int(input()),int(input())
  print("Elementos de la fila 2")
  fila2 = int(input()),int(input())
  key= np.matrix([fila1, fila2])
  if task ==1:
    message= input("Ingrese el mensaje en texto claro. Solo se tendra en cuenta los caracteres correspondientes a letras. Los demas se eliminaran de la lista")
    message_int= convert_to_mod26(message)
    cipher=encrypt(key,message_int)
    print("El mensaje cifrado es:", cipher)
  
  else:
    cipher_m= input("Ingrese el mensaje cifrado")
    cipher_int= convert_to_mod26(cipher_m)
    message=decrypt(key,cipher_int)
    print("El mensaje es:", message)
    
    
  

main()  
