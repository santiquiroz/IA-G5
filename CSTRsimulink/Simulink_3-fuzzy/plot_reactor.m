load data.mat

time  = cstr(1,:);
temp_sp = cstr(2,:);
temp_jacket = cstr(3,:);
inlet_flow  = cstr(4,:);
feed_conc = cstr(5,:);
feed_temp = cstr(6,:);
temp = cstr(7,:);
conc = cstr(8,:);

figure(1)
hold off

subplot(3,1,1)
hold off
plot(time,temp_jacket,'g:','LineWidth',2)
hold on
legend('Jacket Temperature');
axis([min(time) max(time) 250 400]);
ylabel('Temp (degF)')

subplot(3,1,2)
hold off
plot(time,feed_conc,'k-','LineWidth',2)
hold on
plot(time,conc,'r-')
legend('Feed Conc','Outlet Conc')
axis([min(time) max(time) 0 1]);
ylabel('Temp (degF)')

subplot(3,1,3)
hold off
plot(time,temp_sp,'m--','LineWidth',2)
hold on
plot(time,temp,'b:','LineWidth',2)
legend('Temp SP','Temp Rx')
axis([min(time) max(time) ...
    min(min(temp),min(temp_sp))-10 ...
    max(max(temp),max(temp_sp))+10]);
ylabel('Conc (mol/m^3)')
xlabel('Time (min)')


% save data to text file
data = cstr';
% make first row equal initial input conditions
data(1,2)=310;
data(1,3)=280;

save -ascii 'data.txt' data