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
 * Created by oscar oscar@decsai.ugr.es: lun 25 jul, 2005  05:51
 * Last modified: mar 30 ago, 2005  03:49
 * ************************************************************** */

#ifndef UNIFIER_H
#define UNIFIER_H

#include "constants.hh"
#include <iostream>
#include <assert.h>
#include <ext/slist>
#include "undoElement.hh"
#include "constants.hh"
#include "causal.hh"

using namespace std;

class Type;

typedef pair<int,vector<Type *> *> TypeSubstitution;
typedef vector<TypeSubstitution> vTSubstitutions;
typedef vector<TypeSubstitution>::iterator typesubite;

typedef __gnu_cxx::slist<pair<int,pair<int,float> > > vSubstitutions;
typedef vSubstitutions::const_iterator subscit;
typedef vSubstitutions::iterator subsit;

struct ApplyVarSubstitution{
    VUndo * undo;

    ApplyVarSubstitution(VUndo *u);
    void operator()(const pair<const int,pair<int,float> > & item);
};

class Unifier 
{
    public:
	/**
	 * Constructor por defecto.
	 */
	Unifier(void);

	/** 
	 * Constructor de copia.
	 * @param other El elemento del cual haremos una copia exacta.
	 */
	Unifier(const Unifier * other);

	/**
	 * El destructor de la clase
	 */
	~Unifier(void);

	/**
	 * Crea un clon de este unificador.
	 * @return el clon
	 */ 
	Unifier * clone(void) const;

	/**
	 * Devuelve la substitución de una variable.
	 * @param i el índice de la variable
	 * @param p una estructura donde almacenar el valor devuelto.
	 * @return true en caso de que exista sustitución, falso en otro caso.
	 */
	bool getSubstitution(int i, pkey * p) const;

	/**
	 * Devuelve la substitución de una variable.
	 * @param v el nombre de la variable 
	 * @param p una estructura donde almacenar el valor devuelto.
	 * @return true en caso de que exista sustitución, falso en otro caso.
	 */
	bool getSubstitution(const char * v, pkey * p) const;

	/**
	 * Añade una sustitución a la tabla de sustituciones.
	 * ¡¡Comprobar que previamente no exista!!,
	 * En otro caso petará.
	 * @param i El índice de la variable.
	 * @param p La pkey por la que sustituimos.
	 */
	void addSubstitution(int i, pkey p);

	/**
	 * Añade una sustitución a la tabla de sustituciones.
	 * Identica a la anterior, pero machaca si hay una
	 * sustitución previa.
	 * @param i El índice de la variable.
	 * @param p La pkey por la que sustituimos.
	 */
	void addFSubstitution(int i, pkey p);

	/**
	 * Aplica la substituciones de tipos en el caso de que sea
	 * necesario realizar alguna.
	 */
	void applyTypeSubstitutions(VUndo * undoApply) const;

	/**
	 * Añade una type sustitución a la tabla de sustituciones de tipos.
	 * @param i El índice de la variable.
	 * @param p El vector de tipos que deseamos asignar.
	 */
	void addTSubstitution(int i, vector<Type *> * p);

	/**
	 * Añade una type sustitución a la tabla de sustituciones de tipos.
	 * @param i El índice de la variable.
	 * @param p El vector de tipos que deseamos asignar.
	 */
	void addTSubstitution2(int i, const vector<Type *> * p);

	/**
	 * Esta función añade a this los unificadores contenidos en u.
	 * Puede alterar el contenido de u.
	 * @param u El unificador del que queremos extraer la información.
	 */
	void merge(Unifier * u);

	/** 
	 * Reserva mermoria para la tabla de vínculos causales. Si la
	 * memoria ya se encuentra reservada entonces no hace nada
	 */
	inline void createCLTable(void) {if(!cltable) cltable = new CLTable;};

	/**
	 * Registra un vínculo causal en la tabla correspondiente.
	 * @param l El literal al cual queremos enlazar.
	 */
	inline void addCL(Causal * c) {cltable->push_back(c);};

	/**
	 * Registra una acción como consumidora de los vínculos generados
	 * durante la unificación.
	 * @param consumer la tarea, normalmente una primitiva aunque también
	 * podría ser una tarea compuesta.
	 */
	void setCLConsumer(const Task * consumer);

	/** 
	 * Añade los elementos almacenados en la tabla de vínculos de other
	 * a this.
	 * @param other unificador del que se desean extraer los vínculos
	 * causales.
	 */
	void addCLTable(Unifier * other);

	/**
	 * Devuelve la tabla de vínculos causales, asociados a esta
	 * unificación.
	 */
	inline const CLTable * getCLTable(void) const {return cltable;};

	/**
	 * Devuelve la tabla de vínculos causales, asociados a esta
	 * unificación.
	 */
	inline CLTable * getModifiableCLTable(void) const {return cltable;};

	/**
	 * Devuelve true si hay alguna sustitucion de tipos pendiente
	 * en el unificador
	 * @return un booleano
	 */
	inline bool hasTypeSubstitutions(void) {return (typeSubstitutions != 0);};

	/** 
	 * Imprime el contenido del unificador.
	 * @param os el flujo donde escribiremos
	 * @param indent la indentación a usar
	 */
	void print(ostream * os, int indent=0) const;

	/**
	 * Aplica todas las sustituciones pendientes.
	 * Los cambios se almacenan en el vector de undo.
	 * @param undoApply estructora para almacenar los cambios
	 * provocados por la unificación
	 * @return true on success
	 */
	bool apply(VUndo * undoApply=0);

	/**
	 * Aplica las sustituciones que afectan a los tipos de la variable..
	 * Los cambios se almacenan en el vector de undo.
	 * @param undoApply estructora para almacenar los cambios
	 * provocados por la unificación
	 * @return true on success
	 */
	bool applyTypeSubstitutions(VUndo * undoApply=0);

	/**
	 * Aplica todas las sustituciones variable término pendientes.
	 * Los cambios se almacenan en el vector de undo.
	 * @param undoApply estructora para almacenar los cambios
	 * provocados por la unificación
	 * @return true on success
	 */
	bool applyVarSubstitutions(VUndo * undoApply=0);

	/**
	 * Devuelve el número de sustituciones de variables
	 */
	inline int size(void) const {return substitutions.size();};

	/**
	 * Borra n elementos por el principio
	 */
	void erase(int n);

	/**
	 * Devuelve un iterador a la primera sustitución. 
	 */
	inline subsit begin(void) {return substitutions.begin();};

	/**
	 * Devuelve un iterador a la última sustitución. 
	 */
	inline subsit end(void)  {return substitutions.end();};

	/**
	 * Comprueba si el unificador es igual a otro dado.
	 */
	bool equal(const Unifier * other) const;

    protected:
	/** Estructura para almacenar las substituciones de variable por término */
	vSubstitutions substitutions;
	/** Vector para almacenar en el caso de que se produzcan, sustituciones de tipos */
	vTSubstitutions * typeSubstitutions;
	/** Tabla de vínculos causales consumidos durante la unificación */
	CLTable * cltable;
};
#endif
