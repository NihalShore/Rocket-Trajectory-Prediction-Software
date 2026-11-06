function loads=drag_load(altitude,speed,area,baseCd)
%DRAG_LOAD Compute generic drag, Mach, and dynamic pressure.
arguments
 altitude (1,1) double {mustBeNonnegative}
 speed (1,1) double
 area (1,1) double {mustBePositive}
 baseCd (1,1) double {mustBeNonnegative}=0.35
end
atm=standard_atmosphere(altitude); mach=abs(speed)/atm.speed_of_sound;
q=0.5*atm.density*speed^2; rise=0.28*exp(-((mach-1)/0.22)^2);
relief=0.06*(1-exp(-max(0,mach-1)/2)); cd=max(0,baseCd+rise-relief);
loads=struct('mach',mach,'dynamic_pressure',q,'coefficient',cd,'drag',q*area*cd);
end
