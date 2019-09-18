;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Dominio HPDL hecho a mano para generar las mismas acciones que Vladis
;; 
;; ----------------------------------------------------------------------------
;; Dudas:
;; - Cómo ver los valores de las funciones al final de la ejecución del 
;: planificador
;;
;; - Posiblemente haga falta almacenar la posición del turno anterior (para cada
;; objeto), en functions
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

		; For time management
		; :durative-actions
		; :metatags

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
	)

	; Tasks ---------------------------------------------------------------------
    
    ; Método principal para representar un turno en el juego
	(:task Turn
		:parameters (?a - ShootAvatar ?p - sword ; Para el turno del avatar
					;  ?s - Object ; Debería representar todos los objetos posibles, para el turno de estos
					;  ?s1 ?s2 - Object ; Para comprobar interacción, debe representar 
					 				  ; dos objetos cualesquiera (y debe comprobar 
									  ; todas las combinaciones posibles)
					)

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
                            ; (turn_objects ?s)
							(turn_objects)
                            (check-interactions)

							; (Turn ...) ; Para que el planificador no realice un solo turno
						)
		)


		; Si el turno no se ha podido completar (al 100%%), pasamos al siguiente
		; Ahora mismo se quedaría atascado ya que no habría ningún cambio, el
		; objetivo es que turn aplique algún efecto (ya sea el avatar o algún
		; otro movimiento) que haga que el juego continue
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

	; Acción recursiva por cada objeto que compruebe si debe moverse y aplicar la
	; acción que corresponda en cada caso
	(:task turn_objects
		; :parameters (?s - Object)
		:parameters () ; Probando sin objetos, a ver si itera por todos

		(:method turn
			:precondition ()
			:tasks (
						; Como sabemos que hay una roca, ver si se puede mover
						; (BOULDER_FALL ?s) Creo que se podría generalizar para el tipo de objeto
						; (MISSILE_FALL ?s)
						(MISSILE_FALL)
						; (turn_objects ?s)

						; Los objetos con movimientos no determinista (ej: enemigos) 
						; no tiene sentido actualizarlos (no sin planifiación 
						; probabilística)
					)
		)
	)

	; -------------------------------------------------------------------------
	; -------------------------------------------------------------------------

	; Se puede hacer que el UNDOALL sea obligatorio y las de STEPBACK a secas no,
	; por tanto si la primera falla check-interactions no se completa y el 
	; movimiento del avatar y de los objetos tampoco, y si falla la segunda el 
	; juego sigue pero esa interacción no se hace (REALMENTE SE DEBERÍA TENER 
	; ALMACENADA LA POSICIÓN DEL OBJETO ANTERIOR Y COMO EFECTO DEJARLO DONDE ESTABA,
	; ESTO DEBERÍA VOLVER A COMPROBAR SI HAY INTERACCIONES EN SU CASILLA ANTERIOR)
	(:task check-interactions
		; Si se puede hacer que se repita esta tarea con todas las combinaciones
		; posibles de objetos, comprobar la colisión en la precondición del método
		; :parameters (?s1 - Object ?s2 - Object)
		:parameters ()

		(:method provisional_name
			:precondition ()
			:tasks (
				; (forall (?o1 ?o2 - Object)
				; (and
					; (DIRT_AVATAR_KILLSPRITE ?o1 ?o2)
				; )
				; )
					(DIRT_AVATAR_KILLSPRITE)
					(DIRT_SWORD_KILLSPRITE)
					(DIAMOND_AVATAR_COLLECTRESOURCE)
			)
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
	; FUNCIONA
	(:action MISSILE_FALL
		; :parameters (?m - Missile)
		:parameters ()		
		:precondition (
					)
		:effect (
					forall (?m - Missile)
					(and
						(when
							(orientation-up ?m)

							(decrease (coordinate_y ?m) 1)						
						)

						(when
							(orientation-down ?m)

							(increase (coordinate_y ?m) 1)						
						)

						(when
							(orientation-left ?m)

							(decrease (coordinate_x ?m) 1)						
						)

						(when
							(orientation-right ?m)

							(increase (coordinate_x ?m) 1)			
						)
					)
		)
	)

	
	; Acciones para las interacciones -----------------------------------------
	; Por algún motivo NO FUNCIONA, no salta la colisión a pesar de estar en la misma casilla
	(:action DIRT_AVATAR_KILLSPRITE
		; :parameters (?d - dirt ?a - ShootAvatar)
		:parameters ( )
		:precondition (
					)
		:effect (and
			; Comprobamos interacción y eliminamos objeto dirt
			(forall (?d - dirt ?a - avatar) ; IMPORTANTE: Debe ser el tipo declarado
											; en VGDL (no vale porner ShootAvatar)
				(when
					(and
						(= (coordinate_x ?d) (coordinate_x ?a))
						(= (coordinate_y ?d) (coordinate_y ?a))
					)

					(and
						(assign (last_coordinate_y ?d) (coordinate_x ?d))
						(assign (last_coordinate_y ?d) (coordinate_y ?d))
						(assign (coordinate_x ?d) -1)
						(assign (coordinate_y ?d) -1)

						(decrease (counter_dirt) 1)
						(decrease (counter_Immovable) 1)
						(decrease (counter_Object) 1)
					)			
				)
			)
		)
	)

	; Modificación de DIRT_AVATAR_KILLSPRITE
	; NO FUNCIONA
	(:action DIRT_SWORD_KILLSPRITE
		:parameters (  )
		:precondition (

		)
		:effect (
			; Comprobamos interacción y eliminamos objeto dirt
			forall (?d - dirt ?s - sword)
				(when
					(and
						(= (coordinate_x ?d) (coordinate_x ?s))
						(= (coordinate_y ?d) (coordinate_y ?s))
					)

					(and
						(assign (last_coordinate_y ?d) (coordinate_x ?d))
						(assign (last_coordinate_y ?d) (coordinate_y ?d))
						(assign (coordinate_x ?d) -1)
						(assign (coordinate_y ?d) -1)

						(decrease (counter_dirt) 1)
						(decrease (counter_Immovable) 1)
						(decrease (counter_Object) 1)
					)			
				)			
		)
	)

	; Modificación de DIRT_AVATAR_KILLSPRITE
	; NO FUNCIONA
	(:action DIAMOND_AVATAR_COLLECTRESOURCE
		:parameters ( )
		:precondition (

		)
		:effect (
			; Comprobamos interacción, eliminamos diamond e incrementamos recurso
			forall (?d - diamond ?a - avatar)
				(when
					(and
						(= (coordinate_x ?d) (coordinate_x ?a))
						(= (coordinate_y ?d) (coordinate_y ?a))
					)

					(and
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

	; Modificación de DIRT_AVATAR_KILLSPRITE
	; NO FUNCIONA
	(:action AVATAR_BUTTERFLY_KILLSPRITE
		:parameters ( )
		:precondition (

		)
		:effect (
			; Comprobamos interacción, eliminamos diamond e incrementamos recurso
			forall (?a - avatar ?b - butterfly)
				(when
					(and
						(= (coordinate_x ?a) (coordinate_x ?b))
						(= (coordinate_y ?a) (coordinate_y ?b))
					)

					(and
						(assign (last_coordinate_y ?a) (coordinate_x ?a))
						(assign (last_coordinate_y ?a) (coordinate_y ?a))
						(assign (coordinate_x ?a) -1)
						(assign (coordinate_y ?a) -1)

						(decrease (counter_avatar) 1)
						(decrease (counter_ShootAvatar) 1)
						(decrease (counter_Object) 1)
					)			
				)
		)
	)

	; Modificación de DIRT_AVATAR_KILLSPRITE
	; NO FUNCIONA
	(:action AVATAR_CRAB_KILLSPRITE
		:parameters ( )
		:precondition (

		)
		:effect (
			; Comprobamos interacción, eliminamos diamond e incrementamos recurso
			forall (?a - avatar ?c - crab)
				(when
					(and
						(= (coordinate_x ?a) (coordinate_x ?c))
						(= (coordinate_y ?a) (coordinate_y ?c))
					)

					(and
						(assign (last_coordinate_y ?a) (coordinate_x ?a))
						(assign (last_coordinate_y ?a) (coordinate_y ?a))
						(assign (coordinate_x ?a) -1)
						(assign (coordinate_y ?a) -1)

						(decrease (counter_avatar) 1)
						(decrease (counter_ShootAvatar) 1)
						(decrease (counter_Object) 1)
					)			
				)
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

	; Modificación de DIRT_AVATAR_KILLSPRITE
	; NO FUNCIONA
	(:action CRAB_BUTTERFLY_KILLSPRITE
		:parameters ( )
		:precondition (

		)
		:effect (
			; Comprobamos interacción, eliminamos diamond e incrementamos recurso
			forall (?c - crab ?b - butterfly)
				(when
					(and
						(= (coordinate_x ?c) (coordinate_x ?b))
						(= (coordinate_y ?c) (coordinate_y ?b))
					)

					(and
						(assign (last_coordinate_y ?c) (coordinate_x ?c))
						(assign (last_coordinate_y ?c) (coordinate_y ?c))
						(assign (coordinate_x ?c) -1)
						(assign (coordinate_y ?c) -1)

						(decrease (counter_crab) 1)
						(decrease (counter_enemy) 1)
						(decrease (counter_RandomNPC) 1)
						(decrease (counter_Object) 1)
					)			
				)
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
