#include "rocket/vehicle.hpp"
#include <cmath>
#include <stdexcept>
namespace rocket {
void Vehicle::validate() const {
    if(stages.empty()) throw std::invalid_argument("vehicle needs at least one stage");
    if(payload_mass_kg<=0 || reference_area_m2<=0) throw std::invalid_argument("payload and area must be positive");
    for(const auto& s:stages)
        if(s.name.empty() || s.dry_mass_kg<=0 || s.propellant_mass_kg<=0 || s.thrust_n<=0 || s.burn_time_s<=0)
            throw std::invalid_argument("invalid stage data");
}
double Vehicle::initial_mass_kg() const {
    validate(); double mass=payload_mass_kg;
    for(const auto& s:stages) mass+=s.dry_mass_kg+s.propellant_mass_kg;
    return mass;
}
double ideal_delta_v(double initial,double final,double exhaust) {
    if(initial<=final || final<=0 || exhaust<=0) throw std::invalid_argument("invalid rocket equation inputs");
    return exhaust*std::log(initial/final);
}
}
