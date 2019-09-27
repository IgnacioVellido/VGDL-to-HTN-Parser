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
	)
  
	; Functions -----------------------------------------------------------------

	(:functions
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
	)

	; Tasks ---------------------------------------------------------------------
    
    ; Método principal para representar un turno en el juego
	(:task Turn
		:parameters (?a - ShootAvatar ?p - sword)

		; Lo suyo sería poner en la precondición el objetivo final del
		; juego, teniendo varios de estos métodos si hay varios criterios de 
		; terminación definidos
		; (:method finish_game
		; 		:precondition ()
		; 		:tasks ()		
		; )

		(:method turn
				:precondition (
								)
				:tasks ( 
							(turn_avatar ?a ?p) 
							(turn_objects)
                            (check-interactions)
							; (create-interactions)

							; (Turn ...) ; Para que el planificador no realice un solo turno
						)
		)


		; Si el turno no se ha podido completar (al 100%%), pasamos al siguiente.
		; Ahora mismo se quedaría atascado ya que no habría ningún cambio, el
		; objetivo es que turn aplique algún efecto (ya sea el avatar o algún
		; otro movimiento) que haga que el juego no cicle
		(:method turn_undone
			:precondition ()
			:tasks (
				(Turn ?a ?p)
			)
		)
	)

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

    ; Para representar el turno del avatar, tiene un método por cada acción,
    ; que podrían ser ordenados en base a una heurística, y acabando con un
    ; método para ACTION_NIL, en caso de que no se pueda realizar ningún otro
	(:task turn_avatar
        ; Recibe al avatar, su orientación, y en el caso de que pueda usar
        ; ACTION_USE, el sprite que genera
		:parameters (?a - ShootAvatar ?p - sword)

        ; Los métodos no tienen precondiciones, la posibilidad de realizarlos
        ; se comprueba dentro de la acción
		(:method avatar_move_up
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_UP ?a) 
						)
		)

		(:method avatar_move_down
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_DOWN ?a) 
						)
		)

		(:method avatar_move_left
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_LEFT ?a) 
						)
		)

		(:method avatar_move_right
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_RIGHT ?a) 
						)
		)

		(:method avatar_turn_up
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_UP ?a) 
						)
		)

		(:method avatar_turn_down
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_DOWN ?a) 
						)
		)

		(:method avatar_turn_left
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_LEFT ?a) 
						)
		)

		(:method avatar_turn_right
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_RIGHT ?a) 
						)
		)

		(:method avatar_use
				:precondition (
								)
				:tasks ( 
							(AVATAR_USE ?a ?p) 
						)
		)

		(:method avatar_nil
				:precondition (
								)
				:tasks ( 
							(AVATAR_NIL ?a) 
						)
		)
	)

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

	; Por probar
	(:task create-interactions
		:parameters ()

		(:method create
			:precondition (not (evaluate-interaction ?o1 - Object ?o2 - Object))
			:tasks (
				(:inline () (evaluate-interaction ?o1 ?o2))
			)
		)

		(:method caso_base
			:precondition ()
			:tasks ()
		)
	)


	; TAREA RECURSIVA QUE GENERE PREDICADOS DE EVALUACIÓN DE INTERACCIONES

	; Se puede hacer que el UNDOALL sea obligatorio y las de STEPBACK a secas no,
	; por tanto si la primera falla check-interactions no se completa y el 
	; movimiento del avatar y de los objetos tampoco, y si falla la segunda el 
	; juego sigue pero esa interacción no se hace (REALMENTE SE DEBERÍA TENER 
	; ALMACENADA LA POSICIÓN DEL OBJETO ANTERIOR Y COMO EFECTO DEJARLO DONDE ESTABA,
	; ESTO DEBERÍA VOLVER A COMPROBAR SI HAY INTERACCIONES EN SU CASILLA ANTERIOR)
	; TAREA RECURSIVA QUE COMPRUEBE INTERACCIONES
	(:task check-interactions
		:parameters ( )

		(:method dirt_avatar_killsprite
			:precondition (evaluate-interaction ?dirt - dirt ?shoo - ShootAvatar)
			:tasks (
				; (:inline (:print "Probando DIRT_AVATAR_KILLSPRITE\n") ())

				(DIRT_AVATAR_KILLSPRITE ?dirt ?shoo)				
				(:inline () (not (evaluate-interaction ?dirt ?shoo)))

				; (:inline (:print "DIRT_AVATAR_KILLSPRITE funciona\n") ())
				
				(check-interactions)
			)
		)

		(:method dirt_sword_killsprite
			:precondition (evaluate-interaction ?dirt - dirt ?sword - sword)
			:tasks (
				(DIRT_SWORD_KILLSPRITE ?dirt ?sword)
				(:inline () (not (evaluate-interaction ?dirt ?sword)))
				(check-interactions)
			)
		)

		(:method diamond_avatar_collectresource
			:precondition (evaluate-interaction ?diam - diamond ?avat - avatar)
			:tasks (
				(DIAMOND_AVATAR_COLLECTRESOURCE ?diam ?avat)
				(:inline () (not (evaluate-interaction ?diam ?avat)))
				(check-interactions)
			)
		)

		(:method moving_wall_stepback
			:precondition (evaluate-interaction ?movi - moving ?wall - wall)
			:tasks (
				; (:inline (:print "Probando MOVING_WALL_STEPBACK\n") ())

				(MOVING_WALL_STEPBACK ?movi ?wall)
				(:inline () (not (evaluate-interaction ?movi ?wall)))

				; (:inline (:print "MOVING_WALL_STEPBACK funciona\n") ())

				(check-interactions)
			)
		)

		(:method avatar_boulder_killiffromabove
			:precondition (evaluate-interaction ?avat - avatar ?boul - boulder)
			:tasks (
				(AVATAR_BOULDER_KILLIFFROMABOVE ?avat ?boul)
				(:inline () (not (evaluate-interaction ?avat ?boul)))
				(check-interactions)
			)
		)
		
		(:method moving_boulder_stepback
			:precondition (evaluate-interaction ?movi - moving ?boul - boulder)
			:tasks (
				(MOVING_BOULDER_STEPBACK ?movi ?boul)
				(:inline () (not (evaluate-interaction ?movi ?boul)))
				(check-interactions)
			)
		)


		(:method avatar_butterfly_killsprite
			:precondition (evaluate-interaction ?avat - avatar ?b - butterfly)
			:tasks (
				(AVATAR_BUTTERFLY_KILLSPRITE ?avat ?b)
				(:inline () (not (evaluate-interaction ?avat ?b)))
				(check-interactions)
			)
		)

		(:method avatar_crab_killsprite
			:precondition (evaluate-interaction ?avat - avatar ?crab - crab)
			:tasks (
				(AVATAR_CRAB_KILLSPRITE ?avat ?crab)
				(:inline () (not (evaluate-interaction ?avat ?crab)))
				(check-interactions)
			)
		)

		(:method boulder_dirt_stepback
			:precondition (evaluate-interaction ?boul - boulder ?dirt - dirt)
			:tasks (
				(BOULDER_DIRT_STEPBACK ?boul ?dirt)
				(:inline () (not (evaluate-interaction ?boul ?dirt)))
				(check-interactions)
			)
		)

		(:method boulder_wall_stepback
			:precondition (evaluate-interaction ?boul - boulder ?wall - wall)
			:tasks (
				(BOULDER_WALL_STEPBACK ?boul ?wall)
				(:inline () (not (evaluate-interaction ?boul ?wall)))
				(check-interactions)
			)
		)

		(:method boulder_diamond_stepback
			:precondition (evaluate-interaction ?boul - boulder ?diam - diamond)
			:tasks (
				(BOULDER_DIAMOND_STEPBACK ?boul ?diam)
				(:inline () (not (evaluate-interaction ?boul ?diam)))
				(check-interactions)
			)
		)

		(:method boulder_boulder_stepback
			; IMPORTANTE COMPROBAR QUE NO SE REPITAN PARÁMETROS (EN LISTENER)
			:precondition (evaluate-interaction ?boul - boulder ?boul2 - boulder)
			:tasks (
				(BOULDER_BOULDER_STEPBACK ?boul ?boul2)
				(:inline () (not (evaluate-interaction ?boul ?boul2)))
				(check-interactions)
			)
		)

		(:method enemy_dirt_stepback
			:precondition (evaluate-interaction ?enem - enemy ?dirt - dirt)
			:tasks (
				(ENEMY_DIRT_STEPBACK ?enem ?dirt)
				(:inline () (not (evaluate-interaction ?enem ?dirt)))
				(check-interactions)
			)
		)

		(:method enemy_diamond_stepback
			:precondition (evaluate-interaction ?enem - enemy ?diam - diamond)
			:tasks (
				(ENEMY_DIAMOND_STEPBACK ?enem ?diam)
				(:inline () (not (evaluate-interaction ?enem ?diam)))
				(check-interactions)
			)
		)

		(:method crab_butterfly_killsprite
			:precondition (evaluate-interaction ?crab - crab ?b - butterfly)
			:tasks (
				(CRAB_BUTTERFLY_KILLSPRITE ?crab ?b)
				(:inline () (not (evaluate-interaction ?crab ?b)))
				(check-interactions)
			)
		)

		; Por probar
		(:method butterfly_crab_transformto_diamond
			:precondition (and (evaluate-interaction ?b - butterfly ?crab - crab)
								(= (coordinate_x ?diam - diamond) -1)
								(= (coordinate_y ?diam - diamond) -1)
			)
			:tasks (
				(BUTTERFLY_CRAB_TRANSFORMTO_DIAMOND ?b ?crab ?diam)
				(:inline () (not (evaluate-interaction ?b ?crab)))
				(check-interactions)
			)
		)

		(:method exitdoor_avatar_killifotherhasmore_diamond_9
			:precondition (evaluate-interaction ?exit - exitdoor ?avat - avatar)
			:tasks (
				(EXITDOOR_AVATAR_KILLIFOTHERHASMORE_DIAMOND_9 ?exit ?avat)
				(:inline () (not (evaluate-interaction ?exit ?avat)))
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
