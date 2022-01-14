# IBF-pipeline Floods

This is a series of scripts (which are running daily) which extracts all input data (static + dynamic), transforms them to create flood extents and calculated affected population, and loads the output to locations where they can be served to the dashoard.

## Prerequisites

1. Install Docker

### Local installation

1. Clone this directory to `<your_local_directory>`/IBF_FLOOD_PIPELINE/
2. Change `pipeline/lib/flood_model/secrets.py.template` to `pipeline/lib/flood_model/secrets.py` and fill in the necessary secrets.

### Build and run

Build and run Docker image (from the IBF-pipeline root folder).

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
