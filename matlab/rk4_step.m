function nextState=rk4_step(derivative,time,state,step)
%RK4_STEP Classical fourth-order Runge-Kutta update.
arguments
 derivative (1,1) function_handle
 time (1,1) double
 state (:,1) double
 step (1,1) double {mustBePositive}
end
k1=derivative(time,state);
k2=derivative(time+step/2,state+step*k1/2);
k3=derivative(time+step/2,state+step*k2/2);
k4=derivative(time+step,state+step*k3);
nextState=state+step*(k1+2*k2+2*k3+k4)/6;
end
