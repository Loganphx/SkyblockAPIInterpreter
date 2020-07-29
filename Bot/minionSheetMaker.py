from __future__ import print_function

import gspread
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
scope = [
 'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('secret_info.json', scope)
client = gspread.authorize(creds)
template_id = '1xyKEkARObLpVDD-lxphmHHBfO0Hbu6i6Rb0_1EOe6GU'
template_sheet = client.open('Minion Sheet Template')
driveV3 = build('drive', 'v3', credentials=creds)
file_id = ''
title = ''

def copyMinionSheet(username, profile):
    title = username + '[' + profile + "]'s" + 'Minion Sheet'
    copy_title = 'Totally Not a copy lol'
    copied_file = {'title': copy_title}
    request = driveV3.files().copy(fileId=template_id, body=copied_file)
    request_json = request.execute()
    file_id = request_json['id']
    return file_id


def shareMinionSheetWithMe(file_id):

    def callback(request_id, response, exception):
        if exception:
            print(exception)
        else:
            print('Permission Id: %s' % response.get('id'))

    batch = driveV3.new_batch_http_request(callback=callback)
    user_permission = {'type':'user',
     'role':'writer',
     'emailAddress':'phxdiscordbot@gmail.com'}
    batch.add(driveV3.permissions().create(fileId=file_id,
      body=user_permission,
      fields='id'))
    domain_permission = {'type':'domain',
     'role':'reader',
     'domain':'example.com'}
    batch.add(driveV3.permissions().create(fileId=file_id,
      body=domain_permission,
      fields='id'))
    batch.execute()


def renameMinionSheet(username, profile, file_id):
    title = username + '[' + profile + "]'s" + 'Minion Sheet'
    driveV2 = build('drive', 'v2', credentials=creds)
    body = {'title': title}
    patch_request = driveV2.files().patch(fileId=file_id, body=body, fields='title')
    patch_json = patch_request.execute()
    new_sheet = client.open(title)
    api_importer_sheet = new_sheet.worksheet('API Importer')
    api_importer_sheet.update_cell(6, 2, username)
    api_importer_sheet.update_cell(6, 4, profile)
    return title


def makeMinionSheetViewable(title):
    file = client.open(title)
    file.list_permissions()
    file.share(value=None, perm_type='anyone', role='reader', with_link=False)


def returnMinionSheetURL(file_id):
    URL = 'https://docs.google.com/spreadsheets/d/' + file_id + '/edit#gid=991281182'
    return URL


def createMinionSheetFileAndReturnURL(username, profile):
    file_id = copyMinionSheet(username, profile)
    shareMinionSheetWithMe(file_id)
    title = renameMinionSheet(username, profile, file_id)
    makeMinionSheetViewable(title)
    return returnMinionSheetURL(file_id)