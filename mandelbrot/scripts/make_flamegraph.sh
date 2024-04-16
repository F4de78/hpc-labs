perf record --call-graph dwarf $1
perf script | ~/FlameGraph/stackcollapse-perf.pl > out.perf-folded
~/FlameGraph/flamegraph.pl out.perf-folded > flamegraph.svg
