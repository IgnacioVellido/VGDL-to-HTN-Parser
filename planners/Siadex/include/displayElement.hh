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

/***************************************************************************
    file: displayElement.hh 
    begin: jue dic 18 17:11:57 CET 2003
    copyright: (C) 2004 by Óscar Jesús García Pérez
    email: oscar@decsai.ugr.es
    Last modified: 2003 dic 28
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#ifndef DISPLAYELEMENT
#define DISPLAYELEMENT

#include <vector>
#include "term.hh"
#include "termTable.hh"
#include "papi.hh"
#include "goal.hh"

using namespace std;

class DisplayElement
{
    public:
        string name;
        bool pol;
        Goal * goal;

        DisplayElement(void)
        {
            name = "";
            pol = true;
            goal = 0;
        };

        ~DisplayElement(void)
        {
	    if(goal)
		delete goal;
        };

        void print(ostream * os) const
        {
            if(goal){
		goal->print(os,0);
            }
            else
                *os << name;

        };
};
#endif
