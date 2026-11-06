#pragma once
namespace rocket {
struct AtmosphereState { double temperature_k; double pressure_pa; double density_kg_m3; double speed_of_sound_m_s; double viscosity_pa_s; };
AtmosphereState standard_atmosphere(double altitude_m);
double gravity_m_s2(double altitude_m);
}
