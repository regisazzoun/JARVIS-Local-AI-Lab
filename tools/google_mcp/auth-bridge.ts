/** JARVIS glue: reuse upstream OAuth config, scopes and encrypted storage. */
import { OAuthCredentialStorage } from 'workspace-auth';
import { SCOPES } from 'workspace-scopes';
import { loadConfig } from 'workspace-config';
import { AuthManager } from 'workspace-manager';
async function main() {
  const action=process.argv[2];
  if(action==='settings') { console.log(JSON.stringify({...loadConfig(),scopes:SCOPES}));return; }
  if(action==='status') {
    const c=await OAuthCredentialStorage.loadCredentials();
    console.log(JSON.stringify({configured:!!c?.refresh_token,has_access_token:!!c?.access_token,
      expires_at:c?.expiry_date??null,expired:!!c?.expiry_date&&c.expiry_date<Date.now(),
      granted_scopes:c?.scope?.split(' ')??[],remote_access_verified:false}));return;
  }
  if(action==='sheets-api') {
    let raw='';for await(const chunk of process.stdin){raw+=chunk;if(raw.length>65536)throw Error('Input too large');}
    const {name,arguments:a}=JSON.parse(raw);let request:any;
    if(name==='sheets.create'&&typeof a.title==='string')request={method:'POST',url:'https://sheets.googleapis.com/v4/spreadsheets',data:{properties:{title:a.title}}};
    else if(name==='sheets.writeRange'&&/^[a-zA-Z0-9_-]+$/.test(a.spreadsheetId)&&typeof a.range==='string'&&Array.isArray(a.values))request={method:'PUT',url:'https://sheets.googleapis.com/v4/spreadsheets/'+encodeURIComponent(a.spreadsheetId)+'/values/'+encodeURIComponent(a.range),params:{valueInputOption:'RAW'},data:{range:a.range,values:a.values}};
    else throw Error('Unsupported Sheets operation');
    // Both methods officially accept the already requested full Drive scope.
    const manager=new AuthManager(SCOPES);const client=await manager.getAuthenticatedClient();
    const response=await client.request(request);
    console.log(JSON.stringify({http_status:response.status,result:response.data,auth_source:'upstream AuthManager',application_result_independently_verified:false}));return;
  }
  if(action==='save') {
    let raw='';for await(const chunk of process.stdin){raw+=chunk;if(raw.length>65536)throw Error('Credential input too large');}
    const c=JSON.parse(raw);
    if(typeof c.access_token!=='string'||!c.access_token||typeof c.refresh_token!=='string'||!c.refresh_token||!Number.isFinite(Number(c.expiry_date)))throw Error('Incomplete OAuth credentials');
    await OAuthCredentialStorage.saveCredentials({access_token:c.access_token,refresh_token:c.refresh_token,expiry_date:Number(c.expiry_date),scope:c.scope,token_type:c.token_type||'Bearer'});
    console.log(JSON.stringify({saved:true,secrets_printed:false}));return;
  }
  throw Error('Use settings, status or save');
}
main().catch((error)=>{console.error(JSON.stringify({error:'Workspace operation failed; no credential values printed.',http_status:error?.response?.status??null}));process.exit(1);});
