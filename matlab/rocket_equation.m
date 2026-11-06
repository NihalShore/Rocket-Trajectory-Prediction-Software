function deltaV=rocket_equation(initialMass,finalMass,exhaustVelocity)
%ROCKET_EQUATION Ideal Tsiolkovsky velocity increment in m/s.
arguments
 initialMass (1,1) double {mustBePositive}
 finalMass (1,1) double {mustBePositive}
 exhaustVelocity (1,1) double {mustBePositive}
end
if initialMass<=finalMass, error('initialMass must exceed finalMass'); end
deltaV=exhaustVelocity*log(initialMass/finalMass);
end
