"""
Práctica 1: Diseno de controladores

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Morales Diaz Ramon Ivan 
Número de control: 24210589
Correo institucional: l24210589@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
# pip install numpy control matplotlib

# librerias
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# datos generales de la simulacion
x0,t0,tend,dt,w,h, = 0,0,10,1E-3,7,3.5
N = round(tend/dt)+1
t = np.linspace(t0,tend,N)
u1 = np.ones(N)
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1
u3 = t/tend
u4 = np.sin(m.pi/2*t)
u = np.column_stack((u1,u2,u3,u4))
signals = ["step","impulse","ramp","sinusoidal"]

#componentes del circuito
#Mios 10E3,1.5E-3,4.7E-6
#Profe 10E3,1E-6,220-6

R,L,C = 4.7E3,1.5E-3,470E-6
num = [C*R*L,C*R**2+L,R]
den = [3*C*L*R,5*C*R**2,2*R]

sys = ctrl.tf(num,den)
print(f"Funcion de transferencia: {sys}\n")

#Polos del sistema
L = np.roots(den)
print(f"polos del sistema: L1 = {L[0]:.3e}, L2 = {L[1]:.3e}\n")
#4.7E-6
#1E-6
#componenetes del controlador
#Mios 2.922,125.263,0.003
#Profe 289.661,7061.510,0.391

kI = 379.856619065551
Cr = 1E-6
Re = 1/(Cr*kI)
numPID = [1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(f"Capacitancia Cr: {Cr} Faradios\n")
print(f"Resistencia Re: {Re} Ohms\n")
print(f"Funcion de transferencia del controlador: {PID}\n")

#Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign = -1)
print(f"Funcion de transferencia en lazo cerrado: {sysPID}\n")

#Colores
clr1 = np.array([30,100,200])/255
clr2 = np.array([200,40,40])/255
clr3 = np.array([40,170,70])/255

#Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,PAu = ctrl.forced_response(sys,t,u,x0)
    return PAu

def closeloop(t,sysPID,u):
    _,PIDu = ctrl.forced_response(sysPID,t,u,x0)
    return PIDu

# Respuestas: Simulaciones numéricas
for i in range(0,4):
    PAu = openloop(t,sys,u[:,i])
    PIDu = closeloop(t,sysPID,u[:,i])
    fg = plt.figure(i+1)
    fg.set_size_inches(w,h)
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.plot(t,u[:,i],'-',color=clr1,label='Ve(t)')
    plt.plot(t,PAu,'--',color=clr2,label='Vs(t)')
    plt.plot(t,PIDu,':',linewidth=2.5,color=clr3,label='I(t)')
    plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
    if i == 0 or i == 1 or i == 2:
        plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.3,0.1))
    elif i == 3:
        plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.4,0.2))
    plt.xlabel('t [s]')
    plt.ylabel('Vi(t) [V]')
    plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
    plt.show()
    fg.savefig(signals[i]+'_python.pdf',bbox_inches='tight')