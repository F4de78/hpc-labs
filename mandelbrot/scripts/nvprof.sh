nvc++ -DDOUBLE -DRESOLUTION=500 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_500_double
nvc++ -DDOUBLE -DRESOLUTION=1000 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_1000_double
nvc++ -DDOUBLE -DRESOLUTION=1500 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_1500_double
nvc++ -DDOUBLE -DRESOLUTION=2000 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_2000_double

nvprof ../bin/mandelbrot_gpu_500_double ../report/mandelbrot_gpu_500_double
nvprof ../bin/mandelbrot_gpu_1000_double ../report/mandelbrot_gpu_1000_double
nvprof ../bin/mandelbrot_gpu_1500_double ../report/mandelbrot_gpu_1500_double
nvprof ../bin/mandelbrot_gpu_2000_double ../report/mandelbrot_gpu_2000_double