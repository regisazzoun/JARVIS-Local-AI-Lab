"""One-time owner Google OAuth setup. Run via an SSH local forward on port8769."""
import argparse,os,sys
from pathlib import Path
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.google_workspace import SCOPES,profile_path,save_credentials,PRIVATE

def main():
    from google_auth_oauthlib.flow import InstalledAppFlow
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',required=True);parser.add_argument('--client-file',required=True);args=parser.parse_args()
    PRIVATE.mkdir(parents=True,exist_ok=True);PRIVATE.chmod(0o700)
    folder=profile_path(args.profile);folder.mkdir(mode=0o700,exist_ok=True);folder.chmod(0o700)
    flow=InstalledAppFlow.from_client_secrets_file(args.client_file,scopes=SCOPES)
    credentials=flow.run_local_server(host='127.0.0.1',port=8769,open_browser=False,access_type='offline',prompt='consent',timeout_seconds=600,authorization_prompt_message='Ouvre cette URL dans ton navigateur : {url}',success_message='Compte Google raccordé. Tu peux fermer cet onglet et revenir dans Open WebUI.')
    save_credentials(folder/'token.json',credentials)
    print('Profil raccordé :',args.profile,'; jetons conservés localement, aucun secret affiché. Tester google_workspace status puis une recherche réelle.')
if __name__=='__main__':main()
