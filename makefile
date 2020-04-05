compile:
	antlr4 -Dlanguage=Python3 Vgdl.g4

parse-game:
	python3 ./src/main.py -gi $(gi) -go ./output/domain.hpdl

parse-level:
	python3 ./src/main.py -gi $(gi) -li $(li) -go ./output/domain.hpdl -lo ./output/problem.hpdl

run:
	./planners/Siadex/planner -d $(d) -p $(p)

verbose:
	./planners/Siadex/planner -d $(d) -p $(p) -v

# replan:
# 	

help:
	python3 ./src/main.py -h