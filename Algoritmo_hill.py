
import numpy as np


def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modular_inverse(a, m):
  g, x, y = egcd(a, m)
  if g != 1:
    raise Exception('El inverso modulo 26 para este valor no existe')
  else:
    return x % m

def convert_to_mod26(message):
  message=message.replace(" ", "")
  message=message.upper()
  arr = np.array([ord(i) - ord('A') for i in message], dtype=int)
  if len(arr)%2==1:
    arr= np.append(arr,[0])
  return arr
  
def encrypt(matrix, arr):
  cipher= ''
  for i in range(0,len(arr)-1,2):
    pair= np.array([arr[i], arr[i+1]])
    number= np.array( pair* matrix%26)
    cipher += chr(int(str(number[0][0])) + ord('a'))+chr(int(str(number[0][1])) + ord('a'))
  return cipher.upper()

def inverse_mod_26(matrix):
  ct= (np.linalg.inv(matrix).T * np.linalg.det(matrix)).T
  det= int(np.linalg.det(matrix)%26)
  invdet= modular_inverse(det,26)
  invermod26= np.matrix(ct*invdet%26)
  return invermod26
  
def decrypt(matrix, arr):
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
    message= input("Ingrese el mensaje en texto claro")
    message_int= convert_to_mod26(message)
    cipher=encrypt(key,message_int)
    print("El mensaje cifrado es:", cipher)
  
  else:
    cipher_m= input("Ingrese el mensaje cifrado")
    cipher_int= convert_to_mod26(cipher_m)
    message=decrypt(key,cipher_int)
    print("El mensaje es:", message)
    
    
  

main()  

