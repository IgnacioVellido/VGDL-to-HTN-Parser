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
 * Created by oscar oscar@decsai.ugr.es: jue 01 sep, 2005  10:29
 * Last modified: mié 22 feb, 2006  01:57
 * ************************************************************** */

#include "evaluable.hh"
#include "fluentNumber.hh"
#include "timeInterval.hh"
#include "constants.hh"

TimeInterval::TimeInterval(void)
{
    start = 0;
    end = 0;
};

TimeInterval::TimeInterval(const TimeInterval * other)
{
    start = 0;
    end = 0;
    if(other->start)
	start = other->start->cloneEvaluable();
    if(other->end)
	end = other->end->cloneEvaluable();
};

TimeInterval::~TimeInterval(void) {
    delete start;
    delete end;
};

void TimeInterval::setStart(Evaluable * s){
    start = s;
};

void TimeInterval::setEnd(Evaluable * e){
    end = e;
};

void TimeInterval::setStart(double s){
    start = new FluentNumber(s);
};

void TimeInterval::setEnd(double e){
    end = new FluentNumber(e);
};

TimeInterval * TimeInterval::clone(void) const {
    return new TimeInterval(this);
};

void TimeInterval::print(ostream * os, int nindent) const{
    string s(nindent,' ');

    if(!start && !end){
	*os << s << "at start";
	return;
    }
    if(!end) {
	if(start->isFluentNumber()) {
	    if(((FluentNumber *) start)->getValue().second == ATSTART){
		*os << s << "at start";
		return;
	    }
	    else if(((FluentNumber *) start)->getValue().second == ATEND){
		*os << s << "at end";
		return;
	    }
	}
	*os << s << "at ";
	start->printEvaluable(os,0);
	return;
    }
    
    if((!start || (start->isFluentNumber() && ((FluentNumber *) start)->getValue().second == ATSTART)) && (end->isFluentNumber() && ((FluentNumber *) end)->getValue().second == ATEND)){
	*os << s << "over all";
	return;
    }

    *os << s << "between";
    if(!start)
	*os << " at start";
    else
	start->printEvaluable(os,1);
    end->printEvaluable(os,1);
};

void TimeInterval::toxml(XmlWriter * writer) const{
    if(!start && !end){
	writer->startTag("atstart")
	    ->endTag();
	return;
    }
    if(!end) {
	if(start->isFluentNumber()) {
	    if(((FluentNumber *) start)->getValue().second == ATSTART){
		writer->startTag("atstart")
		    ->endTag();
		return;
	    }
	    else if(((FluentNumber *) start)->getValue().second == ATEND){
		writer->startTag("atend")
		    ->endTag();
		return;
	    }
	}
	writer->startTag("at");
	start->toxmlEvaluable(writer);
	writer->endTag();
	return;
    }
    
    if((!start || (start->isFluentNumber() && ((FluentNumber *) start)->getValue().second == ATSTART)) && (end->isFluentNumber() && ((FluentNumber *) end)->getValue().second == ATEND)){
	writer->startTag("overall")
	    ->endTag();
	return;
    }

    writer->startTag("between");
    if(!start)
	writer->startTag("atstart")
	    ->endTag();
    else
	start->toxmlEvaluable(writer);
    end->toxmlEvaluable(writer);
    writer->endTag();
};

void TimeInterval::renameVars(Unifier * u,VUndo * undo){
    if(start)
	start->compRenameVars(u,undo);
    if(end)
	end->compRenameVars(u,undo);
}

pair<int,float> TimeInterval::getTermId(const char * name) const{
    pair<int,float> ret(-1,0);
    if(start){
	ret = start->compGetTermId(name);
	if(ret.first != -1)
	    return ret;
    }
    if(end){
	ret = end->compGetTermId(name);
	if(ret.first != -1)
	    return ret;
    }
    return ret;
}

bool TimeInterval::hasTerm(int id) const{
    if(start && start->compHasTerm(id))
	return true;
    if(end && end->compHasTerm(id))
	return true;

    return false;
}

unsigned int TimeInterval::evalStart(const Unifier * context, const State * sta){
    if(start){
	return (unsigned int) ((FluentNumber *) start)->getValue().second;
    }
    else return 0;
}

unsigned int TimeInterval::evalEnd(const Unifier * context, const State * sta){
    if(end){
	return (unsigned int) ((FluentNumber *) end)->getValue().second;
    }
    else return 0;
}

