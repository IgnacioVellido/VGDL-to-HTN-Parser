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
 * Created by oscar@decsai.ugr.es: mié 22 feb, 2006  10:56
 * Last modified: mié 22 feb, 2006  10:57
 * ********************************************************************************** */

#ifndef IMPLYGOAL
#define IMPLYGOAL

#include "constants.hh"
#include "goal.hh"

using namespace std;

class ImplyGoal: public Goal
{
    public:
	ImplyGoal(void) :Goal() {condition = 0; goal=0;};
	ImplyGoal(Goal * p, Goal * g) :Goal() {condition=p; goal = g;};
	ImplyGoal(const ImplyGoal * o);
	~ImplyGoal(void) {if(condition) delete condition; if(goal) delete goal;};

	virtual void renameVars(Unifier* u, VUndo* undo);
	virtual pkey getTermId(const char* n) const;
	virtual bool hasTerm(int id) const;
	virtual void print(ostream* out, int nindent) const;
	virtual void toxml(XmlWriter * writer) const;
	virtual Expression* clone(void) const;
	/**
	 * Calcula los unificadores para un imply.
	 * Realmente un imply no generará unificaciones. Cuando falle devolverá null, cuando el
	 * imply sea cierto, se devolverá una tabla de unificadores con un solo unificador que estará
	 * vacío en el caso de que u sea null o un clon de u. 
	 * En el caso de que se necesiten almacenar los vínculos causales, en el unificador
	 * devuelto se almacenará la estructura que registra los vínculos causales que fueron necesarios
	 * para llervar a término el imply.
	 * @param state Es el estado actual del mundo.
	 * @param u Es el contexto actual de unificación.
	 * @param polarity Es la polaridad heredada, sirve para llevar la cuenta de los not.
	 * @return Lee arriba
	 */
	virtual UnifierTable* getUnifiers(const State* state, const Unifier* u, bool polarity,  pair<unsigned int,unsigned int> * protection) const;
	virtual bool isReachable(ostream* err, bool p) const;

    protected:
	Goal * condition;
	Goal * goal;
};

#endif
