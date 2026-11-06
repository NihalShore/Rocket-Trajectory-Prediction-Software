#include "rocket/atmosphere.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>
namespace rocket {
namespace { constexpr double R=287.05287,g0=9.80665,gamma=1.4,mu0=1.716e-5,T0=273.15,S=110.4; }
AtmosphereState standard_atmosphere(double h) {
    if(h<0) throw std::invalid_argument("altitude must be nonnegative");
    struct Layer { double top,lapse; };
    constexpr Layer layers[]={{11000,-.0065},{20000,0},{32000,.001},{47000,.0028},{51000,0},{71000,-.0028},{86000,-.002}};
    double t=288.15,p=101325.,base=0.;
    for(const auto& layer:layers) {
        if(h<=base) break;
        const double dz=std::min(h,layer.top)-base;
        if(dz<=0) continue;
        if(std::abs(layer.lapse)<1e-12) p*=std::exp(-g0*dz/(R*t));
        else { const double next=t+layer.lapse*dz; p*=std::pow(next/t,-g0/(R*layer.lapse)); t=next; }
        base=layer.top;
        if(h<=base) break;
    }
    if(h>base) p*=std::exp(-g0*(h-base)/(R*t));
    const double rho=p/(R*t),a=std::sqrt(gamma*R*t);
    const double mu=mu0*std::pow(t/T0,1.5)*(T0+S)/(t+S);
    return {t,p,rho,a,mu};
}
double gravity_m_s2(double h) {
    constexpr double earth_mu=3.986004418e14,radius=6371000.;
    if(h<=-radius) throw std::invalid_argument("altitude outside gravity model");
    return earth_mu/std::pow(radius+h,2);
}
}
