;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Dominio HPDL hecho a mano para generar las mismas acciones que Vladis
;; 
;; ----------------------------------------------------------------------------
;; Dudas:
;; - Cómo ver los valores de las funciones al final de la ejecución del 
;: planificador. Ahora mismo estoy usando print para ver las acciones
;;
;; - Documentación HPDL página 12: ¿Qué implica el '!'? -> Corte, hace que se 
;; olviden el resto de unificaciones. Se puede usar en métodos y precondiciones
;; ----------------------------------------------------------------------------
;;
;; Notas:
;; - Puedo producir las mismas acciones que Vladis pero sin heurística no creo
;; que forme ningún plan eficiente, ya que realizará acciones de forma aleatoria.
;; Sería necesario poder usar objetivos de PDDL o dirigir el orden de los métodos
;; en base a una heurística.
;;
;; - Saber qué casillas están conectadas no es necesario, si un movimiento no es 
;; posible se indica en una interacción (los muros en general hacen undoAll).
;; 
;; Vladis lo usa para indicar en qué casilla se situa un sprite. Si HPDL acepta 
;; incrementos con flotantes podríamos explicar movimientos como el de las rocas 
;; con functions (ya que se mueven a 0.2 casillas por turno)
;;
;; - De la misma manera tampoco podemos mirar el tipo de terreno si queremos 
;; generalizar, en otros juegos no merece la pena averiguar sobre qué casillas 
;; se puede caminar y cuáles no (por el motivo de las interacciones).
;;
;; - Las acciones de "dig-..." se corresponderían con ACTION_USE en la casilla 
;; hacia la que está orientado
;;
;; - "exit-level" solo indica que el avatar está sobre la casilla de salida
;;
;; - "get-gem" no se incluye ya que se recoge automáticamente en base a la
;; interacción
;;
;; ----------------------------
;;
;; - No recordaba que el tipo object ya estaba definido en HPDL, creo que no va
;; a afectar, pero en cualquier caso lo anoto por si es necesario cambiarle el 
;; nombre	
;;
;; - Se pueden usar scripts de Python (ver documentación), considerarlo como
;; último recurso para ciertos problemas. (Solo para functions)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame) 
    ; No todos los requisitos son necesarios por ahora, revisar
	(:requirements
		:derived-predicates
		:universal-preconditions
		:disjuntive-preconditions

		; Necesarios
		:conditional-effects
		:equality
		:fluents
		:htn-expansion
		:negative-preconditions
		:typing
		:existential-preconditions
	)	

	; Types -----------------------------------------------------------------

    ; Un tipo Object (objeto genérico), otro para cada 
    ; sprite definido y otro para cada tipo de sprite declarado
	(:types
		; FALTA EN EL PARSER DECLARAR MOVING, AQUELLOS SPRITES INTERMEDIOS EN LA JERARQUÍA		
		ShootAvatar RandomNPC - moving	
		moving Immovable Flicker Resource Door Missile - Object

		avatar - ShootAvatar
		background - Immovable
		boulder - Missile
		butterfly - enemy	
		crab - enemy
		diamond - Resource
		dirt - Immovable
		enemy - RandomNPC
		exitdoor - Door
		sword - Flicker
		wall - Immovable
	)

	; Constants -----------------------------------------------------------------

	; Predicates ----------------------------------------------------------------

	(:predicates
        ; Todos los objetos pueden estar orientados (avatares, misiles, enemigos...)
		(orientation-up ?s - Object)
		(orientation-down ?s - Object)
		(orientation-left ?s - Object)
		(orientation-right ?s - Object)


        ; Predicados para cada dirección posible en la que se puede mover (depende
        ; del tipo de avatar)
		(can-move-up ?a - ShootAvatar)
		(can-move-down ?a - ShootAvatar)
		(can-move-left ?a - ShootAvatar)
		(can-move-right ?a - ShootAvatar)

        ; Otro para indicar que el avatar puede cambiar de orientación (si no está
        ; definido el avatar debe tener una orientación, que será fija)
		(can-change-orientation ?a - ShootAvatar)

        ; Otro para indicar que tiene el comando ACTION_USE disponible.
        ; 
        ; Este predicado no es necesario en sí ya que sabemos de antemano que 
        ; ACTION-USE solo se puede usar si es un tipo de avatar concreto. Lo dejo
        ; porque creo que podría existir la posibilidad de que por motivos del 
        ; juego (a la hora de generalizar) el avatar no pueda utilizar este comando
        ; y la comprobación que añade no es grande
		(can-use ?a - ShootAvatar)

		; Para comprobar una interacción
		; Habrá una por cada par de objetos definidos en el problema, y duplicadas
		; (intercambiando el sujeto del predicado)
		(evaluate-interaction ?o1 ?o2 - Object)
		(regenerate-interaction ?o1 ?o2 - Object)

		; For the avatar movement (expert knowledge)
		(diamond_selected ?d - diamond)
		(is_diamond_selected ?a - ShootAvatar)
	)
  
	; Functions -----------------------------------------------------------------

	(:functions
		; For the avatar movement (expert knowledge)
		(diamond_selected_distance)
		(auxiliar_distance)


        ; Coordenadas: Esta función tiene sentido si se puede comprobar que dos
        ; objetos tengan el mismo valor de función, en otro caso se debería utilizar
        ; el predicado (at ...).
        ; 
        ; Sería conveniente evitar este predicado porque forzaría a comprobar que
        ; dos casillas sean adyacentes (cosa que GVGAI no hace). Es mejor comprobar
        ; que dos objetos hayan colisionado (y esto habrá que hacerlo tarde o
        ; temprano)
		(coordinate_x ?o - Object)
		(coordinate_y ?o - Object)
		(last_coordinate_x ?o - Object)
		(last_coordinate_y ?o - Object)

        ; Debe haber un contador por cada recurso (en este caso uno)
		(resource_diamond ?a - avatar)

        ; Esto no es necesario por ahora, ya que serviría para representar objetivos
        ; finales como los declarados por VGDL

		; ¿Que los básicos se calculen aquí y el resto sean derived?
		; Habría problemas si se actualiza uno de los deried en alguna acción,
		; mejor tenerlos todos en cuenta en cada acción (la jerarquía hacia arriba)
		(counter_dirt)
		(counter_Object)
		(counter_sword)
		(counter_enemy)
		(counter_ShootAvatar)
		(counter_Immovable)
		(counter_boulder)
		(counter_background)
		(counter_Flicker)
		(counter_Door)
		(counter_avatar)
		(counter_diamond)
		(counter_exitdoor)
		(counter_butterfly)
		(counter_wall)
		(counter_crab)
		(counter_Resource)
		(counter_Missile)
		(counter_RandomNPC)
		(counter_moving)

		; Para llevar la cuenta de los turnos
		(turn)
	)

	; Tasks ---------------------------------------------------------------------
    
    ; Método principal para representar un turno en el juego
	(:task Turn
		:parameters ()

		; Lo suyo sería poner en la precondición el objetivo final del
		; juego, teniendo varios de estos métodos si hay varios criterios de 
		; terminación definidos
		(:method finish_game
			:precondition (= (resource_diamond ?a - avatar) 1)
			; :precondition (= (coordinate_y ?a - avatar) 1)
			; :precondition (= (turn) 2)
			:tasks ()		
		)

		(:method turn
				:precondition (
								)
				:tasks ( 
							(turn_avatar ?a - ShootAvatar ?p - sword) 
							(turn_objects)
                            (check-interactions)
							(create-interactions)

							(:inline () (increase (turn) 1))
							(Turn) ; Para que el planificador no realice un solo turno
						)
		)


		; Si el turno no se ha podido completar (al 100%%), pasamos al siguiente.
		; Ahora mismo se quedaría atascado ya que no habría ningún cambio, el
		; objetivo es que turn aplique algún efecto (ya sea el avatar o algún
		; otro movimiento) que haga que el juego no cicle

		; Esta implementación no haría nada
		; (:method turn_undone
		; 	:precondition ()
		; 	:tasks (
		; 		; (Turn)
		; 	)
		; )
	)

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

	; Choose the diamond at the shortest distance
	(:task select_diamond
		:parameters (?a - ShootAvatar)

		; (:method end_loop
		; 	:precondition(and (is_diamond_selected ?a) 
		; 				(not (evaluate-interaction ?a - ShootAvatar ?d - diamond))
		; 				(not (= (coordinate_x ?diam) -1))
		; 	)
		; 	:tasks ()
		; )

		(:method loop
			:precondition (and
				(is_diamond_selected ?a)
				
				; Trick to get an instance of a diamond without
				; creating additional predicates
				(evaluate-interaction ?a - ShootAvatar ?diam - diamond)
				(not (= (coordinate_x ?diam) -1))

				(diamond_selected ?original - diamond)
				; (regenerate-interaction ?a - ShootAvatar ?original - diamond)
			)
			:tasks (
				; Calculate distance
				(:inline
					()
					(assign (auxiliar_distance) 0)
				)

				; (:inline 
				; 	()
				; 	(forall (?diam - diamond)
				; 		(when
				; 			(not (= (coordinate_x ?diam) -1))
				; 			(and 
				; 				(when 
				; 					(<= (coordinate_x ?a ) (coordinate_x ?diam))
				; 					(increase (auxiliar_distance)
				; 							(- (coordinate_x ?diam) (coordinate_x ?a))									  
				; 					)
				; 				)
				; 				(when 
				; 					(> (coordinate_x ?a ) (coordinate_x ?diam))
				; 					(increase (auxiliar_distance) (- (coordinate_x ?a) (coordinate_x ?diam)))
				; 				)
				; 				(when 
				; 					(<= (coordinate_y ?a ) (coordinate_y ?diam))
				; 					(increase (auxiliar_distance) (- (coordinate_y ?diam) (coordinate_y ?a)))
				; 				)
				; 				(when 
				; 					(> (coordinate_y ?a ) (coordinate_y ?diam))
				; 					(increase (auxiliar_distance) (- (coordinate_y ?a) (coordinate_y ?diam)))
				; 				)					
				; 			)
				; 		)
				; 	)
				; )

				(:inline 
					()					
					(and 
						(when 
							(<= (coordinate_x ?a ) (coordinate_x ?diam))
							(increase (auxiliar_distance)
									(- (coordinate_x ?diam) (coordinate_x ?a))									  
							)
						)
						(when 
							(> (coordinate_x ?a ) (coordinate_x ?diam))
							(increase (auxiliar_distance) (- (coordinate_x ?a) (coordinate_x ?diam)))
						)
						(when 
							(<= (coordinate_y ?a ) (coordinate_y ?diam))
							(increase (auxiliar_distance) (- (coordinate_y ?diam) (coordinate_y ?a)))
						)
						(when 
							(> (coordinate_y ?a ) (coordinate_y ?diam))
							(increase (auxiliar_distance) (- (coordinate_y ?a) (coordinate_y ?diam)))
						)					
					)
				)

				; Check if distance is lower than selected one
				(:inline
					()
					(when
						(< (auxiliar_distance) (diamond_selected_distance))
						(and
							(not (diamond_selected ?original))
							(diamond_selected ?diam)
							(assign (diamond_selected_distance) (auxiliar_distance))							
						)
					)
				)

				; Iterate
				(:inline () (not (evaluate-interaction ?a ?diam)))
				(:inline () (regenerate-interaction ?a ?diam))
				(select_diamond ?a)				
			)
		)

		; No diamond selected yet, or it has been picked (CHANGE ACTION TOO)
		(:method choose_anyone
			:precondition (and 
								(not (is_diamond_selected ?a))

								; Trick to get an instance of a diamond without
								; creating additional predicates
								(evaluate-interaction ?a - ShootAvatar ?diam - diamond)

								(not (= (coordinate_x ?diam) -1))
			)
			:tasks (
				; Calculate distance - MAYBE IN DERIVED ?
				; (:inline (:print "No hay ningundo definido aun\n") ())
				; (:inline (:print (coordinate_x ?diam)) ())
				(:inline
					()
					(assign (auxiliar_distance) 0)
				)

				(:inline 
					()
					(and 
						(when 
							(<= (coordinate_x ?a ) (coordinate_x ?diam))
							(increase (auxiliar_distance)
									  (- (coordinate_x ?diam) (coordinate_x ?a))									  
							)
						)
						(when 
							(> (coordinate_x ?a ) (coordinate_x ?diam))
							(increase (auxiliar_distance) (- (coordinate_x ?a) (coordinate_x ?diam)))
						)
						(when 
							(<= (coordinate_y ?a ) (coordinate_y ?diam))
							(increase (auxiliar_distance) (- (coordinate_y ?diam) (coordinate_y ?a)))
						)
						(when 
							(> (coordinate_y ?a ) (coordinate_y ?diam))
							(increase (auxiliar_distance) (- (coordinate_y ?a) (coordinate_y ?diam)))
						)					
					)
				)

				; Assign diamond
				(:inline
					()
					(and					
						(is_diamond_selected ?a)
						(diamond_selected ?diam)
						(assign (diamond_selected_distance) (auxiliar_distance))

						(not (evaluate-interaction ?a ?diam))
						(regenerate-interaction ?a ?diam)
					)
				)
				; (:inline (:print "Hecho\n") ())

				; Loop
				(select_diamond ?a)
			)
		)

		(:method base_case
			:precondition()
			:tasks ()
		)
	)

	; -------------------------------------------------------------------------

	; Move no matter what
	(:task avatar_force_move
		:parameters (?a - ShootAvatar)

		(:method avatar_move_up
				:precondition (orientation-up ?a)
				:tasks ((AVATAR_MOVE_UP ?a))
		)

		(:method avatar_move_down
				:precondition (orientation-down ?a)
				:tasks ((AVATAR_MOVE_DOWN ?a))
		)

		(:method avatar_move_left
				:precondition (orientation-left ?a)
				:tasks ((AVATAR_MOVE_LEFT ?a))
		)

		(:method avatar_move_right
				:precondition (orientation-right ?a)
				:tasks ((AVATAR_MOVE_RIGHT ?a))
		)
	)

	; -------------------------------------------------------------------------

	; -------------------------------------------------------------------------

	(:task move_torward_no_turn
		:parameters (?a - ShootAvatar)

		(:method move_up
			:precondition(and 
				(orientation-up ?a)
				(not (and
						(= (coordinate_x ?a) (coordinate_x ?w - wall))
						(= (- (coordinate_y ?a) 1) (coordinate_y ?w - wall))
				))
			)
			:tasks (
				(AVATAR_MOVE_UP ?a)
			)
		)

		(:method move_down
			:precondition(and 
				(orientation-down ?a)
				(not (and
						(= (coordinate_x ?a) (coordinate_x ?w - wall))
						(= (+ (coordinate_y ?a) 1) (coordinate_y ?w - wall))
				))
			)
			:tasks (
				(AVATAR_MOVE_DOWN ?a)
			)
		)

		(:method move_left
			:precondition(and 
				(orientation-left ?a)
				(not (and
						(= (- (coordinate_x ?a) 1) (coordinate_x ?w - wall))
						(= (coordinate_y ?a) (coordinate_y ?w - wall))
				))
			)
			:tasks (
				(AVATAR_MOVE_LEFT ?a)
			)
		)

		(:method move_right
			:precondition(and 
				(orientation-right ?a)
				(not (and
						(= (+ (coordinate_x ?a) 1) (coordinate_x ?w - wall))
						(= (coordinate_y ?a) (coordinate_y ?w - wall))
				))
			)
			:tasks (
				(AVATAR_MOVE_RIGHT ?a)
			)
		)
	)

	; -------------------------------------------------------------------------

	(:task move_torward_diamond
		:parameters (?a - ShootAvatar)
		
		(:method no_need_to_turn
			:precondition ()
			:tasks (
				(move_torward_no_turn ?a)
			)
		)

		; The diamond is going up and no wall directly above 
		; (no need to check for enemies or boulder)
		(:method need_turn_up
			:precondition (and
				(diamond_selected ?d)
				(> (coordinate_y ?a) (coordinate_y ?d))
				; ESTO FALLA
				; (not (and
				; 		(= (coordinate_x ?a) (coordinate_x ?w - wall))
				; 		(= (- (coordinate_y ?a) 1) (coordinate_y ?w - wall))
				; ))
			)
			:tasks (
				(AVATAR_TURN_UP ?a)
			)
		)

		(:method need_turn_down
			:precondition (and
				(diamond_selected ?d)
				(< (coordinate_y ?a) (coordinate_y ?d))
				; (not (and
				; 		(= (coordinate_x ?a) (coordinate_x ?w - wall))
				; 		(= (+ (coordinate_y ?a) 1) (coordinate_y ?w))
				; ))
			)
			:tasks (
				(AVATAR_TURN_DOWN ?a)
			)
		)

		(:method need_turn_left
			:precondition (and
				(diamond_selected ?d)
				(> (coordinate_x ?a) (coordinate_x ?d))
				; (not (and
				; 		(= (- (coordinate_x ?a) 1) (coordinate_x ?w - wall))
				; 		(= (coordinate_y ?a) (coordinate_y ?w - wall))
				; ))
			)
			:tasks (
				(AVATAR_TURN_LEFT ?a)
			)
		)

		(:method need_turn_right
			:precondition (and
				(diamond_selected ?d - diamond)
				(< (coordinate_x ?a) (coordinate_x ?d))
				; (not (and
				; 		(= (+ (coordinate_x ?a) 1) (coordinate_x ?w - wall))
				; 		(= (coordinate_y ?a) (coordinate_y ?w - wall))
				; ))
			)
			:tasks (
				(AVATAR_TURN_RIGHT ?a)
			)
		)
	)

	; -------------------------------------------------------------------------

	(:task turn_avatar
		:parameters (?a - ShootAvatar ?p - sword)

		; If no diamond is selected, do it
		(:method select_objective
			; :precondition(not (diamond_selected ?d - diamond))
			:precondition(not (is_diamond_selected ?a))
			:tasks(				
				(select_diamond ?a)
				; (:inline (:print (diamond_selected ?d - diamond)) ())
				(choose_action ?a ?p)
				(create-interactions)
			)
		)

		(:method objective_selected
			:precondition(is_diamond_selected ?a)
			:tasks(				
				(choose_action ?a ?p)
			)
		)
	)

	(:task choose_action
		:parameters (?a - ShootAvatar ?p - sword)
		(:method boulder_up
			; There is a boulder over the avatar
			:precondition(and
				(= (coordinate_x ?d - boulder) (coordinate_x ?a))
				(= (coordinate_y ?d - boulder) (- (coordinate_y ?a) 1))
			)
			:tasks (
				(avatar_force_move ?a)
			)
		)
		
		; (:method enemy_at_1
		; 	:precondition ()
		; 	:tasks (
		; 		(evade_enemy_at_1)
		; 	)
		; )

		; (:method enemy_at_2
		; 	:precondition ()
		; 	:tasks (
		; 		(evade_enemy_at_2)
		; 	)
		; )

		(:method move_torward_diamond
			:precondition ()
			:tasks (
				(move_torward_diamond ?a)
			)
		)

		; WHEN TO USE FLICKER ??

		(:method avatar_nil
				:precondition ()
				:tasks ((AVATAR_NIL ?a))
		)
	)

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

    ; ; Para representar el turno del avatar, tiene un método por cada acción,
    ; ; que podrían ser ordenados en base a una heurística, y acabando con un
    ; ; método para ACTION_NIL, en caso de que no se pueda realizar ningún otro
	; (:task turn_avatar
    ;     ; Recibe al avatar, y en el caso de que pueda usar
    ;     ; ACTION_USE, el sprite que genera
	; 	:parameters (?a - ShootAvatar ?p - sword)

    ;     ; Los métodos no tienen precondiciones, la posibilidad de realizarlos
    ;     ; se comprueba dentro de la acción
	; 	(:method avatar_move_up
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_MOVE_UP ?a) 
	; 					)
	; 	)

	; 	(:method avatar_move_down
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_MOVE_DOWN ?a) 
	; 					)
	; 	)

	; 	(:method avatar_move_left
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_MOVE_LEFT ?a) 
	; 					)
	; 	)

	; 	(:method avatar_move_right
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_MOVE_RIGHT ?a) 
	; 					)
	; 	)

	; 	(:method avatar_turn_up
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_TURN_UP ?a) 
	; 					)
	; 	)

	; 	(:method avatar_turn_down
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_TURN_DOWN ?a) 
	; 					)
	; 	)

	; 	(:method avatar_turn_left
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_TURN_LEFT ?a) 
	; 					)
	; 	)

	; 	(:method avatar_turn_right
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_TURN_RIGHT ?a) 
	; 					)
	; 	)

	; 	(:method avatar_use
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_USE ?a ?p) 
	; 					)
	; 	)

	; 	(:method avatar_nil
	; 			:precondition (
	; 							)
	; 			:tasks ( 
	; 						(AVATAR_NIL ?a) 
	; 					)
	; 	)
	; )

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

	; Llama a cada acción posible de un objeto que comprueba si se puede realizar
	; En caso de que no funcione seguir la implementación de check-interactions
	(:task turn_objects
		:parameters ()

		(:method turn
			:precondition ()
			:tasks (
						; Como sabemos que hay una roca, ver si se puede mover
						(MISSILE_FALL)

						; Los objetos con movimientos no determinista (ej: enemigos) 
						; no tiene sentido actualizarlos (no sin planifiación 
						; probabilística)
					)
		)
	)

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

	(:task create-interactions
		:parameters ()

		(:method create
			:precondition (regenerate-interaction ?o1 ?o2)
			:tasks (
				(:inline () (not (regenerate-interaction ?o1 ?o2)))
				(:inline () (evaluate-interaction ?o1 ?o2))
			)
		)

		(:method caso_base
			:precondition ()
			:tasks ()
		)
	)

	; Se puede hacer que el UNDOALL sea obligatorio y las de STEPBACK a secas no,
	; por tanto si la primera falla check-interactions no se completa y el 
	; movimiento del avatar y de los objetos tampoco, y si falla la segunda el 
	; juego sigue pero esa interacción no se hace (REALMENTE SE DEBERÍA TENER 
	; ALMACENADA LA POSICIÓN DEL OBJETO ANTERIOR Y COMO EFECTO DEJARLO DONDE ESTABA,
	; ESTO DEBERÍA VOLVER A COMPROBAR SI HAY INTERACCIONES EN SU CASILLA ANTERIOR)
	; TAREA RECURSIVA QUE COMPRUEBE INTERACCIONES

	; CONSIDERAR UNDOALL
	(:task check-interactions
		:parameters ( )

		(:method dirt_avatar_killsprite
			:precondition (and (evaluate-interaction ?dirt - dirt ?shoo - ShootAvatar)
								(not (= (coordinate_x ?dirt) -1))	; Comprobando que los objetos estén en el juego
								(not (= (coordinate_x ?shoo) -1))
							)
			:tasks (
				(DIRT_AVATAR_KILLSPRITE ?dirt ?shoo)				
				(:inline () (not (evaluate-interaction ?dirt ?shoo)))
				(:inline () (regenerate-interaction ?dirt ?shoo))
				(check-interactions)
			)
		)

		(:method dirt_sword_killsprite
			:precondition (and (evaluate-interaction ?dirt - dirt ?sword - sword)
								(not (= (coordinate_x ?dirt) -1))
								(not (= (coordinate_x ?sword) -1))
							)
			:tasks (
				(DIRT_SWORD_KILLSPRITE ?dirt ?sword)
				(:inline () (not (evaluate-interaction ?dirt ?sword)))
				(:inline () (regenerate-interaction ?dirt ?sword))
				(check-interactions)
			)
		)

		(:method diamond_avatar_collectresource
			:precondition (and (evaluate-interaction ?diam - diamond ?avat - avatar)
								(not (= (coordinate_x ?diam) -1))
								(not (= (coordinate_x ?avat) -1))
							)
			:tasks (
				(DIAMOND_AVATAR_COLLECTRESOURCE ?diam ?avat)
				(:inline () (not (evaluate-interaction ?diam ?avat)))
				(:inline () (regenerate-interaction ?diam ?avat))
				(check-interactions)
			)
		)

		(:method moving_wall_stepback
			:precondition (and (evaluate-interaction ?movi - moving ?wall - wall)
								(not (= (coordinate_x ?movi) -1))
								(not (= (coordinate_x ?wall) -1))
							)
			:tasks (
				(MOVING_WALL_STEPBACK ?movi ?wall)
				(:inline () (not (evaluate-interaction ?movi ?wall)))
				(:inline () (regenerate-interaction ?movi ?wall))
				(check-interactions)
			)
		)

		(:method avatar_boulder_killiffromabove
			:precondition (and (evaluate-interaction ?avat - avatar ?boul - boulder)
								(not (= (coordinate_x ?avat) -1))
								(not (= (coordinate_x ?boul) -1))
							)
			:tasks (
				(AVATAR_BOULDER_KILLIFFROMABOVE ?avat ?boul)
				(:inline () (not (evaluate-interaction ?avat ?boul)))
				(:inline () (regenerate-interaction ?avat ?boul))
				(check-interactions)
			)
		)
		
		(:method moving_boulder_stepback
			:precondition (and (evaluate-interaction ?movi - moving ?boul - boulder)
								(not (= (coordinate_x ?movi) -1))
								(not (= (coordinate_x ?boul) -1))
							)
			:tasks (
				(MOVING_BOULDER_STEPBACK ?movi ?boul)
				(:inline () (not (evaluate-interaction ?movi ?boul)))
				(:inline () (regenerate-interaction ?movi ?boul))
				(check-interactions)
			)
		)


		(:method avatar_butterfly_killsprite
			:precondition (and (evaluate-interaction ?avat - avatar ?b - butterfly)
								(not (= (coordinate_x ?avat) -1))
								(not (= (coordinate_x ?b) -1))
							)
			:tasks (
				(AVATAR_BUTTERFLY_KILLSPRITE ?avat ?b)
				(:inline () (not (evaluate-interaction ?avat ?b)))
				(:inline () (regenerate-interaction ?avat ?b))
				(check-interactions)
			)
		)

		(:method avatar_crab_killsprite
			:precondition (and (evaluate-interaction ?avat - avatar ?crab - crab)
								(not (= (coordinate_x ?avat) -1))
								(not (= (coordinate_x ?crab) -1))
							)
			:tasks (
				(AVATAR_CRAB_KILLSPRITE ?avat ?crab)
				(:inline () (not (evaluate-interaction ?avat ?crab)))
				(:inline () (regenerate-interaction ?avat ?crab))
				(check-interactions)
			)
		)

		(:method boulder_dirt_stepback
			:precondition (and (evaluate-interaction ?boul - boulder ?dirt - dirt)
								(not (= (coordinate_x ?boul) -1))
								(not (= (coordinate_x ?dirt) -1))
							)
			:tasks (
				(BOULDER_DIRT_STEPBACK ?boul ?dirt)
				(:inline () (not (evaluate-interaction ?boul ?dirt)))
				(:inline () (regenerate-interaction ?boul ?dirt))
				(check-interactions)
			)
		)

		(:method boulder_wall_stepback
			:precondition (and (evaluate-interaction ?boul - boulder ?wall - wall)
								(not (= (coordinate_x ?boul) -1))
								(not (= (coordinate_x ?wall) -1))
							)
			:tasks (
				(BOULDER_WALL_STEPBACK ?boul ?wall)
				(:inline () (not (evaluate-interaction ?boul ?wall)))
				(:inline () (regenerate-interaction ?boul ?wall))
				(check-interactions)
			)
		)

		(:method boulder_diamond_stepback
			:precondition (and (evaluate-interaction ?boul - boulder ?diam - diamond)
								(not (= (coordinate_x ?boul) -1))
								(not (= (coordinate_x ?diam) -1))
							)
			:tasks (
				(BOULDER_DIAMOND_STEPBACK ?boul ?diam)
				(:inline () (not (evaluate-interaction ?boul ?diam)))
				(:inline () (regenerate-interaction ?boul ?diam))
				(check-interactions)
			)
		)

		(:method boulder_boulder_stepback
			:precondition (and (evaluate-interaction ?boul - boulder ?boul2 - boulder)
								(not (= (coordinate_x ?boul) -1))
								(not (= (coordinate_x ?boul2) -1))
							)
			:tasks (
				(BOULDER_BOULDER_STEPBACK ?boul ?boul2)
				(:inline () (not (evaluate-interaction ?boul ?boul2)))
				(:inline () (regenerate-interaction ?boul ?boul2))
				(check-interactions)
			)
		)

		(:method enemy_dirt_stepback
			:precondition (and (evaluate-interaction ?enem - enemy ?dirt - dirt)
								(not (= (coordinate_x ?enem) -1))
								(not (= (coordinate_x ?dirt) -1))
							)
			:tasks (
				(ENEMY_DIRT_STEPBACK ?enem ?dirt)
				(:inline () (not (evaluate-interaction ?enem ?dirt)))
				(:inline () (regenerate-interaction ?enem ?dirt))
				(check-interactions)
			)
		)

		(:method enemy_diamond_stepback
			:precondition (and (evaluate-interaction ?enem - enemy ?diam - diamond)
								(not (= (coordinate_x ?enem) -1))
								(not (= (coordinate_x ?diam) -1))
							)
			:tasks (
				(ENEMY_DIAMOND_STEPBACK ?enem ?diam)
				(:inline () (not (evaluate-interaction ?enem ?diam)))
				(:inline () (regenerate-interaction ?enem ?diam))
				(check-interactions)
			)
		)

		(:method crab_butterfly_killsprite
			:precondition (and (evaluate-interaction ?crab - crab ?b - butterfly)
								(not (= (coordinate_x ?crab) -1))
								(not (= (coordinate_x ?b) -1))
							)
			:tasks (
				(CRAB_BUTTERFLY_KILLSPRITE ?crab ?b)
				(:inline () (not (evaluate-interaction ?crab ?b)))
				(:inline () (regenerate-interaction ?crab ?b))
				(check-interactions)
			)
		)

		(:method butterfly_crab_transformto_diamond
			:precondition (and (evaluate-interaction ?b - butterfly ?crab - crab)
								(not (= (coordinate_x ?b) -1))
								(not (= (coordinate_x ?crab) -1))

								(= (coordinate_x ?diam - diamond) -1)
								(= (coordinate_y ?diam - diamond) -1)								
			)
			:tasks (
				(BUTTERFLY_CRAB_TRANSFORMTO_DIAMOND ?b ?crab ?diam)
				(:inline () (not (evaluate-interaction ?b ?crab)))
				(:inline () (regenerate-interaction ?b ?crab))
				(check-interactions)
			)
		)

		(:method exitdoor_avatar_killifotherhasmore_diamond_9
			:precondition (and (evaluate-interaction ?exit - exitdoor ?avat - avatar)
								(not (= (coordinate_x ?exit) -1))
								(not (= (coordinate_x ?avat) -1))
							)
			:tasks (
				(EXITDOOR_AVATAR_KILLIFOTHERHASMORE_DIAMOND_9 ?exit ?avat)
				(:inline () (not (evaluate-interaction ?exit ?avat)))
				(:inline () (regenerate-interaction ?exit ?avat))
				(check-interactions)
			)
		)

		(:method caso_base 
			:precondition ()
			:tasks ()
		)
	)

	; Actions -------------------------------------------------------------------

    ; Acciones para cada movimiento posible del avatar --------------------------
	(:action AVATAR_MOVE_UP
		:parameters (?a - ShootAvatar)
		:precondition (and 
                        ; Comprobación adicional para asegurarse de que puede
                        ; realizarse el movimiento, como en el caso de can-use
						(can-move-up ?a)    

                        ; Comprobación de que está orientado en esa dirección
						(orientation-up ?a)
					)
		:effect (and 
                    ; Se cambia la coordenada en función de la acción
					(assign (last_coordinate_y ?a) (coordinate_y ?a))
					(decrease (coordinate_y ?a) 1)
				)
	)

	(:action AVATAR_MOVE_DOWN
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-move-down ?a)
						(orientation-down ?a)
					)
		:effect (and 
					(assign (last_coordinate_y ?a) (coordinate_y ?a))
					(increase (coordinate_y ?a) 1)
				)
	)

	(:action AVATAR_MOVE_LEFT
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-move-left ?a)
						(orientation-left ?a)
					)
		:effect (and
					(assign (last_coordinate_x ?a) (coordinate_x ?a)) 
					(decrease (coordinate_x ?a) 1)
				)
	)

	(:action AVATAR_MOVE_RIGHT
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-move-right ?a)
						(orientation-right ?a)
					)
		:effect (and 
					(assign (last_coordinate_y ?a) (coordinate_x ?a))
					(increase (coordinate_x ?a) 1)
				)
	)

	(:action AVATAR_TURN_UP
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-change-orientation ?a)
						(not (orientation-up ?a))
					)
		:effect (and 
					(when
						(orientation-down ?a )
						(not (orientation-down ?a))
					)
					(when
						(orientation-right ?a)
						(not (orientation-right ?a))
					)
					(when
						(orientation-left ?a)
						(not (orientation-left ?a))
					)

					(orientation-up ?a)
				)
	)

	(:action AVATAR_TURN_DOWN
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-change-orientation ?a)
						(not (orientation-down ?a))
					)
		:effect (and 
					(when
						(orientation-up ?a )
						(not (orientation-up ?a))
					)
					(when
						(orientation-right ?a)
						(not (orientation-right ?a))
					)
					(when
						(orientation-left ?a)
						(not (orientation-left ?a))
					)

					(orientation-down ?a)
				)
	)

	(:action AVATAR_TURN_LEFT
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-change-orientation ?a)
						(not (orientation-left ?a))
					)
		:effect (and 
					(when
						(orientation-down ?a )
						(not (orientation-down ?a))
					)
					(when
						(orientation-right ?a)
						(not (orientation-right ?a))
					)
					(when
						(orientation-up ?a)
						(not (orientation-up ?a))
					)

					(orientation-left ?a)
				)
	)

	(:action AVATAR_TURN_RIGHT
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-change-orientation ?a)
						(not (orientation-right ?a))
					)
		:effect (and 
					(when
						(orientation-down ?a )
						(not (orientation-down ?a))
					)
					(when
						(orientation-up ?a)
						(not (orientation-up ?a))
					)
					(when
						(orientation-left ?a)
						(not (orientation-left ?a))
					)

					(orientation-right ?a)
				)
	)

    ; Recibe además de la orientación el objeto partner
	; Esto objeto debería desaparecer en el siguiente turno 
	; (en base a los parámetros o al hecho de ser Flicker ?)
	(:action AVATAR_USE
		:parameters (?a - ShootAvatar ?p - sword)
		:precondition (and 
						(can-use ?a)
					)
		:effect (and 
                    ; Por ahora supongo que se genera delante, 
                    ; debo comprobar si depende del avatar
                    (when
                        (orientation-up ?a)

						(and
							(assign (coordinate_x ?p) (coordinate_x ?a))
							(assign (coordinate_y ?p) (coordinate_y ?a))
							(decrease (coordinate_y ?p) 1)						
						)
                    )

                    (when
                        (orientation-down ?a)

						(and
							(assign (coordinate_x ?p) (coordinate_x ?a))
							(assign (coordinate_y ?p) (coordinate_y ?a))
							(increase (coordinate_y ?p) 1)						
						)
                    )

                    (when
                        (orientation-left ?a)

						(and
							(assign (coordinate_x ?p) (coordinate_x ?a))
							(assign (coordinate_y ?p) (coordinate_y ?a))
							(decrease (coordinate_x ?p) 1)						
						)
                    )

                    (when
                        (orientation-right ?a)

                        (and
							(assign (coordinate_x ?p) (coordinate_x ?a))
							(assign (coordinate_y ?p) (coordinate_y ?a))
							(increase (coordinate_x ?p) 1)						
						)
                    )
					
					(increase (counter_sword) 1)
					(increase (counter_Flicker) 1)
					(increase (counter_Object) 1)
				)
	)

	(:action AVATAR_NIL
		:parameters (?a - ShootAvatar )
		:precondition (
					)
		:effect (
				)
	)

	; Acciones para el resto de objetos ---------------------------------------

	; Debe recorrer todos los misiles del juego
	(:action MISSILE_FALL
		:parameters ()		
		:precondition (
					)
		:effect (
					forall (?m - Missile)
					(and
						(when
							(orientation-up ?m)

							(and
								(assign (last_coordinate_y ?m) (coordinate_y ?m))
								(decrease (coordinate_y ?m) 1)						
							)
						)

						(when
							(orientation-down ?m)

							(and
								(assign (last_coordinate_y ?m) (coordinate_y ?m))
								(increase (coordinate_y ?m) 1)						
							)
						)

						(when
							(orientation-left ?m)

							(and
								(assign (last_coordinate_x ?m) (coordinate_x ?m))
								(decrease (coordinate_x ?m) 1)						
							)
						)

						(when
							(orientation-right ?m)

							(and
								(assign (last_coordinate_x ?m) (coordinate_x ?m))
								(increase (coordinate_x ?m) 1)			
							)
						)
					)
		)
	)

	
	; Acciones para las interacciones -----------------------------------------
	
	(:action DIRT_AVATAR_KILLSPRITE
		:parameters (?d - dirt ?a - ShootAvatar)
		:precondition (and
						(= (coordinate_x ?d) (coordinate_x ?a))
						(= (coordinate_y ?d) (coordinate_y ?a))
					)
		:effect (and
					(assign (last_coordinate_y ?d) (coordinate_x ?d))
					(assign (last_coordinate_y ?d) (coordinate_y ?d))
					(assign (coordinate_x ?d) -1)
					(assign (coordinate_y ?d) -1)

					(decrease (counter_dirt) 1)
					(decrease (counter_Immovable) 1)
					(decrease (counter_Object) 1)
		)
	)
	
	(:action DIRT_SWORD_KILLSPRITE
		:parameters (?d - dirt ?s - sword)
		:precondition (and
						(= (coordinate_x ?d) (coordinate_x ?s))
						(= (coordinate_y ?d) (coordinate_y ?s))
		)
		:effect (and
					(assign (last_coordinate_y ?d) (coordinate_x ?d))
					(assign (last_coordinate_y ?d) (coordinate_y ?d))
					(assign (coordinate_x ?d) -1)
					(assign (coordinate_y ?d) -1)

					(decrease (counter_dirt) 1)
					(decrease (counter_Immovable) 1)
					(decrease (counter_Object) 1)
		)
	)
	
	(:action DIAMOND_AVATAR_COLLECTRESOURCE
		:parameters (?d - diamond ?a - avatar)
		:precondition (and
						(= (coordinate_x ?d) (coordinate_x ?a))
						(= (coordinate_y ?d) (coordinate_y ?a))
		)
		:effect (and
					(assign (last_coordinate_y ?d) (coordinate_x ?d))
					(assign (last_coordinate_y ?d) (coordinate_y ?d))
					(assign (coordinate_x ?d) -1)
					(assign (coordinate_y ?d) -1)

					(decrease (counter_diamond) 1)
					(decrease (counter_Resource) 1)
					(decrease (counter_Object) 1)

					(increase (resource_diamond ?a) 1)
		)
	)

	
	(:action MOVING_WALL_STEPBACK
		:parameters (?m - moving ?w - wall)
		:precondition (and
						(= (coordinate_x ?m) (coordinate_x ?w))
						(= (coordinate_y ?m) (coordinate_y ?w))
		)
		:effect (and
					(assign (coordinate_y ?m) (last_coordinate_x ?m))
					(assign (coordinate_y ?m) (last_coordinate_y ?m))		
		)
	)

	
	(:action MOVING_BOULDER_STEPBACK
		:parameters (?m - moving ?b - boulder)
		:precondition (and
						(= (coordinate_x ?m) (coordinate_x ?b))
						(= (coordinate_y ?m) (coordinate_y ?b))
		)
		:effect (and
					(assign (coordinate_y ?m) (last_coordinate_x ?m))
					(assign (coordinate_y ?m) (last_coordinate_y ?m))
		)
	)

	
	(:action AVATAR_BOULDER_KILLIFFROMABOVE
		:parameters (?a - avatar ?b - boulder)
		:precondition (and
						(= (coordinate_x ?a) (coordinate_x ?b))
						(= (coordinate_y ?a) (coordinate_y ?b))

						; Si la roca se movió hacia abajo
						(= (last_coordinate_y ?b) (- (coordinate_y ?b) 1))
		)
		:effect (and
					(assign (last_coordinate_y ?a) (coordinate_x ?a))
					(assign (last_coordinate_y ?a) (coordinate_y ?a))
					(assign (coordinate_x ?a) -1)
					(assign (coordinate_y ?a) -1)

					(decrease (counter_avatar) 1)
					(decrease (counter_ShootAvatar) 1)
					(decrease (counter_moving) 1)
					(decrease (counter_Object) 1)
		)
	)
	
	(:action AVATAR_BUTTERFLY_KILLSPRITE
		:parameters (?a - avatar ?b - butterfly)
		:precondition (and
						(= (coordinate_x ?a) (coordinate_x ?b))
						(= (coordinate_y ?a) (coordinate_y ?b))
		)
		:effect (and
					(assign (last_coordinate_y ?a) (coordinate_x ?a))
					(assign (last_coordinate_y ?a) (coordinate_y ?a))
					(assign (coordinate_x ?a) -1)
					(assign (coordinate_y ?a) -1)

					(decrease (counter_avatar) 1)
					(decrease (counter_ShootAvatar) 1)
					(decrease (counter_moving) 1)
					(decrease (counter_Object) 1)
		)
	)
	
	(:action AVATAR_CRAB_KILLSPRITE
		:parameters (?a - avatar ?c - crab)
		:precondition (and
						(= (coordinate_x ?a) (coordinate_x ?c))
						(= (coordinate_y ?a) (coordinate_y ?c))
		)
		:effect (and
					(assign (last_coordinate_y ?a) (coordinate_x ?a))
					(assign (last_coordinate_y ?a) (coordinate_y ?a))
					(assign (coordinate_x ?a) -1)
					(assign (coordinate_y ?a) -1)

					(decrease (counter_avatar) 1)
					(decrease (counter_ShootAvatar) 1)
					(decrease (counter_moving) 1)
					(decrease (counter_Object) 1)
		)
	)

	
	(:action BOULDER_DIRT_STEPBACK
		:parameters (?b - boulder ?d - dirt)
		:precondition (and
						(= (coordinate_x ?b) (coordinate_x ?d))
						(= (coordinate_y ?b) (coordinate_y ?d))
		)
		:effect (and
					(assign (coordinate_y ?b) (last_coordinate_x ?b))
					(assign (coordinate_y ?b) (last_coordinate_y ?b))
		)
	)

	
	(:action BOULDER_WALL_STEPBACK
		:parameters (?b - boulder ?w - wall)
		:precondition (and
						(= (coordinate_x ?b) (coordinate_x ?w))
						(= (coordinate_y ?b) (coordinate_y ?w))
		)
		:effect (and
				(assign (coordinate_y ?b) (last_coordinate_x ?b))
				(assign (coordinate_y ?b) (last_coordinate_y ?b))
		)
	)

	
	(:action BOULDER_DIAMOND_STEPBACK
		:parameters (?b - boulder ?d - diamond)
		:precondition (and
						(= (coordinate_x ?b) (coordinate_x ?d))
						(= (coordinate_y ?b) (coordinate_y ?d))
		)
		:effect (and				
					(assign (coordinate_y ?b) (last_coordinate_x ?b))
					(assign (coordinate_y ?b) (last_coordinate_y ?b))
		)
	)
	
	(:action BOULDER_BOULDER_STEPBACK
		:parameters (?b ?b2 - boulder)
		:precondition (and
						(= (coordinate_x ?b) (coordinate_x ?b2))
						(= (coordinate_y ?b) (coordinate_y ?b2))
		)
		:effect (and
					(assign (coordinate_y ?b) (last_coordinate_x ?b))
					(assign (coordinate_y ?b) (last_coordinate_y ?b))
		)
	)
	
	(:action ENEMY_DIRT_STEPBACK
		:parameters (?e - enemy ?d - dirt)
		:precondition (and
						(= (coordinate_x ?e) (coordinate_x ?d))
						(= (coordinate_y ?e) (coordinate_y ?d))
		)
		:effect (and
					(assign (coordinate_y ?e) (last_coordinate_x ?e))
					(assign (coordinate_y ?e) (last_coordinate_y ?e))
		)
	)
		
	(:action ENEMY_DIAMOND_STEPBACK
		:parameters (?e - enemy ?d - diamond)
		:precondition (and
						(= (coordinate_x ?e) (coordinate_x ?d))
						(= (coordinate_y ?e) (coordinate_y ?d))
		)
		:effect (and
					(assign (coordinate_y ?e) (last_coordinate_x ?e))
					(assign (coordinate_y ?e) (last_coordinate_y ?e))
		)
	)	
	
	(:action CRAB_BUTTERFLY_KILLSPRITE
		:parameters (?c - crab ?b - butterfly)
		:precondition (and
						(= (coordinate_x ?c) (coordinate_x ?b))
						(= (coordinate_y ?c) (coordinate_y ?b))
		)
		:effect (and					
					(assign (last_coordinate_y ?c) (coordinate_x ?c))
					(assign (last_coordinate_y ?c) (coordinate_y ?c))
					(assign (coordinate_x ?c) -1)
					(assign (coordinate_y ?c) -1)

					(decrease (counter_crab) 1)
					(decrease (counter_enemy) 1)
					(decrease (counter_RandomNPC) 1)
					(decrease (counter_moving) 1)
					(decrease (counter_Object) 1)
		)
	)

	; Debe transformarse en un diamante, ponerlo en el nombre (en el parser)
	; POR PROBAR
	(:action BUTTERFLY_CRAB_TRANSFORMTO_DIAMOND
		:parameters (?b - butterfly ?c - crab ?d - diamond)
		:precondition (and
						(= (coordinate_x ?c) (coordinate_x ?b))
						(= (coordinate_y ?c) (coordinate_y ?b))

						; Para coger un diamante que no se esté usando
						(= (coordinate_x ?d) -1)
						(= (coordinate_y ?d) -1)
		)
		:effect (and
					(assign (last_coordinate_y ?b) (coordinate_x ?b))
					(assign (last_coordinate_y ?b) (coordinate_y ?b))
					(assign (last_coordinate_y ?c) (coordinate_x ?c))
					(assign (last_coordinate_y ?c) (coordinate_y ?c))
					(assign (coordinate_x ?b) -1)
					(assign (coordinate_y ?b) -1)
					(assign (coordinate_x ?c) -1)
					(assign (coordinate_y ?c) -1)

					(decrease (counter_crab) 1)
					(decrease (counter_enemy) 1)
					(decrease (counter_RandomNPC) 1)
					(decrease (counter_moving) 1)
					(decrease (counter_Object) 1)

					; Simulando al parser repito código
					(decrease (counter_butterfly) 1)
					(decrease (counter_enemy) 1)
					(decrease (counter_RandomNPC) 1)
					(decrease (counter_moving) 1)
					(decrease (counter_Object) 1)

					; Cómo genero el diamante ??
					; No se puede generar, asignar a uno que no se esté utilizando
					; una posición en el juego
					(assign (last_coordinate_y ?d) -1)
					(assign (last_coordinate_y ?d) -1)
					(assign (coordinate_x ?d) (last_coordinate_x ?b))
					(assign (coordinate_y ?d) (last_coordinate_y ?b))
					(increase (counter_diamond) 1)
					(increase (counter_Resource) 1)
					(increase (counter_Object) 1)
		)
	)

	; Poner el con qué se compara en el nombre y el número necesario (listener)
	(:action EXITDOOR_AVATAR_KILLIFOTHERHASMORE_DIAMOND_9
		:parameters (?e - exitdoor ?a - avatar)
		:precondition (and
						(= (coordinate_x ?e) (coordinate_x ?a))
						(= (coordinate_y ?e) (coordinate_y ?a))

						; Si avatar tiene más recursos de diamond que el límite (9)
						(>= (resource_diamond ?a) 9)
		)
		:effect (and
					(assign (last_coordinate_y ?e) (coordinate_x ?e))
					(assign (last_coordinate_y ?e) (coordinate_y ?e))
					(assign (coordinate_x ?e) -1)
					(assign (coordinate_y ?e) -1)

					(decrease (counter_exitdoor) 1)
					(decrease (counter_Door) 1)
					(decrease (counter_Object) 1)
		)
	)
)
