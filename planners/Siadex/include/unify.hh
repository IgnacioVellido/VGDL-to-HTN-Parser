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
 * Created by oscar oscar@decsai.ugr.es: jue 08 sep, 2005  12:53
 * Last modified: jue 16 feb, 2006  10:48
 * ************************************************************** */

#ifndef UNIFY_HH
#define UNIFY_HH

#include "constants.hh"
#include "termTable.hh"

/** Esta función verifica si hay unificación entre dos vectores de keys.
 Es asimétrica, es decir, el orden de los parámetros afecta al resultado.
 Para que se produzca unificación el tipo de un elemento de v1 debe ser
 subtipo de un tipo del elemento con el que estamos comparando de v2.
 /param v1 primer vector
 /param v2 segundo vector
 */
bool unify(const vector<pkey> * v1, const vector<pkey> * v2);
bool unify(const vector<Term *> * v1, const vector<pkey> * v2);
/** Esta variante devuelve una tabla de unificaciones con las sustituciones que
 es necesario aplicar para realizar la unficación.
 Esta unificación supone que los elementos del vector v2 son constantes o números.
 La función no altera u si no hay una unificación correcta.
 Las substituciones de variables son del tipo substituye elemento de v1 por elemento de v2
 No hay sustitución de tipos.
 Si hay alguna sustitución pendiente en u, sobre una variable que vamos a usar se aplica
 con anterioridad.
 /param v1 primer vector
 /param v2 segundo vector
 /param u unificador
*/
bool unify(const vector<pkey> * v1, const vector<pkey> * v2, Unifier * u);
/** Por último esta última variante permite hacer unificaciones con un vector v2
 en el que pueden existir variables. ¡Ojo! es menos eficiente que las anteriores
 y nuevamente no es lo mismo escribir unify(v1,v2) que unify(v2,v1), nuevamente los elementos
 de v1 elemento a elemento deben ser de un subtipo del elemento de v2.
 La función puede alterar el contenido de u incluso si no hay una unificación válida.
 Las substituciones de tipos afectan a las variables de v2.
 Las substituciones de variables son del tipo substituye elemento de v1 por elemento de v2
 /param v1 primer vector
 /param v2 segundo vector
 /param u unificador
 */
bool unify2(const vector<pkey> * v1, const vector<pkey> * v2, Unifier * u);
/** esta unificación es un poco especial. 
 Se suponen que todos los elementos de v2 son variables.
 Si el elemento que toca de v1 es una constante tiene que ser subtipo del elemento de v1.
 Si el elemento que toca de v1 es una variable, se realiza la intersección de sus tipos.
 Esta unificacion solo almacena substituciones de tipos en u.
 Las substituciones de tipos afectan a las variables de v1.
 El contenido de u puede ser alterado incluso si no hay una unificación válida.
 /param v1 primer vector
 /param v2 segundo vector
 /param u unificador
 */
bool unify3(const vector<pkey> * v1, const vector<pkey> * v2, Unifier * u);

#endif
