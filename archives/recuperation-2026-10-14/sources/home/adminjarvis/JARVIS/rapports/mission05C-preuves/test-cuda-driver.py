import ctypes as C,json,time
cuda=C.CDLL('libcuda.so.1'); results={'time':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'steps':[]}
def call(name,args,types):
 f=getattr(cuda,name);f.argtypes=types;f.restype=C.c_int;r=f(*args);results['steps'].append({'api':name,'result':r})
 if r:raise RuntimeError(name+' CUDA error '+str(r))
ctx=C.c_void_p();ptr=C.c_uint64();allocated=False
try:
 call('cuInit',[0],[C.c_uint]);ver=C.c_int();call('cuDriverGetVersion',[C.byref(ver)],[C.POINTER(C.c_int)]);results['driver_api_version']=ver.value
 count=C.c_int();call('cuDeviceGetCount',[C.byref(count)],[C.POINTER(C.c_int)]);results['device_count']=count.value
 dev=C.c_int();call('cuDeviceGet',[C.byref(dev),0],[C.POINTER(C.c_int),C.c_int]);name=C.create_string_buffer(128);call('cuDeviceGetName',[name,128,dev],[C.c_void_p,C.c_int,C.c_int]);results['name']=name.value.decode()
 call('cuCtxCreate_v2',[C.byref(ctx),0,dev],[C.POINTER(C.c_void_p),C.c_uint,C.c_int])
 call('cuMemAlloc_v2',[C.byref(ptr),4096],[C.POINTER(C.c_uint64),C.c_size_t]);allocated=True
 src=(C.c_ubyte*4096)(*[i%251 for i in range(4096)]);dst=(C.c_ubyte*4096)()
 call('cuMemcpyHtoD_v2',[ptr,C.cast(src,C.c_void_p),4096],[C.c_uint64,C.c_void_p,C.c_size_t])
 call('cuMemcpyDtoH_v2',[C.cast(dst,C.c_void_p),ptr,4096],[C.c_void_p,C.c_uint64,C.c_size_t])
 call('cuCtxSynchronize',[],[]);results['roundtrip_4096_bytes_ok']=bytes(src)==bytes(dst)
 if not results['roundtrip_4096_bytes_ok']:raise RuntimeError('Data mismatch')
 results['success']=True
except Exception as e:results['success']=False;results['error']=str(e)
finally:
 if allocated:call('cuMemFree_v2',[ptr],[C.c_uint64])
 if ctx.value:call('cuCtxDestroy_v2',[ctx],[C.c_void_p])
 print(json.dumps(results,indent=2))
raise SystemExit(0 if results.get('success') else 1)
