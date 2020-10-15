# Compile ANTLR grammar
compile-grammar:
	antlr4 -Dlanguage=Python3 Vgdl.g4

# ------------------------------------------------------------------------------

# Parse only the VGDL description
parse-game:
	python3 ./src/main.py -gi $(gi) -go ./output/domain.hpdl

# Parse the VGDL description and a level
parse-level:
	python3 ./src/main.py -gi $(gi) -li $(li) -go ./output/domain.hpdl -lo ./output/problem.hpdl

# Show help
help:
	python3 ./src/main.py -h

# ------------------------------------------------------------------------------

compile-planner:
	cd ./planners/Siadex && cmake . && make -j

# Call planner
run:
	./planners/Siadex/planner -d $(d) -p $(p)

# Call planner in verbose mode
verbose:
	./planners/Siadex/planner -d $(d) -p $(p) -v

# For replanning: Parse and call planner
parse-and-run:
	python3 ./src/main.py -gi $(gi) -li $(li) -go ./output/domain.hpdl -lo ./output/problem.hpdl
	./planners/Siadex/planner -d ./output/domain.hpdl -p ./output/problem.hpdl

# ------------------------------------------------------------------------------

# Used in replanning: Parse and call planner keeping an already defined domain
replan-level:
	python3 ./src/main.py -gi $(gi) -li $(li) -go $(goTMP) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null

# For replanning: Parse and call planner
replan:
	python3 ./src/main.py -gi $(gi) -li $(li) -go $(go) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null


# ------------------------------------------------------------------------------
# PDDL
# ------------------------------------------------------------------------------

pddl:
	# python3 ./src/main.py -l=pddl -gi ./resources/games/brainman.txt -go ./output/domain.pddl
	# planners/Madagascar/MpC output/domain.pddl output/problem.pddl

	python3 ./src/main.py -l=pddl -gi ./resources/games/sokoban.txt -go ./output/domain.pddl
	planners/Madagascar/MpC output/domain.pddl output/problem-sokoban.pddl

	# python3 ./src/main.py -l=pddl -gi ./resources/games/boulderdash.txt -go ./output/domain.pddl
	# python3 ./src/main.py -l=pddl -gi ./resources/games/butterflies.txt -go ./output/domain.pddl


# ------------------------------------------------------------------------------
# Fast Downward
# ------------------------------------------------------------------------------

compile-fd:
	cd ./planners/FastDownward;	python3 ./build.py

run-fd:
	python3 ./planners/FastDownward/fast-downward.py ./output/pddl-domain.pddl ./output/pddl-problem.pddl --search "astar(lmcut())"

run-fd2:
	python3 ./planners/FastDownward/fast-downward.py --alias seq-sat-lama-2011 ./output/pddl-domain.pddl ./output/pddl-problem.pddl

help-fd:
	python3 ./planners/FastDownward/fast-downward.py --help

# ------------------------------------------------------------------------------
# Metric-FF
# ------------------------------------------------------------------------------

# -s 0 = NO optimization
metric:
	./planners/Metric-FF-v2.1/ff -o ./output/pddl-domain.pddl -f ./output/pddl-problem.pddl -s 0
	#  -O -g 1 -h 1

# ------------------------------------------------------------------------------
# MADAGASCAR
# ------------------------------------------------------------------------------

madagascar1:
	planners/Madagascar/MpC output/pddl-domain.pddl output/pddl-problem.pddl -o ./output/plan.txt

madagascar2:
	planners/Madagascar/Mp output/pddl-domain.pddl output/pddl-problem.pddl -o ./output/plan.txt

madagascar3:
	planners/Madagascar/M output/pddl-domain.pddl output/pddl-problem.pddl -o ./output/plan.txt