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
 * Created by oscar oscar@decsai.ugr.es: mar 26 jul, 2005  12:41
 * Last modified: lun 20 feb, 2006  06:57
 * ************************************************************** */

#include "problem.hh"
#include <math.h>
#include "domain.hh"

Problem::Problem(const Domain * domain)
{
    state=new State(); 
    tasknetwork=0; 
    MAX_THORIZON = domain->MAX_THORIZON;
    REL_THORIZON = domain->REL_THORIZON;
    TFORMAT= domain->TFORMAT;
    FLAG_TIME_UNIT = domain->FLAG_TIME_UNIT;
    FLAG_TIME_START = domain->FLAG_TIME_START;
};

Problem::~Problem()
{
    if(state)
	delete state;
    if(tasknetwork)
	delete tasknetwork;
    state=0;
    tasknetwork=0;
}


