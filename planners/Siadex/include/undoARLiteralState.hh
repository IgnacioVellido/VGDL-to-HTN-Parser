/*  ************************************************************************************
 *  Copyright (C) IACTIVE Intelligent Solutions,
 *
 * http://www.iactive.es
 *
 * Este fichero es propiedad intelectual de IACTIVE Intelligent Solutions
 * y queda protegido por las leyes de propiedad intelectual aplicables.
 * Queda totalmente prohibido, su copia, modificación, distribución y lectura
 * Sin el consentimiento explícito y por escrito de IACTIVE Intelligent Solutions
 *
 * ********************************************************************************** */

/* *************************************************************************************
 * Created by oscar@decsai.ugr.es: mié 23 nov, 2005  11:41
 * Last modified: o.garcia mar 27 nov, 2007  02:46
 * ********************************************************************************** */

#ifndef UNDOARLITERALSTATE
#define UNDOARLITERALSTATE

#include "undoElement.hh"
#include "literal.hh"


/**
 * Esta clase almacena los cambios producidos al añadir o eliminar un literal
 * del estado.
 */

class UndoARLiteralState: public UndoElement
{
    public:
	UndoARLiteralState(Literal * l, bool v);

	virtual ~UndoARLiteralState(void);

	virtual void print(ostream * os) const;

	inline bool wasAdded(void) const {return added;};
	inline void setAdded(bool v = true) {added=v;};

	inline void setLiteral(Literal * l) {ref=l;};
	inline Literal * getLiteral(void) const {return ref;};

	virtual bool isUndoARLiteralState(void) const {return true;};
	virtual void undo(void);

	virtual UndoElement * clone(void) const;
	
	// Instante de tiempo en el cual conseguimos el efecto
	// con respecto a la acción que generó el efecto.
	float time;

	virtual void toxml(XmlWriter * writer) const;

    protected:
	// flag para indicar si el literal fue añadido o eliminado
	// del estado.
	bool added;
//	bool deleted;
	// literal con el que estamos tratando
	Literal * ref;
};

#endif
