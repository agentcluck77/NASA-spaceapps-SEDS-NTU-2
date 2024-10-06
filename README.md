# NASA-spaceapps-SEDS-NTU-2
High level project summary

Project Objective
The objective of this project is to simulate how stars would appear from the perspective of an exoplanet by calculating changes in their apparent brightness (magnitude) and position (RA/Dec). The project leverages data from the Gaia mission and exoplanet databases, modeling the effect of an exoplanet's pole orientation and its distance on the observed stellar coordinates.


1. Data Acquisition
   - Gaia Star Data: Queried from Gaia DR3 to gather information about stars within a certain distance from Earth (less than 10 parsecs) using the parallax method. The dataset includes right ascension (RA), declination (Dec), parallax (for distance calculation), and apparent magnitude.
   - Exoplanet Data: Collected from the NASA Exoplanet Archive, focusing on characteristics like the exoplanet’s RA, Dec, distance from Earth, orbital inclination, and true obliquity. 

2. Coordinate Transformations
   - Spherical to Cartesian Conversion: RA, Dec, and distance were converted into Cartesian coordinates (x, y, z) to allow spatial transformations.
   - Rotation Based on Exoplanet Pole Orientation: The coordinates of each star were rotated based on the exoplanet’s inclination (λ) and obliquity (ε) using rotation matrices. This step simulated how the sky would appear from the exoplanet’s perspective.
   - Translation: Star positions were translated to account for the exoplanet’s distance from the Sun.

3. Apparent Brightness Adjustments
   - The apparent magnitude of stars changes when observed from a different point in space. This was calculated using the inverse square law, which modifies the original apparent magnitude based on the new distance of the star from the exoplanet.
   - The formula used was:

   - This provides the new apparent magnitude as seen from the exoplanet.

4. Challenges Encountered
   - Data Retrieval Limits: Gaia queries were initially capped at 2,000 entries due to API restrictions. Optimizations had to be made to refine the query and work around the timeout issues.
   - Zero Magnitude Issue: Initially, recalculating the new apparent magnitude led to values of zero, which was resolved by ensuring the correct treatment of logarithmic scaling in the magnitude calculations.
   - Coordinate Rotation: Handling nan values for planet inclination and obliquity involved incorporating randomness when data was unavailable.

5. Final Outputs
   - A CSV file containing the recalculated star coordinates (RA, Dec, Distance) and new apparent magnitudes from the exoplanet’s perspective.
   - A detailed simulation showing how the star field would change when viewed from an exoplanet 584 light-years away, illustrating changes in both position and brightness.


