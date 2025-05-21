within FMITest.Examples;

model ExampleQuarterCar
  extends Modelica.Icons.Example;
  QuarterCar quarterCar(k_us = 191000, k_s = 16200, c_us = 2500, c_s = 1000, m_us = 15, m_s = 290)  annotation(
    Placement(transformation(origin = {2, -2}, extent = {{-24, -24}, {24, 24}})));
  Modelica.Blocks.Sources.Step step(startTime = 1, height = 1)  annotation(
    Placement(transformation(origin = {-78, -2}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(quarterCar.roadInput, step.y) annotation(
    Line(points = {{-26, -2}, {-67, -2}}, color = {0, 0, 127}));
end ExampleQuarterCar;
