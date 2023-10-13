import random
import math
from array import *
import numpy as np
import matplotlib.pyplot as plt
from scipy. stats import poisson

from clases import Point, Circle, Line

  
A=100 #сторона квадратной области
lamb=0.01 #интенсивность Пуассоновского процесса
r=3 #радиусы объектов
h=20 #раccтояние между точками
experimentsLimit=10000 #максимум экспериментов


firstPoint=Point(random.uniform(0, A), random.uniform(0, A))

lim=30 #Лимит попыток генерации координат второй точки

#Генерация координат второй точки на расстоянии h
i=1 #номер попытки
theta = random.random() * 2 * math.pi  #угол для определения местоположения второй точки
x=h * math.cos(theta) + firstPoint.x
y=h * math.sin(theta)+ firstPoint.y

if x<0 or x>A or y<0 or y>A: #проверка на принадлежность второй точки квадрату со стороной А
  while True: #если не принадлежит
      theta = random.random() * 2 * math.pi #генерируем другой угол
      x=h * math.cos(theta) + firstPoint.x
      y=h * math.sin(theta) + firstPoint.y
      i=i+1
      if x>0 and x<A and y>0 and y<A:
        break
      if i==lim:
        break

if i==lim:
  print("Исчерпан лимит генерации координат второй точки, равный ", lim)
else:
  secondPoint=Point(x, y)
  print("Точки сгенерированы (число попыток: ", i,")")
  print("Первая:", firstPoint)
  print("Вторая:", secondPoint)
  print("Расстояние между точками:", math.sqrt((firstPoint.x-secondPoint.x)**2+((firstPoint.y-secondPoint.y)**2)))
  line=Line(firstPoint, secondPoint) #прямая, которой принадлежат сгенерированные точки


blocks=0 #число блокировок
experimentsCount=0 #счетчик экспериментов

while blocks<10000:
  experimentsCount+=1
  if experimentsCount > experimentsLimit: # если достигнут лимит экспериментов
        break
  ObjCount= poisson.rvs(A**2*lamb) #генерация числа объектов
  #print(experimentsCount, ") Число объектов:", ObjCount)
  objects = [] 
  for i in range(ObjCount): #разбрасываем объекты
    objects.append(Circle(random.uniform(0, A), random.uniform(0, A), r)) #генерация объекта

    if line.distanceToCircleCenter(objects[-1])<=r: #если есть пересечение с линией, на которой находятся точки, нужно проверить пересечение отрезка этой линии и объекта   
      if objects[-1].PointInCicle(firstPoint) == True: #если первая точка отрезка принадлежит кругу, то есть блокировка
        #print("Номер заблокировавшего объекта: ", len(objects), "Причина: 1")
        blocks+=1
        break
      if objects[-1].PointInCicle(secondPoint) == True: #если вторая точка отрезка принадлежит кругу, то есть блокировка
        #print("Номер заблокировавшего объекта: ", len(objects), "Причина: 2")
        blocks+=1
        break
      else: #если точка, в которую падает высота из центра окружности к линии отрезка двух точек, принадлежит отрезку, то есть блокировка
        HeightPoint=line.CoordOfHeight(objects[-1].getCenter())
        if min(firstPoint.x,secondPoint.x)<HeightPoint.x< max(firstPoint.x,secondPoint.x) and min(firstPoint.y,secondPoint.y)<HeightPoint.y< max(firstPoint.y,secondPoint.y): 
          #print("Номер заблокировавшего объекта: ", len(objects), "Причина: 3")
          blocks+=1
          break

print("Число блокировок:", blocks)
print("Число проведенных экспериментов:",experimentsCount)
print("Эмпирическая вероятность блокировки", blocks/experimentsCount)
print("Теоретическая вероятность блокировки", 1-math.exp(-lamb*2*r*(h-2*r)))

#Графики 

blocks=0 #число блокировок
experimentsCount=0 #счетчик экспериментов

while blocks<3:
  plt.axis([0,A,0,A]) 
  rec = plt.Rectangle((0, 0), A, A,color='black', fill=False)
  ax=plt.gca()
  ax.add_patch(rec)
  ax.set_aspect('equal')
  x1, y1 = [firstPoint.x, secondPoint.x], [firstPoint.y, secondPoint.y]
  plt.plot(x1, y1, marker = 'o', color='blue')
  plt.grid(True, which='both')
  experimentsCount+=1
  if experimentsCount > experimentsLimit: # если достигнут лимит экспериментов
        break
  ObjCount= poisson.rvs(A**2*lamb) #генерация числа объектов
  print(experimentsCount, ") Число объектов:", ObjCount)
  objects = [] 
  for i in range(ObjCount): #разбрасываем объекты
    objects.append(Circle(random.uniform(0, A), random.uniform(0, A), r)) #генерация объекта

    if line.distanceToCircleCenter(objects[-1])<=r: #если есть пересечение с линией, на которой находятся точки, нужно проверить пересечение отрезка этой линии и объекта   
      if objects[-1].PointInCicle(firstPoint) == True: #если первая точка отрезка принадлежит кругу, то есть блокировка
        print("Номер заблокировавшего объекта: ", len(objects), "Причина: 1")
        plt.scatter(objects[-1].x, objects[-1].y, color='black')
        circle = plt.Circle((objects[-1].x, objects[-1].y), r,color='red', fill=False)
        ax=plt.gca()
        ax.add_patch(circle)
        blocks+=1
        break
      if objects[-1].PointInCicle(secondPoint) == True: #если вторая точка отрезка принадлежит кругу, то есть блокировка
        print("Номер заблокировавшего объекта: ", len(objects), "Причина: 2")
        plt.scatter(objects[-1].x, objects[-1].y, color='black')
        circle = plt.Circle((objects[-1].x, objects[-1].y), r,color='red', fill=False)
        ax=plt.gca()
        ax.add_patch(circle)
        blocks+=1
        break
      else: #если точка, в которую падает высота из центра окружности к линии отрезка двух точек, принадлежит отрезку, то есть блокировка
        HeightPoint=line.CoordOfHeight(objects[-1].getCenter())
        if min(firstPoint.x,secondPoint.x)<HeightPoint.x< max(firstPoint.x,secondPoint.x) and min(firstPoint.y,secondPoint.y)<HeightPoint.y< max(firstPoint.y,secondPoint.y): 
          print("Номер заблокировавшего объекта: ", len(objects), "Причина: 3")
          plt.scatter(objects[-1].x, objects[-1].y, color='black')
          plt.scatter(line.CoordOfHeight(objects[-1].getCenter()).x, line.CoordOfHeight(objects[-1].getCenter()).y, color='red')
          circle = plt.Circle((objects[-1].x, objects[-1].y), r,color='red', fill=False)
          ax=plt.gca()
          ax.add_patch(circle)
          blocks+=1
          break
    plt.scatter(objects[-1].x, objects[-1].y, color='black')
    circle = plt.Circle((objects[-1].x, objects[-1].y), r,color='black', fill=False)
    ax=plt.gca()
    ax.add_patch(circle)
  plt.savefig(str(blocks)+'.png')
  plt.clf()
    
    

print("------------------------------------------")
print("Число блокировок:", blocks)
print("Число проведенных экспериментов:",experimentsCount)
print("Эмпирическая вероятность блокировки", blocks/experimentsCount)
print("Теоретическая вероятность блокировки", 1-math.exp(-lamb*2*r*(h-2*r)))
