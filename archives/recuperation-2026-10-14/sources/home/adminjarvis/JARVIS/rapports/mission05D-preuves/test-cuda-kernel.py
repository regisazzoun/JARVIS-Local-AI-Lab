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
 ptx=b""".version 6.4
.target sm_75
.address_size 64
.visible .entry math_test(.param .u64 outptr) {
.reg .b32 %r<5>;
.reg .b64 %rd<4>;
ld.param.u64 %rd1,[outptr];
mov.u32 %r1,%tid.x;
mov.u32 %r2,%ctaid.x;
mad.lo.u32 %r3,%r2,256,%r1;
mul.wide.u32 %rd2,%r3,4;
add.u64 %rd3,%rd1,%rd2;
mad.lo.u32 %r4,%r3,3,7;
st.global.u32 [%rd3],%r4;
ret;
}
"""
 module=C.c_void_p();fn=C.c_void_p()
 call('cuModuleLoadData',[C.byref(module),C.c_char_p(ptx)],[C.POINTER(C.c_void_p),C.c_void_p])
 call('cuModuleGetFunction',[C.byref(fn),module,b'math_test'],[C.POINTER(C.c_void_p),C.c_void_p,C.c_char_p])
 args=(C.c_void_p*1)(C.cast(C.byref(ptr),C.c_void_p));dst=(C.c_uint32*1024)();start=time.perf_counter()
 for iteration in range(100):
  call('cuLaunchKernel',[fn,4,1,1,256,1,1,0,None,args,None],[C.c_void_p]+[C.c_uint]*7+[C.c_void_p,C.POINTER(C.c_void_p),C.c_void_p])
  call('cuCtxSynchronize',[],[])
  call('cuMemcpyDtoH_v2',[C.cast(dst,C.c_void_p),ptr,4096],[C.c_void_p,C.c_uint64,C.c_size_t])
  assert list(dst)==[i*3+7 for i in range(1024)],'wrong mathematical result'
 results['iterations']=100;results['verified_values']=102400;results['elapsed_seconds']=time.perf_counter()-start;results['formula']='out[i]=3*i+7';results['last_value']=dst[-1]
 call('cuModuleUnload',[module],[C.c_void_p])
 results['success']=True
except Exception as e:results['success']=False;results['error']=str(e)
finally:
 if allocated:call('cuMemFree_v2',[ptr],[C.c_uint64])
 if ctx.value:call('cuCtxDestroy_v2',[ctx],[C.c_void_p])
 print(json.dumps(results,indent=2))
raise SystemExit(0 if results.get('success') else 1)
