(define (problem ZTRAVEL-1-2)
(:domain zeno-travel)
(:objects
	plane1 - aircraft
	person1 - person
	person2 - person
	city0 - city
	city1 - city
	city2 - city
	)
(:init
	(at plane1 city0)
	(at person1 city0)
	(at person2 city2)
	(goal person1 city0)
	(goal person2 city2)
	(= (capacity plane1) 10232)
	(= (fuel plane1) 3956)
	(= (slow-burn plane1) 4)
	(= (fast-burn plane1) 15)
	(= (onboard plane1) 0)
	(= (zoom-limit plane1) 8)
	(= (distance city0 city0) 0)
	(= (distance city0 city1) 678)
	(= (distance city0 city2) 775)
	(= (distance city1 city0) 678)
	(= (distance city1 city1) 0)
	(= (distance city1 city2) 810)
	(= (distance city2 city0) 775)
	(= (distance city2 city1) 810)
	(= (distance city2 city2) 0)
	(= (total-fuel-used) 0)
)
(:tasks-goal
    :tasks
    (
     [ (transport-person person1 city0)
       (transport-person person2 city2)
     ]
     (transport-aircraft plane1 city1)
    )
)
)
