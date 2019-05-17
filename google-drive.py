# -*- coding: utf-8 -*-
# Python
import os
import pickle
import os.path
import httplib2
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import googleapiclient.http
from google_auth_oauthlib.flow import Flow
from photodrive.settings import GOOGLE_DRIVE
from oauth2client.client import AccessTokenCredentials


SCOPES = ['https://www.googleapis.com/auth/drive.file']

def google_drive():
    creds = None
    if os.path.exists('token'):
        with open('token', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join( settings.BASE_DIR, '<CredentialsJsonFile>' ), SCOPES)
        except Exception as e:
            print(str( e))

        try:
            flow.redirect_uri = GOOGLE_DRIVE['redirect_uri']
            crd = flow.fetch_token(code='<givencode>')
        except Exception as e:
            print(str( e))
        google_credentials = AccessTokenCredentials(crd['access_token'], 'my-user-agent/1.0')
        google_http = httplib2.Http()
        google_http = google_credentials.authorize(google_http)

    service = build('drive', 'v3', http=google_http)
    
    # calling all files in google drive
    try:
        results = service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and trashed = false and name= '<foldername in google drive>'",
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
    except Exception as e:
        print(str( e))
    
    if not items:
        # creating folder in a google drive
        file_metadata = {
            'name': '<Folder Name>',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = file.get('id')
    else:
        for item in items:
            folder_id = item['id']
    
    # creating subfolder in a folder
    projectfolder = {
      'name': '<SubFolder Name>',
      'mimeType': "application/vnd.google-apps.folder"
    }
    rawfolder = {
      'name': 'raw',
      'mimeType': "application/vnd.google-apps.folder"
    }

    if folder_id:
        projectfolder['parents'] = [folder_id]
        try:
            project_folder = service.files().create(body = projectfolder).execute()
        except Exception as e:
            print(str( e))
        try:
            rawfolder['parents'] = [project_folder['id']]
        except Exception as e:
            print(str( e))
        raw_folder = service.files().create(body = rawfolder).execute()

        try:
            batch = service.new_batch_http_request(callback=callback)
        except Exception as e:
            print(str( e))
        domain_permission = {
            'type': 'anyone',
            'role': 'writer',
            'kind': 'drive#permission'
        }
        try:
            batch.add(service.permissions().create(
                fileId=project_folder['id'],
                body=domain_permission,
                fields='id',
            ))
        except Exception as e:
            print(str( e))
        try:
            batch.execute()
        except Exception as e:
            print(str( e))
        
    return data


def callback(request_id, response, exception):
    if exception:
        print( "Error happen: %s" % exception)
    else:
        print( "Permission Id: %s" % response.get('id'))
