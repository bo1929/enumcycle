all: setup E1 E2 E3 S 

setup:
	@mkdir -p ./results/
	@mkdir -p ./results/time_results
	@echo "Directory ./results will be used for the (raw) outputs."

compile:
	@chmod +x ./scripts/compile_all.sh
	./scripts/compile_all.sh

E1:
	g++ ./src/enumCycleE1.cpp -o enumCycleE1

E2:
	g++ ./src/enumCycleE2.cpp -o enumCycleE2 -fopenmp

E3:
	g++ ./src/enumCycleE3.cpp -o enumCycleE3 -fopenmp

S:
	@chmod +x ./scripts/wrt_expt_scripts.sh
	@./scripts/wrt_expt_scripts.sh

clean:
	rm -f ./enumCycleE1 ./enumCycleE2 ./enumCycleE3
	rm -rf ./results
	@rm -f ./*.sh
	@echo "Cleaned. ./results/*.out files are deleted as well."
