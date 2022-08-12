# IBF-pipeline Floods

This pipeline is creating and uploading forecast data to the [IBF-system](https://github.com/rodekruis/IBF-system). This means that to set this pipeline up meaningfully, you must also set up an instance of the IBF-system.

The pipeline consists of a series of Python scripts, which - if activated - are supposed to run daily, to:
- extract relevant forecast input data
- transform them to create flood extents
- calculate affected population
- and uploads the results to an instance of IBF-system's API.

## Methods for running this pipeline

This pipeline is preconfigured to run in 3 different ways:

### 1. Locally
Getting its secrets from a local secrets.py file. 
Obviously, this method can be used also non-locally, e.g. by running it as cronjob on a Virtual Machine.

- Install Docker
- Clone this directory through `git clone https://github.com/<github-account>/IBF_FLOOD_PIPELINE.git`
- Change `pipeline/lib/flood_model/secrets.py.template` to `pipeline/lib/flood_model/secrets.py` and fill in the necessary secrets. Particularly fill in for 
  - <countryCodeISO3>_URL: `https://<ibf-system-url>/api/` (so with a slash at the end!) for every included country
  - <countryCodeISO3>_PASSWORD: the IBF-System admin users' password, set in the `.env` file on the environment where IBF-System is running for every included country
  - ADMIN_LOGIN: retrieve from someone who knows
  - GLOFAS_USER: retrieve from someone who knows
  - GLOFAS_PW: retrieve from someone who knows
  - GOOGLE_DATA_DRIVE_URL: retrieve from someone who knows
- Go to the root folder of the repository
- Build and run Docker image: `docker-compose up --build`
- (Optional) When you are finished, to remove any docker container(s) run: `docker-compose down`
- Check the IBF-system's dashboard to see if data is upload as expected


### 2. Github Actions
Getting its secrets from Github Secrets.

- Fork this repository to your own Github-account.
- Add Github secrets in Settings > Secrets of the forked repository: `https://github.com/<your-github-account>/IBF_FLOOD_PIPELINE/settings/secrets/actions`
  - Add the same 6 secrets as mentioned in the local scenario above.
- The Github action is already scheduled to run daily at a specific time. So wait until that time has passed to test that the pipeline has run correctly.
  - This time can be seen and changed if needed in the 'on: schedule:' part of [floodmodel.yml](.github/workflows/floodmodel.yml), where e.g. `cron:  '0 8 * * *'` means 8:00 AM UTC every day.
- Check the IBF-system's dashboard to see if data is upload as expected


### 3. Azure logic app
Getting its secrets from Azure Key Vault.

- The Azure logic app needs to be set up separately, based on this repository.
- The logic to get the secrets from the Azure Key Vault is already included in the code. 

## Versions
You can find the versions in the [tags](https://github.com/rodekruis/IBF_FLOOD_PIPELINE/tags) of the commits. See below table to find which version of the pipeline corresponds to which version of IBF-Portal.
| Flood Pipeline version  | IBF-Portal version | Changes |
| --- | --- | --- |
| v0.0.1 | 0.103.1 | initial number |
| v0.1.0 | 0.129.0 | alert_threshold upload to API | 
| v0.2.0 | 0.129.0 | rearranged and set up for github actions |
| v0.3.1 | 0.158.3 | add ethiopia multi admin |

