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
 * Created by oscar oscar@decsai.ugr.es: mié 14 sep, 2005  06:37
 * Last modified: vie 24 feb, 2006  12:45
 * ************************************************************** */

#ifndef UNDOCHANGETIME_HH
#define UNDOCHANGETIME_HH

#include "constants.hh"
#include "undoElement.hh"
#include "timeStamped.hh"

/** 
 * Esta clase almacena la información necesaria para deshacer los cambios
 * provocados sobre el time stamp de un objeto 
 * una variable o un literal.
 */
class UndoChangeTime :public UndoElement 
{
    public:
	/**
	 * Constructor de la clase.
	 * @param o El objeto sobre el cual se aplican cambios de tiempo.
	 * @param time Es el tiempo antiguo que se pretende recuperar 
	 * tras hacer el undo.
	 */
	UndoChangeTime(TimeStamped * o, Evaluable * time, const Evaluable * new_time) {
	    obj=o; 
	    oldTime=time;
	    if(new_time)
		newTime = new_time->cloneEvaluable();
	    else
		newTime = 0;
	};

	/**
	 * Destructor.
	 */
	~UndoChangeTime() {
	    if (oldTime) delete oldTime;
	    if (newTime) delete newTime;
	}

	/**
	 * La función que realiza el undo.
	 */
        virtual void undo(void){
	    // se borra el valor actual del time si hay alguno
	    obj->resetTime();
	    obj->setTime(oldTime);
	    oldTime = 0;
	};

        virtual void print(ostream * os) const {*os << "Time change to: "; if(oldTime) oldTime->printEvaluable(os); else *os << "null"; *os << endl;};

	virtual bool isUndoChangeTime(void) const {return true;};

	UndoElement* clone(void) const{return new UndoChangeTime(obj,oldTime->cloneEvaluable(),newTime);};

	virtual void toxml(XmlWriter * writer) const{
	    writer->startTag("changeTime");
	    writer->startTag("from");
	    if(oldTime)
		oldTime->toxmlEvaluable(writer);
	    writer->endTag();
	    writer->startTag("to");
	    if(newTime)
		newTime->toxmlEvaluable(writer);
	    writer->endTag();
	    writer->endTag();
	};

    protected:
	/** objeto sobre el que aplicar el undo. */
	TimeStamped * obj;
	/** El tiempo antiguo */
	Evaluable * oldTime;
	/** El nuevo tiempo */
	Evaluable * newTime;
};

#endif
