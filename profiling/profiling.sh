#!/usr/bin/env bash

MODULE="profiling.py"

pip install -q six psutil memory_profiler line_profiler

cd "$( dirname "${BASH_SOURCE[0]}" )"

echo "+------------------------+"
echo "| Profiling memory usage |"
echo "+------------------------+"
echo ""

/usr/bin/time -f "Total time: %E (%U user, %S system)" python -m memory_profiler $MODULE

echo ""
echo "+----------------------+"
echo "| Profiling time usage |"
echo "+----------------------+"
echo ""

kernprof -l $MODULE > /dev/null
python -m line_profiler "${MODULE}.lprof"
rm -f "${MODULE}.lprof"

cd - > /dev/null
