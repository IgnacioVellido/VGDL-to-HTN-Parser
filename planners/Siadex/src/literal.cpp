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
 * Created by oscar oscar@decsai.ugr.es: vie 26 ago, 2005  11:37
 * Last modified: mié 22 feb, 2006  10:46
 * ************************************************************** */

#include "literal.hh"
#include "goal.hh"
#include <sstream>
#include "state.hh"
#include "constants.hh"
#include "domain.hh"
#include "papi.hh"
#include "problem.hh"
#include "literaleffect.hh"

Literal::Literal(int id, int mid)
    :Header(id,mid)
{
    producer = 0;
}

Literal::Literal(int id, int mid, const KeyList * param)
    :Header(id,mid,param)
{
    producer = 0;
}

Literal::Literal(const Literal * other) 
    :Header(other)
{
    producer = other->producer;
};

void Literal::printL(ostream * os, int indent) const
{
	string s(indent,' ');
	*os << s;
	if (producer)
	    *os << "[" << producer->getName() << "] ";

	headerPrint(os);
}

void Literal::toxmlL(XmlWriter * writer) const
{
    writer->startTag("predicate")
	->addAttrib("name",getName());

    for_each(parameters.begin(),parameters.end(),ToXMLKey(writer));
    writer->endTag();
};

pkey Literal::getTermIdL(const char * name) const
{
    keylistcit i = searchTermName(name);
    if(i != parameters.end())
        return (*i);
    else
        return make_pair(-1,-1);
}

bool Literal::hasTermL(int id) const
{
    return searchTermId(id) != parameters.end();
}

void Literal::renameVarsL(Unifier * u, VUndo * undo)
{
    varRenaming(u,undo);
}

