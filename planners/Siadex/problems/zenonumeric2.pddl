(define (domain zeno-travel)

 (:requirements 
  :typing 
  :fluents
  :derived-predicates 
  :negative-preconditions
  :universal-preconditions
  :disjuntive-preconditions
  :htn-expansion
 )

 (:types 
  aircraft 
  person 
  city - object
  moving-style
 )

 (:constants
  slow -moving-style
  fast -moving-style
 )

    (:predicates (at ?x - (either person aircraft) ?c - city)
     (same ?x ?x)
     (different ?x ?y)
     (goal ?p -person ?c - city)
     (possible-person-in ?c -city)
     (travel-cost-info ?a -aircraft ?from -city ?to -city ?cost -number ?style - moving-style)
     (in ?p - person ?a - aircraft)
     (dest ?a -aircraft ?c -city)
     (no-use ?a -aircraft)
    )

    (:functions 
     (fuel ?a - aircraft)
     (distance ?c1 - city ?c2 - city)
     (slow-burn ?a - aircraft)
     (fast-burn ?a - aircraft)
     (capacity ?a - aircraft)
     (total-fuel-used)
     (onboard ?a - aircraft)
     (zoom-limit ?a - aircraft)
    )

    (:derived (same ?x ?x) ()) 
    (:derived (different ?x ?y) (not (same ?x ?y)))
    (:derived (possible-person-in ?city -city) (and (at ?p -person ?city) (goal ?p ?city2) (different ?city2 ?city)))
    (:derived (travel-cost-info ?a ?from ?to ?cost ?style) (and 
							    (bind ?style slow) 
							    (>= (capacity ?a) (* (distance ?from ?to) (slow-burn ?a)))
							    (bind ?cost (* (distance ?from ?to) (slow-burn ?a)))
							   ))
    (:derived (travel-cost-info ?a ?from ?to ?cost ?style) (and 
							    (bind ?style fast) 
							    (< (onboard ?a) (zoom-limit ?a))
							    (>= (capacity ?a) (* (distance ?from ?to) (fast-burn ?a)))
							    (bind ?cost (* (distance ?from ?to) (fast-burn ?a)))
							   ))

    (:action board
     :parameters (?p - person ?a - aircraft ?c - city)
     :precondition (and (at ?p ?c)
	 (at ?a ?c))
     :effect (and (not (at ?p ?c))
	 (in ?p ?a)
	 (increase (onboard ?a) 1)))


    (:action debark
     :parameters (?p - person ?a - aircraft ?c - city)
     :precondition (and (in ?p ?a)
	 (at ?a ?c))
     :effect (and (not (in ?p ?a))
	 (at ?p ?c)
	 (decrease (onboard ?a) 1)))

    (:action fly 
     :parameters (?a - aircraft ?c1 ?c2 - city)
     :precondition (and (at ?a ?c1)
	 (>= (fuel ?a) 
	  (* (distance ?c1 ?c2) (slow-burn ?a))))
     :effect (and (not (at ?a ?c1))
	 (at ?a ?c2)
	 (increase (total-fuel-used)
	  (* (distance ?c1 ?c2) (slow-burn ?a)))
	 (decrease (fuel ?a) 
	  (* (distance ?c1 ?c2) (slow-burn ?a)))))

    (:action zoom
     :parameters (?a - aircraft ?c1 ?c2 - city)
     :precondition (and (at ?a ?c1)
	 (>= (fuel ?a) 
	  (* (distance ?c1 ?c2) (fast-burn ?a)))
	 (<= (onboard ?a) (zoom-limit ?a)))
     :effect (and (not (at ?a ?c1))
	 (at ?a ?c2)
	 (increase (total-fuel-used)
	  (* (distance ?c1 ?c2) (fast-burn ?a)))
	 (decrease (fuel ?a) 
	  (* (distance ?c1 ?c2) (fast-burn ?a)))
	 )
    ) 

    (:action refuel	
     :parameters (?a - aircraft ?c - city)
     :precondition (and (> (capacity ?a) (fuel ?a))
	 (at ?a ?c)
	 )
     :effect (and (assign (fuel ?a) (capacity ?a)))
    )


    (:task transport-person
     :parameters (?p - person ?cd -city)
     (:method case1
      ;;La persona ya se encuentra en su ciudad destino
      :precondition (at ?p ?cd)
      :tasks ()
     )
     (:method case2
      ;; La persona no se encuntra en su ciudad destino
      ;; El avi�n y la persona se encuentran en la misma ciudad
      :precondition (:sortby ?num :desc
	  (and (at ?p ?co)
	   (different ?cd ?co)
	   (at ?a - aircraft ?co)
	   (bind ?num (onboard ?a))))
      :tasks (
	  (:inline () (dest ?a ?co))
	  !(board ?p ?a ?cd)
	  !(board-rest ?a ?co ?cd)
	  !(:inline () (dest ?a ?cd))
	  !(upper-move-aircraft-no-style ?a ?cd)
	  !(debark ?p ?a ?cd)
	  !(debark-rest ?a ?cd)
	  !(:inline () (not (dest ?a ?x))))
     )
     (:method case3
      ;; Ni la persona ni el avi�n se encuentran en la misma ciudad
      :precondition (:sortby ?cost :asc
	  (and (at ?p ?cp)
	   (different ?cd ?cp)
	   (at ?a -aircraft ?ca)
	   (different ?cp ?ca)
	   (forall (?c - city) (imply (dest ?a ?c) (same ?c ?cp)))
	   ;; En la ciudad donde se encuentra el avi�n no hay ninguna persona esperando
	   ;; desplazarse
	   (imply (different ?cp ?ca) (not (possible-person-in ?ca)))
	   (travel-cost-info ?a ?ca ?cp ?cost ?style)
	  ))
      :tasks (
	  (:inline () (dest ?a ?cp))
	  !(upper-move-aircraft ?a ?cp ?style)
	  !(board ?p ?a ?cp)
	  !(board-rest ?a ?cp ?cd)
	  !(:inline () (dest ?a ?cd))
	  !(upper-move-aircraft-no-style ?a ?cd)
	  !(debark ?p ?a ?cd)
	  !(debark-rest ?a ?cd)
	  !(:inline () (not (dest ?a ?x))))
     )
     )

    (:task upper-move-aircraft
     :parameters(?a -aircraft ?cd -city ?style - moving-style)
     (:method case1
      ;; El avi�n ya est� en la ciudad que le corresponde
      :precondition (at ?a ?cd)
      :tasks ()
     )
     (:method case2
      ;; El avi�n no est� en la ciudad que le corresponde
      :precondition (and
	  (at ?a ?co)
	  (different ?c ?co))
      :tasks 
      (move-aircraft ?a ?co ?cd ?style)
     )
    )

    (:task upper-move-aircraft-no-style
     :parameters (?a -aircraft ?cd - city)
     (:method case1
      :precondition (at ?a ?cd)
      :tasks ()
     )
     (:method case2
      :precondition (:sortby ?cost :asc
	  (and (at ?a ?co)
	   (different ?co ?cd)
	   (travel-cost-info ?a ?co ?cd ?cost ?style)
	  ))
      :tasks 
      (move-aircraft ?a ?co ?cd ?style)
     )
    )

    (:task move-aircraft
     :parameters (?a -aircraft ?co ?cd -city ?style - moving-style)
     (:method case1
      :precondition (and
	  (bind ?moving-style slow)
	  (> (fuel ?a) (* (slow-burn ?a) (distance ?co ?cd)))
	  )
      :tasks
      (fly ?a ?co ?cd)
     )
     (:method case2
      :precondition (and
	  (bind ?moving-style slow)
	  (<= (fuel ?a) (* (slow-burn ?a) (distance ?co ?cd)))
	  )
      :tasks (
	  (refuel ?a ?co)
	  !(fly ?a ?co ?cd)
	  )
     )
     (:method case3
      :precondition (and
	  (bind ?moving-style fast)
	  (> (fuel ?a) (* (fast-burn ?a) (distance ?co ?cd)))
	  )
      :tasks (
	  (fly ?a ?co ?cd)
	  )
     )
     (:method case4
      :precondition (and
	  (bind ?moving-style fast)
	  (<= (fuel ?a) (* (fast-burn ?a) (distance ?co ?cd)))
	  )
      :tasks (
	  (refuel ?a ?co)
	  !(fly ?a ?co ?cd)
	  )
     )
     )

    (:task transport-aircraft
     :parameters (?a -aircraft ?c -city)
     (:method case1
      :precondition (not (no-use ?a))
      :tasks(
	  (:inline () (no-use ?a))
	  !(upper-move-aircraft-no-style ?a ?c)
	  !(:inline () (not (no-use ?a))
	  )
      )
     )
 )

    (:task board-rest
     :parameters (?a -aircraft ?co -city ?cd -city)
     (!
      (:method iterate
       :precondition (and
	   (at ?p -person ?co)
	   (goal ?p -person ?pcd)
	   (< (distance ?cd ?pcd) (distance ?co ?pcd))
	   )
       :tasks(
	   (board ?p ?a ?cp)
	   !(board-rest ?a ?co ?cd)
	   )
      )
      (:method base
       :precondition ()
       :tasks ()
      )
     )
    )

    (:task debark-rest
     :parameters (?a -aircraft ?cd -city)
     (!
      (:method iterate
       :precondition
       (in ?p -person ?a)
       :tasks(
	   (debark ?p ?a ?cd)
	   !(debark-rest ?a ?cd)
	   )
      )
      (:method base
       :precondition ()
       :tasks ()
      )
     )
    )
 )