
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PPDL domain for a VGDL game
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame)  
	(:requirements
		; Available in FD
		; ":strips", ":adl", ":typing", ":negation", ":equality",
		; ":negative-preconditions", ":disjunctive-preconditions",
		; ":existential-preconditions", ":universal-preconditions",
		; ":quantified-preconditions", ":conditional-effects",
		; ":derived-predicates", ":action-costs"
        
        :adl 
        :negative-preconditions
	)

	; Types ---------------------------------------------------------------------

	(:types
		floor - Immovable
		hole - Immovable
		avatar - MovingAvatar
		box - Passive
		wall - Immovable
		Passive MovingAvatar Immovable - Object
	)

	; Constants -----------------------------------------------------------------

	; (:constants
	; )

	; Predicates ----------------------------------------------------------------

	(:predicates
		(oriented-up ?o - Object)
		(oriented-down ?o - Object)
		(oriented-left ?o - Object)
		(oriented-right ?o - Object)
		(can-move-up ?a - MovingAvatar)
		(can-move-down ?a - MovingAvatar)
		(can-move-left ?a - MovingAvatar)
		(can-move-right ?a - MovingAvatar)

        ; Auxiliary predicates to maintain order between tasks
        (turn-avatar)
        (turn-sprites)
		; (turn-sprite1)
		; (turn-sprite2)
        (turn-evaluate-interactions)

		; For tile connections
		(connected-up ?f1 ?f2 - floor)
		(connected-down ?f1 ?f2 - floor)
		(connected-right ?f1 ?f2 - floor)
		(connected-left ?f1 ?f2 - floor)

		(at ?f - floor ?o - Object)
		(last-at ?f - floor ?o - Object)

		; To force undo-all
		(undo-all)
	)

	; Turn tasks ---------------------------------------------------------------
  
	
    (:action Turn-sprites
        :parameters ()
        :precondition (and 
            (not (turn-avatar))
        )
        :effect (and 
            (turn-sprites)

			; (turn-sprite1)
			; (turn-sprite2)
			; (turn-sprite3)
        )
    )

	
    (:action End-Turn-sprites
        :parameters ()
        :precondition (and
			(turn-sprites) 
            ; (not (turn-sprite1))
			; (not (turn-sprite2))
			; (not (turn-sprite3))
        )
        :effect (and 
            (not (turn-sprites))
        )
    )

	
    (:action Turn-interactions
        :parameters ()
        :precondition (and 
            (not (turn-avatar))
            (not (turn-sprites))
        )
        :effect (and 
            (turn-evaluate-interactions)
        )
    )
	
	(:action Stop-interactions
		:parameters ()
		:precondition (and 
			(turn-evaluate-interactions)

			(not 
				(exists (?x - Object ?y - Object ?f - floor) 
					(and
						(not (= ?x ?y))
						(at ?f ?x)
						(at ?f ?y)
					)
				)
			)

			; (not 
			; 	(exists (?x - MovingAvatar ?y - box ?f - floor) 
			; 		(and
			; 			; (not (= ?x ?y))
			; 			(at ?f ?x)
			; 			(at ?f ?y)
			; 		)
			; 	)
			; )

			; (not 
			; 	(exists (?x - box ?y - box ?f - floor) 
			; 		(and
			; 			(not (= ?x ?y))
			; 			(at ?f ?x)
			; 			(at ?f ?y)
			; 		)
			; 	)
			; )

			; (not 
			; 	(exists (?x - wall ?y - box ?f - floor) 
			; 		(and
			; 			; (not (= ?x ?y))
			; 			(at ?f ?x)
			; 			(at ?f ?y)
			; 		)
			; 	)
			; )

			; (not 
			; 	(exists (?x - hole ?y - box ?f - floor) 
			; 		(and
			; 			; (not (= ?x ?y))
			; 			(at ?f ?x)
			; 			(at ?f ?y)
			; 		)
			; 	)
			; )
		)
		:effect (and 
			; Restart turn
            (turn-avatar)
            (not (turn-sprites))
			(not (turn-evaluate-interactions))
		)
	)

	(:action undo-all
		:parameters ()
		:precondition (and 
			(undo-all)
		)
		:effect (and 
			(not (undo-all))
			; Restart turn
            (turn-avatar)
            (not (turn-sprites))
			(not (turn-evaluate-interactions))
		)
	)

    ; ==========================================================================
	
	; Actions -------------------------------------------------------------------
  
	(:action AVATAR_MOVE_UP
		:parameters (?a - MovingAvatar ?f_actual - floor ?f_last - floor ?f_next - floor)
		:precondition (and 
                        (turn-avatar)

						(can-move-up ?a)
						(oriented-up ?a)
						(at ?f_actual ?a)
						(last-at ?f_last ?a)
						(connected-up ?f_actual ?f_next)
					)
		:effect (and 
					(not (last-at ?f_last ?a))
					(last-at ?f_actual ?a)

					(not (at ?f_actual ?a))
					(at ?f_next ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_MOVE_DOWN
		:parameters (?a - MovingAvatar ?f_actual - floor ?f_last - floor ?f_next - floor)
		:precondition (and 
                        (turn-avatar)

						(can-move-down ?a)
						(oriented-down ?a)
						(at ?f_actual ?a)
						(last-at ?f_last ?a)
						(connected-down ?f_actual ?f_next)
					)
		:effect (and 
					(not (last-at ?f_last ?a))
					(last-at ?f_actual ?a)

					(not (at ?f_actual ?a))
					(at ?f_next ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_MOVE_LEFT
		:parameters (?a - MovingAvatar ?f_actual - floor ?f_last - floor ?f_next - floor)
		:precondition (and 
                        (turn-avatar)

						(can-move-left ?a)
						(oriented-left ?a)
						(at ?f_actual ?a)
						(last-at ?f_last ?a)
						(connected-left ?f_actual ?f_next)
					)
		:effect (and 
					(not (last-at ?f_last ?a))
					(last-at ?f_actual ?a)

					(not (at ?f_actual ?a))
					(at ?f_next ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_MOVE_RIGHT
		:parameters (?a - MovingAvatar ?f_actual - floor ?f_last - floor ?f_next - floor)
		:precondition (and 
                        (turn-avatar)

						(can-move-right ?a)
						(oriented-right ?a)
						(at ?f_actual ?a)
						(last-at ?f_last ?a)
						(connected-right ?f_actual ?f_next)
					)
		:effect (and 
					(not (last-at ?f_last ?a))
					(last-at ?f_actual ?a)

					(not (at ?f_actual ?a))
					(at ?f_next ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_TURN_UP
		:parameters (?a - MovingAvatar )
		:precondition (and 
						(not (oriented-up ?a))

						
                        (turn-avatar)
					)
		:effect (and 
					
                    (when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )
					
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )
					
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )
					(oriented-up ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_TURN_DOWN
		:parameters (?a - MovingAvatar )
		:precondition (and 
						(not (oriented-down ?a))

						
                        (turn-avatar)
					)
		:effect (and 					
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )
					
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )
					
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )
					(oriented-down ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_TURN_LEFT
		:parameters (?a - MovingAvatar )
		:precondition (and 
                        (turn-avatar)
						(not (oriented-left ?a))
					)
		:effect (and 
					
                    (when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )
					
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )
					
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )
					(oriented-left ?a)

                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_TURN_RIGHT
		:parameters (?a - MovingAvatar )
		:precondition (and 
                        (turn-avatar)
						(not (oriented-right ?a))
					)
		:effect (and
                    (when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )
					
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )
					
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )
					(oriented-right ?a)

					
                    (not (turn-avatar))
					(turn-sprites)
				)
	)

	(:action AVATAR_NIL
		:parameters (?a - MovingAvatar)
		:precondition (and 						
                        (turn-avatar)
					)
		:effect (and
                	(not (turn-avatar))
			    	(turn-sprites)
				)
	)


	; --------------------------------------------------------------------------


	; Immovable ?? Es por su tipo ?
	(:action AVATAR_WALL_STEPBACK
		:parameters (?x - avatar ?y - wall ?f_actual - floor ?f_last - floor)
		:precondition (and
						(turn-evaluate-interactions)
						(not (= ?x ?y))

						(at ?f_actual ?x)
						(at ?f_actual ?y)
						(last-at ?f_last ?x)
					)
		:effect (and 
					(not (at ?f_actual ?x))
					(at ?f_last ?x)
				)
	)

	; (:action BOX_AVATAR_BOUNCEFORWARD
	; 	:parameters (?x - box ?y - MovingAvatar ?f_actual ?f_north ?f_south ?f_east ?f_west ?f_last - floor)
	; 	:precondition (and
	; 					(turn-evaluate-interactions)
	; 					(not (= ?x ?y))

	; 					(at ?f_actual ?x)
	; 					(at ?f_actual ?y)
	; 					(last-at ?f_last ?x)

	; 					(connected-up ?f_actual ?f_north)
	; 					(connected-down ?f_actual ?f_south)
	; 					(connected-left ?f_actual ?f_west)
	; 					(connected-right ?f_actual ?f_east)
	; 				)
	; 	:effect (and 					
	; 				(when (oriented-up ?y)
	; 					(at ?f_north ?x)
	; 				)
	; 				(when (oriented-down ?y)
	; 					(at ?f_south ?x)
	; 				)
	; 				(when (oriented-left ?y)
	; 					(at ?f_west ?x)
	; 				)
	; 				(when (oriented-right ?y)
	; 					(at ?f_east ?x)
	; 				)
	; 				(not (at ?f_actual ?x))
	; 				(not (at ?f_last ?x))
	; 				(last-at ?f_actual ?x)
	; 			)
	; )

	(:action BOX_AVATAR_BOUNCEFORWARD_UP
		:parameters (?x - box ?y - MovingAvatar ?f_actual ?f_north ?f_last - floor)
		:precondition (and
						(turn-evaluate-interactions)
						(not (= ?x ?y))

						(oriented-up ?y)

						(at ?f_actual ?x)
						(at ?f_actual ?y)
						(last-at ?f_last ?x)

						(connected-up ?f_actual ?f_north)
					)
		:effect (and 					
					(at ?f_north ?x)

					(not (at ?f_actual ?x))
					(not (at ?f_last ?x))
					(last-at ?f_actual ?x)

					
				)
	)

	(:action BOX_AVATAR_BOUNCEFORWARD_DOWN
		:parameters (?x - box ?y - MovingAvatar ?f_actual ?f_south ?f_last - floor)
		:precondition (and
						(turn-evaluate-interactions)
						(not (= ?x ?y))

						(oriented-down ?y)

						(at ?f_actual ?x)
						(at ?f_actual ?y)
						(last-at ?f_last ?x)

						(connected-down ?f_actual ?f_south)
					)
		:effect (and 					
					(at ?f_south ?x)

					(not (at ?f_actual ?x))
					(not (at ?f_last ?x))
					(last-at ?f_actual ?x)
				)
	)

	(:action BOX_AVATAR_BOUNCEFORWARD_LEFT
		:parameters (?x - box ?y - MovingAvatar ?f_actual ?f_west ?f_last - floor)
		:precondition (and
						(turn-evaluate-interactions)
						(not (= ?x ?y))

						(oriented-left ?y)

						(at ?f_actual ?x)
						(at ?f_actual ?y)
						(last-at ?f_last ?x)

						(connected-left ?f_actual ?f_west)
					)
		:effect (and 					
					(at ?f_west ?x)

					(not (at ?f_actual ?x))
					(not (at ?f_last ?x))
					(last-at ?f_actual ?x)

					
				)
	)

	(:action BOX_AVATAR_BOUNCEFORWARD_RIGHT
		:parameters (?x - box ?y - MovingAvatar ?f_actual ?f_east ?f_last - floor)
		:precondition (and
						(turn-evaluate-interactions)
						(not (= ?x ?y))

						(oriented-right ?y)

						(at ?f_actual ?x)
						(at ?f_actual ?y)
						(last-at ?f_last ?x)

						(connected-right ?f_actual ?f_east)
					)
		:effect (and 					
					(at ?f_east ?x)

					(not (at ?f_actual ?x))
					(not (at ?f_last ?x))
					(last-at ?f_actual ?x)

					
				)
	)

	; WHY IMMOVABLE AND NOT WALL
	; (:action BOX_WALL_UNDOALL
	; 	:parameters (?x - box ?y - wall ?f_actual - floor)
	; 	:precondition (and
	; 					(turn-evaluate-interactions)
	; 					(not (= ?x ?y))

	; 					(at ?f_actual ?x)
	; 					(at ?f_actual ?y)
	; 				)
	; 	:effect (and
	; 				(forall (?o - Object ?f ?f2 - floor)
	; 					(when (and (at ?f ?o) (last-at ?f2 ?o))
	; 						(and
	; 							(not (at ?f ?o))
	; 							(at ?f2 ?o)
	; 						)
	; 					)
	; 				)
					
	; 				(undo-all)
	; 			)
	; )

	
	; Make at = last-at && ?force new turn?
	; (:action BOX_BOX_UNDOALL
	; 	:parameters (?x - box ?y - Passive ?f_actual - floor)
	; 	:precondition (and
	; 					(turn-evaluate-interactions)
	; 					(not (= ?x ?y))

	; 					(at ?f_actual ?x)
	; 					(at ?f_actual ?y)
	; 				)
	; 	:effect (and
	; 				(forall (?o - Object ?f ?f2 - floor)
	; 					(when (and (at ?f ?o) (last-at ?f2 ?o))
	; 						(and
	; 							(not (at ?f ?o))
	; 							(at ?f2 ?o)
	; 						)
	; 					)
	; 				)
					
	; 				(undo-all)
	; 			)
	; )

	(:action BOX_HOLE_KILLSPRITE
		:parameters (?x - box ?y - Immovable ?f_actual - floor)
		:precondition (and
						(turn-evaluate-interactions)
						(not (= ?x ?y))

						(at ?f_actual ?x)
						(at ?f_actual ?y)
					)
		:effect (and 
					(not (at ?f_actual ?x))
				)
	)
)