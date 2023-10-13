import random
import math
from array import *
import numpy as np
import matplotlib.pyplot as plt
from scipy. stats import poisson

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
        
  def getX(self):
    return self.x
    
  def getY(self):
    return self.y
    
  def getCoords(self):
    return self.x, self.y
        
  def __repr__(self):
    return f"Point({self.x}, {self.y})"


class Line:
  def __init__(self, point1, point2):
        self.a = point2.y-point1.y
        self.b = point1.x-point2.x
        self.c = point1.y*point2.x-point1.x*point2.y
        self.edge =(point2.y-point1.y)/(point2.x-point1.x)
  
  def CoordOfHeight(self, point): #нахождение координаты высоты от центра окружности до линии, которой принадлежит отрезок длины h
        edge=-1/self.edge
        a=edge
        b=-1
        c=-edge*point.x+point.y
        y=(a*self.c-self.a*c)/(b*self.a-a*self.b)
        x=(-self.c-self.b*y)/self.a
        heightPoint=Point(x,y)
        return heightPoint

  def distanceToPoint(self, point):
        return abs(self.a*point.x+self.b*point.y+self.c)/math.sqrt(self.a**2+self.b**2)

  def distanceToCircleCenter(self, circle):
        return abs(self.a*circle.x+self.b*circle.y+self.c)/math.sqrt(self.a**2+self.b**2)

  def __repr__(self):
    return f"Line: a={self.a}, b={self.b}, c={self.c})"

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __repr__(self):
        return f"Circle({self.x}, {self.y}, r = {self.r})"

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getR(self):
        return self.r
    
    def getCenter(self):
        return Point(self.x,self.y)
    
    def PointInCicle(self, point):
        return (point.x-self.x)**2+(point.y-self.y)**2<=self.r**2
    