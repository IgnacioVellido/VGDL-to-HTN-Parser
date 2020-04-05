package practica_busqueda;

/*  Define qué objeto observación se encuentra en una casilla dada del mapa

WALL -> muro (tanto de los bordes del mapa como paredes interiores)
GROUND -> suelo NO excavado (una casilla ya excavada por el jugador no corresponde a ningún tipo de observación)
BOULDER -> roca
GEM -> gema/diamante
BAT -> enemigo con forma de murciélago rojo
SCORPION -> enemigo con forma de escorpión blanco
PLAYER -> jugador
EXIT -> salida a la que hay que llegar tras conseguir el número necesario de gemas para completar el nivel
EMPTY -> casilla sin nada (suelo que ya ha sido excavado)

Notas:
    > Una casilla en la que haya una observación de tipo EMPTY no tendrá ninguna otra observación
    en dicha casilla en ese momento.

    > Una observación de tipo jugador está determinada también por la orientación, información faltante
    en la clase Observation (que solo aporta posición y tipo de observación)

    > A diferencia de las observaciones de la clase core.game.Observation, las casillas vacías y el jugador
    también son observaciones

Se añade DANGER -> Estas casillas tendrán una penalización por pasar por ellas, pero son transitables
*/

public enum ObservationType {
    WALL, GROUND, BOULDER, GEM, BAT, SCORPION, PLAYER, EXIT, EMPTY, DANGER
}
