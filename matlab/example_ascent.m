%EXAMPLE_ASCENT Illustrative vertical point-mass ascent.
clear; clc;
g0=9.80665; dryMass=12000; propellantMass=65000; payloadMass=900;
thrust=1.5e6; burnTime=100; area=5.2; baseCd=.4;
flow=propellantMass/burnTime; dt=.1; time=0:dt:burnTime;
state=[0;0;dryMass+propellantMass+payloadMass]; history=zeros(3,numel(time));
for k=1:numel(time)
 history(:,k)=state;
 if k==numel(time), break; end
 rhs=@(~,y)[y(2);thrust/y(3)-g0;-flow];
 state=rk4_step(rhs,time(k),state,dt);
 atm=standard_atmosphere(max(0,state(1)));
 loads=drag_load(max(0,state(1)),state(2),area,baseCd);
 state(2)=state(2)-loads.drag/max(state(3),1)*dt;
end
figure; plot(time,history(1,:)/1000,'LineWidth',1.5);
xlabel('Time (s)'); ylabel('Altitude (km)'); grid on;
title('Illustrative vertical ascent');
