from pathlib import Path

import pytest

from app.state import AppState


@pytest.fixture
def fmu_path():
    return Path(__file__).parent.resolve() / "resources/BouncingBall.fmu"


def test_load_fmu(fmu_path):
    state = AppState()
    info = state.load_fmu(fmu_path, return_info=True)

    expect = """
Model Info

  FMI Version        2.0
  FMI Type           Model Exchange, Co-Simulation
  Model Name         FMITest.BouncingBall
  Description        The 'classic' bouncing ball model
  Platforms          c-code, win64
  Continuous States  2
  Event Indicators   1
  Variables          8
  Generation Tool    OpenModelica Compiler OpenModelica v1.23.1 (64-bit)
  Generation Date    2025-05-20T20:01:34Z

Default Experiment

  Stop Time          4.0
  Tolerance          1e-06
  Step Size          0.008

Variables (input, output, parameter)

  Name               Causality              Start Value  Unit     Description
  h                  output                              m        Height
  v                  output                              m/s      Velocity
  e                  parameter                      0.8           Coefficient of restitution
  h0                 parameter                      1.0  m        Initial height"""

    assert expect == info
