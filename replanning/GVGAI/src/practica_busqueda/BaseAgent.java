package practica_busqueda;

// Imports de la superclase
import ontology.Types;
import tools.*;
import core.player.*;
import core.game.StateObservation;

// Otros imports
import java.util.ArrayList;
import java.awt.Dimension;

// Agente base para los juegos números 11 y 10. Implementa métodos específicos
// para obtener información en esos juegos exclusivamente. Heredar de esta clase
// para crear un jugador personalizado para el juego.

public abstract class BaseAgent extends AbstractPlayer{
    public static final int NUM_GEMS_FOR_EXIT = 9; // Número de gemas necesarias para poder pasar al siguiente nivel
                                                   // Hay 23 gemas en total
    //Constructor. It must return in 1 second maximum.
    public BaseAgent(StateObservation so, ElapsedCpuTimer elapsedTimer){}
    
    //Act function. Called every game step, it must return an action in 40 ms maximum.
    @Override
    public abstract Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer);
    
    // Método que devuelve una cuadrícula con todas las observaciones presentes en un momento
    // del juego. Cada posición es un array por si hubiera más de una observación en la misma
    // casilla. ObservationGrid[x][y] corresponde a la lista de observaciones presentes en la
    // cuadrícula (x, y) del mapa.
    // En el caso del jugador, se usará también la clase Observation y no la clase PlayerObservation
    // Por tanto, para obtener la orientación del jugador es necesario usar el método getPlayer
    protected ArrayList<Observation>[][] getObservationGrid(StateObservation stateObs){
        ArrayList<core.game.Observation>[][] grid = stateObs.getObservationGrid();
        ArrayList<Observation>[][] finalGrid;
        
        Dimension worldDimension = stateObs.getWorldDimension();
        int blockSize = stateObs.getBlockSize(); // Tamaño de un sprite en píxeles
        
        int width = worldDimension.width / blockSize; // Cuadrículas de ancho
        int height = worldDimension.height / blockSize; // Cuadrículas de alto
        
        finalGrid = new ArrayList[width][height];
        
        Observation new_obs;
        
        for (int y = 0; y < height; y++)
            for (int x = 0; x < width; x++){
                finalGrid[x][y] = new ArrayList<Observation>();
                        
                if (!grid[x][y].isEmpty()){              
                    
                    for(core.game.Observation obs : grid[x][y]){
                        new_obs = new Observation(obs, stateObs.getBlockSize());
                        
                        // <Solución bug forward model>
                        if (new_obs.getType() != null) // Compruebo que sea una observación válida 
                            finalGrid[x][y].add(new_obs);
                    }
                }
                else{
                    finalGrid[x][y].add(new Observation(x, y, ObservationType.EMPTY));
                }
                
                if (finalGrid[x][y].isEmpty()) // Debido al bug puede que ahora esté vacío
                    finalGrid[x][y].add(new Observation(x, y, ObservationType.EMPTY));
            }
        
        return finalGrid;
    }
    
    // Devuelve un array con todos los enemigos (escorpiones y muerciélagos) presentes en el mapa. Cada
    // elemento del array (observations[x]) corresponde a una lista de enemigos de ese tipo
    protected ArrayList<Observation>[] getEnemiesList(StateObservation stateObs){
        ArrayList<core.game.Observation>[] npcs = stateObs.getNPCPositions();
        ArrayList<Observation>[] finalNpcs = new ArrayList[npcs.length];
        
        Observation new_obs;
        
        for (int enemyType = 0; enemyType < npcs.length; enemyType++){
            finalNpcs[enemyType] = new ArrayList<Observation>();
            
            for (core.game.Observation obs : npcs[enemyType]){
                new_obs = new Observation(obs, stateObs.getBlockSize());
                
                if (new_obs.getType() != null)
                    finalNpcs[enemyType].add(new_obs); 
            }
        }
        
        return finalNpcs;
    }
    
    // Devuelve una lista con los murciélagos presentes en el mapa
    protected ArrayList<Observation> getBatsList(StateObservation stateObs){
        ArrayList<Observation>[] enemies = getEnemiesList(stateObs);
        ArrayList<Observation> bats = new ArrayList<Observation>();
        
        for (ArrayList<Observation> observations : enemies)
            if (!observations.isEmpty())
                if (observations.get(0).getType() == ObservationType.BAT)
                    bats = observations;
                            
        return bats;
    }
    
    // Devuelve una lista con los murciélagos presentes en el mapa
    protected ArrayList<Observation> getScorpionsList(StateObservation stateObs){
        ArrayList<Observation>[] enemies = getEnemiesList(stateObs);
        ArrayList<Observation> scorpions = new ArrayList<Observation>();
        
        for (ArrayList<Observation> observations : enemies)
            if (!observations.isEmpty())
                if (observations.get(0).getType() == ObservationType.SCORPION)
                    scorpions = observations;
                            
        return scorpions;
    }
    
    // Devuelve una lista con las gemas presentes en el mapa
    protected ArrayList<Observation> getGemsList(StateObservation stateObs){
        ArrayList<core.game.Observation>[] gems = stateObs.getResourcesPositions();
        ArrayList<Observation> finalGems = new ArrayList<Observation>();

        Observation new_obs;
        
        for (core.game.Observation obs : gems[0]){
            new_obs = new Observation(obs, stateObs.getBlockSize());
            
            if (new_obs.getType() != null)
                finalGems.add(new_obs);
        }
        
        return finalGems;
    }
    
    // Devuelve una lista con los muros presentes en el mapa
    protected ArrayList<Observation> getWallsList(StateObservation stateObs){
        ArrayList<core.game.Observation>[] immovablePos = stateObs.getImmovablePositions();
        ArrayList<Observation> walls = new ArrayList<Observation>();
        
        for (ArrayList<core.game.Observation> observations : immovablePos)
            if (!observations.isEmpty())
                if (observations.get(0).itype == 0) // itype = 0 -> muro
                    for (core.game.Observation obs : observations)
                        walls.add(new Observation(obs, stateObs.getBlockSize()));
                            
        return walls;
    }
    
    // Devuelve una lista con las casillas con suelo NO excavado del mapa
    protected ArrayList<Observation> getGroundTilesList(StateObservation stateObs){
        ArrayList<core.game.Observation>[] immovablePos = stateObs.getImmovablePositions();
        ArrayList<Observation> groundTiles = new ArrayList<Observation>();
        
        for (ArrayList<core.game.Observation> observations : immovablePos)
            if (!observations.isEmpty())
                if (observations.get(0).itype == 4) // itype = 4 -> suelo
                    for (core.game.Observation obs : observations)
                        groundTiles.add(new Observation(obs, stateObs.getBlockSize()));
                            
        return groundTiles;
    }
    
    // Devuelve una lista con las rocas presentes en el mapa
    protected ArrayList<Observation> getBouldersList(StateObservation stateObs){
        ArrayList<core.game.Observation>[] boulders = stateObs.getMovablePositions();
        ArrayList<Observation> finalBoulders = new ArrayList<Observation>();

        Observation new_obs;
        
        for (core.game.Observation obs : boulders[0]){
            new_obs = new Observation(obs, stateObs.getBlockSize());
                
            if (new_obs.getType() != null)
                finalBoulders.add(new_obs);
        }
            
        return finalBoulders;
    }
    
    // Devuelve una lista con las casilla vacías (suelo ya excavado) del mapa
    protected ArrayList<Observation> getEmptyTilesList(StateObservation stateObs){
        ArrayList<Observation>[][] grid = this.getObservationGrid(stateObs);
        ArrayList<Observation> emptyTiles = new ArrayList<Observation>();
        Observation currentObs;
        
        for (int x = 0; x < grid.length; x++)
            for (int y = 0; y < grid[0].length; y++){
                currentObs = grid[x][y].get(0);
                
                if (currentObs.getType() == ObservationType.EMPTY)
                    emptyTiles.add(currentObs);    
            }
        
        return emptyTiles;
    }
    
    // Devuelve la salida del mapa
    protected Observation getExit(StateObservation stateObs){
        ArrayList<core.game.Observation>[] portals = stateObs.getPortalsPositions();
        Observation exit = new Observation(portals[0].get(0), stateObs.getBlockSize());
        
        return exit;
    }
    
    // Devuelve la posición y orientación del jugador en un momento determinado
    // Si el juego ha terminado, la posición del avatar es (-1, -1) y la orientación, "N"
    protected PlayerObservation getPlayer(StateObservation stateObs){
        Vector2d position = stateObs.getAvatarPosition();
        Vector2d orientation = stateObs.getAvatarOrientation();
        int x, y;
        Orientation finalOr = Orientation.N;
        int blockSize = stateObs.getBlockSize();
        
        if (position == Types.NIL){ // Juego terminado
            return (new PlayerObservation(-1, -1, Orientation.N));
        }
        
        x = (int)(position.x / blockSize);
        y = (int)(position.y / blockSize);
        
        if (orientation.y == -1)
            finalOr = Orientation.N;
        else if (orientation.y == 1)
            finalOr = Orientation.S;
        else if (orientation.x == 1)
            finalOr = Orientation.E;
        else if (orientation.x == -1)
            finalOr = Orientation.W;
        
        return (new PlayerObservation(x, y, finalOr));
    }
    
    // Obtiene el número de gemas del jugador en un estado del juego, stateObs
    protected int getNumGems(StateObservation stateObs){
        Integer numGems = stateObs.getAvatarResources().get(6);
        
        // Si no tiene gemas, el hashmap está vacío 
        return (numGems == null ? 0 : numGems); 
    }
    
    // Obtiene el númer de gemas que le faltan al jugador para poder salir del nivel
    protected int getRemainingGems(StateObservation stateObs){
        return NUM_GEMS_FOR_EXIT - getNumGems(stateObs);
    }
}
