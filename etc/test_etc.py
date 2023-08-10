import pytest
from main import *


def test_calculate_number_of_photons_per_pixel():
  assert isinstance(calculate_number_of_photons_per_pixel(1.0, 1.0, 1.0),
                    float)


def test_calculate_square_pixel_size():
  assert isinstance(calculate_square_pixel_size(1.0, 1.0), float)


def test_calculate_photon_noise():
  assert isinstance(calculate_photon_noise(1.0), float)


def test_calculate_min_photons_for_signal_to_noise_gt_5():
  assert isinstance(calculate_min_photons_for_signal_to_noise_gt_5(1.0, 1.0),
                    float)


if __name__ == "__main__":
  pytest.main()
