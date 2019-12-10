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
 * Created by oscar@decsai.ugr.es: lun 26 sep, 2005  12:43
 * Last modified: mié 22 feb, 2006  12:29
 * ********************************************************************************** */

#include "variablesymbol.hh"
#include <iostream>
#include <sstream>
#include "unifier.hh"
#include "papi.hh"
#include "domain.hh"
#include "constants.hh"

int VAR_COUNTER=0;

//Variable para controlar la impresion
extern bool PRINTING_BINDS;
extern bool PRINTING_COMPARATIONGOAL;
extern bool PRINTING_TASKSNETWORK;
extern bool PRINTING_SORTGOAL;
extern bool PRINTING_DURATIONS;
extern bool PRINTING_PRECONDITIONS;
extern bool PRINTING_CONDITIONS;
extern bool PRINTING_FORALLPARAMETERS;
extern bool PRINTING_PREDICATELIST;
extern bool PRINTING_HEADER_FUNCTION;
extern bool PRINTING_PARAMETERS;
extern bool PRINTING_TYPELIST;
extern bool PRINT_OBJECTTYPE;
extern bool PRINT_DEFINEDTYPES;
extern bool PRINT_NUMBERTYPE;

extern string str2XML(string s);


Term * VariableSymbol::clone(void) const
{
    return new VariableSymbol(this);
};

void VariableSymbol::print(ostream * os, int indent) const
{
    typecit b, e;
    string s(indent,' ');
    bool PRINT = true;

    //*os << s << getName() << "[" << id << "]";
    *os << s << getName();


    int siz = types.size();

    e=types.end();
    for(b=types.begin();b!=e;b++) {
	if(!PRINT_NUMBERTYPE && (strcmp("number",(*b)->getName())==0))
	    PRINT = false;
    }

    if(siz == 1){
	if(PRINT_DEFINEDTYPES && PRINT){
	    *os << " -";
	    for_each(types.begin(), types.end(), Print2<Type>(os,1));
	}
    }
    else if(siz > 1){
	if(PRINT_DEFINEDTYPES && PRINT){
	    *os << " - (either";
	    for_each(types.begin(), types.end(), Print2<Type>(os,1));
	    *os << ")";
	}
    }
    else
	if(PRINT_OBJECTTYPE)
	    *os << " - object";

};

void VariableSymbol::toxml(XmlWriter * writer) const{
    writer->startTag("variable")
	->addAttrib("name",getName())
	->addAttrib("id",getId());

    vector<Type *>::const_iterator i,e;
    e = types.end();
    for(i=types.begin();i!=e;i++)
	(*i)->toxml(writer);

    writer->endTag();
};

const char * VariableSymbol::getName(void) const 
{return parser_api->domain->getMetaName(metaid);};

void VariableSymbol::setName(const char * n) 
{parser_api->domain->setMetaName(metaid,n);};

