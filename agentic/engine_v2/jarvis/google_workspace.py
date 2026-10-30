"""Google Workspace connector using official OAuth credentials and existing audit.

Private per-account tokens; no Google credentials are embedded in model context.
Gmail sending is deliberately not exposed by this mission (drafts only).
"""
import base64,fcntl,json,os,re
from pathlib import Path
from urllib.parse import quote
from email.message import EmailMessage

PRIVATE=Path('/home/adminjarvis/.config/jarvis/google')
SCOPES=['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/documents','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.compose']
ACTIONS=['status','drive_search','drive_get','drive_folder_create','drive_rename','docs_read','docs_create','docs_append','docs_replace','sheets_read','sheets_write','sheets_create','calendar_list','calendar_create','calendar_update','gmail_search','gmail_read','gmail_draft']

def profile_path(profile,root=PRIVATE):
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,32}',profile):raise ValueError('Invalid Google profile identifier')
    path=Path(root)/profile
    if path.is_symlink():raise ValueError('Profile must not be a symbolic link')
    return path

def save_credentials(path,credentials):
    path=Path(path)
    if path.is_symlink():raise ValueError('Credential file must not be a symbolic link')
    temporary=path.with_suffix('.tmp')
    fd=os.open(temporary,os.O_CREAT|os.O_WRONLY|os.O_TRUNC|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as output:output.write(credentials.to_json())
    os.replace(temporary,path);path.chmod(0o600)

def connection(profile,root=PRIVATE):
    folder=profile_path(profile,root);token=folder/'token.json'
    return {'profile':profile,'configured':token.is_file() and not token.is_symlink(),'state':'CONFIGURED_NOT_TESTED' if token.is_file() and not token.is_symlink() else 'AUTH_REQUIRED','remote_access_verified':False,'setup':'google-connect --profile '+profile+' --client-file /private/path/client_secret.json; owner guidance provided at end of mission'}

def session(profile,root=PRIVATE):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request,AuthorizedSession
    folder=profile_path(profile,root);token=folder/'token.json'
    if not token.is_file() or token.is_symlink():return None
    with (folder/'refresh.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        credentials=Credentials.from_authorized_user_file(token)
        if not credentials.valid:
            if not credentials.refresh_token:raise ValueError('AUTH_REQUIRED: no refresh token')
            credentials.refresh(Request());save_credentials(token,credentials)
        return AuthorizedSession(credentials)

def perform(profile,action,parameters,root=PRIVATE):
    if action not in ACTIONS:raise ValueError('Unknown Google operation')
    if action=='status':return connection(profile,root)
    client=session(profile,root)
    if client is None:return {'ok':False,**connection(profile,root),'operation_executed':False}
    p=parameters
    def ident(name):
        value=str(p[name])
        if not re.fullmatch(r'[a-zA-Z0-9_.@-]{1,256}',value):raise ValueError('Invalid resource identifier: '+name)
        return quote(value,safe='')
    method='GET';body=None;params={};endpoint=None
    if action=='drive_search':endpoint='https://www.googleapis.com/drive/v3/files';params={'q':p.get('query','trashed = false'),'pageSize':20,'fields':'files(id,name,mimeType,modifiedTime,webViewLink),nextPageToken','supportsAllDrives':'true','includeItemsFromAllDrives':'true'}
    elif action=='drive_get':endpoint='https://www.googleapis.com/drive/v3/files/'+ident('id');params={'fields':'id,name,mimeType,modifiedTime,webViewLink,size','supportsAllDrives':'true'}
    elif action=='drive_folder_create':endpoint='https://www.googleapis.com/drive/v3/files';method='POST';body={'name':p['name'],'mimeType':'application/vnd.google-apps.folder'};body.update({'parents':[p['parent']]} if p.get('parent') else {})
    elif action=='drive_rename':endpoint='https://www.googleapis.com/drive/v3/files/'+ident('id');method='PATCH';body={'name':p['name']}
    elif action=='docs_read':endpoint='https://docs.googleapis.com/v1/documents/'+ident('id');params={'includeTabsContent':'true'}
    elif action=='docs_create':endpoint='https://docs.googleapis.com/v1/documents';method='POST';body={'title':p['title']}
    elif action in ('docs_append','docs_replace'):
        endpoint='https://docs.googleapis.com/v1/documents/'+ident('id')+':batchUpdate';method='POST'
        update={'insertText':{'endOfSegmentLocation':{},'text':p['text']}} if action=='docs_append' else {'replaceAllText':{'containsText':{'text':p['old'],'matchCase':True},'replaceText':p['new']}}
        body={'requests':[update]}
    elif action=='sheets_create':endpoint='https://sheets.googleapis.com/v4/spreadsheets';method='POST';body={'properties':{'title':p['title']}}
    elif action in ('sheets_read','sheets_write'):
        endpoint='https://sheets.googleapis.com/v4/spreadsheets/'+ident('id')+'/values/'+quote(p['range'],safe='')
        if action=='sheets_write':method='PUT';params={'valueInputOption':'RAW'};body={'range':p['range'],'values':p['values']}
    elif action=='calendar_list':
        endpoint='https://www.googleapis.com/calendar/v3/calendars/'+quote(p.get('calendar','primary'),safe='')+'/events';params={'maxResults':25,'singleEvents':'true','orderBy':'startTime'}
        for field in ['timeMin','timeMax','q','pageToken']:
            if field in p:params[field]=p[field]
    elif action in ('calendar_create','calendar_update'):
        endpoint='https://www.googleapis.com/calendar/v3/calendars/'+quote(p.get('calendar','primary'),safe='')+'/events';method='POST' if action=='calendar_create' else 'PATCH'
        if action=='calendar_update':endpoint+='/'+ident('id')
        event=p['event'];allowed={'summary','description','start','end','location'}
        if not isinstance(event,dict) or set(event)-allowed:raise ValueError('Only summary/description/start/end/location allowed; attendees/notifications not exposed')
        body=event;params={'sendUpdates':'none'}
    elif action=='gmail_search':endpoint='https://gmail.googleapis.com/gmail/v1/users/me/messages';params={'q':p.get('query',''),'maxResults':10}
    elif action=='gmail_read':endpoint='https://gmail.googleapis.com/gmail/v1/users/me/messages/'+ident('id');params={'format':'full'}
    elif action=='gmail_draft':
        message=EmailMessage();message['Subject']=p['subject']
        if p.get('to'):message['To']=p['to']
        message.set_content(p['text']);endpoint='https://gmail.googleapis.com/gmail/v1/users/me/drafts';method='POST';body={'message':{'raw':base64.urlsafe_b64encode(message.as_bytes()).decode()}}
    if not endpoint:raise ValueError('Unsupported Google operation')
    response=client.request(method,endpoint,params=params,json=body,timeout=60)
    if response.status_code>=400:return {'ok':False,'profile':profile,'action':action,'http_status':response.status_code,'error':response.json().get('error',{}).get('message','Google API rejected request'),'operation_executed':'UNKNOWN' if method!='GET' else False}
    return {'ok':True,'profile':profile,'action':action,'http_status':response.status_code,'result':response.json(),'remote_access_verified':True,'application_result_independently_verified':False}

def register(registry):
    registry.specs['google_workspace']=('Google Workspace réel via compte OAuth local explicite. Commencer par status ; AUTH_REQUIRED signifie aucune opération exécutée. Drive recherche/lecture/dossiers/renommage, Docs lecture/création/ajout/remplacement, Sheets lecture/écriture/création, Calendar lecture/création/modification sans invités, Gmail recherche/lecture/brouillons. Aucun envoi Gmail. paramètres spécifiques dans parameters objet JSON : query,id,name,parent,title,text,old,new,range,values,calendar,timeMin,timeMax,event,subject,to selon action. Vérifier indépendamment toute écriture.',{'profile':{'type':'string','pattern':'^[a-zA-Z0-9_-]{1,32}$'},'action':{'type':'string','enum':ACTIONS},'parameters':{'type':'object','maxProperties':16}},['profile','action','parameters'],'host_authorized',lambda a:perform(a['profile'],a['action'],a['parameters']))
