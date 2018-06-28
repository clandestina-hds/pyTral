import numpy as np
from scipy.signal import butter, filtfilt

class Operations():
#%%
    def fracTriangle(senial):
        tam = len(senial) 
        senial=senial.reshape((tam,))
        fracta = np.zeros((tam, 5))
        fracta[:,0] = np.arange(tam)
        fracta[:,1] = senial
        fracta = fracta[fracta[:,1].argsort()[::-1]]
        tamGroup=tam//3
        ini=0
        fin=tamGroup
        for i in range(3):
            fracta[ini:fin,2]=i+1
            ini=ini+tamGroup
            fin=fin+tamGroup
        fracta = fracta[fracta[:,0].argsort()]
        pInicial=[0.5,0.33]
        p1=[0,0]
        p2=[1,0]
        p3=[0.5,1]
        for i in range(tam):
            if(fracta[i,2]==1):
                pInicial=np.mean([p1,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==2):
                pInicial=np.mean([p2,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==3):
                pInicial=np.mean([p3,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
        #fracta=np.round(fracta,6)
        return fracta
    
#%%
    def fracSquare(senial):
        tam = len(senial) 
        senial=senial.reshape((tam,))
        fracta = np.zeros((tam, 5))
        fracta[:,0] = np.arange(tam)
        fracta[:,1]=senial
        
        fracta = fracta[fracta[:,1].argsort()[::-1]]
        tamGroup=tam//4
        ini=0
        fin=tamGroup
        for i in range(4):
            fracta[ini:fin,2]=i+1
            ini=ini+tamGroup
            fin=fin+tamGroup
        fracta = fracta[fracta[:,0].argsort()]
        pInicial=[0.5,0.33]
        p1=[0,0]
        p2=[1,0]
        p4=[1,1]
        p3=[0,1]
        for i in range(tam):
            if(fracta[i,2]==1):
                pInicial=np.mean([p1,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==2):
                pInicial=np.mean([p2,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==3):
                pInicial=np.mean([p3,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==4):
                pInicial=np.mean([p4,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
        #fracta=np.round(fracta,6)
        return fracta
 
#%%
    def fracPenta(senial):
        tam = len(senial) 
        senial=senial.reshape((tam,))
        fracta = np.zeros((tam, 5))
        fracta[:,0] = np.arange(tam)
        fracta[:,1]=senial
        
        fracta = fracta[fracta[:,1].argsort()[::-1]]
        tamGroup=tam//5
        ini=0
        fin=tamGroup
        for i in range(5):
            fracta[ini:fin,2]=i+1
            ini=ini+tamGroup
            fin=fin+tamGroup
        fracta = fracta[fracta[:,0].argsort()]
        pInicial=[0.5,0.4]
        p1=[0.25,0]
        p2=[0.75,0]
        p3=[1,0.5]
        p4=[0,0.5]
        p5=[0.5,1]
        for i in range(tam):
            if(fracta[i,2]==1):
                pInicial=np.mean([p1,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==2):
                pInicial=np.mean([p2,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==3):
                pInicial=np.mean([p3,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==4):
                pInicial=np.mean([p4,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==5):
                pInicial=np.mean([p5,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
        #fracta=np.round(fracta,6)
        return fracta
    
#%%
    def fracHexa(senial):
        tam = len(senial) 
        senial=senial.reshape((tam,))
        fracta = np.zeros((tam, 5))
        fracta[:,0] = np.arange(tam)
        fracta[:,1]=senial

        fracta = fracta[fracta[:,1].argsort()[::-1]]
        tamGroup=tam//6
        ini=0
        fin=tamGroup
        for i in range(6):
            fracta[ini:fin,2]=i+1
            ini=ini+tamGroup
            fin=fin+tamGroup
        fracta = fracta[fracta[:,0].argsort()]
        pInicial=[0.5,0.5]
        p1=[0.25,0]
        p2=[0.75,0]
        p3=[1,0.5]
        p4=[0.75,1]
        p5=[0.25,1]
        p6=[0,0.5]
        for i in range(tam):
            if(fracta[i,2]==1):
                pInicial=np.mean([p1,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==2):
                pInicial=np.mean([p2,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==3):
                pInicial=np.mean([p3,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==4):
                pInicial=np.mean([p4,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==5):
                pInicial=np.mean([p5,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
            elif(fracta[i,2]==6):
                pInicial=np.mean([p6,pInicial],axis=0)
                fracta[i,3]=pInicial[0]
                fracta[i,4]=pInicial[1]
        #fracta=np.round(fracta,6)
        return fracta
		
#%%
#    def nombredefractal(senial):
#        tam = len(senial) 
#        senial=senial.reshape((tam,))
#        fracta = np.zeros((tam, 5))
#        fracta[:,0] = np.arange(tam)
#        fracta[:,1]=senial
#        N=Número de vértices
#
#        fracta = fracta[fracta[:,1].argsort()[::-1]]
#        tamGroup=tam//N 
#        ini=0
#        fin=tamGroup
#        for i in range(N): 
#            fracta[ini:fin,2]=i+1
#            ini=ini+tamGroup
#            fin=fin+tamGroup
#        fracta = fracta[fracta[:,0].argsort()]
#        pInicial=[0.5,0.5] #Este es el punto inicial
#        #Estas son las coordenadas de los vértices, agregar hasta pN
#        p1=[0.25,0]
#        p2=[0.75,0]
#        p3=[1,0.5]
#        p4=[0.75,1]
#        p5=[0.25,1]
#        p6=[0,0.5]
#        for i in range(tam):
#            if(fracta[i,2]==1): #Aqui se pregunta por la clase a la que pertenece
#                pInicial=np.mean([p1,pInicial],axis=0)#Coincide con el punto 1 
#                fracta[i,3]=pInicial[0]
#                fracta[i,4]=pInicial[1]
#            elif(fracta[i,2]==2):
#                pInicial=np.mean([p2,pInicial],axis=0)
#                fracta[i,3]=pInicial[0]
#                fracta[i,4]=pInicial[1]
#            elif(fracta[i,2]==3):
#                pInicial=np.mean([p3,pInicial],axis=0)
#                fracta[i,3]=pInicial[0]
#                fracta[i,4]=pInicial[1]
#            elif(fracta[i,2]==4):
#                pInicial=np.mean([p4,pInicial],axis=0)
#                fracta[i,3]=pInicial[0]
#                fracta[i,4]=pInicial[1]
#            elif(fracta[i,2]==5):
#                pInicial=np.mean([p5,pInicial],axis=0)
#                fracta[i,3]=pInicial[0]
#                fracta[i,4]=pInicial[1]
#            #Agregar un bloque como las siguientes 4 líneas para cada clase extra 
#            #En la primer línea cambiar por el punto que se está examinando 
#            #al igual que la clase
#            #(cuidar la identación)
#            elif(fracta[i,2]==6):
#                pInicial=np.mean([p6,pInicial],axis=0)
#                fracta[i,3]=pInicial[0]
#                fracta[i,4]=pInicial[1]
#        #fracta=np.round(fracta,6)
#        return fracta
       
#%%
    def noiseDelete(signa):
        M1 = np.max(signa)
        pos = np.argmax(signa)
        signa2=np.delete(signa,pos)
        M2 = np.max(signa2)
        if(M1-M2>0.5):
            print("APLICANDO DESRUIDIZACION")
            positivos = signa[signa>0]
            pos2 = np.argmax(positivos)
            if (pos2>10):
                sLeft = positivos[pos2-10:pos2]
                sRight = positivos[pos2+1:pos2+10]
                values = np.append(sLeft,sRight)
                m = np.mean(values)
                print("VF: ",m)
                signa[pos]=m
        else:
            print("No se aplica eliminación de ruido")
        
#%%    
    def normalSignal(signa):
        Ma = np.max(signa)
        res = signa/Ma
        res = np.squeeze(res)
        n=len(res)
        res=res.reshape(n,1)
        return res
    
#%%    
    #signal : array
    def shiftSignal(signa):
        M=np.mean(signa)
        res = signa-M
        res = np.squeeze(res)
        n=len(res)
        res=res.reshape(n,1)
        return res
    
#%%
    def graphPoinc(s1, s2, lag):
        t1 = len(s1)
        t2 = len(s2)
        lf = np.min((t1, t2))-lag
        if (lf == 0):
            s11=[]
            s22=[]
        else:
            s11 = s1[:lf]
            s22 = s2[lag:lag+lf]
        return s11, s22

#%%
    def centerPoints(s1, s2):
        length = s1.shape[0]
        sum_x = np.sum(s1)
        sum_y = np.sum(s2)
        return sum_x/length, sum_y/length
    
#%%
    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

#%%
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = Operations.butter_lowpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        