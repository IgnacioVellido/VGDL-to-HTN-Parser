/* ****************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

#ifndef TASKNETWORK_HH
#define TASKNETWORK_HH

#include "constants.hh"
#include "task.hh"
#include "taskheader.hh"
#include "primitivetask.hh"
#include <assert.h>
#include <vector>
#include <sstream>
#include "unifier.hh"
#include "xmlwriter.hh"

using namespace std;

typedef vector<Task *> TaskList;
typedef pair<string,int> str2intPair;
typedef vector<vector<int>*>::iterator intvvit;
typedef vector<vector<int>*>::const_iterator intvvcit;
typedef vector<int>::iterator intvit;
typedef vector<int>::reverse_iterator intvrit;
typedef vector<int>::const_reverse_iterator intvrcit;
typedef vector<int>::const_iterator intvcit;
typedef TaskList::const_iterator tasklistcit;
typedef TaskList::iterator tasklistit;

class TaskNetwork : public Unifiable {
public:

  /**
     @brief Destructor
  */
  virtual ~TaskNetwork(void);

  /*!
   * Constructor por defecto.
   */
  TaskNetwork(void);

  /**
   * Construye una red de tareas a partir de un vector
   * de tareas dado. Las puede construir secuencialmente
   * o en paralelo.
   \param vt el vector de tareas
   \param parallel construirlas en paralelo o no
   */
  TaskNetwork(vector<Task *> * vt, bool parallel);

  /*!
   Construye una red de tareas con una sola tarea
   la dada como argumento
   \param t la tarea
   */
  TaskNetwork(Task * t);

  /*!
   * Constructor de copia.
   * \param other red de tareas a clonar.
   */
  TaskNetwork(const TaskNetwork * other);

  /**
    @brief Añade una nueva tarea a la red de tareas.
    @param t Puntero a la tarea
    \deprecated
   */
  int addTask(Task *t);

  /**
    @brief Tras construir la red de tareas con los métodos addTask y link
    es necesario llamar a este método para que fije los puntos de inicio
    y de fin (nodos falsos antes de las primeras tareas y después de las
    últimas)
    \deprecated
  */
  void fixTaskNetwork(void);

  /*!
   * Une con this la red de tareas dada como argumento, de forma secuencial.
   * No se realiza ningún tipo de clonación, por lo que hay que mantener
   * un especial cuidado al utilizar las estructuras de datos de other, que
   * serán destruidas.
   * @param other la red de tareas a unir
   */
  void join(TaskNetwork * other);

  /*!
   * Une con this la red de tareas dada como argumento, de forma paralela.
   * No se realiza ningún tipo de clonación, por lo que hay que mantener
   * un especial cuidado al utilizar las estructuras de datos de other, que
   * serán destruidas.
   * \param other la red de tareas a unir
   */
  void merge(TaskNetwork * other);

  /**
    @brief Devuelve una tarea a partir de su índice.
    El índice no puede estar fuera de rango o el programa abortara
  */
  inline const Task * getTask(int index) const {assert(index > -1 && index < (int) tasklist.size()); return tasklist[index];};

  inline Task * getModificableTask(int index)  {assert(index > -1 && index < (int) tasklist.size()); return tasklist[index];};

  /**
    @brief Devuelve un iterador al primer elemento de la tabla tasklist
  */
  inline tasklistcit getBeginTask(void) const {return tasklist.begin();};

  /**
    @brief Devuelve un iterador uno después del último elemento de la
    tabla tasklist
  */
  inline tasklistcit getEndTask(void) const {return tasklist.end();};

  /**
    @brief Devuelve un iterador al primer elemento de la tabla tasklist
  */
  inline tasklistit getModificableBeginTask(void) {return tasklist.begin();};

  /**
    @brief Devuelve un iterador uno después del último elemento de la
    tabla tasklist
  */
  inline tasklistit getModificableEndTask(void) {return tasklist.end();};

  /**
    @brief Devuelve la tarea apuntada por el iterador
  */
  inline const Task * getTask(tasklistcit i) const {return (*i);};

  /**
    @brief Devuelve la tarea apuntada por el iterador
  */
  inline const Task * getTask(tasklistit i) const {return (*i);};

  /**
    @brief Devuelve true si la tarea A se realiza inmediatamente despues que la B
  */
  inline bool inmediatelyAfter(int taskA, int taskB) const {intvcit e = succ[taskB]->end(); for(intvcit i = succ[taskB]->begin();i != e; i++) if((*i) == taskA) return true; return false;};

  /**
    @brief Devuelve true si la tarea A se realiza inmediatamente antes que la B
  */
  inline bool inmediatelyBefore(int taskA, int taskB) const {intvcit e = pred[taskB]->end(); for(intvcit i = pred[taskB]->begin();i != e; i++) if((*i) == taskA) return true; return false;};

  /**
    @brief Devuelve true si la tarea A se realiza inmediatamente despues que la B, las inline son ignoradas
  */
  bool iAfter(int taskA, int taskB) const;

  /**
    @brief Devuelve true si la tarea A se realiza inmediatamente antes que la B
  */
  bool iBefore(int taskA, int taskB) const;

  /**
    @brief Enlaza las tareas A y B (A antes que B)
  */
  inline void link(int taskA, int taskB) {succ[taskA]->push_back(taskB); pred[taskB]->push_back(taskA);};

  /**
    @brief Reemplaza una cabecera de tarea por una tarea primitiva.
    @param indexTask el índice de la tarea abstracta que se desea sustituir.
    @param newTask La tarea primitiva que se pasa, tener en cuenta de que NO se
    clona, sin embargo this, la libera al destruirse, con lo que hay que tener
    un especial cuidado. Lo que se intenta es evitar clonaciones que realmente
    no son necesarias.

    El algoritmo hace lo siguiente.
    1. Invalida la entrada indexTask de las tablas de sucesores y de predecesores.
    2. Añade newTask a la lista de tareas, se crea una entrada en todas las tablas para
    la nueva tarea.
    3. Se añaden los sucesores y predecesores de indexTask a newTask.
    4. En added y deleted se guardan los datos necesarios para poder deshacer posteriormente
    los cambios. Estos dos vectores deben estar reservados antes de hacer la llamada.
  */
   void replacePrimitive(int indexTask, PrimitiveTask * newTask, vector<pair<int,bool> > * agenda, vector<pair<bool,pair<int,int> > > * added, vector<pair<bool,pair<int,int> > > * deleted);

  /**
    @brief Reemplaza una cabecera de tarea por una red de tareas.
    La fusión de la red de tareas, automáticamente
    mueve índices y asigna enlaces.
    @param indexTask El índice del TaskHeader que queremos sustituir.
    @param newTN la nueva red de tareas a poner en lugar de indexTask.
  */
   void replaceTN(int indexTask, TaskNetwork * newTN, vector<pair<int, bool> > * agenda, vector<pair<bool,pair<int,int> > > * added, vector<pair<bool,pair<int,int> > > * deleted);

   /**
     @brief esta es la función inversa al replace de las tareas primitiva y compuesta. Deshace
     la última sustitución en la red de tareas.
    */
   void undoReplace(int oldsize, vector<pair<bool,pair<int,int> > > * lAdded, vector<pair<bool,pair<int,int> > > * lDeleted);

  /**
    @brief Devuelve el número de nodos en la matriz de tareas
  */
  inline int getNumOfNodes(void) const {return tasklist.size();};

  /**
    @brief imprime la matriz de adyacencia
  */
  void print(ostream * os, int indent=0);

  void print(ostream * out, int tid, int nindent) const;

  void print(ostream * out, int tid, int nindent);

  void print(ostream * out, int id_root, int id_limit, int nindent) const;

  bool hasThisSuccesor(int id_root, int s) const;

  vector <int> getConvergenceNodes(int id_root, int id_limit) const;

  int getLastConvergenceNode(int id_root, int id_limit) const;

  bool isFirstSuccesor(int i, vector<int> convergence_nodes) const;

  bool allFathersPrinted(int tid) const;

  void printArc(ostream *out, int origin, int destiny, int nindent);

  void toxml(ostream * os, bool primitives = true, bool compound=false, bool inlines=false) const;

  void toxml(XmlWriter * writer, bool primitives= true, bool compound=false, bool inlines=false) const;

  void printConstraints(int nindent, ostream * out) const;

  void printUnifyTask(const char * name, const vector<Term *> * args, ostream * out) const;

  void printAgenda(ostream * out, int nindent, const vector<pair<int,bool> > * agenda) const;

  void printDebug(ostream * out) const;

  /**
    @brief Crea una agenda a partir de esta red de tareas
    Para que el algoritmo funcione, deja los argumentos por defecto en la
    primera llamada.
  */
  int initializeAgenda(vector<pair<int,bool> > * agenda, int node) const;

  /**
    @brief Realiza una copia exacta de la red de tareas.
    La copia no debe compartir memoria de estructuras de datos con this.
  */
  TaskNetwork * clone(void) const;

  virtual pkey getTermId(const char * name) const;

  bool hasTerm(int id) const;

  virtual void renameVars(Unifier * u, VUndo * undo);

  inline intvit getPredBegin(int pos) const {return pred[pos]->begin();};

  inline intvit getPredEnd(int pos) const {return pred[pos]->end();};

  inline intvit getSuccBegin(int pos) const {return succ[pos]->begin();};

  inline intvit getSuccEnd(int pos) const {return succ[pos]->end();};

  inline intvrcit getSuccRBegin(int pos) const {return succ[pos]->rbegin();};

  inline intvrcit getSuccREnd(int pos) const {return succ[pos]->rend();};

  tasklistcit searchLabel(const char * l, tasklistcit b, tasklistcit e) const;

  /** comprobar si todas las taskheaders que contiene la red de tareas, son
   alcanzables, es decir existe al menos una acción que me permite realizarla.
   changes indica que se han realizado cambios sobre la red de tareas.
   \param err es el flujo en el cual se generarán mensajes de error en el caso
   de que algún elemento no esté bien definiso.
  */
  bool isWellDefined(ostream * err, bool * changes) const;


  /** Quita los últimos n elementos de la red de tareas.
   Es útil cuando sabemos que los punteros a los que apunta  el resto de
   elementos de dicho vector han sido eliminados en otro lugar.
   (De uso interno)
   \param n el número de elementos a quitar por la cola
  */
  void clearLast(int n) {tasklist.erase(tasklist.end() -n, tasklist.end());};

  /**
   * Añade una precondición que será necesaria mantener por todos las
   * tareas pertenecientes a esta red de tareas.
   * \param g la precondición a mantener.
   */
//  void addMaintain(Goal * g);

  /*!
   * Devuelve si la tarea e se debe de ejecutar inmediatamente después
   * de la ejecución de sus predecesoras.
   * \param indice de la tarea
   */
  inline int isInmediate(int index) const {return inmediate[index];};

  /*!
   * Establece si la tarea se ejecuta inmediatamente despues de la
   * ejecución de sus predecesoras.
   * \param i, identificador de la tarea.
   * \param v por defecto true
   */
  inline void setInmediate(int i, bool v=true) {inmediate[i] = v;};

  /*!
   * Devuelve si la tarea index se puede o no paralelizar con respecto
   * a la tarea anterior
   * \param indice de la tarea
   */
  inline int isBTTask(int index) const {return backtracking[index];};

  /*!
   * Establece si la tarea se puede o no paralelizar con respecto a la
   * tarea anterior en la red de tareas.
   * \param i, identificador de la tarea.
   * \param v por defecto true
   */
  inline void setBTTask(int i, bool v=true) {backtracking[i] = v;};

  inline void makeAllBT(void) {fill(backtracking.begin(),backtracking.end(),true);};

  /*!
   * Devuelve true si la tarea con indice a se debe de ejecutar
   * antes que b en la red de tareas.
   * \param a el índice de la primera tarea
   * \param b el índice de la segunsa
   */
  bool before(int a, int b) const;

  /**
   * Devuelve el índice asociado a la tarea en la red de tareas.
   * @param t la tarea a buscar.
   * @return -1 si no se encuentra
   */
  int getIndexOf(const Task * t) const;

  /*
   * Pone nuevas restricciónes temporales sobre todas las tareas de la red de tareas.
   * @param v La restricciones a añadir.
   */
  void addTConstraint(TCTR & v);

  /**
   * No llamar a esta función a no ser que sepas lo que estas haciendo.
   * Esta función restaura la red de tareas hasta el estado en el que tenía
   * n elementos.
   * Esta función es llamada desde el undo
   */
  void restoreTo(int n);

  const vector<TCTR> * getTConstraints(int index) const;

protected:
  /**
   * Lista de tareas que forman parte de la red de tareas.
   * Las tareas que aparecen en esta lista no tienen porque estar siendo usadas
   * actualmente en la red de tareas. Pueden haber sido sustituidas en un paso
   * previo, en ese caso aparecerán marcadas como inválidas. */
  TaskList tasklist;
  /**
   * Este vector mantiene los índices de los sucesores de la tarea i-esima.
   * Los índices no coinciden exactamente con los usados en TaskNetwork::tasklist.
   * El índice 0 no se corresponde con ninguna tarea de las que se encuentran en
   * TaskNetwork::tasklist, tiene un significado especial los sucesores de 0 serán
   * aquellas tareas que no tienen ningún predecesor. Así pues el índice 1 se
   * corresponde con el índice 0 en TaskNetwork::tasklist
   */
  vector<vector<int> * > succ;
  /**
   * Es el vector de predecesores de una tarea. Es el inverso del vector de sucesores
   * ver TaskNetwork::pred para obtener información mas detallada.
   */
  vector<vector<int> * > pred;
  /**
   * Este vector marca las tareas como inmediatas.
   */
  vector<bool> inmediate;
  /**
   * Las tareas marcadas como inválidas (true) en este vector no deberán ser tenidas
   * en cuenta. Solo se mantienen por motivo de eficiencia al hacer el "undo"
   */
  vector<bool> invalid;
  /**
   * Este vector marca las tareas como paralelizables o no.
   */
  vector<bool> backtracking;
  /**
   * Una red de tareas puede tener una clausula maintain que actuará como una especie
   * de vínculo causal que debe mantener.
   * El índice i-esimo contendrá las precondiciones que se deben de mantener por la
   * tarea i-esima. Observar que tanto el vector, como los elementos que contienen
   * pueden ser null.
   */
//  vector< vector<Goal *> > * maintain;

  /**
   * Este vector almacena las restricciones sobre la duración de las tareas de la red de tareas.
   */
  vector<TCTR> tconstraints;
  /**
   * Aqui se almacenan las referencias a las restricciones. Si en la posición 0 aparecen por ejemplo
   * 1 y 2, significa que las tareas con id 1 y 2 de la red de tareas tienen la restricción indicada en
   * 0
   */
  vector<vector<int> * > constraintref;

private:
  static void printTable(ostream * out, const vector<vector<int> *> * v);

  /**
  * Nos indica si la tarea ha sido ya imprimida en el proceso de escritura a PDDL.
  */
  bool * writed;

  /**
  * Nos indica si han sido escritas las llaves para abrir y cerrar tareas paralelas.
  */
  bool * rightKey;
  bool * leftKey;

  /**
   * Esta función sirve para detectar posibles errores en la estructura de predecesores
   * y de sucesores, solo se usa para tareas de depuración.
   */
  void comprobarEstructura(void);

};

#endif
