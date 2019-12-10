/*  ************************************************************************************
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

/* **************************************************************
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  10:23
 * Last modified: mié 22 feb, 2006  10:55
 * ************************************************************** */

#ifndef BOUNDGOAL
#define BOUNDGOAL

#include "fluentVar.hh"
#include "goal.hh"

using namespace std;

/**
 * Esta construcción no es parte del PDDL standard. Sirve para en las preconduciones
 * forzar la unificación de una variable con una expresión.
 */
class BoundGoal: public Goal
{
    public:
	BoundGoal(void) :Goal() {};
	BoundGoal(FluentVar * v, Evaluable * e) :Goal() {var=v; exp=e;};
	BoundGoal(const BoundGoal * o); 
	virtual ~BoundGoal(void) {delete var; delete exp;};

	virtual bool isBoundGoal(void) const {return true;};
	virtual Expression * clone(void) const;
	virtual UnifierTable * getUnifiers(const State * state, const Unifier * context, bool inheritPolarity,  pair<unsigned int,unsigned int> * protection) const;
	virtual bool isReachable(ostream * err, bool pol) const;
	virtual void renameVars(Unifier*, VUndo*);
	virtual pkey getTermId(const char*) const;
	virtual bool hasTerm(int) const;
	virtual void print(ostream*, int) const;
	virtual void toxml(XmlWriter * writer) const;

    protected:
	FluentVar * var;
	Evaluable * exp;
};

#endif
