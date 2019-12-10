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
 * Created by oscar oscar@decsai.ugr.es: lun 29 ago, 2005  05:42
 * Last modified: vie 24 feb, 2006  10:08
 * ************************************************************** */

#ifndef UNDOELEMENT
#define UNDOELEMENT

#include "constants.hh"
#include <iostream>
#include <vector>
#include "xmlwriter.hh"
using namespace std;

/**
 * Esta clase trata de servir de base para todas aquellas estructuras
 * de datos que mantienen información para durante el proceso de backtracking
 * deshacer los cambios que se hicieron sobre las ED al ir hacia adelante.
 * La información que hay que mantener es demasiado variopinta para que esta
 * clase base implemente mucha funcionalidad, lo que tratamos es intentar
 * disponer de una clase raíz para tratar de unificar toda la información.
 */

class UndoElement
{
    public:
	// Es interesante poder mostrar por pantalla el contenido de las
	// ED de undo. De esta forma se facilita la depuración
	virtual void print(ostream * os) const = 0;
	// Se supone que cada elemento almacena información suficiente para
	// poder hacer el undo por sí mismo sin necesidad de más parámetros.
	virtual void undo(void) = 0;

	virtual bool isUndoChangeValue(void) const {return false;};
	virtual bool isUndoTypeValue(void) const {return false;};
	virtual bool isUndoARLiteralState(void) const {return false;};
	virtual bool isUndoChangeProducer(void) const {return false;};
	virtual bool isUndoCLinks(void) const {return false;};
	virtual bool isUndoChangeTime(void) const {return false;};
	virtual ~UndoElement(void) {};
	virtual UndoElement * clone(void) const = 0;

	/**
	 * Devuelve una descripción como documento xml del cambio realizado.
	 **/
	virtual void toxml(ostream * os) const{
	    XmlWriter w(os);
	    toxml(&w);
	    w.flush();
	};

	virtual void toxml(XmlWriter * writer) const = 0;
};

typedef vector<UndoElement *> VUndo;
typedef VUndo::iterator undoit;
typedef VUndo::const_iterator undocit;

#endif
