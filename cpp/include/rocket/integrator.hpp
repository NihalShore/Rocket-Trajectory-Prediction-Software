#pragma once
#include <array>
#include <functional>
namespace rocket {
using State4=std::array<double,4>;
using Derivative=std::function<State4(double,const State4&)>;
State4 rk4_step(const Derivative& derivative,double time_s,const State4& state,double step_s);
}
