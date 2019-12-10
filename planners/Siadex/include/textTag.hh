/*  ************************************************************************************
 *  Copyright (C) 2003, 2004, 2005, 2006
 *  Luis Castillo Vidal, Juan Fernandez Olivares,
 *  Oscar Jesus Garcia Perez, Francisco Carlos Palao Reines.
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
 * Created by oscar@decsai.ugr.es: jue 16 mar, 2006  07:22
 * Last modified: o.garcia mié 21 may, 2008  02:30
 * ********************************************************************************** */
#ifndef TEXTTAG_HH
#define TEXTTAG_HH   

#include "constants.hh"
#include "tag.hh" 
#include "parameterContainer.hh"

using namespace std;

/** 
 * función para hacer el procesado de los metatags de texto interpretado.
 * @param input La cadena a procesar.
 * @param pc El óbjeto que contiene una lista de parámetros con nombre que podemos
 * sustuir en la cadena dada.
 **/
string processTextTag(const string & input, const ParameterContainer * pc);

/**
 * Esta clase implementa una meta-propiedad que contiene una cadena de texto.
 **/
class TextTag : public Tag{
    public:
	/**
	 * Constructor.
	 * @param n el nombre que tendra la meta-propiedad.
	 **/
	TextTag(const char * n);

	inline void setValue(const char * s) {value =s;};

	inline const char * getValue(void) const {return value.c_str();};

    protected:
	/// El contenido de la meta-propiedad
	string value;
};
#endif /* METATEXT_HH */
