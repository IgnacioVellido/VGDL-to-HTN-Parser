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
 * Created by oscar: mar 20 sep, 2005  12:53
 * Last modified: mié 22 feb, 2006  05:00
 * ********************************************************************************** */

#include "andEffect.hh"
#include <sstream>
#include <string>

AndEffect::AndEffect(const AndEffect * ae)
    :ContainerEffect(ae)
{
    for_each(ae->effects.begin(),ae->effects.end(),CloneV<Effect>(&effects));
};

AndEffect::~AndEffect(void)
{
    clear();
}

void AndEffect::clear(void)
{
    for_each(effects.begin(),effects.end(),Delete<Effect>());
    effects.clear();
}

Expression * AndEffect::clone(void) const
{
    return new AndEffect(this);
}

void AndEffect::print(ostream * os, int indent) const
{
    string s(indent,' ');

    *os << s;
    *os << "(and" << endl;
    for_each(effects.begin(),effects.end(),Print<Effect>(os,indent + 3));
    *os << s;
    *os << ")" << endl;
}

void AndEffect::toxml(XmlWriter * writer) const{
    writer->startTag("and");
    for_each(effects.begin(),effects.end(),ToXML<Effect,XmlWriter>(writer));
    writer->endTag();
}

bool AndEffect::apply(State *sta, VUndo * undo, Unifier * uf)
{
  effectcit it, e;
  e = getEnd();
  for (it = getBegin(); it != e; it++)
      if(!(*it)->apply(sta,undo,uf))
	  return false;
  return true;
}

pkey AndEffect::getTermId(const char * name) const
{
    pkey result(-1,-1);
    effectcit i,e;
    e = getEnd();
    for(i = getBegin(); i != e; i++)
    {
        result = (*i)->getTermId(name);
        if(result.first != -1)
            return result;
    }
    return result;
}

bool AndEffect::hasTerm(int id) const
{
    const_mem_fun1_t<bool,Unifiable,int > f(&Unifiable::hasTerm);
    return find_if(effects.begin(),effects.end(),bind2nd(f,id)) != effects.end();
}

void AndEffect::renameVars(Unifier * u, VUndo * undo)
{
    effectcit i, e = effects.end();
    for(i=effects.begin();i!=e;i++)
	(*i)->renameVars(u,undo);
}

bool AndEffect::provides(const Literal * l) const
{
  effectcit i, e = effects.end();

  for(i = effects.begin(); i != e; i++)
      if((*i)->provides(l))
	  return true;
  return false;
};

