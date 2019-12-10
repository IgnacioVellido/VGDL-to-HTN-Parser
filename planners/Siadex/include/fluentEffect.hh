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
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  10:13
 * Last modified: mié 22 feb, 2006  10:42
 * ************************************************************** */

#ifndef FLUENTEFFECT
#define FLUENTEFFECT

#include "constants.hh"
#include "effect.hh"
#include "function.hh"
#include "evaluable.hh"
#include "fluentLiteral.hh"
#include "timeStamped.hh"

enum FOperation {FASSIGN,FSCALEUP,FSCALEDOWN,FINCREASE,FDECREASE};

/**
 * Esta clase define operaciones realizadas sobre objetos de tipo fluent
 * com el assign el increase o el decrease
 */
class FluentEffect: public Effect, public TimeStamped
{
    public:
	/**
	 * Constructor por defecto
	 */
	FluentEffect(FOperation o, FluentLiteral * fhead, Evaluable * fexp);

	/**
	 * El constructor de copia
	 */
	FluentEffect(const FluentEffect * fo);

	/**
	 * Destructor de la clase.
	 */
	virtual ~FluentEffect(void) {delete f; delete exp;}

	inline void setOperation(FOperation o) {op = o;};
	inline FOperation getOperation(void) {return op;};

	inline void setFunction(FluentLiteral * f) {this->f = f;};
	inline FluentLiteral * getFunction(void) {return f;};

	inline void setExpression(Evaluable * exp) {this->exp = exp;};
	inline Evaluable * getExpression(void) {return exp;};

	virtual bool isFluentEffect(void) const {return true;};
	virtual bool apply(State *sta, VUndo * u, Unifier * uf);
	virtual bool provides(const Literal *) const;

	virtual void print(ostream * out, int indent=0) const;
	virtual void toxml(XmlWriter * writer) const;
	virtual Expression * clone(void) const {return new FluentEffect(this);};

	virtual void renameVars(Unifier * u,VUndo * undo);
	virtual pkey getTermId(const char * name) const;
	virtual bool hasTerm(int id) const;

	virtual const char * printOperation(void) const;


    protected:
	// el operador a realizar
	FOperation op;
	// el literal sobre el que realizarlo
	FluentLiteral * f;
	// la expresion con cuyo resultado operaremos
	Evaluable * exp;
};

#endif
