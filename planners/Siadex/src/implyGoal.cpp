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

#include "implyGoal.hh"
#include "problem.hh"
#include "papi.hh"

ImplyGoal::ImplyGoal(const ImplyGoal * o) 
    :Goal(o) 
{
    if(o->condition)
	condition = (Goal *) o->condition->clone(); 
    else
	condition =0;
    if(o->goal)
	goal = (Goal *) o->goal->clone();
    else
	goal = 0;
};

void ImplyGoal::renameVars(Unifier* u, VUndo* undo)
{
    if(condition)
	condition->renameVars(u,undo);
    if(goal)
	goal->renameVars(u,undo);
    if(isTimed())
	time->renameVars(u,undo);
};

pkey ImplyGoal::getTermId(const char* n) const
{
    pkey ret(-1,0);

    if(condition)
	ret = condition->getTermId(n);
    if(ret.first != -1)
	return ret;
    else if(goal)
	ret = goal->getTermId(n);
    if(ret.first != -1)
	return ret;
    else if(isTimed())
	ret = time->getTermId(n);
	
    return ret;
};

bool ImplyGoal::hasTerm(int id) const
{
    if(condition && condition->hasTerm(id))
	return true;
    else if(goal && goal->hasTerm(id))
	return true;
    else if(isTimed() && time->hasTerm(id))
	return true;
    return false; 
};

void ImplyGoal::print(ostream* out, int nindent) const
{
    string s(nindent,' ');
    *out << s;
    if(isTimed()){
	*out << "(";
	time->print(out,0);
	*out << " ";
    }
    *out << "(imply" << endl;
    if(condition)
	condition->print(out,nindent + NINDENT);
    else
	*out << s << "()";
    *out  << endl;

    if(goal)
	goal->print(out,nindent + NINDENT);
    else
	*out << s << "()" ;
    *out << endl;

    if(isTimed())
	*out << s << "))" << endl;
    else
	*out << s << ")" << endl;
};

void ImplyGoal::toxml(XmlWriter * writer) const{
    writer->startTag("imply");

    if(!polarity)
	writer->addAttrib("polarity","negated");
    else 
	writer->addAttrib("polarity","affirmed");

    if(isTimed())
	time->toxml(writer);
    if(condition)
	condition->toxml(writer);
    if(goal)
	goal->toxml(writer);
    writer->endTag();
};

Expression* ImplyGoal::clone(void) const
{
    return new ImplyGoal(this);
};

UnifierTable* ImplyGoal::getUnifiers(const State* state, const Unifier* u, bool polarity, Protection * protection) const
{
    bool pol = true;
    // determinar si el predicado está negado
    if((!getPolarity() || !polarity) && (!(!getPolarity() && !polarity)))
        pol = false;

    Protection  p;
    if(time){
	p.first = time->evalStart(u,state);
	p.second = time->evalEnd(u,state);
	protection = &p;
    }

    if(pol)
    {
	// La única condición con la cual el imply falla
	// es cuando se da a y no b. Es lo que compruebo.
	Unifier * uf;
	if(u)
	    uf= u->clone();
	else
	    uf = new Unifier();

	// comprobar si el antecedente es cierto
	UnifierTable * ret=0;
	if(condition)
	    ret = condition->getUnifiers(state,u,true,protection);

	// Cuando el antecedente sea cierto el consecuente 
	// también lo debe ser.
	if(ret && !ret->isEmpty()){
	    if(goal){
		UnifierTable * aux;
		unifiercit j, e = ret->getUnifierEnd();
		for(j = ret->getUnifierBegin(); j != e; j++)
		{
		    aux = goal->getUnifiers(state,*j,true,protection);
		    if(aux == 0 || aux->isEmpty()){
			// esto es un fallo, tenemos un consecuente
			// falso con un antecedente cierto.
			// a y no b
			delete aux;
			delete ret;
			delete uf;
			return 0;
		    }
		    uf->addCLTable((*j));
		    unifiercit k , ke = aux->getUnifierEnd();
		    for(k=aux->getUnifierBegin();k!=ke;k++)
			uf->addCLTable((*k));
		    delete aux;
		}
		delete ret;
	    }
	}
	ret = new UnifierTable();
	ret->addUnifier(uf);
	return ret; 
    }
    else {
	// La unica situación en que el imply falla cuando este está
	// negado es que se dé b y no a 
	Unifier * uf;
	if(u)
	    uf= u->clone();
	else
	    uf = new Unifier();

	// comprobar cuando el consecuente es cierto
	// el antecedente también lo debe ser 
	UnifierTable * ret=0;
	if(goal)
	    ret = goal->getUnifiers(state,u,true,protection);

	if(ret && !ret->isEmpty()){
	    if(condition){
		UnifierTable * aux;
		unifiercit j, e = ret->getUnifierEnd();
		for(j = ret->getUnifierBegin(); j != e; j++)
		{
		    aux = condition->getUnifiers(state,*j,true,protection);
		    if(aux == 0 || aux->isEmpty()){
			// esta es la situación de fallo
			delete aux;
			delete ret;
			delete uf;
			return 0;
		    }
		    uf->addCLTable((*j));
		    unifiercit k , ke = aux->getUnifierEnd();
		    for(k=aux->getUnifierBegin();k!=ke;k++)
			uf->addCLTable((*k));
		    delete aux;
		}
		delete ret;
	    }
	}
	ret = new UnifierTable();
	ret->addUnifier(uf);
	return ret; 
    }
    return 0;
};

bool ImplyGoal::isReachable(ostream* err, bool p) const
{
    bool pol = true,r=true;
    // determinar si el predicado está negado
    if((!getPolarity() || !p) && (!(!getPolarity() && !p)))
        pol = false;

    if(condition)
	r = (r && condition->isReachable(err,pol));
    if(goal)
	r = (r && goal->isReachable(err,pol));

    return r;
};

