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
 * Created by oscar@decsai.ugr.es: mié 15 feb, 2006  07:01
 * Last modified: vie 24 feb, 2006  01:19
 * ********************************************************************************** */

#include "parameterContainer.hh"
#include "undoChangeValue.hh"
#include "unifier.hh"
#include "termTable.hh"

ParameterContainer::ParameterContainer(const KeyList * v) 
{
    parameters.insert(parameters.begin(),v->begin(),v->end());
};

ParameterContainer::ParameterContainer(const ParameterContainer * pc) 
{
    parameters.insert(parameters.begin(),pc->parameters.begin(),pc->parameters.end());
};

ParameterContainer::~ParameterContainer(void)
{

    //cerr << "==================================================================" << endl;
    //parser_api->termtable->print(&cerr);
    // si hay una variable que nos referencia eliminar dicha referencia
    keylistit i, e = parameters.end();
    for(i=parameters.begin() ;i!= e;i++) {
	if((*i).first < -1) {
	    parser_api->termtable->getVariable((*i))->removeReference(this);
	    //cerr << "(ee)";
	    //parser_api->termtable->getVariable(*i)->print(&cerr);
	    //cerr << " ";
	}
    }
    //cerr << "Erased: " << this << endl;
    //cerr << "==================================================================" << endl;
    //parser_api->termtable->print(&cerr);
    //cerr << "==================================================================" << endl;
};

void ParameterContainer::varRenaming(Unifier *u, VUndo * undo){
    int pos = 0;
    keylistit i,e;
    pkey p;

    e = parameters.end();
    for(i=parameters.begin() ;i!= e;i++, pos++){
        if((*i).first < -1){
	    // si queremos guardar información para posteriormente
	    // deshacer los cambios provocados por el renaming
            if(u->getSubstitution((*i).first,&p)){
		if(undo) 
		    undo->push_back(new UndoChangeValue(this,pos,(*i),p));
		(*i) = p;
		if((*i).first < -1)
		    parser_api->termtable->getVariable(*i)->addReference(new UndoChangeValue(this,pos,*i,*i));
	    }
            else
            {
                //se crea una nueva entrada en la tabla de términos
                pkey nv = parser_api->termtable->addVariable((VariableSymbol *) parser_api->termtable->getVariable((*i))->clone());
		if(undo)
		    undo->push_back(new UndoChangeValue(this,pos,(*i),nv));
                parser_api->termtable->getVariable(nv)->addReference(new UndoChangeValue(this,pos,nv,nv));
                u->addSubstitution((*i).first,nv);
                (*i) = nv; 
            }
        }
    }
};

void ParameterContainer::setVar(int pos, pkey &newval)
{
    setParameter(pos,newval);
}; 
   
