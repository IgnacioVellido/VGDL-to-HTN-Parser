(define (domain mia-p2-visita)

 ;; Requerimientos del dominio
 (:requirements
  :typing
  :fluents
  :derived-predicates 
  :negative-preconditions
  :universal-preconditions
  :disjuntive-preconditions
  :conditional-effects
  :htn-expansion
 )

 (:types
 )

 (:constants
  palacios
  edificios
 )

 (:predicates
  (igual ?x ?y)
  (diferente ?x ?y)
  (palacio ?p ?id)
  (edificio ?e ?id)
  (iglesia ?i ?id)
  (parque ?p ?id)
  (museo ?m ?id)
  (exposicion ?e ?id)
  (espectaculo ?e ?id)
  (plaza ?p ?id)
  (camino ?origen ?destino ?camino)
  (prefiere ?p ?x)
 )

 (:functions

  ;; LLamada externa a python
  ;; Por favor: CUIDADO CON LA INDENTACION
  ;; Establece la variable path al lugar donde tienes el ejecutable
  ;; y los ficheros de datos para el pathfinder
  (distancia ?origen ?destino)
{
  import os
  import string
  import re
  path = '/home/oscar/siadexdev/problems/samap/'
  call = path + 'pathfinder-ext '
  call += path + 'cruces.txt '
  call += path + 'tramos.txt '
  call += path + 'sitios.txt '
  call += str(?origen) + ' '
  call += str(?destino) + ' '
  call += path + 'camino.txt &> /dev/null'
  os.system(call)
  f = open(path + 'camino.txt','r')
  s = f.readline()
  f.close()
  p = re.compile("\d+.\d+");
  m = p.findall(s)
  if len(m) > 0:
    return float(m[0]) 
  else:
    return 0;
}

  (posicion ?p)
  (limite_andando ?p)
  (dinero_disponible ?p)
  (precio ?visita)
 )

 ;; Axiomas del dominio

 ;; igualdad entre objetos
 (:derived (igual ?x ?x) ())
 ;; desigualdad entre objetos
 (:derived (diferente ?x ?y) (not (igual ?x ?y)))

  ;; LLamada externa a python
  ;; Por favor: NO ALTERAR LA INDENTACION
 (:derived (camino ?origen ?destino ?camino)
{
  import os
  import string
  path = '/home/oscar/siadexdev/problems/samap/'
  call = path + 'pathfinder-ext '
  call += path + 'cruces.txt '
  call += path + 'tramos.txt '
  call += path + 'sitios.txt '
  call += str(?origen) + ' '
  call += str(?destino) + ' '
  call += path + 'camino.txt &> /dev/null'
  os.system(call)
  f = open(path + 'camino.txt','r')
  s = f.readline()
  ret = ""
  s = f.readlines()
  f.close()
  for i in range(len(s)):
    ret += s[i] 

  ?camino.append(ret)
  return 1;
}
)


 ;; Tareas abstractas

 ;;Desplazamientos

 (:task moverse
  :parameters (?quien ?destino)
  (!
    (:method en-destino
     :precondition (= (posicion ?quien) ?destino)
     :tasks ()
    )
    (:method andando
     :precondition (and (bound ?donde (posicion ?quien)) (<= (distancia ?donde ?destino) (limite_andando ?quien)))
     :tasks (ir_caminando ?quien ?destino)
    )
    (:method en_taxi
     :precondition ()
     :tasks (ir_en_taxi ?quien ?destino)
    )
  )
 )

 (:task ir_caminando
  :parameters (?quien ?destino)
  (:method caminar
   :precondition (bound ?origen (posicion ?quien))
   :tasks (caminar ?quien ?origen ?destino ?camino)
  )
 )

 (:task ir_en_taxi
  :parameters (?quien ?destino)
  (:method ir_en_taxi
   :precondition (bound ?origen (posicion ?quien))
   :tasks (
       (esperar_taxi_en ?quien ?origen)
       (coger_taxi_a ?quien ?destino))
  )
 )

 ;; Visitas

 (:task visitar_palacio
  :parameters (?quien ?palacio)
  (:method visitar_palacio
   :precondition (and
       (prefiere ?quien palacios)
       (palacio ?palacio ?x))
   :tasks (visitar ?quien ?palacio)
  )
 )

 (:task visitar_edificio
  :parameters (?quien ?edificio)
  (:method visitar_edificio
   :precondition (and
       (prefiere ?quien edificios)
       (edificio ?edificio ?x))
   :tasks (visitar ?quien ?edificio)
  )
 )

 (:task visitar 
  :parameters (?quien ?visita)
  (:method visitar
   :precondition (bound ?posicion (posicion ?visita))
   :tasks (
       (moverse ?quien ?posicion)
       (pagar_entrada ?quien ?visita)
       (realizar_visita ?visita))
  )
 )

 (:task pagar_entrada
  :parameters (?quien ?visita)
  (:method pagar_entrada
   :precondition (bound ?precio (precio ?visita))
   :tasks (gastar ?quien ?precio ?queda)
  )
 )

 ;;Operaciones primitivas

 (:action caminar
  :parameters (?quien ?origen ?destino ?camino)
  :precondition (camino ?origen ?destino ?camino)
  :effect (assign (posicion ?quien) ?destino)
 )

 (:action esperar_taxi_en 
  :parameters (?quien ?origen)
  :precondition ()
  :effect ()
 )

 (:action coger_taxi_a
  :parameters (?quien ?destino)
  :precondition ()
  :effect (assign (posicion ?quien) ?destino)
 )

 ;; Esto se puede hacer en los efectos directamente sin
 ;; usar la variable ?despues y con una precondicion vacia
 (:action gastar
  :parameters (?quien -object ?dinero -number ?despues)
  :precondition (bound ?despues (- (dinero_disponible ?quien) ?dinero))
  :effect (assign (dinero_disponible ?quien) ?despues)
 )

 (:action realizar_visita
  :parameters (?visita)
  :precondition ()
  :effect ()
 )
)


