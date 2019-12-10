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
 * Created by oscar oscar@decsai.ugr.es: mar 30 ago, 2005  10:48
 * Last modified: mié 22 feb, 2006  11:00
 * ************************************************************** */

#ifndef ANDEFFECT_HH
#define ANDEFFECT_HH

#include "constants.hh"
#include <vector>
#include "containerEffect.hh"
#include "unifierTable.hh"
#include "termTable.hh"

using namespace std;

class AndEffect : public ContainerEffect
{
    public:
	AndEffect(void) :ContainerEffect() {};

	AndEffect(const AndEffect * ae);

	inline effectcit getBegin(void) const {return effects.begin();}; 

	inline effectcit getEnd(void) const {return effects.end();}; 

	inline int size(void) const {return effects.size();};

	void clear(void);

	virtual void addEffect(const Effect * g) {assert(g!=0); effects.push_back((Effect *) g->clone());};

	virtual void addEffectByRef(Effect * g) {assert(g!=0); effects.push_back(g);};

	virtual bool isAndEffect(void) {return true;};

	virtual ~AndEffect(void);

	/**
	 * @brief Crea una copia exacta del objeto.
	 * @description Todos los herederos deben implementar este método.
	 */
	virtual Expression * clone(void) const;

	/**
	  @brief Imprime el contenido del objeto por la salida estandard.
	  @param indent el número de espacios a dejar antes de la cadena.
	  */
	virtual void print(ostream * os,int indent=0) const;

	virtual void toxml(XmlWriter * writer) const;

	virtual bool apply(State *sta, VUndo * undo, Unifier * uf);

	virtual pkey getTermId(const char * name) const;

	bool hasTerm(int id) const;

	virtual void renameVars(Unifier * u, VUndo * undo);

	virtual bool provides(const Literal *) const;

    private:
	vector<Effect *> effects;
};

#endif
