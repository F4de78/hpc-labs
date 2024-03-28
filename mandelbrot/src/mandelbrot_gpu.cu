#include <iostream>
#include <fstream>
//#include <complex>
#include <complex.h>
#include <chrono>

#define FTYPE double
#if FTYPE == double
    typedef double __ftype;
#else
    typedef float __ftype;
#endif

#ifndef THREADS_X
    #define THREADS_X 16
#endif
#ifndef THREADS_Y
    #define THREADS_Y 16
#endif

// Ranges of the set
#define MIN_X -2
#define MAX_X 1
#define MIN_Y -1
#define MAX_Y 1

// Image ratio
#define RATIO_X (MAX_X - MIN_X)
#define RATIO_Y (MAX_Y - MIN_Y)

// Image size
#ifndef RESOLUTION
    #define RESOLUTION 1000
#endif
#define WIDTH (RATIO_X * RESOLUTION)
#define HEIGHT (RATIO_Y * RESOLUTION)

#define STEP ((__ftype)RATIO_X / WIDTH)

#ifndef DEGREE
    #define DEGREE 2        // Degree of the polynomial
#endif

#ifndef ITERATIONS
    #define ITERATIONS 1000 // Maximum number of iterations
#endif
using namespace std;

__global__ void mandelbrot(double *const image) {

    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;    
    
    int pos = row * WIDTH + col;
    
    if (pos < 0 || pos >= HEIGHT * WIDTH) {
        return;
    }

    image[pos] = 0;

    
    // const cuda::std::complex<double> c(col * STEP + MIN_X, row * STEP + MIN_Y);
    __ftype c_re = col * STEP + MIN_X;
    __ftype c_im = row * STEP + MIN_Y;

    __ftype z_re = 0.0;
    __ftype z_im = 0.0;

    
    // z = z^2 + c
    // cuda::std::complex<double> z(0, 0);

    for (int i = 1; i <= ITERATIONS; i++)
    {
            
        // xy	=	(a+ib)(c+id)	
        // 	    =	(ac-bd)+i(ad+bc).
        // a == c, b == d
        // ==> x * x = (a * a - b * b) + i (2 * a * b)
        __ftype z2_re = z_re * z_re - z_im * z_im;
        __ftype z2_im = 2.0 * z_re * z_im;


        // z = pow(z, 2) + c;
        z_re = z2_re + c_re;
        z_im = z2_im + c_im;

        // |z|2 = x2 + y2.
        __ftype abs2 = z_re * z_re + z_im * z_im;

        // If it is convergent
        if (abs2 >= 4)
        {
            image[pos] = i;
            return;
        }
    }
}

void handle_error(cudaError_t err){
    if(err != cudaSuccess){
        cerr << "GPUassert: " << cudaGetErrorString(err) << endl;
        exit(err);
    }
}

int main(int argc, char **argv)
{   
    cout << "Width: " << WIDTH << ", Height: " << HEIGHT << ", Step: "<< STEP << endl;
    int *const image = new int[HEIGHT * WIDTH];
    const int size = HEIGHT * WIDTH * sizeof(int);
    
    int *image_gpu = nullptr;

    const auto start = chrono::steady_clock::now();

    memset(image, 0, size);

    handle_error(cudaMalloc((void **)&image_gpu, size));
    
    handle_error(cudaMemcpy(image_gpu, image, size, cudaMemcpyHostToDevice));    

    dim3 threadsPerBlock(THREADS_X, THREADS_Y);
    dim3 numBlocks((WIDTH + threadsPerBlock.x - 1) / threadsPerBlock.x, (HEIGHT + threadsPerBlock.y - 1) / threadsPerBlock.y);
    cout << "Threads: " << threadsPerBlock.x << "x" << threadsPerBlock.y << endl;
    cout << "Blocks: " << numBlocks.x << "x" << numBlocks.y << endl;
   
    mandelbrot<<<numBlocks, threadsPerBlock>>>(image_gpu);

    handle_error(cudaMemcpy(image, image_gpu, size, cudaMemcpyDeviceToHost));    
    
    const auto end = chrono::steady_clock::now();
    cout << "Time elapsed: "
         << chrono::duration_cast<chrono::milliseconds>(end - start).count()
         << " ms." << endl;

    // Write the result to a file
    ofstream matrix_out;

    if (argc < 2)
    {
        cout << "Please specify the output file as a parameter." << endl;
        return -1;
    }

    matrix_out.open(argv[1], ios::trunc);
    if (!matrix_out.is_open())
    {
        cout << "Unable to open file." << endl;
        return -2;
    }

    for (int row = 0; row < HEIGHT; row++)
    {
        for (int col = 0; col < WIDTH; col++)
        {
            matrix_out << image[row * WIDTH + col];

            if (col < WIDTH - 1)
                matrix_out << ',';
        }
        if (row < HEIGHT - 1)
            matrix_out << endl;
    }
    matrix_out.close();

    handle_error(cudaFree(image_gpu));
    delete[] image; // It's here for coding style, but useless
    return 0;
}