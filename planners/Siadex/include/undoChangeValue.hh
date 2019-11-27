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
 * Created by oscar oscar@decsai.ugr.es: mi� 14 sep, 2005  06:37
 * Last modified: vie 03 mar, 2006  05:48
 * ************************************************************** */

#ifndef UNDOCHANGEVALUE_HH
#define UNDOCHANGEVALUE_HH

#include "constants.hh"
#include "undoElement.hh"
#include "termTable.hh"
#include "papi.hh"
#include "xmlwriter.hh"

using namespace std;
class UndoChangeValue;

struct SREQUAL
{
    UndoChangeValue * sr;
    SREQUAL(UndoChangeValue * base) {sr=base;};

    bool operator()(UndoChangeValue * o) const
    {
        return (sr == o);
    };
};

class ValueChangeable
{
    public:
	virtual void setVar(int pos, pkey &newval) {};
	virtual void vcprint(ostream * os, int nindent=0) const {};
	virtual ~ValueChangeable() {};
	virtual void vctoxml(ostream * os) const{
	    XmlWriter w(os);
	    vctoxml(&w);
	    w.flush();
	};
	virtual void vctoxml(XmlWriter * writer) const {};
};

/**
 * Esta clase almacena la informaci�n necesaria para deshacer los cambios
 * provocados sobre un elemento que puede contener valores, por ejemplo
 * una variable o un literal.
 */

class UndoChangeValue :public UndoElement
{
    public:
	// Posici�n en un vector o en cualquier otra estructura del valor
	// que hemos cabiado.
        int pos;
	// valor antiguo para restaurar.
        pkey val;
	// la clase objetivo que sufri� los cambios
        ValueChangeable *target;
	// valor por el que se cambi�.
	pkey new_val;

        virtual void undo(void);

        virtual  ~UndoChangeValue(void)
        {
            target= 0;
	    time = -1;
        }

        UndoChangeValue(ValueChangeable *target, int pos, pkey id, pkey newval) {
	    this->pos = pos;
	    this->val = id;
	    this->target=target;
	    this->new_val = newval;
	};

        UndoChangeValue(const UndoChangeValue * u) {
	    this->pos = u->pos;
	    this->val = u->val;
	    this->target= u->target;
	    this->new_val = u->new_val;
	    this->time = u->time;
	};

        virtual bool refers(int id) const {return (val.first == id);};

	virtual bool hasTarget(const ValueChangeable *t) {return t == target;};

        inline void applySubstitution(pkey ttsb)
        {
            target->setVar(pos,ttsb);
        };

        virtual void setTarget(void * t) {target = (ValueChangeable *) t;};

        virtual ValueChangeable * getTarget(void) const {return target;};

        virtual void print(ostream * os) const;

	virtual bool isUndoChangeValue(void) const {return true;};

	virtual UndoElement * clone(void) const {
	    return new UndoChangeValue(this);
	};

	virtual void toxml(XmlWriter * writer) const;

	// Instante de tiempo en el cual conseguimos el efecto
	// con respecto a la acci�n que gener� el efecto.
	float time;
};

typedef vector<UndoChangeValue *> VReferences;
typedef VReferences::const_iterator referencescit;
typedef VReferences::iterator referencesit;
#endif
