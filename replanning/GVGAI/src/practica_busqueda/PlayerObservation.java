package practica_busqueda;

/* Clase para representar la información de un jugador en un momento dado.
 Contiene su posición (x, y), según la cuadrícula que ocupa en el mapa, y su
 orientación */

public class PlayerObservation extends Observation{
    private Orientation orientation;
    
    public PlayerObservation(int x, int y, Orientation orientation){
        super(x, y, ObservationType.PLAYER);
        
        this.orientation = orientation;
    }
    
    public Orientation getOrientation(){
        return orientation;
    }
    
    // Si el juego ha terminado, la posición del jugador es (-1, -1) y la orientación, "N"
    public boolean hasDied(){
        return (this.getX() == -1);
    }
       
    @Override
    public String toString(){
        return (super.toString() + " orientación: " + orientation);
    }
    
    // Para que dos jugadores sean iguales, sus posiciones (x, y) y orientaciones
    // tienen que ser la misma
    @Override
    public boolean equals(Object otherPlayer){
        if (otherPlayer == null)
            return false;
        
        if ( !(otherPlayer instanceof PlayerObservation))
            return false;
        
        PlayerObservation otherPlayer2 = (PlayerObservation)otherPlayer;
        
        if (otherPlayer2 == this)
            return true;
        
        if (otherPlayer2.getX() == this.getX() && otherPlayer2.getY() == this.getY() 
                && otherPlayer2.orientation == this.orientation)
            return true;
        else
            return false;
    }

}