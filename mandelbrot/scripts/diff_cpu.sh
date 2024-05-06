icpx -qopenmp -fast -xHost -DFMA -DDOUBLE -DRESOLUTION=500 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_500_double
icpx -qopenmp -fast -xHost -DFMA -DDOUBLE -DRESOLUTION=1000 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_1000_double
icpx -qopenmp -fast -xHost -DFMA -DDOUBLE -DRESOLUTION=1500 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_1500_double
icpx -qopenmp -fast -xHost -DFMA -DDOUBLE -DRESOLUTION=2000 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_2000_double
icpx -qopenmp -fast -xHost -DFMA -DRESOLUTION=500 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_500_float
icpx -qopenmp -fast -xHost -DFMA -DRESOLUTION=1000 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_1000_float
icpx -qopenmp -fast -xHost -DFMA -DRESOLUTION=1500 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_1500_float
icpx -qopenmp -fast -xHost -DFMA -DRESOLUTION=2000 ../src/mandelbrot_cpu_vect_omp.cpp -o ../bin/mandelbrot_cpu_2000_float

../bin/mandelbrot_cpu_500_double ../report/mandelbrot_cpu_500_double
../bin/mandelbrot_cpu_1000_double ../report/mandelbrot_cpu_1000_double
../bin/mandelbrot_cpu_1500_double ../report/mandelbrot_cpu_1500_double
../bin/mandelbrot_cpu_2000_double ../report/mandelbrot_cpu_2000_double

../bin/mandelbrot_cpu_500_float ../report/mandelbrot_cpu_500_float
../bin/mandelbrot_cpu_1000_float ../report/mandelbrot_cpu_1000_float
../bin/mandelbrot_cpu_1500_float ../report/mandelbrot_cpu_1500_float
../bin/mandelbrot_cpu_2000_float ../report/mandelbrot_cpu_2000_float

python3 ./diff.py --ref ../report/mandelbrot_cpu_500_float --gpu ../report/mandelbrot_cpu_500_double | wc -l > ../report/diff_cpu
python3 ./diff.py --ref ../report/mandelbrot_cpu_1000_float --gpu ../report/mandelbrot_cpu_1000_double | wc -l >> ../report/diff_cpu
python3 ./diff.py --ref ../report/mandelbrot_cpu_1500_float --gpu ../report/mandelbrot_cpu_1500_double | wc -l >> ../report/diff_cpu
python3 ./diff.py --ref ../report/mandelbrot_cpu_2000_float --gpu ../report/mandelbrot_cpu_2000_double | wc -l >> ../report/diff_cpu