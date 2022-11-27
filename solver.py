import numpy as np

def gaussjordan(a,b):
    a = np.array(a,float)
    b = np.array(b,float)
    n = len(b)
    y = len(a[n-1])
    solution_str= ''
    solution_str+=f'{a}\n{"="*10}\n{b}\n'
    # main loop 
    for k in range(n):
         #partial pivoting
        if k == n-1 and a[k,k]==0 and y==n:
            if b[k] == 0:
                return('A system infinite solutions')
            else:
                return('A system has no solution')
                
        elif n==y:
            if np.fabs(a[k,k]) < 0.00000001:
                for i in range(k+1,n):
                    if np.fabs(a[i,k]) > np.fabs(a[k,k]):
                        for j in range(k,n):
                            a[k,j],a[i,j] = a[i,j],a[k,j]
                
                        b[k], b[i] = b[i],b[k]
                        solution_str+=f'R{k+1}<====>R{i+1}\n{a}\n{"="*10}\n{b}\n'
               
                        break
            #division of the pivot row
            pivot = a[k,k]
            for j in range(k,n):
                a[k,j] /= pivot
            
            b[k] /= pivot
            solution_str+=f'R{k+1}*1/{pivot}=====>R{k+1}\n{a}\n{"="*10}\n{b}\n\n'
        
            
            #Elimaination loop
            for i in range(n):
                if i == k or a[i,k] == 0: continue
                factor =  a[i,k]  
                for j in range(k,n):
                    a[i,j] -= factor * a [k,j]
            
                b[i] -= factor * b[k]
                solution_str+=f'(-{factor}R{k+1})+R{i+1}====>R{i+1}\n'

            solution_str+=f"\n{a}\n{'='*10}\n{b}\n"
        elif y > n:
            return('A system has no solution')
    return solution_str 

# a = [[0,2,9,5],[4,6,2,5],[1,5,4,8],[3,4,7,5]]
# b = [2,6,9,3]

# print(gaussjordan(a,b))