/* 
  Ignacio Vellido Expósito
  GVGAI agent with HTN replanning for the games Sokoban, Brainman, Aliens and
  Boulderdash
*/

package main;

import java.io.*;
import java.util.*;

import core.game.StateObservation;
import core.player.AbstractPlayer;
import core.vgdl.VGDLRegistry;
import ontology.Types;
import tools.ElapsedCpuTimer;

public class Agent extends AbstractPlayer {

  private ArrayList<Types.ACTIONS> actions = new ArrayList<>();

  // Level grid
  private ArrayList<core.game.Observation>[][] map;
  private String[][] stringMap;
  private int width, height;

  // LevelMapping
  HashMap<Character, ArrayList<String>> charMapping;
  HashMap<String, String> levelMapping = new HashMap<>();

  // Needed for calling the planner
  String levelOutputPath = "../tmp/level.txt",
         levelPath = "replanning/tmp/level.txt",
         gamePath = "replanning/tmp/game.txt",
         domainPath = "replanning/tmp/domain.hpdl",
         problemPath = "replanning/tmp/problem.hpdl";

  String avatarName; // Name of the avatar in the output of Siadex

  // ---------------------------------------------------------------------------

  public Agent (StateObservation so, ElapsedCpuTimer elapsedTimer) {
    // Set level dimensions
    int blockSize = so.getBlockSize(); // Sprite size in pixels
    width = so.getWorldDimension().width / blockSize;
    height = so.getWorldDimension().height / blockSize;
    stringMap = new String[height][width];

    charMapping = so.getModel().getCharMapping();

    // Change 'floor' to 'background' in the values
    charMapping.forEach( (k,v) -> {
      v.replaceAll(s -> {
        if (s.equals("floor")) {
          s = "background";
        }
        return s;
      });
    });

    // If "floor"/"background" is at the beggining
    boolean invert = true;
    Collection<ArrayList<String>> values = charMapping.values();
    Object[] toArray = values.toArray();
    ArrayList values1 = (ArrayList) toArray[0],
              values2 = (ArrayList) toArray[1];

    if (!values1.get(0).equals(values2.get(0))) { // UNSAFE OPERATION
      invert = false;
    }

    invertMapping(invert);
  }

  // ---------------------------------------------------------------------------
  // ---------------------------------------------------------------------------

  @Override
  public Types.ACTIONS act (StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
    Types.ACTIONS action;
    map = stateObs.getObservationGrid();

    // If no actions saved
    if (actions.isEmpty()) {
      parseState();
      writeLevel();

      try {
        System.out.println("\nReplanning");
        replanning();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }

    action = actions.get(0);
    actions.remove(0);

    return action;
  }

  // ---------------------------------------------------------------------------
  // ---------------------------------------------------------------------------

  /**
   * @return The current level state as a unique String
   */
  private String getState() {
    StringBuilder state = new StringBuilder();
    for (int i = 0; i < height; i++) {
      for (int j = 0; j < width; j++) {
        state.append(stringMap[i][j]);
      }
      state.append("\n");
    }
    state.deleteCharAt(state.length()-1); // Remove last \n

    return state.toString();
  }

  // ---------------------------------------------------------------------------

  /**
   * Transform the current observationGrid into string (of values in the levelMapping)
   */
  private void parseState() {
    // Get values
    for (int i = 0; i < height; i++) {
      for (int j = 0; j < width; j++) {
        String key;

        if (map[j][i].size() > 0) {
          int itype = map[j][i].get(0).itype; // GVGAI gives the observationGrid rotated
          key = VGDLRegistry.GetInstance().getRegisteredSpriteKey(itype);

          if (key.equals("floor")) {
            key = "background";
          }
        }
        else {
          key = "background";
        }

        stringMap[i][j] = levelMapping.get(key);
      }
    }
  }

  // ---------------------------------------------------------------------------

  /**
   * Fills levelMapping with the characters associated to each map
   */
  private void invertMapping(Boolean invert) {
    charMapping.forEach((key, value) -> {
      if (invert) {
        levelMapping.put(value.get(value.size() - 1), key.toString());
      } else {
        levelMapping.put(value.get(0), key.toString());
      }
    });
  }

  // ---------------------------------------------------------------------------

  /**
   * Parses plan output into agent actions
   * @param input Siadex plan output
   */
  private void parseActions(ArrayList<String> input) {
    for (String action : input) {
      if (action.contains("AVATAR")) {
        action = action.substring(8);
        String[] split = action.split(" ");

        // If it is an avatar action
        if (split.length == 2
                || (split.length == 3 && split[2].contains("partner"))) {
          String act = split[0].replace("(AVATAR_", "");
          System.out.println("Adding action: " + act);

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
            case "NIL":  actions.add(Types.ACTIONS.ACTION_NIL);  break;
            default: System.out.println(act + " is a not an available action for the avatar");
                     break; // An non-avatar action passed through
          }
        }
      }
    }
  }

  // ---------------------------------------------------------------------------
  // ---------------------------------------------------------------------------

  private void replanning() throws IOException {
    String[] commands = {"make", "replan",
                         "gi="+gamePath, "li="+levelPath,
                         "go="+domainPath, "lo="+problemPath},
             envp = { };
    File dir = new File("../../");
    Process proc = Runtime.getRuntime().exec(commands, envp, dir);

    // Get inputs
    BufferedReader stdInput = new BufferedReader(new
            InputStreamReader(proc.getInputStream()));
    BufferedReader stdError = new BufferedReader(new
            InputStreamReader(proc.getErrorStream()));

    // Transform inputs into strings
    String s;
    ArrayList<String> input = new ArrayList<>();
    ArrayList<String> error = new ArrayList<>();

    while ((s = stdInput.readLine()) != null) {
      input.add(s);
    }
    while ((s = stdError.readLine()) != null) {
      error.add(s);
    }

    // Check for errors
    if (!error.isEmpty() && error.contains("Error")) {
      System.out.println(error.toString());
    }

    // Get the avatar actions
    parseActions(input);
  }

  // ---------------------------------------------------------------------------

  /**
   * Writes the actual level state in a file
   */
  private void writeLevel() {
    String state = getState();

    try (BufferedWriter bf = new BufferedWriter(new FileWriter(levelOutputPath))) {
      bf.write(state);
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}