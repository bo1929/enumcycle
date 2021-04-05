#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
names=("GD02_a" "GD02_b" "ibm32")
for NAME in ${names[@]}; do
    echo "#!/bin/bash
threads=(2 4 8)
for ((i=1;i<=4;i++));
do
    ./enumCycleE1 ${NAME}
    for THD in \${threads[@]};
    do
        OMP_NUM_THREADS=\${THD} ./enumCycleE2 ${NAME}
        OMP_NUM_THREADS=\${THD} ./enumCycleE3 ${NAME}
    done
done
exit 0
"       >"${SCRIPTPATH}/../run_expt_${NAME}.sh"
    chmod +x "${SCRIPTPATH}/../run_expt_${NAME}.sh" 
done
exit 0
