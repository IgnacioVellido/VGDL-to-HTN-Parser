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
 * Last modified: vie 24 feb, 2006  12:09
 * ********************************************************************************** */

#ifndef FORALLEFFECT_H
#define FORALLEFFECT_H

#include "constants.hh"
#include <assert.h>
#include "effect.hh"
#include "state.hh"
#include "header.hh"
#include "unifierTable.hh"

using namespace std;

class State;

class ForallEffect : public Effect, public ParameterContainer
{
    public:

        /**
          @brief Constructor.
         */
        ForallEffect(Effect *e);

        ForallEffect(Effect *e, const KeyList * p);

	ForallEffect(const ForallEffect * g);

	ForallEffect(void);

        /**
          @brief Devuelve el objetivo del forall.
         */
        inline Effect * getEffect() const {return effect;};

        /**
          @brief Edita el objetivo del forall.
          @param g el nuevo objetivo.
         */
        inline void setEffect(Effect * e) {effect = e;};

        /**
          @brief Destructor
         */
        virtual ~ForallEffect() {if(effect) delete effect;};

        virtual bool isForallEffect(void) const {return true;};

        /**
          @brief realiza una copia exacta a this.
         */
        virtual Expression * clone(void) const;

        /**
          @brief Imprime el contenido del objeto.
          @param indent el número de espacios a dejar antes de la cadena.
          @param os Un flujo de salida por defecto la salida estandard.
         */
        virtual void print(ostream * os, int indent=0) const;

        virtual void vcprint(ostream * os, int indent=0) const {print(os,indent);};

        virtual void toxml(XmlWriter * writer) const;

	virtual void vctoxml(XmlWriter * w) const {toxml(w);};

        virtual pkey getTermId(const char * name) const;

        bool hasTerm(int id) const;

        void renameVars(Unifier * u, VUndo * undo);

	virtual bool apply(State *sta, VUndo * undo, Unifier * uf);

	virtual bool provides(const Literal *) const;

    protected:

        Effect * effect;         /**< @brief Objetivo que deben cumplir en un estado todos los objetos
                              que tengan los mismos tipos que los parámetros del forall */

	bool assertl(State * sta, VUndo * u, Unifier * context, int pos, Unifier * uf);

};

#endif
