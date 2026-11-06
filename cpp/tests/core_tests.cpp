#include "rocket/atmosphere.hpp"
#include "rocket/integrator.hpp"
#include "rocket/vehicle.hpp"
#include <cassert>
#include <cmath>
int main() {
    const auto sea=rocket::standard_atmosphere(0.);
    assert(std::abs(sea.pressure_pa-101325.)<1e-6);
    assert(sea.density_kg_m3>1.0 && sea.density_kg_m3<1.3);
    assert(rocket::gravity_m_s2(100000.)<rocket::gravity_m_s2(0.));
    assert(std::abs(rocket::ideal_delta_v(1000.,500.,3000.)-3000.*std::log(2.))<1e-9);
    const auto decay=[](double,const rocket::State4& y){return rocket::State4{-y[0],0,0,0};};
    const auto stepped=rocket::rk4_step(decay,0.,{1.,0.,0.,0.},.1);
    assert(std::abs(stepped[0]-std::exp(-.1))<1e-6);
    return 0;
}
