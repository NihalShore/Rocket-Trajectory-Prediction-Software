#include "rocket/atmosphere.hpp"
#include "rocket/vehicle.hpp"
#include <iostream>
int main() {
    const auto sea=rocket::standard_atmosphere(0.);
    const double dv=rocket::ideal_delta_v(100000.,20000.,3000.);
    std::cout<<"Sea-level density: "<<sea.density_kg_m3<<" kg/m^3\n";
    std::cout<<"Illustrative ideal delta-v: "<<dv<<" m/s\n";
    return 0;
}
