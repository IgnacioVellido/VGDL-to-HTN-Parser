/*  ************************************************************************************
 *  Copyright (C) 2003, 2004, 2005  Luis Castillo Vidal,  Juan Fernandez Olivares,
 *  Oscar Jesus Garcia Perez, Francisco Carlos Palao Reines.
 *
 * More information about SIADEX project:
 * http://siadex.ugr.es
 * siadexwww@decsai.ugr.es
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or any later version.
 *
 * Please cite the authors above in your publications or in your
 * software when you made use of this software.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 * ********************************************************************************** */

/* *************************************************************************************
 * Created by oscar@decsai.ugr.es: mié 09 nov, 2005  10:03
 * Last modified: mié 09 nov , 2005  10:03
 * ********************************************************************************** */

#ifndef REPLAN_HH
#define REPLAN_HH   

#include "constants.hh"
#include "selector.hh"
#include "oldDecision.hh"
#include <ext/slist>

typedef __gnu_cxx::slist<int> gislist; 

using namespace std;

class Problem;

#define eqpair(x,y) ((x).first == (y).first && (x).second == (y).second)

/**
 * Esta clase implementa el proceso de reparación de planes.
 */
class RePlan :public Selector{
    public:
	RePlan(Problem * prob) {setProblem(prob); maxDepth=0; seluni=-1;};

	~RePlan(void) {deleteOldDecisions();};

	/**
	 * Realiza una reparación del plan tras una unificación fallida.
	 * @param depth Es la profundidad a la que hay que reparar.
	 * @param uni Es la unificación que queremos forzar a tomar. -1 para
	 * probar todas las que quedan.
	 */
	bool repairUnification(int depth, int uni);

	inline void setProblem(Problem * p) {this->p=p;};

	// esta es la reimplementación de las funciones de toma de decisiones
	// para el proceso de planificación.
	virtual int selectUnification(State * state, const StackNode * sn, const TaskNetwork * tn, const TPlan * plan);

	virtual int selectFromAgenda(State * state, const StackNode * sn, const TaskNetwork * tn, const TPlan * plan);

	virtual int selectTask(State * state, const StackNode * sn, const TaskNetwork * tn, const TPlan * plan);

	virtual int selectMethod(State * state, const StackNode * sn, const TaskNetwork * tn, const TPlan * plan);

    protected:
	/** El objeto que contiene el plan a reparar */
	Problem * p;

	/** Mantiene un vector con las decisiones que se tomaron con anterioridad
	 * y que sirven de heurística para la búsqueda de un nuevo plan */
	vector<OldDecision *> oldDecisions;
	// El elemento de decisión que se corresponde con el nodo en evaluación
	OldDecision * tope;
	// Nodo que se está evaluando en el planificador
	StackNode * current;

	/**
	 * @brief Realiza sucesivos undos hasta llegar a la profundidad en la búsqueda dada como
	 * argumento. Devuelve un vector con los contextos que se han ido quitando de la
	 * pila de contextos.
	 * @return Devuelve true en caso de que no ocurra ningún error.
	 */
	bool undoUntilDepth(int depth);

	/**
	 * Mirar si la tarea y el th unifican
	 */
	bool match(const Task * t , const Task * th);

	gislist * searchNode(StackNode * n, vector<StackNode *> * l, int from);

	/**
	 * profundidad a partir de la cual se realizará la reparación. No se repara por
	 * encima de esta profundidad en la búsqueda.
	 */
	int maxDepth;

	/**
	 * Es la selección de unificación tomada para realizar la replanificación.
	 */
	int seluni;

	/**
	 * Este es el índice que controla en la lista de antiguos nodos por donde 
	 * vamos siguiendo el rastro de antes.
	 */
	int posOD;

	/**
	 * Borra el contenido del vector oldDeccisions
	 */
	void deleteOldDecisions(void);

	/**
	 * Compara las agendas de dos nodos en el espacio de búsqueda.
	 * Devuelve un número muy próximo a uno cuanto más parecidas sean.
	 * @param a primer nodo a comparar, se supone del plan en reaparación
	 * @param b el segundo nodo, se supone del plan antiguo
	 */
	double compareAgenda(StackNode * a, StackNode * b);

	/**
	 * El orden en el que se va llamando a los select.
	 * Sirve para determinar si se produjo algún backtracking.
	 */
	int orden;
};

#endif /* REPLAN_HH */
