# -*- coding: utf-8 -*-
"""ConjugateGradient.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q_IiPg8YGlwTixiuo6e2mOKfhda4F3mD
"""

import numpy as np
import scipy.io

def CG(pval):
  X = np.zeros((pval+1,pval+1))
  for i in range(pval):
    X[0,i] = 1.0*i/pval
    X[i,pval] = 1 - 1.0*i/pval
     
  for i in range(1,pval+1):
    X[i,0] = 1.0*i/pval
    X[pval,i] = 1 - 1.0*i/pval
  
  grad = gradF(X,pval).flatten()
  p = -1*grad
  grad_norm = np.linalg.norm(grad)
  grad_new_norm = np.linalg.norm(grad)
  count = 1
  num_restart = 0
  while(grad_new_norm/grad_norm > 1e-5):
    
    # calculate alpha 
    alpha = 1
    c = 0.25
    rho = 0.5
    flag=0
    while(func(X+alpha*p.reshape((pval+1,pval+1)),pval) >= func(X,pval) + c*alpha*np.dot(grad, p)):
      alpha = rho*alpha
      # restart condition
      if alpha<=0.5:
        flag=1
        break
    print alpha
    
    # update X
    X = X + alpha*p.reshape((pval+1,pval+1))
        
    # calculate gradF
    grad_new = gradF(X,pval).flatten()
    if flag==1:
      beta=0
      print "Restart"
      num_restart+=1
    else:
      # different betas for all the 4 methods. Uncomment appropriately to run for the corrsponding method.
      
      beta = np.dot(grad_new, grad_new)/np.dot(grad, grad) # Fletcher Reeves method
#       beta = np.dot(grad_new, (grad_new - grad))/np.linalg.norm(grad) # PR mrthod
#       beta = np.max(np.dot(grad_new, (grad_new - grad))/np.linalg.norm(grad), 0) # PR+ method
#       beta = np.dot(grad_new, (grad_new - grad))/np.dot((grad_new - grad),p) # HS method
  
      
    if num_restart==10:
      break
    
    p = -1*grad_new + beta*p
    grad_new_norm = np.linalg.norm(grad_new)
    
      
    grad = np.copy(grad_new)
    print grad_new_norm/grad_norm
    print "Beta is", beta
    count+=1
    
  return X,count,num_restart

def func(x,pval):
  val = 1/float(pval**2)
  summation = 0
  for i in range(pval):
    for j in range(pval):
      v1 = (x[i,j] - x[i+1,j+1])**2
      v2 = (x[i,j+1] - x[i+1,j])**2
      summation = summation + np.sqrt(1 + (pval**2/float(2))*(v1 + v2))
  return val*summation

def gradF(x, pval):
  grad = np.zeros((pval+1,pval+1))
  for i in range(1,pval):
    for j in range(1,pval):
      val1 = x[i,j] - x[i+1,j+1]
      v1 = (x[i,j] - x[i+1,j+1])**2
      v2 = (x[i,j+1] - x[i+1,j])**2
      val2 = 2*np.sqrt(1 + (pval**2/float(2))*(v1 + v2))

      val3 = x[i,j] - x[i-1,j+1]
      v3 = (x[i-1,j] - x[i,j+1])**2
      v4 = (x[i-1,j+1] - x[i,j])**2
      val4 = 2*np.sqrt(1 + (pval**2/float(2))*(v3 + v4))

      val5 = x[i,j] - x[i+1,j-1]
      v5 = (x[i,j-1] - x[i+1,j])**2
      v6 = (x[i,j] - x[i+1,j-1])**2
      val6 = 2*np.sqrt(1 + (pval**2/float(2))*(v5 + v6))
      
      val7 = x[i,j] - x[i-1,j-1]
      v7 = (x[i-1,j-1] - x[i,j])**2
      v8 = (x[i-1,j] - x[i,j-1])**2
      val8 = 2*np.sqrt(1 + (pval**2/float(2))*(v7 + v8))
      
      grad[i,j] = 1.0*val1/val2 + 1.0*val3/val4 + 1.0*val5/val6 + 1.0*val7/val8
    
  return grad

X,count,num_restart = CG(pval=101)
print X,count,num_restart
