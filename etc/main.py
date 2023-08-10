# module imports
import math
import argparse


# functions
def calculate_number_of_photons_per_pixel(square_pixel_size: float,
                                          spectral_radiance: float,
                                          exposure_time: float) -> float:
  """
    Calculates the number of photons per pixel given the square pixel size,
    spectral radiance, and exposure time.

    Parameters:
        - square_pixel_size (float): The size of the pixel in square micrometers.
        - spectral_radiance (float): The spectral radiance of the thermal background
                                     in W/(m^2·sr·μm).
        - exposure_time (float): The exposure time in seconds.

    Returns:
        float: The calculated number of photons per pixel.
    """

  collecting_area = square_pixel_size  # Assuming the collecting area of the pixel
  # is the same as its size

  number_of_photons: float = spectral_radiance * collecting_area * exposure_time
  return number_of_photons


def calculate_square_pixel_size(focal_length: float,
                                angular_size: float) -> float:
  """
    Calculates the pixel size in square micrometers given the focal length
    and angular size.

    Parameters:
        - focal_length (float): The focal length of the lens in meters.
        - angular_size (float): The angular size of the object in radians.

    Returns:
        float: The calculated square pixel size.
    """
  square_pixel_size: float = ((focal_length * (math.tan(angular_size))) *
                              1e6)**2
  return square_pixel_size


def calculate_photon_noise(number_of_photons: float) -> float:
  """
    Calculates the photon noise of the sensor given the number of photons.

    Poisson noise, also known as shot noise or photon noise, is a type of 
    noise that arises from the quantized nature of light and the independence of photon 
    detections. It is a statistical noise that occurs when counting independent, random 
    events that occur at a constant rate over a long period of time. In the case of 
    measuring photons, Poisson noise arises from the statistics of photon-counting. 
    The formula to calculate Poisson noise is the square root of the expected number 
    of photons, which is equal to the standard deviation of the Poisson distribution. 
    Therefore, to calculate the inherent noise of a certain number of photons, you can 
    simply take the square root of that number. For example, if you expect to detect
    100 photons on average, you can expect to receive about 100 ± 10 photons during
    any particular run.

    Parameters:
    - number_of_photons (float): The number of photons in the sensor.

    Returns:
      float: The photon noise = square root of the expected number of photons.
  """
  photon_noise: float = math.sqrt(number_of_photons)
  return photon_noise


def calculate_min_photons_for_signal_to_noise_gt_5(
    background_noise: float, signal_to_noise_ratio: float) -> float:
  """
    Calculates the minimum number of photons required to achieve a signal-to-noise 
    ratio greater than 5.
    
    Parameters:
    - background_noise (float): The background noise of the sensor in photons.
    - signal_to_noise_ratio (float): The signal-to-noise ratio of the sensor.
    
    Returns:
      float: The minimum number of photons required to achieve a signal-to-noise
      ratio greater than 5.
      
  """
  min_photons: float = background_noise * signal_to_noise_ratio
  return min_photons


def main(args):
  # Define the necessary inputs for functions

  spectral_radiance: float = args.spectral_radiance if args.spectral_radiance else 1e-6  # Spectral radiance of the thermal background
  # in W/(m^2·sr·μm)
  # completely guessing spectral radiance at the moment
  # just to end up with a whole number of photons striking
  # a single pixel in 1 hour

  exposure_time: float = args.exposure_time if args.exposure_time else 3600  # 1 hour in seconds

  focal_length: float = args.focal_length if args.focal_length else 120  # Focal length of the Paranal UT4 lens in meters

  sky_arcseconds: float = args.sky_arcseconds if args.sky_arcseconds else 0.106  # 1 pixel corresponds to 0.106′′ on the sky

  angular_size: float = sky_arcseconds / (
      (3600 * 180) / math.pi)  # Angular size of the object in radians

  # Calculate the square micrometer size of each pixel
  square_pixel_size: float = calculate_square_pixel_size(
      focal_length, angular_size)

  # Calculate the number of photons in the thermal background
  number_of_background_photons: float = calculate_number_of_photons_per_pixel(
      square_pixel_size, spectral_radiance, exposure_time)

  # Calculate the noise of photons from thermal background
  photon_noise = calculate_photon_noise(number_of_background_photons)

  # Calculate the number of photons in the thermal background plus the photon noise
  total_number_of_background_photons: float = number_of_background_photons + photon_noise

  # Calculates the minimum number of photons required to achieve a signal-to-noise
  # ratio greater than 5
  min_photons_for_signal_to_noise_gt_5: float = calculate_min_photons_for_signal_to_noise_gt_5(
      total_number_of_background_photons, 5)

  # Print the result
  print(
      "\nNumber of photons from the thermal background \nthat strike a single pixel in 1 hour =",
      number_of_background_photons, "\n")
  print("\nThermal background Poisson noise = ", photon_noise, "\n")

  print(
      "\nMinimum number of photons required to achieve a \nsignal-to-noise ratio greater than 5 =",
      min_photons_for_signal_to_noise_gt_5, "\n")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "-sr",
      "--spectral_radiance",
      type=float,
      help="Spectral radiance of the thermal background in W/(m^2·sr·μm)")
  parser.add_argument("-et",
                      "--exposure_time",
                      type=float,
                      help="Exposure time in seconds")
  parser.add_argument("-fl",
                      "--focal_length",
                      type=float,
                      help="Focal length of the Paranal UT4 lens in meters")
  parser.add_argument("-sa",
                      "--sky_arcseconds",
                      type=float,
                      help="1 pixel corresponds to 0.106′′ on the sky")

  args = parser.parse_args()
  main(args)
