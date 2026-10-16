#!/usr/bin/env python3
"""Create deployment-only secret; never touches Mac accounts or SSH keys."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,datetime,json,os,pathlib,secrets,subprocess
p=argparse.ArgumentParser();p.add_argument('directory',type=pathlib.Path);a=p.parse_args()
os.umask(0o077);a.directory.mkdir(mode=0o700)
password=secrets.token_urlsafe(32)
crypted=subprocess.run(['openssl','passwd','-6','-stdin'],input=(password+'\n').encode(),capture_output=True,check=True).stdout
(a.directory/'password').write_text(password+'\n')
(a.directory/'password.sha512').write_bytes(crypted)
(a.directory/'lifecycle.json').write_text(json.dumps(dict(created=datetime.datetime.now(datetime.timezone.utc).isoformat(),review_after_hours=24,delete_plaintext_after='independent key SSH AND bootstrap revocation confirmed',rotate_on='new installation or compromise',resume='same installation only; never recreate password blindly'),indent=2)+'\n')
print('Private deployment secret created; no account modified; no secret printed.')
