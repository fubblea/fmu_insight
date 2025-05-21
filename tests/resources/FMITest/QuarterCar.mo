within FMITest;

model QuarterCar
  import Modelica.Units.SI;
  
  // Parameters
  parameter SI.TranslationalSpringConstant k_us = 191000 "Tire Stiffness";
  parameter SI.TranslationalSpringConstant k_s = 16200 "Suspension Stiffness";
  parameter SI.TranslationalDampingConstant c_us = 2500 "Tire Damping";
  parameter SI.TranslationalDampingConstant c_s = 1000 "Suspension Damping";
  parameter SI.Mass m_us = 15 "Unsprung Mass";
  parameter SI.Mass m_s = 290 "Sprung Mass";
  
  // Input
  Modelica.Blocks.Interfaces.RealInput roadInput(unit="m") "Road Input" annotation(
    Placement(transformation(origin = {-80, -60}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}})));
  
  // Components
  Modelica.Mechanics.Translational.Components.SpringDamper tire(c = k_us, d = c_us)  annotation(
    Placement(transformation(origin = {0, -42}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Mechanics.Translational.Components.Mass unsprungMass(m = m_us)  annotation(
    Placement(transformation(origin = {0, -14}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Mechanics.Translational.Components.SpringDamper suspension(c = k_s, d = c_s)  annotation(
    Placement(transformation(origin = {0, 14}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Mechanics.Translational.Components.Mass sprungMass(m = m_s)  annotation(
    Placement(transformation(origin = {0, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  
  // Outputs & Sensors
  Modelica.Mechanics.Translational.Sensors.PositionSensor sprungMassDisp annotation(
    Placement(transformation(origin = {22, 68}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput sprungMassZ(unit="m") "Sprung Mass Displacement" annotation(
    Placement(transformation(origin = {76, 68}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {110, 60}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Mechanics.Translational.Sensors.PositionSensor unsprungMassDisp annotation(
    Placement(transformation(origin = {30, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput unsprungMassZ(unit="m") "Unsprung Mass Displacement" annotation(
    Placement(transformation(origin = {76, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {110, -42}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Mechanics.Translational.Sources.Position road annotation(
    Placement(transformation(origin = {-34, -60}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(tire.flange_b, unsprungMass.flange_a) annotation(
    Line(points = {{0, -32}, {0, -24}}, color = {0, 127, 0}));
  connect(unsprungMass.flange_b, suspension.flange_a) annotation(
    Line(points = {{0, -4}, {0, 4}}, color = {0, 127, 0}));
  connect(suspension.flange_b, sprungMass.flange_a) annotation(
    Line(points = {{0, 24}, {0, 34}}, color = {0, 127, 0}));
  connect(sprungMassDisp.flange, sprungMass.flange_b) annotation(
    Line(points = {{12, 68}, {0, 68}, {0, 54}}, color = {0, 127, 0}));
  connect(sprungMassDisp.s, sprungMassZ) annotation(
    Line(points = {{34, 68}, {76, 68}}, color = {0, 0, 127}));
  connect(unsprungMass.flange_b, unsprungMassDisp.flange) annotation(
    Line(points = {{0, -4}, {20, -4}, {20, 0}}, color = {0, 127, 0}));
  connect(unsprungMassZ, unsprungMassDisp.s) annotation(
    Line(points = {{76, 0}, {42, 0}}, color = {0, 0, 127}));
  connect(road.flange, tire.flange_a) annotation(
    Line(points = {{-24, -60}, {0, -60}, {0, -52}}, color = {0, 127, 0}));
  connect(road.s_ref, roadInput) annotation(
    Line(points = {{-46, -60}, {-80, -60}}, color = {0, 0, 127}));
end QuarterCar;
