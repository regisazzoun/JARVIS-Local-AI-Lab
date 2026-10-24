#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#define CK(x) do { cudaError_t e=(x);if(e!=cudaSuccess){fprintf(stderr,"CUDA_FAIL %s: %s\n",#x,cudaGetErrorString(e));return 1;} }while(0)
__global__ void probe(int* out){int i=threadIdx.x+blockIdx.x*blockDim.x;if(i<1024)out[i]=i*i+7;}
int main(){int n=0;CK(cudaGetDeviceCount(&n));if(n<1)return 2;printf("CUDA_DEVICE_COUNT %d\n",n);for(int d=0;d<n;++d){CK(cudaSetDevice(d));cudaDeviceProp p;CK(cudaGetDeviceProperties(&p,d));int* out;CK(cudaMalloc((void**)&out,1024*sizeof(int)));probe<<<32,32>>>(out);CK(cudaGetLastError());CK(cudaDeviceSynchronize());int host[1024];CK(cudaMemcpy(host,out,sizeof(host),cudaMemcpyDeviceToHost));for(int i=0;i<1024;++i)if(host[i]!=i*i+7){fprintf(stderr,"FAIL GPU%d index%d\n",d,i);return 3;}CK(cudaFree(out));printf("CUDA_GPU_PASS index=%d name=%s vram_bytes=%zu values_checked=1024\n",d,p.name,p.totalGlobalMem);}return 0;}
