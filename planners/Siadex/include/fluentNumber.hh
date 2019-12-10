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
 * This file is copyrighted by SIADEX project.
 * Visit http://siadex.ugr.es for more information.
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  10:07
 * Last modified: mi� 22 feb, 2006  01:08
 * ************************************************************** */

#ifndef FLUENTNUMBER_HH
#define FLUENTNUMBER_HH

using namespace std;

#include "constants.hh"
#include <assert.h>
#include "evaluable.hh"
#include "domain.hh"
#include "papi.hh"

/**
 * Esta clase representa a un n�mero simple, que se
 * puede usar dentro de las operaciones aritm�ticas
 * o comparaciones.
 */
class FluentNumber :public Evaluable 
{
    public:
	/**
	 * Constructor de la clase.
	 */
        FluentNumber(pkey val) {setValue(val); type = parser_api->domain->getModificableType(0);};

	/**
	 * Constructor de la clase.
	 */
        FluentNumber(double v) {value.first= -1; value.second=v; type = parser_api->domain->getModificableType(0);};

	/**
	 * Constructor de copia.
	 */
	FluentNumber(const FluentNumber * other) :Evaluable(other) {value = other->value; type = parser_api->domain->getModificableType(0);};

	/**
	 * Destructor de la clase.
	 */
	virtual ~FluentNumber(void) {};

	/**
	 * Establecer el valor del fluent.
	 * @param v El nuevo valor.
	 */
        inline void setValue(pkey v) {value = v;};

	/**
	 * Devuelve el valor contenido por el fluent.
	 * @return la pkey del objeto contenido.
	 */
        inline pkey getValue(void) const {return value;};

	/**
	 * Hace un clon the this.
	 * @return una copia exacta a this.
	 */
        virtual Evaluable * cloneEvaluable(void) const {return new FluentNumber(this);};

	/**
	 * Imprime en texto la informaci�n sobre la clase.
	 * @param os El flujo de salida.
	 * @param indent N�mero de espacios que se utilizar�n al principio de cada l�nea
	 */
	virtual void printEvaluable(ostream * os,int indent=0) const {string s(indent,' '); *os << s << value.second;};

	/**
	 * Imprime en xml la informaci�n sobre la clase.
	 * @param os El flujo de salida.
	 * @param indent N�mero de espacios que se utilizar�n al principio de cada l�nea
	 */
	virtual void toxmlEvaluable(XmlWriter * writer) const {
	    writer->startTag("fluent")
		->addAttrib("value",value.second)
		->endTag();
	};

        virtual pkey compGetTermId(const char * name) const {return make_pair(-1,0);};
        virtual bool compHasTerm(int id) const {return false;};
        virtual void compRenameVars(Unifier * u, VUndo * undo) {};

	/**
	 * Devuelve el resultado de la evaluaci�n de la clase.
	 * @param state el estado actual.
	 * @param context El contexto de unificaci�n.
	 * @return El resultado de la unificaci�n.
	 */
        virtual pkey eval(const State * state, const Unifier * context) const {return value;};


	/**
	 * Devuelve el resultado de la evaluaci�n de la clase.
	 * Esta evaluaci�n es ligeramente diferente en el sentido de que est� pensada
	 * para poder trabajar con las restricciones temporales impuestas sobre
	 * las tareas. Se hace un tratamiento diferente para manejar los time points.
	 * @param state El estado actual de planificaci�n.
	 * @param contex El contexto de planificaci�n.
	 * @param tp Es un par�metro de salida. Contendr� un time point si
	 * durante la evaluaci�n se encuentra una referencia a dicho elemento.
	 * @param pol Es un par�metro de salida. Si es true el tp no va afectado
	 * por un signo negativo, false en otro caso.
	 * @return un pkey con el resultado de la evaluaci�n.
	 */
        virtual pkey evaltp(const State * state, const Unifier * context, pkey * tp, bool * pol) const {return value;};

	/**
	 * Comprueba si la instancia es del tipo dado
	 * @return true en caso afirmativ
	 */
	virtual bool isType(const Type * t) const {return type->isSubTypeOf(t);};

	/**
	 * Sirve para identificar las instancias como de tipo fluent. 
	 * @return true siempre
	 */
	virtual bool isFluentNumber(void) const {return true;};

    protected:
	/** Este es el valor almacenado en el fluent. */
        pkey value;
	/** El tipo del fluent, generalmente ser� number. */
	const Type * type;
};

#endif

