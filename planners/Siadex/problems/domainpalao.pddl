(define (domain mini_siadex)
(:requirements
:typing
:htn-expansion
:fluents
:negative-preconditions
:durative-actions
)
(:types
	Vehiculo - object
	Vehiculo_Terrestre - Vehiculo
	Recursos_Humanos - object
	Infoca_GIS - object
	Instalacion - Infoca_GIS
	Metodo_Ataque - object
)
(:constants
)
(:predicates

	(recursos_desplegados ?objeto - Recursos_Humanos ?objetivo - Infoca_GIS)
	
	(fuego_en ?objetivo - Infoca_GIS)

	; predicados manuales
	(coordenadas ?pos - Infoca_GIS ?huso - number ?x - number ?y - number )
	(en_vehiculo ?obj - Recursos_Humanos ?v - Vehiculo)
	(activado-p ?R - Vehiculo_Terrestre ?P - Infoca_GIS)

	; predicados generados por slots
	(posicion_actual ?x - (either Recursos_Humanos Vehiculo) ?o -  Infoca_GIS) 	; Posición GIS en la que se encuentra un recurso móvil (no instalaciones). Puede ser un punto, una línea o un área. En los casos complejos se utilizará el centro de gravedad para aproximar la situación real.

	(asignado_en ?x - (either Recursos_Humanos Vehiculo_Terrestre) ?i - Infoca_GIS)

)

;;(:functions
;;(distancia ?x - number ?y - number) - number
;;{
;;   return ?y - ?x
;;}
;;)

;; Tareas Logistica


(:task activar_vehiculo_terrestre
	:parameters (?act_actor - Vehiculo_Terrestre ?punto_de_activacion - Infoca_GIS)
	(
		:method activar_vehiculo_terrestre
		:precondition ()
		:tasks ( (preparar_vehiculo_terrestre ?act_actor ?punto_de_activacion) )
	)
)

(:task transportar_vehiculo_terrestre_transporte
	:parameters (?act_actor - Vehiculo_Terrestre ?objeto - Recursos_Humanos ?posicion_actual ?posicion_destino - Infoca_GIS)
	(
		:method transportar_vehiculo_terrestre_transporte
		:precondition ()
		:tasks ( (activar_vehiculo_terrestre ?act_actor ?posicion_actual)
			   (cargar_vehiculo_terrestre ?act_actor ?objeto ?posicion_actual)
			   (rodar_vehiculo_terrestre ?act_actor ?posicion_actual ?posicion_destino)
			   (descargar_vehiculo_terrestre_Transporte ?act_actor ?objeto ?posicion_destino) )
	)
)

(:task movilizar_recursos
	:parameters (?zona - Infoca_GIS)
	(
		:method movilizar_recursos
		:precondition ()
		:tasks ( (transportar_vehiculo_terrestre_transporte ?act_actor ?objeto ?posicion_actual ?zona) )
	)
)


(:task desmovilizar_recursos
	:parameters ()
	(
		:method desmovilizar_recursos
		:precondition (and (recursos_desplegados ?objeto ?posicion_actual) (asignado_en ?act_actor ?posicion_original) (asignado_en ?objeto ?posicion_original) (posicion_actual ?act_actor ?posicion_actual) (posicion_actual ?objeto ?posicion_actual))
		:tasks ((transportar_vehiculo_terrestre_transporte ?act_actor ?objeto ?posicion_actual ?posicion_original))
	)
)

;; Tareas Ataque

(:task ataque
	:parameters ( ?objetivo - Infoca_GIS )
	(
		:method ataque_aguayretardantes
		:precondition ()
		:tasks ((despliegue_grupo ?objeto ?objetivo)(atacar_aguayretardantes ?objeto ?objetivo))
	)
	(
		:method ataque_rastrillos
		:precondition ()
		:tasks ((despliegue_grupo ?objeto ?objetivo)(atacar_rastrillos ?objeto ?objetivo))
	)
)

;; Tareas Alto Nivel

(:task extinguir
	:parameters (?objetivo - Infoca_GIS)
	(
		:method extinguir
		:precondition (and (fuego_en ?objetivo))
		:tasks ((movilizar_recursos ?objetivo)(ataque ?objetivo)(desmovilizar_recursos))
	)
)

;; Operadores Logistica

(:action preparar_vehiculo_terrestre
	:parameters (?act_actor - Vehiculo_Terrestre ?punto_de_activacion - Infoca_GIS)
	:precondition (and
    (posicion_actual ?act_actor ?punto_de_activacion))
	:effect (and
       (activado-p ?act_actor ?punto_de_activacion))
)


(:action cargar_vehiculo_terrestre
	:parameters (?act_actor - Vehiculo_Terrestre ?objeto - Recursos_Humanos ?posicion_actual - Infoca_GIS)
	:precondition (and (posicion_actual ?act_actor ?posicion_actual) (posicion_actual ?objeto ?posicion_actual) (activado-p ?act_actor ?posicion_actual))
	:effect (and (en_vehiculo ?objeto ?act_actor) (not (posicion_actual ?objeto ?posicion_actual)) (not (recursos_desplegados ?objeto ?posicion_actual)) )
)


(:action descargar_vehiculo_terrestre_Transporte
	:parameters (?act_actor - Vehiculo_Terrestre ?objeto - Recursos_Humanos ?posicion_actual - Infoca_GIS)
	:precondition (and (en_vehiculo ?objeto ?act_actor)
    (posicion_actual ?act_actor ?posicion_actual))
	:effect (and (posicion_actual ?objeto ?posicion_actual)
        (not (en_vehiculo ?objeto ?act_actor)))
)

(:action rodar_vehiculo_terrestre
	:parameters (?act_actor - Vehiculo_Terrestre ?posicion_actual ?posicion_final - Infoca_GIS)
    ;;:precondition (and  (< (distancia ?posicion_actual ?posicion_final) 10) (coordenadas ?posicion_final ?h2 ?x2 ?y2) (coordenadas  ?posicion_actual ?h1 ?x1 ?y1) (posicion_actual ?act_actor ?posicion_actual)(activado-p ?act_actor ?posicion_actual))
    :precondition (and  
    (coordenadas ?posicion_final ?h2 ?x2 ?y2) 
    (coordenadas  ?posicion_actual ?h1 ?x1 ?y1) 
    (posicion_actual ?act_actor ?posicion_actual)
    (activado-p ?act_actor ?posicion_actual))
	:effect (and (posicion_actual ?act_actor ?posicion_final) (not (posicion_actual ?act_actor ?posicion_actual))
			(not (activado-p ?act_actor ?posicion_actual)))
)




(:action despliegue_grupo
	:parameters (?objeto - Recursos_Humanos ?objetivo - Infoca_GIS)
	:precondition (and (posicion_actual ?objeto ?objetivo))
	:effect (and (recursos_desplegados ?objeto ?objetivo))
)


;; Operadores Ataque

;; Falta por introducir en las precondiciones que el metodo de ataque agua y retardantes está disponible
(:action atacar_aguayretardantes
	:parameters (?objeto - Recursos_Humanos ?objetivo - Infoca_GIS)
	:precondition (and (recursos_desplegados ?objeto ?objetivo) )
	:effect (not (fuego_en ?objetivo))
)


;; Falta por introducir en las precondiciones que el metodo de ataque rastrillos
(:action atacar_rastrillos
	:parameters (?objeto - Recursos_Humanos ?objetivo - Infoca_GIS)
	:precondition (and (recursos_desplegados ?objeto ?objetivo) )
	:effect (not (fuego_en ?objetivo))
)

)
