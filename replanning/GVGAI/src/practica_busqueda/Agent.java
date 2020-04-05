/* 
  Ignacio Vellido Expósito - TSI
  Se define el agente
*/

// PONER package practica_busqueda;
package practica_busqueda;

// Métodos de Java
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

// Métodos para GVGAI
//import com.sun.deploy.util.ArrayUtil;
import core.game.StateObservation;
import core.player.AbstractPlayer;
import core.vgdl.VGDLRegistry;
import ontology.Types;
import tools.ElapsedCpuTimer;

public class Agent extends AbstractPlayer {

  private ArrayList<core.game.Observation>[][] map;
  private String[][] stringMap;
  private int width, height;

  // -------------------------------------------------------------------------------------------------------------------
  public Agent (StateObservation so, ElapsedCpuTimer elapsedTimer) {
    //super(so, elapsedTimer);
    int blockSize = so.getBlockSize(); // Tamaño de un sprite en píxeles
    width = so.getWorldDimension().width / blockSize;
    height = so.getWorldDimension().height / blockSize;
    stringMap = new String[width][height];
  }

  // -------------------------------------------------------------------------------------------------------------------
  // -------------------------------------------------------------------------------------------------------------------

  public void printState() {
    for (int i = 0; i < width; i++) {
      for (int j = 0; j < height; j++) {
        System.out.print(stringMap[i][j]);
        System.out.print(" ");
      }
      System.out.print("\n");
    }
  }

  public void parseState() {
    for (int i = 0; i < width; i++) {
      for (int j = 0; j < height; j++) {
        if (map[i][j].size() > 0) {
          int itype = map[i][j].get(0).itype;
          stringMap[i][j] = VGDLRegistry.GetInstance().getRegisteredSpriteKey(itype);;
        }
        else {
          stringMap[i][j] = "background";
        }
      }
    }
  }

  @Override
  public Types.ACTIONS act (StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
    Types.ACTIONS action = Types.ACTIONS.ACTION_NIL;
    map = stateObs.getObservationGrid();

    // En game hay un charMapping

    if (hola) {
      try {
        replanning();
      } catch (IOException e) {
        e.printStackTrace();
      }

      parseState();
      printState();
      hola = false;
    }

    return action;
  }

  Boolean hola = true;

  public void replanning() throws IOException {
    //String[] commands = {"make", "replan"};
    String[] commands = {"ls"};
    String [] envp = { };
    File dir = new File("../../");
    Process proc = Runtime.getRuntime().exec(commands, envp, dir);

    BufferedReader stdInput = new BufferedReader(new
            InputStreamReader(proc.getInputStream()));

    BufferedReader stdError = new BufferedReader(new
            InputStreamReader(proc.getErrorStream()));

    // Read the output from the command
    System.out.println("Here is the standard output of the command:\n");
    String s = null;
    while ((s = stdInput.readLine()) != null) {
      System.out.println(s);
    }

    // Read any errors from the attempted command
    System.out.println("Here is the standard error of the command (if any):\n");
    while ((s = stdError.readLine()) != null) {
      System.out.println(s);
    }
  }
}