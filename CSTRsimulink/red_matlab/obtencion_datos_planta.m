clear
close all
clc
x1o   =0.9951;    %Concentracion Ca punto de operaxion X1
x2o     =350.4;     %Tempratura T punto de operacion X2
x3o     =13.89;     %Volumen V punto de operacion X3
u1     =82;        %Flujo de Entrada q punto de operacion U1
u2    =105;       %Flujo de Salida qc punto de operacion U2
n=100;
tf=20; %tiempo de simulacion
xop=[x1o;x2o;x3o]; %punto de operacion
xin=[1;273.15;0.1]; %condiciones iniciales 

% [t,x]=ode45(@reactor,[0 tf],xin);%solucion de ecaciones y sistema del reactor
% erx1=abs(xop(1)-x(:,1));%error de la variable de concentracion
% erx2=abs(xop(2)-x(:,2));%error de la variable de temperatura
% erx3=abs(xop(3)-x(:,3));%error de la variable de volumen 
% er=[erx1 erx2 erx3];%error de medidas esperadas y reales 


%%
for i=1:n

    [t,x]=ode45(@reactor,[0 tf],xin);%solucion de ecaciones y sistema del reactor
    erx1=abs(xop(1)-x(:,1));%error de la variable de concentracion
    erx2=abs(xop(2)-x(:,2));%error de la variable de temperatura
    erx3=abs(xop(3)-x(:,3));%error de la variable de volumen 
    er=[erx1 erx2 erx3];%error de medidas esperadas y reales 
    xx(:,:,i)=x(1:500,:);
    era(:,:,i)=er(1:500,:);
    for l=1:500
        U(:,l,i)=[u1+3*(rand*2-1),u2+3*(rand*2-1)];
    end
end
%%
figure
for i=1:n
    plot(t(1:500),xx(:,1,i))
    grid on;
    hold on;
end
figure
for i=1:n
    plot(t(1:500),xx(:,2,i))
    grid on;
    hold on;
end
figure
for i=1:n
    plot(t(1:500),xx(:,3,i))
    grid on;
    hold on;
end
figure
for i=1:n
    plot(t(1:500),era(:,1,i))
    grid on;
    hold on;
end
figure
for i=1:n
    plot(t(1:500),era(:,2,i))
    grid on;
    hold on;
end
figure
for i=1:n
    plot(t(1:500),era(:,3,i))
    grid on;
    hold on;
end
t=t(1:500);


%%
Unq=U(1,:,1);
Unqc=U(2,:,1);
SnCr=xx(:,1,1)';
SnTr=xx(:,2,1)';
SnVr=xx(:,3,1)';
for i=2:n
    Unq=[Unq U(1,:,i)];
    Unqc=[Unqc U(2,:,i)];
    SnCr=[SnCr xx(:,1,1)'];
    SnTr=[SnTr xx(:,2,1)'];
    SnVr=[SnVr xx(:,3,1)'];
end 
Un=[Unq;Unqc];
Sn=[SnCr;SnTr;SnVr];
Cop=SnCr;
Top=SnTr;
Vop=SnVr;
Tn=[SnCr;SnTr;SnVr];
save('entrada_flujo_reactivo','Unq');
save('entrada_flujo_servicio','Unqc');
save('Concentracion','SnCr');
save('Temperatura','SnTr');
save('volumen','SnVr');
%datos para el entrenamiento y uso de la red 