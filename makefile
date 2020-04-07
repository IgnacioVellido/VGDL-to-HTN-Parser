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

replan:
	python3 ./src/main.py -gi $(gi) -li $(li) -go $(go) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null

help:
	python3 ./src/main.py -h