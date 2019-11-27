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
 * Created by oscar oscar@decsai.ugr.es: vie 02 sep, 2005  11:25
 * Last modified: vie 24 feb, 2006  12:12
 * ************************************************************** */

#ifndef PY_DEF_FUNCTION_HH
#define PY_DEF_FUNCTION_HH

using namespace std;

#include "constants.hh"
#include <limits.h>
#include "literal.hh"
#include "pythonWrapper.hh"

/**
 * Esta clase almacena las definiciones de funciones PDDL y además simultáneamente 
 * las definiciones de las funciones python.
 * Ambas son equivalentes, se pueden usar en los mismos lugares de la 
 * descripción de dominio y problema. 
 * Se diferencian a la horad e evaluarlas (llamada a python), o buscar el
 * objeto Function almacenado en el estado. 
 * @see Function
 */

class PyDefFunction: public Literal 
{
  public:
      /**
       * Constructor de clase.
       * @param id el identificador de la instancia
       * @param mid el metaidentificador
       */
      PyDefFunction(int id, int mid);

      /**
       * Constructor de clase.
       * @param id el identificador de la instancia
       * @param mid el metaidentificador
       * @param parameters Una lista de parámetros 
       */
      PyDefFunction(int id, int mid, const KeyList * parameters);

      /**
       * Destructor de la clase.
       */
      virtual ~PyDefFunction(void);

      /**
       * Devuelve true siempre.
       */
      virtual bool isFunction(void) const {return true;};

      /**
       * Distingue entre definiciones normales y definiciones
       * de funciones python.
       */
      inline bool isPython(void) const {return code != 0;};

      /**
       * Establece el código de una función python.
       */
      inline void setCode(PyObject * c) {code = c;};

      /**
       * Devuelve el código asociado a la función.
       */
      inline PyObject * getCode(void) const {return code;};

      /**
       * Establece el código python sin compilar
       */
      virtual bool setCode(const char * c);

      /**
       * Devuelve una descripción como una cadena de la definición
       * de función.
       * @return un puntero a cadena con la descripción del objeto.
       */
      virtual const char * toString(void) const {static string s; ostringstream os; printL(&os,0); s = os.str(); return s.c_str();}; 

      /**
       * Imprime en un flujo de salida una descripción del objeto.
       */
      virtual void printL(ostream * os, int indent=0) const;

      virtual void vcprint(ostream * os, int indent=0) const {printL(os,indent);};

      /**
       * Devuelve en un documento xml la descripción de la tarea.
       * @param writer el objeto donde escribir.
       **/
      virtual void toxml(XmlWriter * writer) const;

      /**
       * Devuelve en un documento xml la descripción de la tarea.
       * @param writer el objeto donde escribir.
       **/
      virtual void toxmlL(XmlWriter * writer) const {toxml(writer);};

      virtual void vctoxml(XmlWriter * w) const {toxml(w);};

      /**
       * Añade un tipo a la lista soportada por la función
       */
      virtual void compAddType(Type * t) {assert(t != 0); types.push_back(t);};

      /**
       * Añade la lista de tipos soportada por la función.
       */
      virtual void addTypes(const vector<Type *> * vt) {types.insert(types.end(),vt->begin(),vt->end());};

      /**
	@brief Devuelve el primer tipo del término. 
	@return el primer tipo o getEndType() si el término es de tipo object.
	*/
      virtual typecit getBeginType(void) const {return types.begin();};

      /**
	@brief Devuelve un iterador uno después del último elemento. 
	*/
      virtual typecit getEndType(void) const {return types.end();};

      /**
	@brief Devuelve el tipo apuntado por el iterador. 
	*/
      virtual const Type * getType(typecit i) const {return (*i);};

      virtual vctype * getTypes(void) {return &types;};

      /**
	@brief Algo es de tipo object si no tiene tipos asociados.
	*/
      virtual bool isObjectType(void) const {return types.empty();};

      /**
	@brief Devuelve true si el término es del tipo indicado, false en otro caso
	*/
      virtual bool isType(const Type *t) const {for(typecit i=types.begin(); i!= types.end(); i++) if((*i)->isSubTypeOf(t)) return true; return false;};

      virtual bool hasType(const Type *t) const {for(typecit i=types.begin(); i!= types.end(); i++) if((*i)->equal(t)) return true; return false;};

      virtual bool hasTypeId(int id) const {for(typecit i=types.begin(); i!= types.end(); i++) if((*i)->getId()== id) return true; return false;};

      virtual void setPol(bool b) {};

      virtual bool getPol(void) const {return false;}

      virtual Literal * cloneL(void) const {return 0;};
	
  protected:

      virtual void clearTypes(void) {types.clear();};
      
      // Objeto de la librería python que tiene el código compilado de la
      // función.
      PyObject * code;

      // el tipo del elemento que estamos comparando
      // de momento tiene que ser compatible con lo
      // definido en pddl
      vctype types;
};
#endif
