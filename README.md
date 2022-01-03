# IBF-pipeline Floods

This is a series of scripts (which are running daily) which extracts all input data (static + dynamic), transforms them to create flood extents and calculated affected population, and loads the output to locations where they can be served to the dashoard.

## Prerequisites

1. Install Docker
2. Upload data-floods.zip file to a google drive, then update GOOGLE_DRIVE_DATA_URL in pipeline/lib/flood_model/settings.py 



### Installation

1. Clone this directory to `<your_local_directory>`/IBF_FLOOD_PIPELINE/
2. Change `secrets_template` to `secrets` and fill in the necessary passwords.

### Set up Data pipeline

1. Build Docker image (from the IBF-pipeline root folder) and run container with volume. ${PWD} should take automatically your Present Working Directory as the local folder to attach the volume though; if this fails, you can always replace it by the literal path (e.g. "C:/IBF-system/services/IBF-pipeline:/home/ibf" instead of "${PWD}:/home/ibf")

To build and run the image, ensure you are in the top-level directory and execute:

```
docker-compose up --build
```
When you are finished,to remove any docker container(s) run
```
docker-compose down
```

### Versions
You can find the versions in the [tags](https://github.com/rodekruis/IBF_FLOOD_PIPELINE/tags) of the commits. See below table to find which version of the pipeline corresponds to which version of IBF-Portal.
| Flood Pipeline version  | IBF-Portal version |
| --- | --- |
| 0.0.1  | 0.103.1  |
