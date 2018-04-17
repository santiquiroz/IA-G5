%Trabajo #1 Control Estrada Salida
%Diego Alejandro Santana Clavijo
clc; clear all; close all
%Punto 1 Modelo Gran Señal Simulink
%Puntos de operacion personalizados
k4    =25;        %Constante de la válvula de salida del tanque
% u1 =q =76;        %Flujo de Entrada q punto de operacion U1
% u2 =qc=108;       %Flujo de Salida qc punto de operacion U2
% x1 =Ca=0.9965;    %Concentracion Ca punto de operaxion X1
% x2 =T =350.3;     %Tempratura T punto de operacion X2
% x3 =V =9.242;     %Volumen V punto de operacion X3
%Parámetros
Vt    =120;       %Volumen total 
To    =350;       %Temperatura del flujo entrada
Tco   =350;       %Temperatura del líquido refrigerante
deltH =-2e5;      %Calor de la reacción
Eact  =1e4;       %Energía de activación(E/R)
Cp    =1;         %Calores específicos
rho   =1e3;       %Densidad de los líquidos
ha    =7*10^5;    %Coeficiente de transferencia de calor
Cao   =1;         %Concentración de producto A en la alimentación del reactor
ko    =7.2e10;    %Constante de la velocidad de reacción
%Ecuaciones Complementarias
k1    =(deltH*ko)/(rho*Cp);
k2    =(rho*Cp)/(rho*Cp);
k3    =ha/(rho*Cp);

%%
%Punto 2
clc; clear all;
%Punto de equilibrio Sistema
x=[0.9965; 350.3; 9.242]; %x1,x2,x3 10%
u=[76; 108];    %U1,U2
%x =[Ca; T; V]; %x1,x2,x3
%u =[q;qc];     %U1,U2

%%
%Punto 2-1
%Linealizacion
[A,B,C,D]=linmod('TanqueCSTRinout',x,u);
sys =ss(A,B,C,D)
%Comprobar el sistema en el punto de operacion
figure(1)
    step(sys)
    grid on
%%[num,den] =ss2tf(A,B,C,D,1)

%%
%Punto 3 
%Funcion de Transferencia
%nvo=A(3,:)*B(:,1)multiflicando colxfila
G=tf(sys(3,1))%Funcion de transferencia salida3/entrada1

%%
%Punto4 Simulink Pequeña y Gran Señal
%%
%Punto 5 Respuestas en el Dominio del Tiempo y Dominio de la Frecuencia
%lazo Abierto
figure(2)
    step(G)
    grid on
    title('Respuesta del Sistema en el Dominio del Tiempo')
figure(3)
    bode(G)
    grid on
    title('Respuesta del Sistema en el Dominio de la Frecuencia')
% figure(4)
%     pzmap(G)
% figure(5)
%     rlocus(G)
%%
%Punto 6 Analisis del Sistema con diferentes polos y ceros adicionales
%Polo original en -4.112

%Polos Adicionales
for p=[0.1,0.5,4.112,8.224,41.12]
    Gp =zpk([],[-1,-p],p);
    figure(5)
        step(Gp);hold on;grid on
        title('Respuesta en el tiempo a polos adicionales','fontsize',16)
    figure(6)
        bode(Gp);hold on;grid on
        title('Respuesta en frecuencia a polos adicionales','fontsize',16)
    figure(7)
        pzmap(Gp);hold on
        title('Lugar de los polos adicionales','fontsize',16)
end
figure(5)
    legend('P=0.1','P=0.5','P Org','P=8.224','P=41.12','Location','South')
figure(6)
    legend('P=0.1','P=0.5','P Org','P=8.224','P=41.12','Location','West')
figure(7)
    legend('P=0.1','P=0.5','P Org','P=8.224','P=41.12','Location','South')
%%
%%%%%%%%%%
%Zero Adicional Semiplano izquierdo y derecho

for z=[0.1,0.5,4.112,6,-.1,-.5,-4.112]
    Gz =zpk([-z],[-1,-4.112],4.112/z);
    figure(8)
        step(Gz);hold on;grid on
        title('Respuesta en el tiempo a ceros adicionales en los dos semiplanos','fontsize',16)
    figure(9)
        bode(Gz);hold on;grid on
        title('Respuesta en frecuencia a ceros adicionales en los dos semiplanos','fontsize',16)
    figure(10)
        pzmap(Gz);hold on
        title('Lugar de los ceros adicionales en los dos semiplanos','fontsize',16)
end
figure(8)
    legend('Z=0.1','Z=0.5','Orginal','Z=6','Z= -0.1','Z= -0.5','Z= Inv Original','Location','South')
figure(9)
    legend('Z=0.1','Z=0.5','Orginal','Z=6','Z= -0.1','Z= -0.5','Z= Inv Original','Location','West')
figure(10)
    legend('Z=0.1','Z=0.5','Orginal','Z=6','Z= -0.1','Z= -0.5','Z= Inv Original','Location','South')
    
    
%%
%Polos Adicionales semiplano derecho 
for p=[-2,-8,4.112]
    Gp =zpk([],[-1,-p],p);
    figure(11)
        step(Gp);hold on;grid on
        title('Respuesta en el tiempo a polos adic. semi inestable','fontsize',12)
    figure(12)
        bode(Gp);hold on;grid on
        title('Respuesta en frecuencia a polos adic. semi inestable','fontsize',12)
    figure(13)
        pzmap(Gp);hold on
        title('Lugar de los polos adic. semi inestable','fontsize',12)
end
    