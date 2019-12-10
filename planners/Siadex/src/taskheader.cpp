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
 * Created by oscar oscar@decsai.ugr.es: mar 26 jul, 2005  12:38
 * Last modified: mié 22 feb, 2006  07:00
 * ************************************************************** */

#include "taskheader.hh"
#include <sstream>

TaskHeader::TaskHeader(int id, int mid)
    :Task(id,mid)
{
};

TaskHeader::TaskHeader(int id, int mid, const KeyList * v)
    :Task(id,mid,v)
{
};

TaskHeader::TaskHeader(const TaskHeader * t)
    :Task(t->id,t->getMetaId(),t->getParameters())
{
};

Expression *TaskHeader::clone(void) const
{
 return new TaskHeader(this);
};

void TaskHeader::print(ostream * os,int indent) const
{
	string s(indent,' ');

	*os << s << "(" << getName();
	for_each(parameters.begin(),parameters.end(), PrintKey(os));
	* os << ")" << endl;
};

void TaskHeader::toxml(XmlWriter * writer, bool complete) const{
    writer->startTag("task")
	->addAttrib("name",getName())
	->startTag("parameters");
    for_each(parameters.begin(),parameters.end(), ToXMLKey(writer));
    writer->endTag()
	->endTag();
};

pkey TaskHeader::getTermId(const char * name) const
{
    keylistcit i = searchTermName(name);
    if(i != parameters.end())
        return (*i);
    else
        return make_pair(-1,-1);
};

bool TaskHeader::hasTerm(int id) const
{
    return searchTermId(id) != parameters.end();
};

void TaskHeader::renameVars(Unifier * u, VUndo * undo)
{
    varRenaming(u,undo);
}

