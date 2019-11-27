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
 * Created by oscar oscar@decsai.ugr.es: mar 30 ago, 2005  10:49
 * Last modified: mié 22 feb, 2006  07:30
 * ************************************************************** */

#include "wheneffect.hh"
#include <sstream>
#include "undoElement.hh"

WhenEffect::WhenEffect(const WhenEffect *eff)
    :Effect(eff)
{
    if(eff->goal)
	goal = (Goal *) eff->goal->clone();
    effect = (Effect *) eff->effect->clone();
}

WhenEffect::WhenEffect(Goal *g, Effect *eff)
    :Effect()
{
  goal = g;
  effect = eff;
}

WhenEffect::~WhenEffect()
{
    if(goal)
	delete goal;
    delete effect;
}

Expression * WhenEffect::clone(void) const
{
  return new WhenEffect(this);
}

void WhenEffect::print(ostream * os, int nindent) const
{
  string sind(nindent,' ');

  *os << sind << "(when " << endl;
  if(goal)
      goal->print(os,nindent + NINDENT);
  else
      *os << sind << "    ()";
  *os << endl;
  effect->print(os,nindent + NINDENT);
  *os << endl << sind << ")";
};

void WhenEffect::toxml(XmlWriter * writer) const{
    writer->startTag("when");
    if(goal)
	goal->toxml(writer);

    effect->toxml(writer);
    writer->endTag();
};

pkey WhenEffect::getTermId(const char * name) const
{
    pkey ret = effect->getTermId(name);
    if(ret.first != 1 || !goal)
	return ret;
    else 
	return goal->getTermId(name);
};

bool WhenEffect::hasTerm(int id) const
{
    if(goal)
	if(goal->hasTerm(id))
	    return true;
    return effect->hasTerm(id);
}

void WhenEffect::renameVars(Unifier * u, VUndo * undo)
{
    if(goal)
	goal->renameVars(u,undo);
    effect->renameVars(u,undo);
}

bool WhenEffect::provides(const Literal* l) const
{
    return effect->provides(l);
}

bool WhenEffect::apply(State *sta, VUndo * undo, Unifier * uf)
{
  bool ret=true;;
  // Si existe el objetivo, obtenemos todas las instanciaciones que lo cumplen
  if (goal) {
      UnifierTable * v;
      Unifier c;
      unifierit i,e;

      v = goal->getUnifiers(sta, &c,true,0);
      if(v) {
	  // En v tenemos todos los Unifiers obtenidos (todas las unificaciones posibles)
	  // Aplicamos el efecto para cada una de ellas
	  e=v->getUnifierEnd();
	  VUndo vu;
	  for (i=v->getUnifierBegin(); i != e && ret; i++) {
	      // realizar la unificación
	      (*i)->apply(&vu);
	      // registro de los vínculos causales necesitados para alcanzar el goal
	      if(uf)
		  uf->addCLTable((*i));
	      // aplicar el efecto
	      ret = effect->apply(sta,undo,uf);
	      // restaurar a antes de la unificacion
	      for_each(vu.begin(),vu.end(),mem_fun(&UndoElement::undo));
	      // limpiar el vector
	      vu.clear();
	  }
      delete v;
      }
  }
  else
      return effect->apply(sta,undo,uf);
  return ret;
}
