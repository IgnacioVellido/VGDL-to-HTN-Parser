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
 * Created by oscar@decsai.ugr.es: jue 18 dic, 2003  17:11
 * Last modified: mi� 22 feb, 2006  10:29
 * ********************************************************************************** */

#ifndef EXPRESSION_HH
#define EXPRESSION_HH
using namespace std;

#include "unifier.hh"
#include "termTable.hh"
#include "unifiable.hh"
#include "xmlwriter.hh"

class Expression : public Unifiable
{
    public:
	virtual ~Expression(void) {};

        virtual bool isGoal(void) const {return false;};
        virtual bool isAndGoal(void) const {return false;};
        virtual bool isEffect(void) const {return false;};
        virtual bool isAndEffect(void) const {return false;};
        virtual bool isLiteral(void) const {return false;};
        virtual bool isLiteralEffect(void) const {return false;};
        virtual bool isForallGoal(void) const {return false;};
        virtual bool isForallEffect(void) const {return false;};
        virtual bool isFluent(void) const {return false;};

	/**
	 * Devuelve una descripci�n textual del objeto.
	 * @param out El flujo donde escribir.
	 * @param indent, el n�mero de espacios a dejar como tabulado antes de la impresi�n.
	 **/
	virtual void print(ostream * out, int indent=0) const {};

	/**
	 * Devuelve una descripci�n como cadena del objeto.
	 **/
        virtual const char * toString(void) const {
	    static string s; ostringstream os;
	    print(&os,0); s = os.str();
	    return s.c_str();
	};

	/**
	 * Realiza una copia exacta del objeto.
	 **/
	virtual Expression * clone(void) const { return NULL; };

	/**
	 * Devuelve en un documento xml la descripci�n de la tarea.
	 * @param os El flujo en el que escribir.
	 **/
	virtual void toxml(ostream * os) const{
	    XmlWriter * writer = new XmlWriter(os);
	    toxml(writer);
	    writer->flush();
	    delete writer;
	};

	/**
	 * Devuelve en un documento xml la descripci�n de la tarea.
	 * @param writer El objeto en donde escribir.
	 **/
	virtual void toxml(XmlWriter * writer) const {};
};

#endif
