# IBF Flood Forecast Pipeline

This pipeline generates and uploads forecast data to the [IBF-system](https://github.com/rodekruis/IBF-system). To deploy this pipeline effectively, it's essential to also have an instance of the IBF-system.

The pipeline employs several Python scripts designed to execute daily when triggered. Their tasks are to:
- Extract the necessary forecast input data.
- Process this data to derive flood extents.
- Evaluate the affected population.
- Upload the computed results to the IBF-system via its API.

## How to Execute the Pipeline

The pipeline can be initiated in three distinct manners:

### 1. **Local Execution**
Here, the pipeline fetches its secrets from a local `secrets.env` file. Though termed "local," this method is adaptable for non-local uses, like setting it as a cron job on a Virtual Machine.

**Steps:**
- Install Docker.
- Clone the repository: `git clone https://github.com/<github-account>/IBF_FLOOD_PIPELINE.git`.
- Rename `secrets.env.template` to `secrets.env` and populate the secrets fields. Notably:
  - `IBF_URL`: `https://<ibf-system-url>/api/` (ensure it ends with a slash!)
  - `IBF_PASSWORD`: Use the IBF-System admin user password from the `.env` file where IBF-System is deployed.
  - Others: Obtain details like `ADMIN_LOGIN` and `COUNTRY_CODES` (e.g., ZMB for Zambia) from a knowledgeable source.
- Rename `pipeline/lib/flood_model/secrets.py.template` to `pipeline/lib/flood_model/secrets.py` and populate required fields (e.g., `GLOFAS_USER`, `GLOFAS_PW`, and `GLOFAS_FTP`).
- Navigate to the repository's root folder.
- Build and start the Docker image: `docker-compose up --build`.
- Optionally, to clean up Docker containers: `docker-compose down`.
- Verify the data on the IBF-system dashboard.

### 2. **GitHub Actions**
For this method, the pipeline derives its secrets from GitHub Secrets.

**Steps:**
- Fork this repository to your GitHub account.
- Define GitHub secrets under: `https://github.com/<your-github-account>/IBF_FLOOD_PIPELINE/settings/secrets/actions`.
  - Incorporate the four secrets highlighted in the local setup.
- The GitHub Action is pre-set to initiate daily. Check its status post-scheduled run time.
  - Adjust the scheduled time in [floodmodel.yml](.github/workflows/floodmodel.yml) if needed. For instance, `cron:  '0 8 * * *'` translates to 8:00 AM UTC daily.
- Verify the data on the IBF-system dashboard.

### 3. **Azure Logic App**
This method fetches its secrets from Azure Key Vault.

**Note:** The Azure Logic App requires an independent setup, inspired by this repository. The logic to pull secrets from the Azure Key Vault is integrated into the existing code.



## Versions
You can find the versions in the [tags](https://github.com/rodekruis/IBF_FLOOD_PIPELINE/tags) of the commits. See below table to find which version of the pipeline corresponds to which version of IBF-Portal.
| Flood Pipeline version  | IBF-Portal version | Changes |
| --- | --- | --- |
| v0.0.1 | 0.103.1 | initial number |
| v0.1.0 | 0.129.0 | alert_threshold upload to API | 
| v0.2.0 | 0.129.0 | rearranged and set up for github actions |
| v0.3.1 | 0.158.3 | add ethiopia multi admin |

