/*  ************************************************************************************
 *  Copyright (C) 2003, 2004, 2005, 2006
 *  Luis Castillo Vidal, Juan Fernandez Olivares,
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
 * Created by oscar@decsai.ugr.es: vie 24 feb, 2006  12:01
 * Last modified: vie 03 mar, 2006  05:50
 * ********************************************************************************** */

#include "undoChangeValue.hh"
#include "variablesymbol.hh"
#include "parameterContainer.hh"
#define ATEND INT_MAX

void UndoChangeValue::undo(void)
{
    // Restaurar el valor antiguo
    //cerr << "==================================================================" << endl;
    //parser_api->termtable->print(&cerr);
    //cerr << "UNDO ";
    //parser_api->termtable->getVariable(val.first)->print(&cerr);
    //cerr << " " << target << endl;
    target->setVar(pos,val);
    if(val.first < -1)
	parser_api->termtable->getVariable(val.first)->addReference(this);
    // Las variables tienen un mecanismo de referencias inversas para acelerar
    // el proceso de sustitución. En el caso de que el término a sustituir fuera
    // una variable al hacer el undo volvemos a añadir la referencia.
    //cerr << "==================================================================" << endl;
    //parser_api->termtable->print(&cerr);
    //cerr << "==================================================================" << endl;
};

void UndoChangeValue::print(ostream * os) const
{
    target->vcprint(os,0);
    *os << " at pos [" << pos << "] put value: ";
    parser_api->termtable->print(val,os);
};

void UndoChangeValue::toxml(XmlWriter * writer) const{
    writer->startTag("changeValue")
	->addAttrib("pos",pos);
    if(time== -1 || time >= ATEND)
	writer->addAttrib("at","end");
    else
	writer->addAttrib("at",time);

    ToXMLKey w(writer);

    writer->startTag("from");
    w(val);
    writer->endTag();

    writer->startTag("to");
    w(new_val);
    writer->endTag();

    target->vctoxml(writer);
    writer->endTag();
};


