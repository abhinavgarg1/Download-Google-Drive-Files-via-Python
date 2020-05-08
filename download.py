File_id =                          #File ID mentioned on the URL of the google Drive File
Credential_file =                  #JSON file pulled from Google API console
file_path =                        #Local path to which file is to be downloaded

#Authorization from google drive
def get_credentials():
    """Gets google api credentials, or generates new credentials
    if they don't exist or are invalid."""
    scope = 'https://www.googleapis.com/auth/drive'

    flow = oauth2client.client.flow_from_clientsecrets(
            mypath + 'client_secret_other.json', scope,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    storage = oauth2client.file.Storage(mypath + 'credentials1.dat')
    credentials = storage.get()

    if not credentials or credentials.invalid:
        auth_uri = flow.step1_get_authorize_url()
        webbrowser.open(auth_uri)

        auth_code = input("Enter the auth code: ")
        print(auth_code)
        credentials = flow.step2_exchange(auth_code)

        storage.put(credentials)

    return credentials

def get_service():
    """Returns an authorised blogger api service."""
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)
    DRIVE = discovery.build('drive', 'v3', http=http, cache_discovery=False, cache=None)

    return DRIVE

DRIVE = get_service()

#Downloading Function
def download_file(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except (errors.HttpError, error):
      print ('An error occurred: %s' % error)
      return
    if download_progress:
      print ('Download Progress: %d%%' % int(download_progress.progress() * 100))
    if done:
      print ('Download Complete')
      return        

download_file(DRIVE, ids, file_path)
