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
 * Created by oscar oscar@decsai.ugr.es: mar 06 abr, 2004 14:13
 * Last modified: vie 24 mar, 2006  07:05
 * ************************************************************** */

#ifndef STATE_HH
#define STATE_HH

#include "literal.hh"
#include "unifier.hh"
#include "goal.hh"
#include "termTable.hh"

using namespace std;

typedef pair<iscit, iscit> ISTable_range;
typedef pair<isit, isit> ISTable_mrange;

class State
{
public:
  /**
   * @brief Añade un predicado a la tabla. No hace una copia, sólo asigna el puntero, cuidadín con esto
   * @param symbol el literal a añadir.
   * @return true si se ha asignado correctamente. False en otro caso (es decir, si ya existe)
   */
  isit addLiteral(Literal * symbol);

  /**
   * @brief Cuenta el número de predicados existentes con el nombre dado.
   * @param El nombre del predicado
   * @return El número de predicados
   */
  int countElements(int id) const;

  /**
   * @brief Devuelve los iteradores necesarios para recorrer los predicados con
   * un determinado nombre (clave).
   * @description Puede haber varios predicados con el mismo nombre pero distinto
   * número de argumentos. Esta función sirve para recorrerlos.
   * @return el rango.
   */
  ISTable_range getRange(int id) const;

  inline ISTable_mrange getModificableRange(int id) {return Literaltable.equal_range(id);};

  /**
   * @brief Devuelve un iterador con el contenido del primer predicado.
   * @param range El rango devuelto por la función getRange
   * @see getLiteral
   * @see getRange
   * @return un iterador
   */
  iscit getFirstLiteral(ISTable_range range);

  iscit getEndLiteral(ISTable_range range);

  inline iscit getBeginLiteral(void) const {return Literaltable.begin();};
  inline iscit getEndLiteral(void) const {return Literaltable.end();};

  /**
   * @brief Devuelve un iterador con el contenido del i-ésimo predicado.
   * @param range El rango devuelto por la función getRange
   * @param it, el iterador devuelto por una llamada anterior a getFirstLiteral o
   * a getNextLiteral
   * @see getLiteral
   * @see getFirstLiteral
   * @see getRange
   * @return un iterador
   */
  iscit getNextLiteral(ISTable_range range, iscit it);

  /**
   * @brief Devuelve el predicado apuntado por un iterador.
   * @description Hay que mantener especial cuidado de no alterar el puntero.
   * La memoria es liberada por la tabla de predicados.
   * @param it el iterador que deseamos referenciar 
   * @see getFirstLiteral
   * @return 0 en caso de que no haya predicado, o que sea el último,
   * en otro caso un puntero a él.
   */
  const Literal * getLiteral(iscit it) const;

  /**
   * @brief No deterministicamente devuelve un predicado de la tabla de predicados que
   * coincida con el nombre, si éste existe.
   * @description Hay que mantener especial cuidado de no alterar el puntero.
   * La memoria es liberada por la tabla de predicados.
   * @param name la clave del predicado
   * @return 0 en caso de que no se encuentre el predicado.
   */
  Literal * getModificableLiteral(int id);

  const Literal * getLiteral(int id) const;

  /**
   * @brief Borra el elemento apuntado por el iterador.
   * @param it El iterador
   * @return true en caso de fallo, false en otro caso
   */
  inline void deleteLiteral(isit it) {Literaltable.erase(it);};

  /**
   * @brief Devuelve el número de elementos en la tabla de predicados
   */
  inline int size(void) {return Literaltable.size();}

  /**
   * @brief Pinta todas las claves de la tabla de predicados.
   */
  void printKeys(ostream *) const;

  /**
   * @brief Pinta el estado en la salida pasada como argumento.
   */
  void print(ostream *) const;

  /**
   * @brief Borra todos los elementos de la tabla de predicados (estado)
   */
  void deleteAll(void);

  virtual ~State(void);

  /**
    Ojo, no modifiques la estructura si no sabes bien lo que estas
    haciendo!!
  */
  inline ISTable * getLiteralTable(void) {return &Literaltable;};

  /*
   * Esta función no hace nada. Simplemente recorre todos los elementos
   * del estado. Sirve para comprobar que los valores que se encuentran
   * en la tabla de literales son correctos, y detectar posibles fallos
   */
  void test(void) const;

  /**
   * Realiza un clon de este objeto
   **/
  State * clone(void) const;

protected:

  ISTable Literaltable;

};

#endif
