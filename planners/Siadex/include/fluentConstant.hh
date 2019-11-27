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
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  10:15
 * Last modified: mi� 22 feb, 2006  01:11
 * ************************************************************** */

#ifndef FLUENTCONSTANT_HH
#define FLUENTCONSTANT_HH

#include "constants.hh"
#include <assert.h>
#include "evaluable.hh"
#include "constantsymbol.hh"

using namespace std;

/**
 * Esta clas representa constantes que pudieran ser
 * utilizadas dentro de expresiones aritm�ticas o de
 * comparaci�n. Normalmente una constante no puede
 * ser utilizada dentro de una expresi�n aritm�tica pero
 * podr�a tener sentido dentro de una expresi�n de comparaci�n.
 */
class FluentConstant :public Evaluable 
{
    public:
        FluentConstant(int id) {setId(id);};
        FluentConstant(const pkey * id) {setId(id->first);};
        FluentConstant(pkey id) {setId(id.first);};
	FluentConstant(const FluentConstant * other) :Evaluable(other) {value = other->value;};

        inline void setId(int v) {value.first = v; value.second=0;};

        inline int getId(void) const {return value.first;};

        virtual Evaluable * cloneEvaluable(void) const {return new FluentConstant(this);};
	virtual void printEvaluable(ostream * os,int indent=0) const {string s(indent,' '); *os << s << parser_api->termtable->getTerm(value.first)->getName();};
	virtual void toxmlEvaluable(XmlWriter * writer) const {
	    writer->startTag("fluent")
		->addAttrib("value",parser_api->termtable->getTerm(value.first)->getName())
		->endTag();
	};
        virtual pkey compGetTermId(const char * name) const {if(strcasecmp(name,parser_api->termtable->getTerm(value.first)->getName()) == 0) return value ; else return make_pair(-1,0);};
        virtual bool compHasTerm(int i) const {if(value.first==i)return true; else return false;};

	/**
	 * Realiza la evaluaci�n de un objeto evaluable con el fin de hacer una 
	 * comparaci�n o una asignaci�n.
	 * En caso de error durante la evaluaci�n el primer elemento del par 
	 * devuelto tendr� valor INT_MAX
	 * @param state El estado actual de planificaci�n.
	 * @param contex El contexto de planificaci�n.
	 * @return un pkey con el resultado de la evaluaci�n.
	 */
        virtual pkey eval(const State * state, const Unifier * context) const {return value;};

	/**
	 * Realiza la evaluaci�n de un objeto evaluable con el fin de hacer una 
	 * comparaci�n o una asignaci�n. 
	 * Esta evaluaci�n es especial para dar tratamiento a los time points.
	 * En caso de error durante la evaluaci�n el primer elemento del par 
	 * devuelto tendr� valor INT_MAX
	 * @param state El estado actual de planificaci�n.
	 * @param contex El contexto de planificaci�n.
	 * @param tp Es un par�metro de salida. Contendr� un time point si
	 * durante la evaluaci�n se encuentra una referencia a dicho elemento.
	 * (espera inicializado a (-1,0))
	 * @param pol Es un par�metro de salida. Si es true el tp no va afectado
	 * por un signo negativo, false en otro caso. (espera inicializado a true)
	 * @return un pkey con el resultado de la evaluaci�n.
	 */
        virtual pkey evaltp(const State * state, const Unifier * context, pkey * tp, bool * pol) const {return value;};

	virtual void compRenameVars(Unifier*, VUndo*) {};

	/**
	  @brief Devuelve true si el t�rmino es del tipo indicado, false en otro caso
	  */
	virtual bool isType(const Type *t) const {for(typecit i=getConstantTypes()->begin(); i!=getConstantTypes()->end(); i++) if((*i)->isSubTypeOf(t)) return true; return false;};

    protected:
	vctype * getConstantTypes(void) const {return parser_api->termtable->getTerm(value.first)->getTypes();};

	pkey value;
};

#endif

