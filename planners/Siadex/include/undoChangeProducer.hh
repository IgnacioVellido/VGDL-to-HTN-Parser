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
 * Created by oscar@decsai.ugr.es: mié 23 nov, 2005  12:35
 * Last modified: vie 24 feb, 2006  10:53
 * ********************************************************************************** */

#ifndef UNDOCHANGEPRODUCER
#define UNDOCHANGEPRODUCER

#include "undoElement.hh"
#include "literal.hh"
#include "primitivetask.hh"

using namespace std;

/**
 * Cuando introducimos literales en el estado producto de la aplicación
 * de algún efecto, puede darse el caso de que dos tareas proporcioenen
 * el mismo literal. En ese caso la última tarea productora marcará el
 * literal como producida por ella. Al volver por bactracking se debe de
 * recuperar el valor antiguo.
 * Esta clase se encarga de deshacer dichos cambios.
 */
class UndoChangeProducer: public UndoElement
{
    public:
	/**
	 * Constructor de la clase.
	 * @param l El literal al que afectan los cambios.
	 * @param op Productor que tenía el literal antes de establecer uno nuevo.
	 */
	UndoChangeProducer(Literal * l, const PrimitiveTask * op) {lit=l; oldProducer = op;};

	/**
	 * Imprime en el flujo dado. Util para depurar.
	 * @param os el flujo por el que imprimiremos.
	 */
	virtual void print(ostream * os) const
	{
	    *os << lit->getName() << " was produced by: ";
	    if(oldProducer)
		*os << oldProducer->getName();
	    else
		*os << "initial state";
	};

	/**
	 * Restaura el producer del literal a su valor antiguo.
	 */
	virtual void undo(void)
	{
	    lit->setProducer(oldProducer);
	};

	/**
	 * Para poder hacer type castings.
	 */
	virtual bool isUndoChangeProducer(void) const {return true;};

	/** 
	 * Destructor de la clase
	 */
	virtual ~UndoChangeProducer(void) {};

	virtual UndoElement * clone(void) const {return new UndoChangeProducer(lit,oldProducer);};

	virtual void toxml(XmlWriter * writer) const{
	    writer->startTag("produced_by");
	    if(oldProducer)
		writer->addAttrib("name",oldProducer->getName());
	    else
		writer->addAttrib("name","init");
	    writer->endTag();
	};

    private:
	/** Literal al que afectan los cambios */
	Literal * lit;
	/** Su productor angituo */
	const PrimitiveTask * oldProducer;
};
#endif
