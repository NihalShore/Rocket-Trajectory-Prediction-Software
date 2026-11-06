import pytest
from rocket_sim.config import StageConfig,VehicleConfig
from rocket_sim.mass_properties import AxialComponent,center_of_mass,stack_mass_properties
def test_center_of_mass_weighted_average():
    result=center_of_mass([AxialComponent("a",1,0),AxialComponent("b",3,2)])
    assert result.center_of_mass_from_base==pytest.approx(1.5)
def test_stack_mass_properties():
    stage=StageConfig("Stage",100,200,10000,20)
    vehicle=VehicleConfig([stage],50,1)
    result=stack_mass_properties(vehicle,[4],2)
    assert result.total_mass==350
    assert result.component_count==2
def test_negative_component_mass_rejected():
    with pytest.raises(ValueError): center_of_mass([AxialComponent("bad",-1,0)])
