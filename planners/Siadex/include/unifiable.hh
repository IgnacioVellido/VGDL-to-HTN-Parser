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

#ifndef UNIFIABLE_HH
#define UNIFIABLE_HH

#include "undoElement.hh"

using namespace std;

/** Esta clase trata de representar una interfaz com�n para todos aquellos objetos que
 * sobre los cuales se puede aplicar el resultado de una unificaci�n.
 */
class Unifiable
{
    public:

	virtual ~Unifiable(void) {};

	/**
	 * Realiza un renombrado de las variables, al mismo tiempo va aplicando
	 * las sustituciones de variables que hay en u.
	 * @param u Estructura para ir almacenando las sustituciones que vamos realizando
	 * @param undo Estructura para ser capaces de deshacer los cambios que se van
	 * haciendo durante el renombrado. Puede ser null.
	 */
	virtual void renameVars(Unifier * u,VUndo * undo){};

	/** Dado el nombre de una variable o una constante, devuelve su identificador asociado
	 * ��No busca t�rminos de tipo number!!. Si se devuelve pair<-1,...> no debe interpretarse
	 * como un n�mero sino como que el elemento no ha sido encontrado.
	 * @param name el nombre del t�rmino a buscar
	 * @return la pkey del t�rmino
	*/
	virtual pair<int,float> getTermId(const char * name) const { return pair<int, float>(0,0.0); };

	/** devuelve true si el objeto contiene el identificador pasado como argumento, en
	 * alguna de sus variables o constantes.
	 * @param id El identificador del t�rmino buscado.
	 * @return true si contenemos el identificador de t�rmino buscado.
	 */
	virtual bool hasTerm(int id) const { return false; };
};

#endif
