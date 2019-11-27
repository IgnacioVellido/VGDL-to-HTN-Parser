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
 * Created by francisco palao@decsai.ugr.es: sab 22 oct, 2005  12:41
 * Last modified: sab 22 oct, 2005  14:26
 * ************************************************************** */

 
#include "controlrules.hh"
#include <math.h>
#include "debugger.hh"
#include "domain.hh"
#include "undoElement.hh"
#include "undoChangeValue.hh"
#include "function.hh"
#include "fluentEffect.hh"
#include "plan.hh"

Controlrules * controlrules;

Controlrules::Controlrules(void) {
	id = 1;
}

Controlrules::~Controlrules(void) {
}


// CONTROL SOBRE EL PUNTO DE DECISION BT1
int Controlrules::selectPermutableTask(StackNode *context) {
	
	//Obtenemos las distintas opciones
	int sucount;
	sucount = context->agenda.size();
	
	//Hacemos la seleccion
	int suselected;
	suselected = context->agenda.at(sucount-1).first;

	//*errflow << "Numero de Selecciones unordered: " << sucount << " elegimos la " << suselected << endl;
	
	return suselected;
}

// CONTROL SOBRE EL PUNTO DE DECISION BT2
int Controlrules::selectTaskExpansion(StackNode *context) {

	//Obtenemos las distintas opciones
	int ecount;
	ecount = context->offspring->size();
	
	//Hacemos la seleccion
	int eselected;
	eselected = ecount - 1;
	
	//*errflow << "Numero de Expansiones Posibles: " << ecount << " elegimos la " << eselected << endl;
	
	return eselected;

}

// CONTROL SOBRE EL PUNTO DE DECISION BT3
int Controlrules::selectMethod(StackNode *context) {
	
	// Obtenemos las distintas opciones
	int mcount;
	mcount = context->methods->size();
	
	//Hacemos la seleccion
	int mselected;
	mselected = 0;
	
	//*errflow << "Numero de Metodos Posibles: " << mcount << " elegimos el " << mselected << endl;
	
	return mselected;
}


// CONTROL SOBRE EL PUNTO DE DECISION BT4
int Controlrules::selectUnification(StackNode *context) {
	
	//Obtenemos las distintas opciones
	int ucount;
	ucount = context->utable->countUnifiers();
		
	//Hacemos la seleccion
	int uselected;
	uselected = 0;	
		
	//*errflow << "Numero de Unificaciones Posible: " << ucount << " elegimos la " << uselected << " Tarea(" << context->task << " " << context->taskid << ")" << endl;
	
	return uselected;
}
