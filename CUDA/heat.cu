#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Simple define to index into a 1D array from 2D space
#define I2D(row_len, c, r) ((r) * (row_len) + (c))

#define BLOCKS 256
#define THREADS 512

__global__ void step_kernel_mod(int ni, int nj, float fact, float *temp_in, float *temp_out)
{
  int i00, im10, ip10, i0m1, i0p1;
  float d2tdx2, d2tdy2;

  int j = threadIdx.x + blockDim.x * blockIdx.x;
  int i = threadIdx.y + blockDim.y * blockIdx.y;

  if(i>=ni-1 || j>=nj-1){
    printf("altro bound %d %d\n",i,j );
    return;
  }
  if(i==0 || j==0){
    printf("bound %d %d\n",i,j );
    return;
  }

  printf("i:%d j:%d\n", i, j);
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


  //  int i00, im10, ip10, i0m1, i0p1;
  // float d2tdx2, d2tdy2;

  // // loop over all points in domain (except boundary)
  // for (int j = 1; j < nj - 1; j++)
  // {
  //   for (int i = 1; i < ni - 1; i++)
  //   {
  //     // find indices into linear memory
  //     // for central point and neighbours
  //     i00 = I2D(ni, i, j);
  //     im10 = I2D(ni, i - 1, j);
  //     ip10 = I2D(ni, i + 1, j);
  //     i0m1 = I2D(ni, i, j - 1);
  //     i0p1 = I2D(ni, i, j + 1);

  //     // evaluate derivatives
  //     d2tdx2 = temp_in[im10] - 2 * temp_in[i00] + temp_in[ip10];
  //     d2tdy2 = temp_in[i0m1] - 2 * temp_in[i00] + temp_in[i0p1];

  //     // update temperatures
  //     temp_out[i00] = temp_in[i00] + fact * (d2tdx2 + d2tdy2);
  //   }
  // }
}

void step_kernel_ref(int ni, int nj, float fact, float *temp_in, float *temp_out)
{
  int i00, im10, ip10, i0m1, i0p1;
  float d2tdx2, d2tdy2;
  printf("%d %d\n", ni, nj);
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
  const int ni = 10;
  const int nj = 10;
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

//  printf("Temp1: 69420, Temp1ref: %f\n", temp1_ref[0]);

//  cudaMemcpy(cpu_arr, temp1, size, cudaMemcpyDeviceToHost);
//  printf("YAYAYAY %f %f\n", cpu_arr[0], cpu_arr[1]);

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
  for (istep = 0; istep < nstep; istep++)
  {
    step_kernel_mod<<<BLOCKS, THREADS>>>(ni, nj, tfac, temp1, temp2);

    // swap the temperature pointers
    // cudaMemcpy(temp1, temp2, size, cudaMemcpyDeviceToHost);
    temp_tmp = temp1;
    temp1 = temp2;
    temp2 = temp_tmp;
    //cudaMemcpy(temp1, temp2, size, cudaMemcpyDeviceToDevice);
  }
  //cudaDeviceSynchronize();

  cudaMemcpy(cpu_arr, temp2, size, cudaMemcpyDeviceToHost);

  float maxError = 0;
  // Output should always be stored in the temp1 and temp1_ref at this point
  for (int i = 0; i < ni * nj; ++i)
  {
    // printf("Doing stuff at cell: %d\n", i);
    //printf("era questo:%f %f\n", cpu_arr[i], temp1_ref[i]);
    if (abs(cpu_arr[i] - temp1_ref[i]) > maxError)
    {
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
