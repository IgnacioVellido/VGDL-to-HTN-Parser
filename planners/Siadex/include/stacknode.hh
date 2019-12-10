/* ****************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

#ifndef STACKNODE_HH
#define STACKNODE_HH

#include "constants.hh"
#include <string>
#include <vector>
#include <list>
#include "method.hh"
#include "undoElement.hh"
#include "tcnm.hh"


using namespace std;

typedef vector<pair<int,bool> > VAgenda;
typedef vector<pair<bool,pair<int,int> > > VLinks;
typedef vector<Method *> VMethods;
typedef vector<VUndo *> VVUndo;

typedef vector<int>::iterator vintit;
typedef vector<int>::const_iterator vintcit;
typedef VLinks::const_iterator vlit;
typedef vector<pair<int,int> > VIntervals;

/** Tipo para almacenar los índices de la red de tareas que representan
 * las tareas que van a formar parte del plan. */
typedef list<int> TPlan;
typedef TPlan::iterator planite;
typedef TPlan::const_iterator plancite;


 /**
  * A grandes rasgos podemos distinguir la información que se guarda en un nodo de la pila
  * en dos grandes grupos información que mantiene el "estado actual (contexto)" e información
  * para poder volver al contexto anterior (información de undo)
  */
/*!
    Esta clase es de uso interno, almacena la información necesaria para poder hacer backtrack
    durante el proceso de búsqueda. El proceso de búsqueda en profundidad es "incremental", este
    nodo guarda información del incremento. Se guarda también en la clase información del contexto
    en el que queda la función Problem::solve para poder recuperarse correctamente tras un backtracking.\n
    Aunque por comodidad todos los miembros de la clase son públicos, se debe guardar especial
    cuidado con la alteración de los mismos.\n
    A grandes rasgos podemos distinguir los miembros de la clase StackNode que se almacenan en la pila
    Problem::Stack
    en dos grandes grupos información que mantiene el "estado actual (contexto)" e información
    para poder volver al contexto anterior (información de undo).
 */
class StackNode
{
    public:
	// -------------------------------------------------------------------
	// DECLARACIÓN DE VARIABLES
	// -------------------------------------------------------------------

	// INFORMACIÓN DE UNDO

        /*! estructura para guardar información sobre los vínculos cambiados en la
        red de tareas */
        VLinks lAdded;
        VLinks lDeleted;
        int oldsize;

        /*! estructura para hacer el "undo" de las unificaciones. */
        VUndo undoApply;

        /*! estructura para hacer el "undo" en la tabla de vínculos causales. */
        VUndo undoCL;

	/*! undo de las sustituciones de variables en las tareas */
        VVUndo undoTask;

	/// Undo para las decisiones tomadas contra el timeline

	/** Vector con las intersecciones calculadas en el timeline */
	VIntervals * intervals;

	/** Posición en la cual encontramos la última inersección válida */
	int tcnpos;

	/** Tope de la pila de la  red de tareas antes de aplicar las restricciones
	 * impuestas por el timeline */
	int tl_tcnStackSize;

	/** Tope de la pila de la red de tareas antes de aplicar
	 * cualquier restriccion*/
	int tcnStackSize;

	/*! estructura para guardar información sobre los cambios en el estado */
	VUndo stateChanges;

	// INFORMACIÓN DEL CONTEXTO ACTUAL

        /*! Agenda de tareas pendientes */
        VAgenda agenda;

	/// registro de tareas ya consideradas de la agenda
	VAgenda explored;

	// Se llega a este punto tras un backtracking
	bool backtrack;

        /*! La tarea que estoy expandiendo en la red de tareas */
        int taskid;

        /*! El nodo se ejecuta como inmediate */
        int inmediate;

        /*! Lista de tareas que han unificado y que aún quedan por expandir */
        vector<Task *> * offspring;

        /*! De esa lista de tareas, la tarea por la que voy */
        int task;

        /*! De esa lista de unificaciones ... por el que voy */
        int unif;

        /*! Lista de unificaciones encontradas para task */
        UnifierTable * utable;

        /*! Lista de métodos no expandidos si task es una tarea compuesta */
        VMethods * methods;

        /*! De la lista de métodos... por el que voy */
        int mpos;

        /*! Flag para controlar que no se caiga en un bucle infintio cuando una tarea no
           tiene precondiciones */
        bool done;

	/** Tamaño de la termtable */
	int ttsize;

	// -------------------------------------------------------------------
	// DECLARACIÓN DE FUNCIONES
	// -------------------------------------------------------------------

	// Inicializar las estructuras de datos.
        StackNode(void);

	/**
	 * Constructor de copia. Tener cuidado con él, no se debería usar si no sabes
	 * lo que estás haciendo. No realiza una copia completa del contexto. ¡OJO!, solo
	 * de los puntos de decisión.
	 */
	StackNode(const StackNode * o);

	StackNode(const VAgenda * a);

	// destructor del nodo
        ~StackNode(void);

	// --------------------------------------------------------------------
	// INFORMACIÓN DE UNDO
	// --------------------------------------------------------------------

	/*! Realiza el undo "completo" para retornar al contexto anterior, cuando
	 * no quedan mas opciones */
	void undo(TaskNetwork * tasknetwork, TPlan * plan);

	void undo(TaskNetwork * tasknetwork, TPlan * plan, STP * stp);

	/**
	 * Restaura todos los puntos de decisión como si todavía no se
	 * hubiese realizado ninguna selección.
	 */
	void restoreAllDP(void);

	/**
	 * Deshace los cambios provocados sobre la red de restricciones temporales
	 * @param l Si se deja a -1 (por defecto) se restaurará hasta el nivel guardado
	 * en la pila de contextos
	 */
	void undoSTP(STP * stp, int l=-1);

	// --------------------------------------------------------------------

	/// deshace los efectos producidos por una acción primitiva
	void undoEffects(void);

	void clearUndoEffects(void);
	// --------------------------------------------------------------------

	/// deshacer cambios sobre la red de tareas y el plan
	void undoTaskNetwork(TaskNetwork * tasknetwork, TPlan * plan);

	void clearUndoTaskNetwork(void);

	// --------------------------------------------------------------------
        void clearUndoApply(void);

	void undoApplyUnification(void);
	// --------------------------------------------------------------------

	// --------------------------------------------------------------------
        void clearUndoCL(void);

	void undoCLchanges(void);
	// --------------------------------------------------------------------

        void clearUndoTask(void);

	// t normalmente coincidirá con this->task
	void undoTaskSelection(int t);

	void undoPlan(TPlan * plan, TaskNetwork * tasknetwork);

	// --------------------------------------------------------------------
	// INFORMACIÓN DEL CONTEXTO ACTUAL
	// --------------------------------------------------------------------

	/// eliminar la tarea i-esima porque ya ha sido explorada
	void removeTask(int index);

	/// hacer una copia de la agenda
        void copyAgenda(const VAgenda * other) {if(other) agenda.insert(agenda.end(),other->begin(),other->end());};


};
#endif
