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

/* **************************************************************
 * Created by oscar oscar@decsai.ugr.es: mié 14 sep, 2005  06:41
 * Last modified: vie 20 oct, 2006  05:04
 * ************************************************************** */

#ifndef TIMESTAMPED_HH
#define TIMESTAMPED_HH   

#include "constants.hh"
#include "evaluable.hh"

/**
 * Esta clase será heredada por aquellos objetos que puedan llevar
 * alguna marca de tiempo (típicamente un efecto temporizado).
 */

class TimeStamped{
    public:
	/**
	 * Constructor por defecto.
	 */
	TimeStamped(void) {
	    time = 0;
	};

	/**
	 * Constructor de copia.
	 */
	TimeStamped(const TimeStamped * other) {
	    if(other->time) 
		time = other->time->cloneEvaluable();
	    else time=0;
	};

	/**
	 * El destructor de la clase.
	 */
	virtual ~TimeStamped() {
	    if(time) 
		delete time;
	};

	/**
	 * Establece el momento en el cual se consigue el objetivo.
	 * Ojo que la función hace uso del puntero directamente, no lo clona.
	 */
	inline void setTime(Evaluable * c) {
	    time = c;
	};

	/**
	 * Obtiene el momento en el cual se consigue el objetivo.
	 */
	inline const Evaluable * getTime(void) const {return time;};

	inline Evaluable * getModificableTime(void) const {return time;};

	/**
	 * Evalua el momento en el cual se hace cierto el efecto respecto a la
	 * tarea que lo consique.
	 */
	virtual float evalTime(void) const {
	    if(time)
		return time->eval(0,0).second;
	    else
		return ATEND;
	};

	virtual void setNewTime(const Evaluable * o) {
	    if(time) 
		delete time; 
	    time=0; 
	    if(o) 
		time = o->cloneEvaluable();
	};

	virtual void resetTime(void) {
	    if(time) 
		delete time; 
	    time = 0;
	};

	virtual bool isTimed(void) const {return (time != 0);};

    protected:
	/** Marca de tiempo en la cual se consigue el efecto */ 
	Evaluable * time;
};

#endif /* TIMESTAMPED_HH */
