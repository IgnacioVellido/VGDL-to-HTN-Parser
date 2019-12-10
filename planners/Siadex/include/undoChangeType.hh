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

/* *************************************************************************************
 * Created by oscar@decsai.ugr.es: mié 23 nov, 2005  12:29
 * Last modified: vie 24 feb, 2006  11:49
 * ********************************************************************************** */

#ifndef UNDOCHANGETYPE_HH
#define UNDOCHANGETYPE_HH
#include <vector>
#include "undoElement.hh"
#include "type.hh"
#include "constants.hh"

using namespace std;

class TypeChangeable
{
    public:
	virtual ~TypeChangeable() {};
	virtual vctype * getTypeRef(void)=0;
};

/**
 * Esta clase trata de almacenar la información necesaria para
 * poder deshacer los cambios realizados sobre los tipos de un
 * determinado objeto.
 */
class UndoChangeType: public UndoElement 
{
    public:
        vctype types;
        TypeChangeable * target;

        virtual void undo(void) 
        {
            vctype * ref = target->getTypeRef();
	    ref->clear();
            for_each(types.begin(),types.end(),AddV<Type>(ref));
        };

        UndoChangeType(TypeChangeable * target) {this->target= target;};

        UndoChangeType(TypeChangeable * target, const vctype * v) :types(*v) {this->target= target;};

        virtual ~UndoChangeType(void) {types.clear();};

        virtual void setTarget(void * t) {target = (TypeChangeable *)t;};

        virtual void * getTarget(void) const {return target;};

        virtual void print(ostream * os) const
        {
	    typecit i, e;
	    *os << "[" << target << " ";
	    e = types.end();
	    for(i = types.begin(); i!= e; i++) 
	    {
		*os << (*i)->getName() << " ";
	    }
	    *os << "]" ;
        }

	virtual bool isUndoTypeValue(void) const {return true;};

	virtual UndoElement * clone(void) const {return new UndoChangeType(target,&types);};

	virtual void toxml(XmlWriter * writer) const{
	    writer->startTag("changeType")
		->endTag();
	};
};

#endif
