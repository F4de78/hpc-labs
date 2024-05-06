nvc++ -DFMA -DDOUBLE -DRESOLUTION=500 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_500_double
nvc++ -DFMA -DDOUBLE -DRESOLUTION=1000 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_1000_double
nvc++ -DFMA -DDOUBLE -DRESOLUTION=1500 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_1500_double
nvc++ -DFMA -DDOUBLE -DRESOLUTION=2000 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_2000_double
nvc++ -DFMA -DRESOLUTION=500 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_500_float
nvc++ -DFMA -DRESOLUTION=1000 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_1000_float
nvc++ -DFMA -DRESOLUTION=1500 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_1500_float
nvc++ -DFMA -DRESOLUTION=2000 ../src/mandelbrot_gpu.cu -o ../bin/mandelbrot_gpu_2000_float

../bin/mandelbrot_gpu_500_double ../report/mandelbrot_gpu_500_double
../bin/mandelbrot_gpu_1000_double ../report/mandelbrot_gpu_1000_double
../bin/mandelbrot_gpu_1500_double ../report/mandelbrot_gpu_1500_double
../bin/mandelbrot_gpu_2000_double ../report/mandelbrot_gpu_2000_double

../bin/mandelbrot_gpu_500_float ../report/mandelbrot_gpu_500_float
../bin/mandelbrot_gpu_1000_float ../report/mandelbrot_gpu_1000_float
../bin/mandelbrot_gpu_1500_float ../report/mandelbrot_gpu_1500_float
../bin/mandelbrot_gpu_2000_float ../report/mandelbrot_gpu_2000_float

python3 ./diff.py --ref ../report/mandelbrot_gpu_500_float --gpu ../report/mandelbrot_gpu_500_double | wc -l > ../report/diff_gpu
python3 ./diff.py --ref ../report/mandelbrot_gpu_1000_float --gpu ../report/mandelbrot_gpu_1000_double | wc -l >> ../report/diff_gpu
python3 ./diff.py --ref ../report/mandelbrot_gpu_1500_float --gpu ../report/mandelbrot_gpu_1500_double | wc -l >> ../report/diff_gpu
python3 ./diff.py --ref ../report/mandelbrot_gpu_2000_float --gpu ../report/mandelbrot_gpu_2000_double | wc -l >> ../report/diff_gpu