;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Dominio HPDL hecho a mano para generar las mismas acciones que Vladis
;; 
;; ----------------------------------------------------------------------------
;; Dudas:
;; - Posiblemente haga falta almacenar la posición del turno anterior, en functions
;;
;; - Cómo hacer que se compruebe una tarea para un objeto concreto ?
;; Por ejemplo, que se compruebe las interacciones con todos los objetos o que
;; se aplique una acción o todos los objetos del mismo tipo (MISSILE_FALL)
;;
;; - ¿Cómo crear un nuevo objeto? ¿Mediante un predicado? 
;; A Flicker se le puede poner unas coordenadas negativas para indicar que no 
;; existe, pero no se podrían generar nuevos objetos con esta idea
;; ¿Quizás un predicado derivado para cuando las coordenadas sean negativas?
;;
;; - Documentación HPDL página 12: ¿Qué implica el '!'? -> Corte, hace que se 
;; olviden el resto de unificaciones. Se puede usar en métodos y precondiciones
;; ----------------------------------------------------------------------------
;;
;; Notas:
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
;; - "exit-level" solo indica que el avatar está sobre la casilla de salida (y 
;; debería comprobar que tiene antes 9 gemas, cosa que se le olvida)
;;
;; - "get-gem" no se incluye ya que se recoge automáticamente en base a la
;; interacción
;;
;; ----------------------------
;;
;; - No recordaba que el tipo object ya estaba definido en HPDL, creo que no va
;; a afectar pero en cualquier caso lo anoto por si es necesario cambiarle el 
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
		:conditional-effects

		; For time management
		; :durative-actions
		; :metatags

		; Necesarios
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
		background - Immovable
		wall - Immovable
		sword - Flicker
		dirt - Immovable
		exitdoor - Door
		diamond - Resource
		boulder - Missile
		avatar - ShootAvatar
		enemy - RandomNPC
		crab - enemy
		butterfly - enemy
		ShootAvatar Immovable Flicker Resource Door Missile RandomNPC - Object
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

        ; Debe haber un contador por cada recurso (en este caso uno)
		(resource_diamond ?a - avatar)

        ; Esto no es necesario por ahora, ya que serviría para representar objetivos
        ; finales como los declarados por VGDL
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
	)

	; Tasks ---------------------------------------------------------------------
    
    ; Método principal para representar un turno en el juego
	(:task Turn
		:parameters (?a - ShootAvatar ?p - sword ; Para el turno del avatar
					 ?s - Object ; Debería representar todos los objetos posibles, para el turno de estos
					;  ?s1 ?s2 - Object ; Para comprobar interacción, debe representar 
					 				  ; dos objetos cualesquiera (y debe comprobar 
									  ; todas las combinaciones posibles)
					)

		(:method turn
				:precondition (
								)
				:tasks ( 
							(turn_avatar ?a ?p) 
                            (turn_objects ?s)
                            ; (check-interactions ?s1 ?s2)

							; (Turn ...) ; Para que el planificador no realice un solo turno
						)
		)

		; Cuando no se puedan realizar más movimientos (?)
		; Quizás lo suyo sería poner en la precondición el objetivo final del
		; juego, teniendo varios de estos métodos si hay varios criterios de 
		; terminación definidos
		(:method finish_game
				:precondition ()
				:tasks ()		
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

	; Acción recursiva por cada objeto que compruebe si debe moverse y aplicar la
	; acción que corresponda en cada caso
	(:task turn_objects
		:parameters (?s - Object)

		(:method turn
			:precondition ()
			:tasks (
						; Como sabemos que hay una roca, ver si se puede mover
						; (BOULDER_FALL ?s) Creo que se podría generalizar para el tipo de objeto
						(MISSILE_FALL ?s)
						; (turn_objects ?s)

						; Los objetos con movimientos no determinista (ej: enemigos) 
						; no tiene sentido actualizarlos (no sin planifiación 
						; probabilística)
					)
		)
	)

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

	(:task check-interactions
		; Si se puede hacer que se repita esta tarea con todas las combinaciones
		; posibles de objetos, comprobar la colisión en la precondición del método
		:parameters (?s1 - Object ?s2 - Object)

		(:method provisional_name
			:precondition 
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
					(decrease (coordinate_x ?a) 1)
				)
	)

	(:action AVATAR_MOVE_DOWN
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-move-down ?a)
						(orientation-down ?a)
					)
		:effect (and 
					(increase (coordinate_x ?a) 1)
				)
	)

	(:action AVATAR_MOVE_LEFT
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-move-left ?a)
						(orientation-left ?a)
					)
		:effect (and 
					(decrease (coordinate_y ?a) 1)
				)
	)

	(:action AVATAR_MOVE_RIGHT
		:parameters (?a - ShootAvatar)
		:precondition (and 
						(can-move-right ?a)
						(orientation-right ?a)
					)
		:effect (and 
					(increase (coordinate_y ?a) 1)
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
		:parameters (?m - Missile)
		:precondition (

		)
		:effect (
					forall (?m2 - Missile)
					(and
						(when
							(orientation-up ?m2)

							(decrease (coordinate_y ?m2) 1)						
						)

						(when
							(orientation-down ?a)

							(increase (coordinate_y ?m2) 1)						
						)

						(when
							(orientation-left ?a)

							(decrease (coordinate_x ?m2) 1)						
						)

						(when
							(orientation-right ?a)

							(increase (coordinate_x ?m2) 1)						
						)
					)
		)
	)

	
	; Acciones para las interacciones -----------------------------------------
	(:action DIRT_AVATAR_KILLSPRITE
		:parameters (?d - dirt ?a - ShootAvatar)
		:precondition (
			; Mismas coordenadas, son las mismas para todas las interacciones
			(= (coordinate_x ?d) (coordinate_x ?a))
			(= (coordinate_y ?d) (coordinate_y ?a))
		)
		:effect (
			; Eliminamos objeto dirt
		)
	)

	(:action DIRT_SWORD_KILLSPRITE
		:parameters (  )
		:precondition (

		)
		:effect (

		)
	)

	(:action DIAMOND_AVATAR_COLLECTRESOURCE
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action MOVING_WALL_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action MOVING_BOULDER_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action AVATAR_BOULDER_KILLIFFROMABOVE
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action AVATAR_BUTTERFLY_KILLSPRITE
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action AVATAR_CRAB_KILLSPRITE
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action BOULDER_DIRT_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action BOULDER_WALL_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action BOULDER_DIAMOND_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action BOULDER_BOULDER_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action ENEMY_DIRT_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action ENEMY_DIAMOND_STEPBACK
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action CRAB_BUTTERFLY_KILLSPRITE
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action BUTTERFLY_CRAB_TRANSFORMTO
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)

	(:action EXITDOOR_AVATAR_KILLIFOTHERHASMORE
		:parameters ( )
		:precondition (

		)
		:effect (

		)
	)
)
