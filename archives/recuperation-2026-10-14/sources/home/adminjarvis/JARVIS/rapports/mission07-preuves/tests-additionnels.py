import batterie as b
b.login();b.RESULTS=[];b.RESULT_PATH=b.P/'web-comparaison-avant.json'
for cfg,opts,system in [('A',{'num_ctx':4096},False),('G',{'num_ctx':8192,'temperature':.1,'top_p':.9,'num_predict':2048},True)]:
 for rag in [False,True]:b.test(cfg,opts,system,'web',rag,essential=True)
b.RESULTS=[];b.RESULT_PATH=b.P/'h-direct.json';b.SYSTEM=(b.P/'instruction-renforcee.txt').read_text();b.test('H',{'num_ctx':8192,'temperature':.1,'top_p':.9,'num_predict':2048},True)
