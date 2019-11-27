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
 * Created by oscar@decsai.ugr.es: jue 24 nov, 2005  05:19
 * Last modified: jue 24 nov , 2005  05:19
 * ********************************************************************************** */

#include "oldDecision.hh"

OldDecision::OldDecision(const StackNode * st, const TaskNetwork * tn){
    // Obtener cual es la tarea que se decidió expandir en este nodo
    const Task * t;

    primitive = true;
    method_id = -1;
    if(st->taskid != -1 && st->taskid < tn->getNumOfNodes()){
	t = (*(st->offspring))[st->task];	
	task_selected = new TaskHeader(t->getId(),t->getMetaId(),t->getParameters());
	if(!t->isPrimitiveTask()){
	    primitive = false;
	    const Method * m = (*(st->methods))[st->mpos];
	    method_id = m->getMetaId();
	}
	const Unifier * uf = 0;
	if (st->utable)
	    uf = st->utable->getUnifierAt(st->unif);
	if(uf)
	    u = uf->clone();
	else
	    u = 0;
    }
    else
	task_selected = 0;

};

OldDecision::~OldDecision(void){
    if(task_selected)
	delete task_selected;
    if(u)
	delete u;
};

void OldDecision::print(ostream * os, int tab) const {
    string t(' ',tab);

    *os << t << "Expanding task:" << endl;
    if(task_selected){
	if(primitive){
	    *os << "Primitive: ";
	    task_selected->print(os);
	}
	else{
	    *os << "Compound: ";
	    task_selected->print(os);
	    *os << "Method: " << method_id << endl;
	}
	if(u)
	    u->print(os);
    }
    else 
	*os << "none" << endl;
};

