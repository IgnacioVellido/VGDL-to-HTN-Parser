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
 * Created by oscar o.garcia@iactive.es: lun 29 ago, 2005  05:49
 * Last modified: o.garcia vie 19 sep, 2008  02:41
 * ************************************************************** */

#include "undoCLinks.hh"
#include "causalTable.hh"
#include "task.hh"

void UndoCLinks::print(ostream * os) const {
    *os <<  "UndoCLinks:: key = " << key << endl;
};

void UndoCLinks::undo(void) {
    causalTable.eraseCausalLinks(key);
};

void UndoCLinks::toxml(XmlWriter * writer) const{
};

