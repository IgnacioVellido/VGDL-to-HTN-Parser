/*  ************************************************************************************
 *  Copyright (C) 2003, 2004, 2005  Luis Castillo Vidal,  Juan Fernandez Olivares,
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
 * Created by oscar@decsai.ugr.es: lun 3 may, 2004  01:10
 * Last modified: mié 23 nov , 2005  01:10
 * ********************************************************************************** */

#include "unifierTable.hh"

UnifierTable::~UnifierTable()
{
    eraseAll();
}

void UnifierTable::eraseAll(void)
{
    for_each(utable.begin(),utable.end(),Delete<Unifier>());
    utable.clear();
}

void UnifierTable::addUnifiers(UnifierTable * t)
{
    for_each(t->getUnifierBegin(),t->getUnifierEnd(),AddV<Unifier>(&utable));
    t->clearUnifiers();
}

void UnifierTable::print(ostream * os) const
{
    for_each(utable.begin(),utable.end(),Print<Unifier>(os));
}

void UnifierTable::cut(void)
{
    if(!utable.empty()){
	for_each(utable.begin()+1,utable.end(),Delete<Unifier>());
	utable.erase(utable.begin()+1,utable.end());
    }
}

UnifierTable::UnifierTable() {};

UnifierTable::UnifierTable(const UnifierTable * o){
    for_each(o->utable.begin(), o->utable.end(), CloneV<Unifier>(&utable));
};

