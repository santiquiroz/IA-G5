

function [dxdt]= reactor(t,x)
i=1;
Vt    =120;       %Volumen total 
x20    =350+2*(rand*2-1);       %Temperatura del flujo entrada
x210   =350+2*(rand*2-1);       %Temperatura del líquido refrigerante
deltH =-2e5+10*(rand*2-1);      %Calor de la reacción
Ex  =1e4+10*(rand*2-1);       %Energía de activación(E/R)
Cp    =1+0.005*(rand*2-1);         %Calores específicos
rho   =1e3+5*(rand*2-1);       %Densidad de los líquidos
ha    =7*10^5+10*(rand*2-1);    %Coeficiente de transferencia de calor
x10   =1+0.002*(rand*2-1);         %Concentración de producto A en la alimentación del reactor
k0    =7.2e10+100*(rand*2-1);    %Constante de la velocidad de reacción
%Puntos de operacion personalizados
k4     =22+0.01*(rand*2-1);        %Constante de la válvula de salida del tanque
u1     =82+3*(rand*2-1);        %Flujo de Entrada q punto de operacion U1
u2     =105+3*(rand*2-1);       %Flujo de Salida qc punto de operacion U2
k1    =(deltH*k0)/(rho*Cp);%calculo de constante k1
k2    =(rho*Cp)/(rho*Cp);%calculo de constante k2
k3    =ha/(rho*Cp);%calculo de constante k3 
dxdt=[(u1/x(3))*(x10-x(1))-k0*x(1)*exp(-Ex/x(2));(u1/x(3))*(x20-x(2))+k1*x(1)*exp(-Ex/x(2))+k2*(u1/x(3))*(1-exp(-k3/u2))*(x210-x(2));u1-k4*(x(3)^(0.5))]; %sistema de ecaucipones

end

