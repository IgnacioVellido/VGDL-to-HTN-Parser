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
 * Created by oscar@decsai.ugr.es: mié 15 feb, 2006  07:02
 * Last modified: vie 24 feb, 2006  12:22
 * ********************************************************************************** */

#include "function.hh"

Function::Function(int id, int mid, bool p, double val) 
    :LiteralEffect(id,mid), value(-1,val) 
{
};

Function::Function(int id, int mid, bool p, double val, const KeyList * parameters) 
    :LiteralEffect(id,mid,parameters,p), value(-1,val) 
{
};

Function::Function(const Function *c) 
    :LiteralEffect(c) 
{
    value = c->getValue();
};

Literal * Function::cloneL(void) const{
    return new Function(this);
};

void Function::printL(ostream * os, int indent) const 
{
    string s(indent,' '); 
    *os << s << "(= ";
    headerPrint(os);
    *os << s;
    parser_api->termtable->print(value,os);
    *os << ")";
};

void Function::toxml(XmlWriter * writer) const {
    writer->startTag("function")
	->addAttrib("name",getName())
	->startTag("value");

    ToXMLKey s(writer);
    s(value);
    writer->endTag();
    for_each(parameters.begin(),parameters.end(),s);
    writer->endTag();
};

