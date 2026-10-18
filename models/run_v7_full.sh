#!/bin/sh
# Version 7, final configuration (M8_FINAL=1): all runs in sequence, then the extra analyses and figures.
# Logs go to LOG (default: the current folder). Each stage resumes or stops cleanly if interrupted:
# finished variants are cached in M8_CACHE, and the network grid resumes from its partial file.
cd "$(dirname "$0")" || exit 1
LOG=${LOG:-.}
export M8_FINAL=1
M8_TBATCH=2 M8_CACHE=${M8_CACHE:-$LOG/m8v7_cache} python m8_v7.py > "$LOG/v7_m8.log" 2>&1 || { echo "m8_v7 failed"; exit 1; }
python integrate_v7.py > "$LOG/v7_int.log" 2>&1 || { echo "integrate_v7 failed"; exit 1; }
LV_TAG=_v7 python m9_lever_v7.py > "$LOG/v7_lever.log" 2>&1 || { echo "m9_lever_v7 failed"; exit 1; }
python v7_variance.py > "$LOG/v7_variance.log" 2>&1 || { echo "v7_variance failed"; exit 1; }
python v7_extras.py > "$LOG/v7_extras.log" 2>&1 || { echo "v7_extras failed"; exit 1; }
LV_FIG_IN=lever_v7_grid_v7.json LV_FIG_DIR=lever_v7 python m9_figures.py
python m10_structure_diagram_v7.py
echo "all done"
