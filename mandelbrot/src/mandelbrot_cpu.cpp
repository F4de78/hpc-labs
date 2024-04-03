#include <iostream>
#include <fstream>
#include <complex>
#include <chrono>
#include <omp.h>
#include <immintrin.h>



#define FTYPE double
#if FTYPE == double
typedef double __ftype;
#else
typedef float __ftype;
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
#define DEGREE 2 // Degree of the polynomial
#endif

#ifndef ITERATIONS
#define ITERATIONS 1000 // Maximum number of iterations
#endif

#ifndef THREAD_NO
#define THREAD_NO 24
#endif

#ifndef OMP_SCHEDULE
#define OMP_SCHEDULE dynamic
#endif

using namespace std;

int main(int argc, char **argv)
{
    int *const image = new int[HEIGHT * WIDTH];

    const auto start = chrono::steady_clock::now();

    const int block_size = HEIGHT * WIDTH / THREAD_NO;

    //#pragma omp parallel for schedule(OMP_SCHEDULE) num_threads(THREAD_NO)
    for (int block_idx = 0; block_idx < THREAD_NO; block_idx++)
    {


        __m256d step = _mm256_set1_pd(STEP);
        __m256d min_x = _mm256_set1_pd(MIN_X);
        __m256d min_y = _mm256_set1_pd(MIN_Y);

        //TODO: check for leftover stuff
        //TODO: what to do when we have less than 4 items?

        //TODO: have different offsets for different float types

        //TODO: the < check on pos may overflow the array
        for (int pos = block_size * block_idx; pos < block_size * (block_idx + 1); pos+=4)
        {
            // image[pos] = 0;
            _mm_store_epi32((void *) &image[pos], _mm_set1_epi32(0));

            //TODO: try to see if loading pos, pos + 1, ... and then dividing by W, W, W, W is better (created with _mm256_set1_epi64x)
            __m128i row_vec = _mm_set_epi32(pos / WIDTH, (pos + 1) / WIDTH, (pos + 2) / WIDTH, (pos + 3) / WIDTH);
            __m128i col_vec = _mm_set_epi32(pos % WIDTH, (pos + 1) % WIDTH, (pos + 2) % WIDTH, (pos + 3) % WIDTH);


            // __ftype c_re = col * STEP + MIN_X;
            // Convert from vec of long long to vec of double
            __m256d c_re = _mm256_cvtepi32_pd(col_vec);
            c_re = _mm256_mul_pd(c_re, step);
            c_re = _mm256_add_pd(c_re, min_x);


            // __ftype c_im = row * STEP + MIN_Y;
            __m256d c_im = _mm256_cvtepi32_pd(row_vec);
            c_im = _mm256_mul_pd(c_im, step);
            c_im = _mm256_add_pd(c_im, min_y);

            // set vectors to 0
            __m256d z_re = _mm256_setzero_pd();
            __m256d z_im = _mm256_setzero_pd();

            // z = z^2 + c
            for (int i = 1; i <= ITERATIONS; i++)
            {
                //TODO: fused add and multiplication operations? (if exists)

                // xy	=	(a+ib)(c+id)	
                // 	    =	(ac-bd)+i(ad+bc).
                // a == c, b == d
                // ==> x * x = (a * a - b * b) + i (2 * a * b)
                __m256d z2_re = _mm256_mul_pd(z_re, z_re);
                __m256d tmp = _mm256_mul_pd(z_im, z_im);
                z2_re = _mm256_add_pd(z2_re, tmp);

                __m256d z2_im = _mm256_mul_pd(z_re, z_im);
                z2_im = _mm256_add_pd(z2_im, z2_im);

                // z = z^2 + c;
                // => z2 + c
                z_re = _mm256_add_pd(z2_re, c_re);
                z_im = _mm256_add_pd(z2_im, c_im);

                // |z|2 = x2 + y2.
                tmp = _mm256_mul_pd(z_im, z_im);
                __m256d abs2= _mm256_add_pd(z2_re, tmp);

                // Settare image[pos] se vale abs2 >= 4

                // image[pos] = should_update * i + (1 - should_update) * image[pos]

                __m256d abs2_gt_4 = _mm256_cmp_pd(abs2, _mm256_set1_pd(4.0), _CMP_GT_OQ);

                __m128i image_vec = _mm_load_epi32((void *) &image[pos]);
                __m128i image_vec_all_zeros = _mm_cmpeq_epi8(image_vec, _mm_setzero_si128());

                __m128i current_step = _mm_set1_epi32(i);

                //TODO: is there a AND function for vectors?
                // should_update = abs2 >= 4 && image[pos] == 0  
                // Perform an AND by multiplying
                // _mm_mul_epi32 only multiplies the 1st and 3rd 32bit numbers of each vector with each other and stores the 64bit results in the 128bit vector result
                // We know we're multiplying by either 0 or 1, so we know that the multiplication will never exceed 32 bits, thus we can keep the low 32 bits of
                // each of the multiplications
                __m128i should_update = _mm_mullo_epi32(_mm256_cvtpd_epi32(abs2_gt_4), image_vec_all_zeros);

                // tmp2 = (1 - should_update)
                __m128i tmp2 = _mm_sub_epi32(_mm_set1_epi32(1), should_update);
                // tmp2 = tmp2 * image[pos]
                // Same considerations as above
                tmp2 = _mm_mullo_epi32(tmp2, _mm_load_epi32((void*) &image[pos]));
                // tmp2 = tmp2 + should_update * i
                tmp2 = _mm_add_epi32(tmp2, _mm_mul_epi32(should_update, current_step));

                // image[pos] = tmp2
                _mm_store_epi32((void*) &image[pos], tmp2);

                // If all of the image pixels have diverged, then break out of the loop
                // mask = image[pos] != 0
                if(_mm_movemask_epi8(_mm_xor_si128(image_vec_all_zeros, _mm_set1_epi32(-1))) == 0xFFFF) {
                    break;
                }

                // mask = image[pos] != 0
                // int mask = _mm_movemask_
                // if mask break;

                // Questo probabilmente e' rotto perche' non e' detto che dopo un loop in cui e' >= 4 poi continui ad essere >=4 anche nei cicli dopo? (o cresce sempre)
                // In ogni caso se si controlla se tutti i vari image[pos, pos+1, ...] sono != 0 vuol dire che sono tutti divergenti                // Break when all of them
                // _CMP_GT_OQ -> Greater-than (ordered, non-signaling)
                // int mask = _mm256_movemask_pd(abs2_gt_4);
                // // If they all converge
                // if(mask == 0xFFFF) {
                //     break;
                // }
            }
        }
    }

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

    delete[] image; // It's here for coding style, but useless
    return 0;
}
