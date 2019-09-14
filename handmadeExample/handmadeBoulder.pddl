
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Dominio HPDL hecho a mano para generar las mismas acciones que Vladis
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
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame) 
    ; No todos los requisitos son necesarios por ahora, revisar
	(:requirements
		:typing
		:fluents
		:derived-predicates
		:negative-preconditions
		:universal-preconditions
		:disjuntive-preconditions
		:conditional-effects
		:htn-expansion

		; For time management
		; :durative-actions
		; :metatags

		:equality
	)

	; Types -----------------------------------------------------------------

    ; Un tipo orientación y otro Object (objeto genérico), otro para cada 
    ; sprite definido y otro para cada tipo de sprite declarado
	(:types
		Orientation
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

    ; Las constantes solo se utilizan para la orientación, se podría tener un
    ; predicado para esto
	(:constants
		up down left right - Orientation
	)

	; Predicates ----------------------------------------------------------------

	(:predicates
        ; Uno para la orientación del avatar (ampliable a varios)
		(orientation ?a - ShootAvatar ?o - Orientation)

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
		(counter_Orientation)
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
		:parameters (?a - ShootAvatar ?o - Orientation ?p - sword ; Para el turno del avatar
					 ?o - Object ; Debería representar todos los objetos posibles, para el turno de estos
					 ?o1 ?o2 - Object ; Para comprobar interacción, debe representar 
					 				  ; dos objetos cualesquiera (y debe comprobar 
									  ; todas las combinaciones posibles)
					)

		(:method turn
				:precondition (
								)
				:tasks ( 
							(turn_avatar ?a ?o ?p) 
                            (turn_objects ?o)
                            (check-interactions ?o1 ?o2)
						)
		)
	)

    ; Para representar el turno del avatar, tiene un método por cada acción,
    ; que podrían ser ordenados en base a una heurística, y acabando con un
    ; método para ACTION_NIL, en caso de que no se pueda realizar ningún otro
	(:task turn_avatar
        ; Recibe al avatar, su orientación, y en el caso de que pueda usar
        ; ACTION_USE, el sprite que genera
		:parameters (?a - ShootAvatar ?o - Orientation ?p - sword)

        ; Los métodos no tienen precondiciones, la posibilidad de realizarlos
        ; se comprueba dentro de la acción
		(:method avatar_move_up
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_UP ?a ?o) 
						)
		)

		(:method avatar_move_down
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_DOWN ?a ?o) 
						)
		)

		(:method avatar_move_left
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_LEFT ?a ?o) 
						)
		)

		(:method avatar_move_right
				:precondition (
								)
				:tasks ( 
							(AVATAR_MOVE_RIGHT ?a ?o) 
						)
		)

		(:method avatar_turn_up
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_UP ?a ?o) 
						)
		)

		(:method avatar_turn_down
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_DOWN ?a ?o) 
						)
		)

		(:method avatar_turn_left
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_LEFT ?a ?o) 
						)
		)

		(:method avatar_turn_right
				:precondition (
								)
				:tasks ( 
							(AVATAR_TURN_RIGHT ?a ?o) 
						)
		)

		(:method avatar_use
				:precondition (
								)
				:tasks ( 
							(AVATAR_USE ?a ?o ?p) 
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

	; Acción recursiva por cada objeto que compruebe si debe moverse y aplicar la
	; acción que corresponda en cada caso
	(:task turn_objects
		:parameters (?o - Object)

		(:method turn
			:precondition ()
			:tasks (
						; Como sabemos que hay una roca, ver si se puede mover
						(BOULDER_FALL ?o)						
						(turn_objects ?)

						; Los objetos con movimientos no determinista no tiene
						; sentido actualizarlos (no sin planifiación probabilística)
					)
		)
	
	)

	; Actions -------------------------------------------------------------------

    ; Acciones para cada movimiento posible del avatar --------------------------
	(:action AVATAR_MOVE_UP
		:parameters (?a - ShootAvatar ?o - Orientation)
		:precondition (and 
                        ; Comprobación adicional para asegurarse de que puede
                        ; realizarse el movimiento, como en el caso de can-use
						(can-move-up ?a)    

                        ; Comprobación de que está orientado en esa dirección
						(orientation ?a ?o)
						(= ?o up)
					)
		:effect (and 
                    ; Se cambia la coordenada en función de la acción
					(decrease (coordinate_x ?a) 1)
				)
	)

	(:action AVATAR_MOVE_DOWN
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-move-down ?a)
						(orientation ?a ?o)
						(= ?o down)
					)
		:effect (and 
					(increase (coordinate_x ?a) 1)
				)
	)

	(:action AVATAR_MOVE_LEFT
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-move-left ?a)
						(orientation ?a ?o)
						(= ?o left)
					)
		:effect (and 
					(decrease (coordinate_y ?a) 1)
				)
	)

	(:action AVATAR_MOVE_RIGHT
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-move-right ?a)
						(orientation ?a ?o)
						(= ?o right)
					)
		:effect (and 
					(increase (coordinate_y ?a) 1)
				)
	)

	(:action AVATAR_TURN_UP
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-change-orientation ?a)
						(orientation ?a ?o)
					)
		:effect (and 
					(not (orientation ?a ?o))
					(orientation ?a up)
				)
	)

	(:action AVATAR_TURN_DOWN
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-change-orientation ?a)
						(orientation ?a ?o)
					)
		:effect (and 
					(not (orientation ?a ?o))
					(orientation ?a down)
				)
	)

	(:action AVATAR_TURN_LEFT
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-change-orientation ?a)
						(orientation ?a ?o)
					)
		:effect (and 
					(not (orientation ?a ?o))
					(orientation ?a left)
				)
	)

	(:action AVATAR_TURN_RIGHT
		:parameters (?a - ShootAvatar ?o - Orientation )
		:precondition (and 
						(can-change-orientation ?a)
						(orientation ?a ?o)
					)
		:effect (and 
					(not (orientation ?a ?o))
					(orientation ?a right)
				)
	)

    ; Recibe además de la orientación el objeto partner
	(:action AVATAR_USE
		:parameters (?a - ShootAvatar ?o - Orientation ?p - sword)
		:precondition (and 
						(can-use ?a)
                        (orientation ?a ?o)
					)
		:effect (and 
                    ; Por ahora supongo que se genera delante, 
                    ; debo comprobar si depende del avatar
                    (when
                        (orientation ?a up)

                        (= (coordinate_x ?p) (coordinate_x ?a))
                        (= (coordinate_y ?p) (decrease (coordinate_y ?a) 1))
                    )

                    (when
                        (orientation ?a down)

                        (= (coordinate_x ?p) (coordinate_x ?a))
                        (= (coordinate_y ?p) (increase (coordinate_y ?a) 1))
                    )

                    (when
                        (orientation ?a left)

                        (= (coordinate_x ?p) (decrease (coordinate_x ?a) 1))
                        (= (coordinate_y ?p) (coordinate_y ?a))
                    )

                    (when
                        (orientation ?a right)

                        (= (coordinate_x ?p) (increase (coordinate_x ?a) 1))
                        (= (coordinate_y ?p) (coordinate_y ?a))
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


)
