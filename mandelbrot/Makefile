ref:
	icpx -faxt -xHost -ggdb src/mandelbrot.cpp -o bin/ref

ref-norm-optim:
	icpx -fast -xHost -ggdb -DNORM_OPTIM src/mandelbrot_cpu_omp.cpp -o bin/ref-norm-optim

omp:
	icpx -fast -xHost -ggdb -qopenmp -DNORM_OPTIM -DTHREAD_NO=24 src/mandelbrot_cpu_omp.cpp -o bin/omp

vect-st-f:
	icpx -fast -xHost -ggdb -DFMA src/mandelbrot_cpu_vect_omp.cpp -o bin/vect-st-f

vect-st-d:
	icpx -fast -xHost -ggdb -DFMA -DDOUBLE src/mandelbrot_cpu_vect_omp.cpp -o bin/vect-st-d

vect-f:
	icpx -fast -xHost -ggdb -DFMA -qopenmp -DTHREAD_NO=24 src/mandelbrot_cpu_vect_omp.cpp -o bin/vect-st-f

vect-d:
	icpx -fast -xHost -ggdb -DFMA -DDOUBLE -qopenmp -DTHREAD_NO=24 src/mandelbrot_cpu_vect_omp.cpp -o bin/vect-st-d

vect-f-static:
	icpx -fast -xHost -ggdb -DFMA -qopenmp -DTHREAD_NO=24 -DOMP_SCHEDULE=static -DRESOLUTION=5000 src/mandelbrot_cpu_vect_omp.cpp -o bin/vect-st-f

vect-d-static:
	icpx -fast -xHost -ggdb -DFMA -DDOUBLE -qopenmp -DTHREAD_NO=24 -DOMP_SCHEDULE=static -DRESOLUTION=5000 src/mandelbrot_cpu_vect_omp.cpp -o bin/vect-st-d

gpu-f:
	nvc++ src/mandelbrot_gpu.cu -o bin/gpu-f

gpu-d:
	nvc++ -DDOUBLE src/mandelbrot_gpu.cu -o bin/gpu-d