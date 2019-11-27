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
 * Created by oscar@decsai.ugr.es: mar 21 feb, 2006  09:55
 * Last modified: jue 23 feb, 2006  07:16
 * ********************************************************************************** */
#ifndef XMLWRITER_HH
#define XMLWRITER_HH

#include "constants.hh"
#include <iostream>
#include <stack>
#include <string>
#include <sstream>

using namespace std;

/**
 * Esta clase trata de facilitar el trabajo de escribir información en formato XML.
 * Realiza adecuadamente el escape de carácteres especiales y la apertura y cierre
 * de tags.
 */
class XmlWriter{
    public:
	/**
	 * El constructor.
	 * @param os El flujo donde se escribirá el xml. No debe cerrarse mientras
	 * XmlWriter no haya sido liberado.
	 **/
	XmlWriter(ostream * os);

	/**
	 * El destructor de la clase.
	 **/
	~XmlWriter(void);

	/**
	 * Abre un elemento.
	 * @param el nombre del elemento.
	 **/
	XmlWriter * startTag(const char * name);

	/**
	 * Cierra el último elemento abierto. 
	 **/
	XmlWriter * endTag();

	/**
	 * Cierra todos los tags abiertos hasta ahora.
	 **/
	void flush();

	/**
	 * Añade un atributo al tag abierto actualmente.
	 * @param name El nombre.
	 * @param value el contenido.
	 **/
	XmlWriter * addAttrib(const char * name, const char * value);

	/**
	 * Añade un atributo al tag abierto actualmente.
	 * @param name El nombre.
	 * @param value el contenido.
	 **/
	XmlWriter * addAttrib(const char * name, int value);

	/**
	 * Añade un atributo al tag abierto actualmente.
	 * @param name El nombre.
	 * @param value el contenido.
	 **/
	XmlWriter * addAttrib(const char * name, double value);

	/**
	 * Añade un atributo al tag abierto actualmente.
	 * @param name El nombre.
	 * @param value el contenido.
	 **/
	XmlWriter * addAttrib(const char * name, const string & value);

	/**
	 * Añade datos de contenido "character data" a un tag abierto.
	 * @param value el contenido.
	 **/
	XmlWriter * addCharacter(const char * value);

	/**
	 * Añade datos de contenido "character data" a un tag abierto.
	 * @param value el contenido.
	 **/
	XmlWriter * addCharacter(const string & value);

	/**
	 * Establece el número de espacios a dejar cada vez que se abra un
	 * nuevo tag.
	 * @param n el número de espacios a dejar.
	 **/
	inline void setDefaultIndent(int n) {indent = n;};

    protected:
	/** El flujo donde escribiremos la información */
	ostream * flow;
	/** La pila de tags abiertos */
	stack<string> stk;
	/** La lista de atributos del tag actual */
	ostringstream * attribs;
	/** El character data del tag actual */
	ostringstream * text;
	/** Número de indentaciones por defecto */
	int indent;
	/** Flag para marcar si un tag se encuentra abierto */
	bool open;

	/**
	 * Esta función realiza el escapado de los carácteres reservados en
	 * xml
	 * @param flow el flujo donde escribir.
	 * @param content el contenido a escapar y escribir en el flujo.
	 **/
	void escapeXml(ostream * flow, const char * content);
};

#endif /* XMLWRITER_HH */
