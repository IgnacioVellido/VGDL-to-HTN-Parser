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
 * Created by oscar@decsai.ugr.es: lun 20 mar, 2006  09:20
 * Last modified: lun 20 mar, 2006  10:42
 * ********************************************************************************** */
#ifndef TAG_HH
#define TAG_HH   

#include "constants.hh"
#include <vector>

using namespace std;

/**
 * Esta clase define meta-propiedades que pueden ser utilizadas por
 * una acción u otro elemento de SIADEX, para incluir conocimiento no necesariamente
 * empleado en el proceso de planificación. Pero útil para, por ejemplo, un análisis 
 * posterior del plan resultante.
 **/
class Tag{
    public:
	/**
	 * Constructor.
	 * @param n el nombre que tendra la meta-propiedad.
	 **/
	Tag(const char * n) {name = n;};

	inline const char * getName(void) const {return name.c_str();};

	inline void setName(const char * n) {name = n;};

    protected:
	/// El nombre de la meta-propiedad
	string name;
};

// Algunos typedefs útiles
typedef vector<Tag *> TagVector;
typedef TagVector::const_iterator tagv_cite;
typedef TagVector::iterator tagv_ite;

#endif /* TAG_HH */
