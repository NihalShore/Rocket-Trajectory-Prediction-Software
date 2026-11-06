function state = standard_atmosphere(altitude_m)
%STANDARD_ATMOSPHERE Layered lower-atmosphere approximation in SI units.
arguments
 altitude_m (1,1) double {mustBeNonnegative}
end
g0=9.80665; R=287.05287; T=288.15; p=101325;
tops=[11000 20000 32000 47000 51000 71000 86000];
lapse=[-.0065 0 .001 .0028 0 -.0028 -.002]; base=0;
for k=1:numel(tops)
 if altitude_m<=base, break; end
 dz=min(altitude_m,tops(k))-base;
 if abs(lapse(k))<1e-12
  p=p*exp(-g0*dz/(R*T));
 else
  nextT=T+lapse(k)*dz; p=p*(nextT/T)^(-g0/(R*lapse(k))); T=nextT;
 end
 base=tops(k);
 if altitude_m<=base, break; end
end
if altitude_m>base, p=p*exp(-g0*(altitude_m-base)/(R*T)); end
rho=p/(R*T); a=sqrt(1.4*R*T);
S=110.4; mu0=1.716e-5; T0=273.15;
mu=mu0*(T/T0)^1.5*(T0+S)/(T+S);
state=struct('temperature',T,'pressure',p,'density',rho,'speed_of_sound',a,'dynamic_viscosity',mu);
end
