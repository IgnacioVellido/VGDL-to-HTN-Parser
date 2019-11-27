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
 * Created by oscar@decsai.ugr.es: mié 23 nov, 2005  11:26
 * Last modified: mié 23 nov , 2005  11:26
 * ********************************************************************************** */

#ifndef UNIFIERTABLE_H
#define UNIFIERTABLE_H

#include "constants.hh"
#include <iostream>
#include <vector>
#include <algorithm>
#include "unifier.hh"

using namespace std;

typedef vector<Unifier *> unifierTable;
typedef unifierTable::const_iterator unifiercit;
typedef unifierTable::iterator unifierit;

class UnifierTable 
{

    protected:
        unifierTable utable; /**< @brief Vector de Substitutions*/

    public: 
	/**
	 * @brief Constructor por defecto.
	 */
	UnifierTable();

	/**
	 * @brief Constructor de copia.
	 */
	UnifierTable(const UnifierTable * o);

        /**
          @brief Destructor
         */  
        ~UnifierTable();

        /**
          @brief Anade una Unifier al unificador
          @param uni: Unifier que anadiremos al unificador
         */
        inline void addUnifier(Unifier * uni) {utable.push_back(uni);};

        /**
           @brief iterador al primer elemento para recorrer la estructura.
        */
        inline unifierit getUnifierBegin(void) {return utable.begin();};

        /**
           @brief iterador al elemento uno pasado al último para recorrer la estructura.
        */
        inline unifierit getUnifierEnd(void) {return utable.end();};

        inline Unifier * getback(void) {Unifier * u = utable.back(); utable.pop_back(); return u;};

	/**
	 * Borra el unificador en la posición pos.
	 * /param pos la posición a borrar
	 */
        void erase(int pos) {unifierit i = utable.begin() + pos; Unifier * u = (*i); utable.erase(i); delete u;};

	/**
	 * Borra todos los unificadores
	 */
        void eraseAll(void);

        Unifier *  getUnifierAt(int pos) {unifierit i = utable.begin() + pos; return (*i);};
        
        /**
            @brief Dado un iterador menor que el getUnifierEnd() devuelve su objeto asociado
        */
        inline const Unifier * getUnifier(unifierit i) {return (*i);}; 

        /**
            @brief añade los unificadores de ut a this. Ut se queda vacía de unificadores en el proceso.
        */
        void addUnifiers(UnifierTable * t);

        /**
            @brief Función de uso interno, no llamar directamente
        */
        inline void clearUnifiers(void) {utable.clear();};

        inline bool isEmpty(void) {return utable.empty();};

        void print(ostream * os) const;

        inline int countUnifiers(void) {return utable.size();};

	// Elimina todos los elementos de la tabla de unificaciones excepto el primero
	void cut(void);
};

#endif
