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
 * Created by oscar@decsai.ugr.es: jue 24 nov, 2005  05:18
 * Last modified: jue 24 nov , 2005  05:18
 * ********************************************************************************** */
#ifndef OLDDECISION_HH
#define OLDDECISION_HH   

#include "constants.hh"
#include "stacknode.hh"

using namespace std;

typedef vector<Task *> VTask;
typedef vector<pair<int,int> > VODAgenda;

/**
 * Esta clase sirve para mantener la cuenta de las decisiones que se han llevado a
 * cabo con anterioridad y que pueden ser útiles para el proceso de replanificación.
 */
class OldDecision{
    public:
	/**
	 * @brief La información necesaria para mantener las decisiones que se
	 * realizaron con anterioridad se extrae del contexto que se utilizó
	 * durante la etapa de planificación.
	 */
	OldDecision(const StackNode * st, const TaskNetwork * tn);

	/**
	 * Destructor
	 */
	~OldDecision(void);

	void print(ostream * os, int tab=0) const;

	/** control de agenda primer punto de backtracking*/
	Task * task_selected;

	/** flag que dice si la tarea es o no primitiva */
	bool primitive;

	/** Si la tarea es compuesta el id del método que se expandió */
	int method_id;

	/** El unificador que se seleccionó */
	Unifier * u;
};

#endif /* OLDDECISION_HH */
