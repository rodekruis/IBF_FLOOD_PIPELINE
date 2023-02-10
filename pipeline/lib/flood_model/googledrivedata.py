import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def downloaddatalack(countryCode): 
    if countryCode:
        countryCode=countryCode.lower()
        url=f'https://510ibfsystem.blob.core.windows.net/ibfdatapipelines/flood/data_{countryCode}.zip'
        response = requests.get(url)
        if response.status_code == 200:
            # If the request is successful, the response content can be saved to a file
            with open(f'data_{countryCode}.zip', "wb") as f:
                f.write(response.content)
        else:
            # If the request fails, print an error message
            print(f"Failed to download data from {url} with status code {response.status_code}")
        
    else:
        url='https://510ibfsystem.blob.core.windows.net/ibfdatapipelines/flood/data.zip'

        response = requests.get(url)
        if response.status_code == 200:
            # If the request is successful, the response content can be saved to a file
            with open(f'data.zip', "wb") as f:
                f.write(response.content)
        else:
            # If the request fails, print an error message
            print(f"Failed to download data from {url} with status code {response.status_code}")