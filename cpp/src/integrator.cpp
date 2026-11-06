#include "rocket/integrator.hpp"
namespace rocket {
State4 rk4_step(const Derivative& f,double t,const State4& y,double h) {
    const auto k1=f(t,y); State4 tmp{};
    for(int i=0;i<4;++i) tmp[i]=y[i]+h*k1[i]/2;
    const auto k2=f(t+h/2,tmp);
    for(int i=0;i<4;++i) tmp[i]=y[i]+h*k2[i]/2;
    const auto k3=f(t+h/2,tmp);
    for(int i=0;i<4;++i) tmp[i]=y[i]+h*k3[i];
    const auto k4=f(t+h,tmp); State4 out{};
    for(int i=0;i<4;++i) out[i]=y[i]+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6;
    return out;
}
}
