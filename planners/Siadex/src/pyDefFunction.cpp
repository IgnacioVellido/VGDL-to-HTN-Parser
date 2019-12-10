/* ****************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

/* **************************************************************
 * Created by o.garcia o.garcia@iactive.es: mié 14 sep, 2005  07:45
 * Last modified: o.garcia lun 15 sep, 2008  01:32
 * ************************************************************** */

#include "pyDefFunction.hh"

PyDefFunction::PyDefFunction(int id, int mid) 
    :Literal(id,mid) 
{
    code = 0;
};

PyDefFunction::PyDefFunction(int id, int mid, const KeyList * parameters) 
    :Literal(id,mid,parameters)
{
    code = 0;
};

PyDefFunction::~PyDefFunction(void) 
{
#ifdef PYTHON_FOUND
    if(code) {
	Py_DECREF(code);
    }
#endif
};


void PyDefFunction::printL(ostream * os, int indent) const 
{
    string s(indent,' '); 
    *os << s << "(= ";
    headerPrint(os);
    if(!isPython()) {
	*os << s;
	*os << ")";
    }
    else {
	*os << s << "{<python>})";
    }
};

void PyDefFunction::toxml(XmlWriter * writer) const 
{
    writer->startTag("function")
	->addAttrib("name",getName());

    if(isPython()) {
	writer->addAttrib("value","python");
    }
    for_each(parameters.begin(),parameters.end(),ToXMLKey(writer));
    writer->endTag();
};

bool PyDefFunction::setCode(const char * c) {
    if(!(code= parser_api->wpython.parse(this,c)))
    {
	return false;
    }
    return true;
}; 

