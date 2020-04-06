/* 
  Ignacio Vellido Expósito - TSI
  Se define el agente
*/

// PONER package practica_busqueda;
package practica_busqueda;

// Métodos de Java
import java.io.*;
import java.util.*;

// Métodos para GVGAI
//import com.sun.deploy.util.ArrayUtil;
import core.game.StateObservation;
import core.player.AbstractPlayer;
import core.vgdl.VGDLRegistry;
import ontology.Types;
import tools.ElapsedCpuTimer;

import javax.swing.*;

public class Agent extends AbstractPlayer {

  private ArrayList<core.game.Observation>[][] map;
  private String[][] stringMap;
  private int width, height;
  HashMap<Character, ArrayList<String>> charMapping;
  HashMap<String, String> levelMapping = new HashMap<>();
  private ArrayList<Types.ACTIONS> actions = new ArrayList<>();

  // -------------------------------------------------------------------------------------------------------------------
  public Agent (StateObservation so, ElapsedCpuTimer elapsedTimer) {
    int blockSize = so.getBlockSize(); // Tamaño de un sprite en píxeles
    width = so.getWorldDimension().width / blockSize;
    height = so.getWorldDimension().height / blockSize;
    stringMap = new String[height][width];

    charMapping = so.getModel().getCharMapping();
    invertMapping();
  }

  // -------------------------------------------------------------------------------------------------------------------
  // -------------------------------------------------------------------------------------------------------------------

  private String getState() {
    StringBuilder state = new StringBuilder();
    for (int i = 0; i < height; i++) {
      for (int j = 0; j < width; j++) {
        state.append(stringMap[i][j]);//.append(" ");
      }
      state.append("\n");
    }
    state.deleteCharAt(state.length()-1); // Remove last \n

    return state.toString();
  }


  private void writeLevel() {
    String state = getState();

    try (BufferedWriter bf = new BufferedWriter(new FileWriter("../level.txt"))) {
      bf.write(state);
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  private void parseState() {
    // Get values
    for (int i = 0; i < height; i++) {
      for (int j = 0; j < width; j++) {
        if (map[j][i].size() > 0) {
          int itype = map[j][i].get(0).itype; // GVGAI gives the observationGrid rotated
          stringMap[i][j] = levelMapping.get(VGDLRegistry.GetInstance().getRegisteredSpriteKey(itype));
        }
        else {
          stringMap[i][j] = levelMapping.get("background");
        }
      }
    }
  }

  private void parseGameData() {

  }

  // Invert charMapping to fill levelMapping
  private void invertMapping() {
    // TODO: OPTIMIZE
    for (Map.Entry<Character, ArrayList<String>> entry : charMapping.entrySet()) {
      levelMapping.put(entry.getValue().get(entry.getValue().size()-1), entry.getKey().toString());
    }
  }

  @Override
  public Types.ACTIONS act (StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
    Types.ACTIONS action;
    map = stateObs.getObservationGrid();

    if (actions.isEmpty()) {
      try {
        System.out.println("Replanning");
        replanning();
      } catch (IOException e) {
        e.printStackTrace();
      }

      parseState();
      writeLevel();
    }

    action = actions.get(0);
    actions.remove(0);

    return action;
  }

  String levelPath = "replanning/level.txt";
  String gamePath = "replanning/game.txt"; // Parsearlo de un archivo
  String domainPath = "replanning/domain.hpdl";
  String problemPath = "replanning/problem.hpdl";

  private void parseActions(ArrayList<String> input) {
    for (String action : input) {
      if (action.contains("AVATAR")) {
        action = action.substring(8);
        String[] split = action.split(" ");
        if (split.length == 2) {
          String act = split[0].replace("(AVATAR_", "");

          switch (act) {
            case "MOVE_UP":
            case "TURN_UP":
              actions.add(Types.ACTIONS.ACTION_UP);    break;
            case "MOVE_DOWN":
            case "TURN_DOWN":
              actions.add(Types.ACTIONS.ACTION_DOWN);  break;
            case "MOVE_LEFT":
            case "TURN_LEFT":
              actions.add(Types.ACTIONS.ACTION_LEFT);  break;
            case "MOVE_RIGHT":
            case "TURN_RIGHT":
              actions.add(Types.ACTIONS.ACTION_RIGHT); break;

            case "USE":  actions.add(Types.ACTIONS.ACTION_USE);  break;
            // case "NIL":  actions.add(Types.ACTIONS.ACTION_NIL);  break;
            default: actions.add(Types.ACTIONS.ACTION_NIL);  break;
          }
        }
      }
    }
  }

  private void replanning() throws IOException {
    String[] commands = {"make", "replan", "gi="+gamePath, "li="+levelPath, "go="+domainPath, "lo="+problemPath};
    //String[] commands = {"ls"};
    String [] envp = { };
    File dir = new File("../../");
    Process proc = Runtime.getRuntime().exec(commands, envp, dir);

    BufferedReader stdInput = new BufferedReader(new
            InputStreamReader(proc.getInputStream()));

    BufferedReader stdError = new BufferedReader(new
            InputStreamReader(proc.getErrorStream()));

    // Read the output from the command
    String s = null;
    ArrayList<String> input = new ArrayList<>();
    ArrayList<String> error = new ArrayList<>();
    while ((s = stdInput.readLine()) != null) {
      input.add(s);
    }

    parseActions(input);

    // Read any errors from the attempted command
    while ((s = stdError.readLine()) != null) {
      error.add(s);
    }
  }
}