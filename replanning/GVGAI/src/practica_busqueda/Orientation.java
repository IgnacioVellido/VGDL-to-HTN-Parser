package practica_busqueda;

/* Orientación del jugador en un determinado momento del juego.

Es importante conocerla porque para ir en una dirección es primero necesario
estar orientado hacia esa dirección. Por ejemplo, si queremos ir al Norte y estamos
orientados hacia el Este, primero tendremos que ejecutar la acción ACTION_UP para
orientarnos hacia arriba y después volver a ejecutarla para movernos una casilla
en esa dirección.
 */

public enum Orientation {
    N, S, E, W
}
