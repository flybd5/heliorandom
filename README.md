# heliorandom
Python proof-of-concept code to seed random generator with solar image data from the helioviewer API using Solar Dynamics Observer's AIA instrument.

## API call available
There is now a REST call on the HelioViewer API that implements this idea I came up with in a very simple way. This also means it can be used in any language that can generate a REST call.

https://api.helioviewer.org/?action=getRandomSeed

This endpoint selects the closest image from one of the AIA datasources (8-16, selected randomly by "timestamp % 9 + 8") and then runs a sha256 hash on the image file. This image file hash is then concatenated with a timestamp measured in microseconds and then hashed again using sha256. The result is returned as a seed value.

The code for the API call is here: https://github.com/Helioviewer-Project/api/blob/beta/src/Module/WebClient.php#L991
