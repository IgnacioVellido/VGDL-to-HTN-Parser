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
 * Last modified: mar 31 oct, 2006  04:37
 * ************************************************************** */

 
 #ifndef CONTROLRULES_HH
#define CONTROLRULES_HH 
 
 #include "constants.hh"
#include <iostream>
#include <stdlib.h>
#include "debugger.hh"
#include "termTable.hh"
#include "pythonWrapper.hh"
#include <time.h>
#include "papi.hh"
#include "problem.hh"
#include <sys/resource.h>
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <pthread.h>
#include "clock.hh"

using namespace std;

class Controlrules
{

	public:
		Controlrules(void);
		~Controlrules();
		
	int selectPermutableTask(StackNode *context);
	
	int selectTaskExpansion(StackNode *context);
	
	int selectMethod(StackNode *context);
	
	int selectUnification(StackNode *context);
	
	int id;
	
};

#endif
