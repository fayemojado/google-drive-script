# google-drive-script
Python3 script to create google drive folder in your account.

Things to consider
==================
* Generate a `token.pickle` and `credentials.json` by enabling the google drive activity api you can just refer 
  here https://developers.google.com/drive/activity/v1/quickstart/python.
  
* Embed a JS script example below :
   
   `"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=<client_id>.apps.googleusercontent.com&redirect_uri=<http://url.com>&scope=<https://www.googleapis.com/auth/drive&state=<random_code>&access_type=offline", 'Google Drive Access', 'height=600,width=500'`

* Once it's done, simply run the python script.
