import batterie as b,time
for i in range(60):
 try:b.req(b.WEB+'/health');break
 except:time.sleep(1)
b.login();b.RESULTS=[];b.RESULT_PATH=b.P/'web-rag-corrige.json';b.SYSTEM=(b.P/'instruction-renforcee.txt').read_text()
for label,ctx,rag,essential in [('H8-clean',8192,False,False),('H8-rag',8192,True,True),('H16-rag',16384,True,True)]:
 b.test(label,{'num_ctx':ctx,'temperature':.1,'top_p':.9,'num_predict':2048},True,'web',rag,essential)
b.RESULTS=[];b.RESULT_PATH=b.P/'a0-reference.json';b.SYSTEM=(b.P/'instruction-qualite.txt').read_text();b.test('A0',{'num_ctx':4096,'seed':-1},False)
