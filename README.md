# heliorandom
Python proof-of-concept code to seed pseudorandom number generators with solar image data from the helioviewer API using Solar Dynamics Observer's Atmospheric Imaging Array instrument. The concept is based on the idea that high-cadence, high-resolution images of the surface of the Sun are about as excellent an example of a high-entropy source of seeds as you will be able find, at least on our solar system.

## API call available
There is now a REST call on the HelioViewer API that implements this idea I came up with in a very simple way. This also means it can be used in any language that can generate a REST call.

https://api.helioviewer.org/?action=getRandomSeed

This endpoint selects the closest image from one of the AIA datasources (8-16, selected randomly by "timestamp % 9 + 8") and then runs a sha256 hash on the image file. This image file hash is then concatenated with a timestamp measured in microseconds and then hashed again using sha256. The result is returned as a seed value.

The code for the API call is here: https://github.com/Helioviewer-Project/api/blob/beta/src/Module/WebClient.php#L991

The program heliorandom_sha uses this API call to generate keys and saves them to a text file. Heliorandom_bin does the same thing but saves them in binary format to a file. Look in the source to modify the filename and the number of keys requested. Do NOT change the 20ms delay between calls or the API will throw you out after a short while. Be respectful of Helioviewer resources.
