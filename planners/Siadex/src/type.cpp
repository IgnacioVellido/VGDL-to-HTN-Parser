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
 * Created by oscar@decsai.ugr.es: mar 10 ene, 2006  02:26
 * Last modified: jue 23 feb, 2006  05:55
 * ********************************************************************************** */

#include "type.hh"
#include <assert.h>
#include "constantsymbol.hh"
#include "constants.hh"

extern bool PRINTING_TYPELIST;
extern bool PRINT_OBJECTTYPE;

void Type::addSuperType(Type * t){
    assert(t!=0);
    vector<Type *>::iterator i,e;

    e = parents.end();
    for(i=parents.begin(); i != e; i++) {
	if((*i)==t)
	    return;
	if((*i)->getId()==t->getId())
	    return;
    }
    parents.push_back(t);
    t->addSubType(this);
}

void Type::addSuperTypes(const vector<Type *> * v) 
{
    vector<Type *>::const_iterator i,e = v->end();
    for(i=v->begin();i!=e;i++)
	addSuperType((*i));
    //for_each(v->begin(),v->end(),AddV<Type>(&parents));
};

void Type::addSubType(Type * t){
    children.push_back(t);
}

bool Type::isSubTypeOf(const Type * type) const
{
    assert(type != NULL);
    int tid = type->getId();
    vector<Type *>::const_iterator i,e;
    e = parents.end();

    // reflexive relation
    if(tid == getId())
	return true;

    // transitive relation
    for(i=parents.begin();i!=e;i++)
    {
	if((*i)->getId() == getId())
	    return true;

	if((*i)->isSubTypeOf(type))
	    return true;
    }

    return false;
}

bool Type::equal(const Type * t) const
{
    if(!t)
	return false;
    //cerr << "Comparando... " <<  this->getId() << " " << t->getId() << " " << (this->getId() == t->getId()) << endl;
    return (this->getId() == t->getId());
}

void Type::addReferencedBy(const ConstantSymbol * cs)
{
    vconstants::const_iterator i,e;
    e = referencedBy.end();
    for(i=referencedBy.begin();i!=e;i++)
	if((*i)->getId() == cs->getId())
	    return;

    referencedBy.push_back(cs);

    vector<Type *>::iterator j,k;
    k = parents.end();
    k=parents.end();
    for(j=parents.begin();j!=k;j++)
    {
	((*j))->addReferencedBy(cs);
    }
};

void Type::toxml(XmlWriter * writer, bool super,bool sub) const{ 
    writer->startTag("type")
	->addAttrib("name",name)
	->addAttrib("id",getId());

    if(super && !parents.empty()){
	writer->startTag("subtype_of");
	vector<Type *>::const_iterator i,e;
	e = parents.end();
	for(i=parents.begin();i!=e;i++)
	    (*i)->toxml(writer,super,sub);
	writer->endTag();
    }
    else if(!super && sub && !children.empty()){
	writer->startTag("supertype_of");
	vector<Type *>::const_iterator i,e;
	e = children.end();
	for(i=children.begin();i!=e;i++)
	    (*i)->toxml(writer,super,sub);
	writer->endTag();
    }

    writer->endTag();
};

void Type::printSuperTypes(ostream * os) const 
{ 
    int size = parents.size();

    if(size == 0){
	if(PRINT_OBJECTTYPE)
	    *os << " - object";
    }
    else if(size == 1){
	*os << " - ";
	parents[0]->print(os,0);
    }
    else if(size > 1){
	*os << " - (either";
	for_each(parents.begin(),parents.end(),Print<Type>(os,1));
	*os << ")";
    }
};

