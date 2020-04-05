package practica_busqueda;

// Objeto presente en una posición del mapa en un momento del juego.
// Sustituye a la clase core.game.Observation para los juegos 10 y 11

public class Observation {
    private ObservationType type; // Tipo de objeto
    
    private int x; // Posición x en cuadrículas (no píxeles)
    
    private int y; // Posición y en cuadrículas (no píxeles)
    
    public Observation(int x, int y, ObservationType type){
        this.x = x;
        this.y = y;
        this.type = type;
    }
    
    public Observation(core.game.Observation obs, int blockSize){
        int itype = obs.itype;
        
        switch(itype){
            case(0):
                type = ObservationType.WALL;
                break;
            case(4):
                type = ObservationType.GROUND;
                break; 
            case(7):
                type = ObservationType.BOULDER;
                break;   
            case(6):
                type = ObservationType.GEM;
                break; 
            case(11):
                type = ObservationType.BAT;
                break; 
            case(10):
                type = ObservationType.SCORPION;
                break; 
            case(1):
                type = ObservationType.PLAYER;
                break;
            case(5):
                type = ObservationType.EXIT;
                break;
        }
        
        tools.Vector2d pos = obs.position;
        
        this.x = (int)(pos.x / blockSize);
        this.y = (int)(pos.y / blockSize);
    }
  
    public int getX(){
        return x;
    }
    
    public int getY(){
        return y;
    }
    
    public ObservationType getType(){
        return type;
    }

    public void setType(ObservationType t) {type = t; }
    
    // Devuelve true si dos observaciones "chocan" (ocupan la misma casilla
    // en un momento dado)
    public boolean collides(Observation otherOb){
        return (otherOb.x == x && otherOb.y == y);
    }
    
    // Obtiene la distancia euclídea (en línea recta) entre esta observación y otra
    protected float getEuclideanDistance(Observation otherOb){
        float difX = x - otherOb.x;
        float difY = y - otherOb.y;
        
        return ((float)Math.sqrt(difX*difX + difY*difY));
    }
    
    // Obtiene la distancia Manhattan entre esta observación y otra
    protected int getManhattanDistance(Observation otherOb){
        return (Math.abs(x - otherOb.x) + Math.abs(y - otherOb.y));
    }
   
    @Override
    public String toString(){
        return ("Tipo: " + type + " x: " + x + " y: " + y);
    }

    @Override
    public Observation clone() {
        Observation clone = new Observation(x, y, type);
        return clone;
    }
}