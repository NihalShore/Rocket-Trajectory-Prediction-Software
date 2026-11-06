#pragma once
#include <string>
#include <vector>
namespace rocket {
struct Stage { std::string name; double dry_mass_kg; double propellant_mass_kg; double thrust_n; double burn_time_s; };
struct Vehicle { std::vector<Stage> stages; double payload_mass_kg; double reference_area_m2; void validate() const; double initial_mass_kg() const; };
double ideal_delta_v(double initial_mass_kg,double final_mass_kg,double exhaust_velocity_m_s);
}
