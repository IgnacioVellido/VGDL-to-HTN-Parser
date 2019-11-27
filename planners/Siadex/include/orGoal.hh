/* ************************************************************************************
 * Copyright (C) 2003, 2004, 2005  Luis Castillo Vidal,  Juan Fernandez Olivares,
 * Oscar Jesus Garcia Perez, Francisco Carlos Palao Reines.
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
 * Created by oscar@decsai.ugr.es: mié 22 feb, 2006  10:56
 * Last modified: mié 22 feb, 2006  10:56
 * ********************************************************************************** */

#ifndef ORGOAL_HH
#define ORGOAL_HH

#include "constants.hh"
#include <vector>
#include "containerGoal.hh"
#include "unifierTable.hh"
#include "termTable.hh"

using namespace std;

class OrGoal :public ContainerGoal
{
    public:
	   OrGoal(void) :ContainerGoal() {};

	   OrGoal(const OrGoal * ag);

           virtual ~OrGoal(void);
	
           inline goalcit getBegin(void) const {return goals.begin();}; 

           inline goalcit getEnd(void) const {return goals.end();}; 

           inline int size(void) const {return goals.size();};

           virtual void addGoal(const Goal * g) {assert(g!=0); goals.push_back((Goal *) g->clone());};

           virtual void addGoalByRef(Goal * g) {assert(g!=0); goals.push_back(g);};

           virtual bool isOrGoal(void) {return true;};

           /**
            * @brief Crea una copia exacta del objeto.
            * @description Todos los herederos deben implementar este método.
            * @author oscar
            */
           virtual Expression * clone(void) const;

           /**
             @brief Imprime el contenido del objeto por la salida estandard.
             @param indent el número de espacios a dejar antes de la cadena.
            */
           virtual void print(ostream * os, int indent=0) const;

           virtual void toxml(XmlWriter * writer) const;

           virtual UnifierTable * getUnifiers(const State * state, const Unifier * context, bool inheritPolarity, pair<unsigned int,unsigned int> * protection) const;

           virtual pkey getTermId(const char *) const;

           virtual bool hasTerm(int id) const;

           virtual void renameVars(Unifier * u, VUndo * undo);

	   virtual bool isReachable(ostream * err, bool inheritPolarity) const;

    protected:
        vector<Goal *> goals;
};

#endif
