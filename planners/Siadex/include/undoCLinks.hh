/* ************************************************************************************
 * Copyright (C) IACTIVE Intelligent Solutions,
 *
 * http://www.iactive.es
 *
 * Este fichero es propiedad intelectual de IACTIVE Intelligent Solutions
 * y queda protegido por las leyes de propiedad intelectual aplicables.
 * Queda totalmente prohibido, su copia, modificación, distribución y lectura
 * Sin el consentimiento explícito y por escrito de IACTIVE Intelligent Solutions
 *
 * ********************************************************************************** */

/* **************************************************************
 * Created by oscar o.garciar@iactive.es: lun 29 ago, 2005  05:42
 * Last modified: o.garcia vie 19 sep, 2008  01:52
 * ************************************************************** */

#ifndef UNDOCLINKS
#define UNDOCLINKS

#include "constants.hh"
#include "undoElement.hh"

class Task;

using namespace std;

/**
 * Clase para deshacer tras un backtracking los cambios
 * provocados sobre la estructura causal.
 */
class UndoCLinks: public UndoElement
{
    public:
	virtual void print(ostream * os) const ;
	virtual void undo(void);

	virtual bool isUndoCLinks(void) const {return true;};
	virtual ~UndoCLinks(void) {};

	// clave de la tarea a eliminar
	const Task * key;

	virtual UndoElement * clone(void) const {
	    UndoCLinks * ul = new UndoCLinks();
	    ul->key = key;
	    return ul;
	};

	virtual void toxml(XmlWriter * writer) const;
};

#endif
