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
 * Created by oscar@decsai.ugr.es: mié 22 feb, 2006  11:01
 * Last modified: mié 22 feb, 2006  11:02
 * ********************************************************************************** */

#ifndef WHENEFFECT_H
#define WHENEFFECT_H

#include "constants.hh"
#include <assert.h>
#include "effect.hh"
#include "state.hh"
#include "goal.hh"
#include "effect.hh"
#include "unifierTable.hh"

using namespace std;

class State;

class WhenEffect : public Effect
{
    public:

	/**
	  @brief Constructor.
	  */
	WhenEffect(const WhenEffect *eff);
	WhenEffect(Goal *g, Effect *eff);

	/**
	  @brief Devuelve el objetivo del when.
	  */
	inline Goal * getGoal(void) const {return goal;};

	/**
	  @brief Devuelve el efecto del when.
	  */
	inline Effect * getEffect(void) const {return effect;};

	/**
	  @brief Edita el objetivo del when.
	  @param g el nuevo objetivo.
	  */
	inline void setGoal(Goal * g) {goal = g;};

	/**
	  @brief Edita el efecto del when.
	  @param e el nuevo efecto.
	  */
	inline void setEffect(Effect * e) {effect = e;};

	/**
	  @brief Destructor
	  */
	virtual ~WhenEffect(void);

	virtual bool isWhenEffect(void) const {return true;};

	/**
	  @brief realiza una copia exacta a this.
	  */
	virtual Expression * clone(void) const;

	/**
	  @brief Imprime el contenido del objeto.
	  @param indent el número de espacios a dejar antes de la cadena.
	  @param os Un flujo de salida por defecto la salida estandard.
	  */
	virtual void print(ostream * os, int nindent=0) const;

	virtual void toxml(XmlWriter * writer) const;

	virtual pkey getTermId(const char * name) const;

	virtual bool hasTerm(int id) const;

	virtual void renameVars(Unifier * u, VUndo * undo);

	virtual bool apply(State *sta, VUndo * u, Unifier * uf);

	virtual bool provides(const Literal*) const;

    protected:

	/**< @brief Estructura del when: (when <goal> <effect>) */

	Goal *goal;         /**< @brief Objetivo que debe cumplirse para aplicar el efecto */
	Effect *effect;     /**< @brief Efecto a aplicar si se cumple el objetivo */
};

#endif
