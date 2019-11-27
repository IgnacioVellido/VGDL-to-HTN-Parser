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
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  09:39
 * Last modified: mié 22 feb, 2006  01:25
 * ************************************************************** */

#ifndef FLUENT_OPERATOR_HH
#define FLUENT_OPERATOR_HH

#include "constants.hh"
#include "domain.hh"
#include "evaluable.hh"

using namespace std;

enum Operation {OADD,OSUBSTRACT,OTIMES,ODIVIDE,UABS,USQRT,OPOW};

/**
 * Esta clase representa las operaciones aritméticas binarias que
 * se llevan a cabo entre dos expresiones de tipo numérico.
 */
class FluentOperator: public Evaluable
{
    public:
	FluentOperator(Operation o) :Evaluable() {first=0;second=0;op=o;tnumber = parser_api->domain->getModificableType(0);};

	FluentOperator(const FluentOperator * other);

	/**
	  @brief establece el primer elemento para hacer la operación
	  */
	virtual void setFirst(Evaluable* first) {this->first = first;};

	/**
	  @brief establece el segundo elemento para hacer la operación
	  */
	virtual void setSecond(Evaluable* second) {this->second = second;};

	/**
	  @brief establece el primer elemento para hacer la operación
	  */
	virtual const Evaluable*  getFirst(void) const {return first;};

	/**
	  @brief establece el segundo elemento para hacer la operación
	  */
	virtual const Evaluable* getSecond(void) const {return second;};

	virtual void setOperator(Operation o) {op = o;};

	virtual Operation getOperator(void) const {return op;};

	const char * printOp(Operation c) const;

	void printEvaluable(ostream * os, int indent) const;

	void toxmlEvaluable(XmlWriter * writer) const;

	void compRenameVars(Unifier * u, VUndo * undo);

	bool compHasTerm(int id) const;

	pkey compGetTermId(const char * name) const;

	Evaluable * cloneEvaluable(void) const;

	virtual pkey eval(const State * state, const Unifier * u) const;

	virtual pkey evaltp(const State * state, const Unifier * u, pkey * tp, bool * p) const;

	virtual bool isType(const Type * t) const {return tnumber->isSubTypeOf(t);};

    protected:
	/** El primer operando */
	Evaluable * first;
	/** El segundo operando */
	Evaluable * second;
	/** El operador */
	Operation op;
	/** El tipo resultante de la operacion (numerico) */
	const Type * tnumber;
};
#endif
