compile:
	antlr4 -Dlanguage=Python3 Vgdl.g4

parse-game:
	python3 ./src/main.py -gi $(g) -go ./output/domain.hpdl

parse-level:
	python3 ./src/main.py -gi $(g) -li $(l) -go ./output/domain.hpdl -lo ./output/problem.hpdl

run:
	./planners/Siadex/planner -d $(d) -p $(p)

verbose:
	./planners/Siadex/planner -d $(d) -p $(p) -v

help:
	python Main.py -h