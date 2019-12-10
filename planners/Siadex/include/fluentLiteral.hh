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
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  10:14
 * Last modified: vie 24 feb, 2006  12:09
 * ************************************************************** */

#ifndef FLUENT_LITERAL_HH
#define FLUENT_LITERAL_HH

#include "constants.hh"
#include "literal.hh"
#include "evaluable.hh"
#include "state.hh"
#include "literaleffect.hh"
#include "problem.hh"

using namespace std;

class Function;

/**
 * Esta función representa a los llamados fluents en PDDL.
 * Un fluent es un literal de la forma (cabeza par1, ... , parn)
 * que tiene un comportamiento similar al de una variable.
 * Un ejemplo de fluent podría ser: (distancia granada motril)
 * que contendría el valor 50.
 * Los fluent literals pueden ser resueltos al evaluarse de tres formas:
 * - Mediante un axioma.
 * - Mediante un fluent almacenado en el estado.
 * - Usando una definición Python.
 */
class FluentLiteral: public Evaluable, public Literal 
{
    public:
	FluentLiteral(const FluentLiteral * o) :Evaluable(o), Literal(o) {};
	FluentLiteral(int id, int mid) :Evaluable(), Literal(id,mid) {};
	virtual ~FluentLiteral(void) {};
	virtual Evaluable * cloneEvaluable(void) const;
	virtual Literal * cloneL(void) const;
	virtual void printEvaluable(ostream * os, int indent=0) const;
	virtual void vcprint(ostream * os, int indent=0) const {printEvaluable(os,indent);};
	virtual void toxmlEvaluable(XmlWriter * writer) const;
	virtual pkey compGetTermId(const char * name) const;
	virtual bool compHasTerm(int id) const;
	virtual void compRenameVars(Unifier * u, VUndo * undo);
	virtual pkey eval(const State* sta, const Unifier* u) const {return eval(sta,u,0);};
	virtual pkey evaltp(const State* sta, const Unifier* u, pkey * tp, bool * pol) const;
	virtual pkey eval(const State* sta, const Unifier* u, Function ** f) const;
	virtual bool isType(const Type * t) const;
	virtual const char * toString(void) const {static string s; ostringstream os; printEvaluable(&os,0); s = os.str(); return s.c_str();}; 
	virtual void printL(ostream * os, int indent=0) const {printEvaluable(os,indent);};
	virtual void toxmlL(XmlWriter * writer) const {toxmlEvaluable(writer);};
	virtual bool getPol(void) const {return true;};
	virtual void setPol(bool t){};
	virtual void vctoxml(XmlWriter * w) const {toxmlL(w);};
	virtual bool isFluentLiteral(void) const {return true;}; 
};

#endif
