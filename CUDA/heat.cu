#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Simple define to index into a 1D array from 2D space
#define I2D(row_len, c, r) ((r) * (row_len) + (c))

__global__ void step_kernel_mod(int ni, int nj, float fact, float *temp_in, float *temp_out) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  int j = blockIdx.y * blockDim.y + threadIdx.y;

  if (i >= 1 && i < ni - 1 && j >= 1 && j < nj - 1) {
    int i00 = I2D(ni, i, j);
    int im10 = I2D(ni, i - 1, j);
    int ip10 = I2D(ni, i + 1, j);
    int i0m1 = I2D(ni, i, j - 1);
    int i0p1 = I2D(ni, i, j + 1);

    float d2tdx2 = temp_in[im10] - 2 * temp_in[i00] + temp_in[ip10];
    float d2tdy2 = temp_in[i0m1] - 2 * temp_in[i00] + temp_in[i0p1];

    temp_out[i00] = temp_in[i00] + fact * (d2tdx2 + d2tdy2);
  }
}

void step_kernel_ref(int ni, int nj, float fact, float *temp_in, float *temp_out)
{
  int i00, im10, ip10, i0m1, i0p1;
  float d2tdx2, d2tdy2;
  //printf("%d %d\n", ni, nj);
  // loop over all points in domain (except boundary)
  for (int j = 1; j < nj - 1; j++)
  {
    for (int i = 1; i < ni - 1; i++)
    {
      // find indices into linear memory
      // for central point and neighbours
      i00 = I2D(ni, i, j);
      im10 = I2D(ni, i - 1, j);
      ip10 = I2D(ni, i + 1, j);
      i0m1 = I2D(ni, i, j - 1);
      i0p1 = I2D(ni, i, j + 1);

      // evaluate derivatives
      d2tdx2 = temp_in[im10] - 2 * temp_in[i00] + temp_in[ip10];
      d2tdy2 = temp_in[i0m1] - 2 * temp_in[i00] + temp_in[i0p1];

      // update temperatures
      temp_out[i00] = temp_in[i00] + fact * (d2tdx2 + d2tdy2);
    }
  }
}

int main()
{
  int istep;
  int nstep = 200; // number of time steps

  // Specify our 2D dimensions
  const int ni = 1000;
  const int nj = 1000;
  float tfac = 8.418e-5; // thermal diffusivity of silver

  float *temp1_ref, *temp2_ref, *temp1, *temp2, *temp_tmp, *cpu_arr;

  const int size = ni * nj * sizeof(float);

  temp1_ref = (float *)malloc(size);
  temp2_ref = (float *)malloc(size);
  cpu_arr = (float *)malloc(size);

  cudaMalloc((void **)&temp1, size);
  cudaMalloc((void **)&temp2, size);

  // Initialize with random data
  for (int i = 0; i < ni * nj; ++i)
  {
    float rnd = (float)rand() / (float)(RAND_MAX / 100.0f);
    temp1_ref[i] = temp2_ref[i] = rnd;
  }

  cudaMemcpy(temp1, temp1_ref, size, cudaMemcpyHostToDevice);
  cudaMemcpy(temp2, temp2_ref, size, cudaMemcpyHostToDevice);

  // Execute the CPU-only reference version
  for (istep = 0; istep < nstep; istep++)
  {
    step_kernel_ref(ni, nj, tfac, temp1_ref, temp2_ref);

    // swap the temperature pointers
    temp_tmp = temp1_ref;
    temp1_ref = temp2_ref;
    temp2_ref = temp_tmp;
  }

  // Execute the modified version using same data
  // https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/
  dim3 threadsPerBlock(16, 16); // 1024 threads per block
  dim3 numBlocks((ni + threadsPerBlock.x - 1) / threadsPerBlock.x, (nj + threadsPerBlock.y - 1) / threadsPerBlock.y);
  
  for (istep = 0; istep < nstep; istep++)
  {
    step_kernel_mod<<<numBlocks, threadsPerBlock>>>(ni, nj, tfac, temp1, temp2);

    // swap the temperature pointers
    temp_tmp = temp1;
    temp1 = temp2;
    temp2 = temp_tmp;
  }

  cudaMemcpy(cpu_arr, temp1, size, cudaMemcpyDeviceToHost);

  float maxError = 0;
  // Output should always be stored in the temp1 and temp1_ref at this point
  for (int i = 0; i < ni * nj; ++i)
  {
    if (abs(cpu_arr[i] - temp1_ref[i]) > maxError)
    { 
      printf("cpu_arr: %f - temp1_ref:%f\n",cpu_arr[i] ,temp1_ref[i] );
      maxError = abs(cpu_arr[i] - temp1_ref[i]);
    }
  }

  // Check and see if our maxError is greater than an error bound
  if (maxError > 0.0005f)
  {
    printf("Problem! The Max Error of %.5f is NOT within acceptable bounds.\n", maxError);
  }
  else
  {
    printf("The Max Error of %.5f is within acceptable bounds.\n", maxError);
  }

  free(temp1_ref);
  free(temp2_ref);
  cudaFree(temp1);
  cudaFree(temp2);

  return 0;
}
