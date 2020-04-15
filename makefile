# Compile ANTLR grammar
compile:
	antlr4 -Dlanguage=Python3 Vgdl.g4

# Parse only the VGDL description
parse-game:
	python3 ./src/main.py -gi $(gi) -go ./output/domain.hpdl

# Parse the VGDL description and a level
parse-level:
	python3 ./src/main.py -gi $(gi) -li $(li) -go ./output/domain.hpdl -lo ./output/problem.hpdl

# Call planner
run:
	./planners/Siadex/planner -d $(d) -p $(p)

# Call planner in verbose mode
verbose:
	./planners/Siadex/planner -d $(d) -p $(p) -v

# For replanning: Parse and call planner
replan:
	python3 ./src/main.py -gi $(gi) -li $(li) -go $(go) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null

# For replanning: Parse and call planner keeping an already defined domain
replan-level:
	python3 ./src/main.py -gi $(gi) -li $(li) -go $(goTMP) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null

# Show help
help:
	python3 ./src/main.py -h