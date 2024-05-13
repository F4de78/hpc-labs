#include "stdio.h"  // printf
#include "stdlib.h" // malloc and rand for instance. Rand not thread safe!
#include "time.h"   // time(0) to get random seed
#include "math.h"   // sine and cosine
#include "omp.h"    // openmp library like timing

#define PI2 6.28318530718
#define R_ERROR 0.01

#ifndef N
#define N 10000
#endif

#define DSIZE sizeof(double)

#ifndef THREAD_NO
#define THREAD_NO 1
#endif

int DFT(int idft, double xr[restrict], double xi[restrict], double Xr_o[restrict], double Xi_o[restrict]);
int fillInput(double *xr, double *xi);
int setOutputZero(double *Xr_o, double *Xi_o);
int checkResults(double *xr, double *xi, double *xr_check, double *xi_check, double *Xr_o, double *Xi_r);
int printResults(double *xr, double *xi);

int main(int argc, char *argv[])
{
    // size of input array
    printf("DFTW calculation with N = %d \n", N);

    double *xr = (double *)_mm_malloc(N * DSIZE, DSIZE);
    double *xi = (double *)_mm_malloc(N * DSIZE, DSIZE);
    fillInput(xr, xi);

    double *xr_check = (double *)_mm_malloc(N * DSIZE, DSIZE);
    double *xi_check = (double *)_mm_malloc(N * DSIZE, DSIZE);
    setOutputZero(xr_check, xi_check);

    double *Xr_o = (double *)_mm_malloc(N * DSIZE, DSIZE);
    double *Xi_o = (double *)_mm_malloc(N * DSIZE, DSIZE);
    setOutputZero(Xr_o, Xi_o);

    // start timer
    double start_time = omp_get_wtime();

    // DFT
    int idft = 1;
    DFT(idft, xr, xi, Xr_o, Xi_o);
    // IDFT
    idft = -1;
    DFT(idft, Xr_o, Xi_o, xr_check, xi_check);

    // stop timer
    double run_time = omp_get_wtime() - start_time;
    printf("DFTW computation in %f seconds\n", run_time);

    // check the results: easy to make correctness errors with openMP
    checkResults(xr, xi, xr_check, xi_check, Xr_o, Xi_o);

// print the results of the DFT
#ifdef DEBUG
    printResults(Xr_o, Xi_o);
#endif

    // take out the garbage
    _mm_free(xr);
    _mm_free(xi);
    _mm_free(Xi_o);
    _mm_free(Xr_o);
    _mm_free(xr_check);
    _mm_free(xi_check);

    return 1;
}

// DFT/IDFT routine
// idft: 1 direct DFT, -1 inverse IDFT (Inverse DFT)
int DFT(int idft, double xr[restrict], double xi[restrict], double Xr_o[restrict], double Xi_o[restrict])
{

    __assume_aligned(Xr_o, DSIZE);
    __assume_aligned(Xi_o, DSIZE);
    __assume_aligned(xr, DSIZE);
    __assume_aligned(xi, DSIZE);

#pragma omp parallel for schedule(dynamic) num_threads(THREAD_NO)
    for (int k = 0; k < N; k++)
    {
        for (int n = 0; n < N; n++)
        {
            double c = cos(n * k * PI2 / N);
            double s = sin(n * k * PI2 / N);

            // Real part of X[k]
            Xr_o[k] += xr[n] * c + idft * xi[n] * s;
            // Imaginary part of X[k]
            Xi_o[k] += -idft * xr[n] * s + xi[n] * c;
        }
    }

    // normalize if you are doing IDFT
    if (idft == -1)
    {
        for (int n = 0; n < N; n++)
        {
            Xr_o[n] /= N;
            Xi_o[n] /= N;
        }
    }
    return 1;
}

// set the initial signal
// be careful with this
// rand() is NOT thread safe in case
int fillInput(double *xr, double *xi)
{
    int n;
    srand(time(0));
    // genera 100000 numeri casuali che butta via per riscaldamento
    for (n = 0; n < 100000; n++) // get some random number first
        rand();
    for (n = 0; n < N; n++)
    {
        // Generate random discrete-time signal x in range (-1,+1)
        xr[n] = ((double)(2.0 * rand()) / RAND_MAX) - 1.0;
        xi[n] = ((double)(2.0 * rand()) / RAND_MAX) - 1.0;
        // constant real signal
        // xr[n] = 1.0;
        // xi[n] = 0.0;
    }
    return 1;
}

// set to zero the output vector
int setOutputZero(double *Xr_o, double *Xi_o)
{
    int n;
    for (n = 0; n < N; n++)
    {
        Xr_o[n] = 0.0;
        Xi_o[n] = 0.0;
    }
    return 1;
}

// check if x = IDFT(DFT(x))
int checkResults(double *xr, double *xi, double *xr_check, double *xi_check, double *Xr_o, double *Xi_r)
{
    int n;
    for (n = 0; n < N; n++)
    {
        if (fabs(xr[n] - xr_check[n]) > R_ERROR)
            printf("ERROR - x[%d] = %f, inv(X)[%d]=%f \n", n, xr[n], n, xr_check[n]);
        if (fabs(xi[n] - xi_check[n]) > R_ERROR)
            printf("ERROR - x[%d] = %f, inv(X)[%d]=%f \n", n, xi[n], n, xi_check[n]);
    }
    printf("Xre[0] = %f \n", Xr_o[0]);
    return 1;
}

// print the results of the DFT
int printResults(double *xr, double *xi)
{
    int n;
    for (n = 0; n < N; n++)
        printf("Xre[%d] = %f, Xim[%d] = %f \n", n, xr[n], n, xi[n]);
    return 1;
}