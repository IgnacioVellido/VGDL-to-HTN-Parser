/* ****************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

#ifndef EVALUABLE_HH
#define EVALUABLE_HH

using namespace std;

#include "constants.hh"
#include "termTable.hh"

class State;
class Unifier;

/**
 * Esta clase representa a los elementos que puedan ser utilizados
 * tanto en los operadores aritméticos como de comparación.
*/
class Evaluable
{
    public:
        /**
        * El constructor de copia.
        */
        Evaluable(const Evaluable * other) {};

        /**
        * El constructor por defecto
        */
        Evaluable(void) {};

        /**
        * El destructor.
        */
        virtual ~Evaluable(void) {};

        /**
        * Operador para clonar la clase.
        * @return Una copia exacta a this.
        */
        virtual Evaluable * cloneEvaluable(void) const = 0;

        /**
        * Imprime en un flujo de salida una descripción textual
        * de la clase
        * @param os Un flujo de salida.
        * @param Una indentación (número de espacios en blanco al comienzo de
        * cada linea.
        */
        virtual void printEvaluable(ostream * os,int indent=0) const = 0;

        /**
        * Devuelve en un documento xml la descripción del objeto.
        * @param os El flujo en el que escribir.
        **/
        virtual void toxmlEvaluable(ostream * os) const{
            XmlWriter * writer = new XmlWriter(os);
            toxmlEvaluable(writer);
            writer->flush();
            delete writer;
        };

        /**
        * Devuelve en un documento xml la descripción del objeto.
        * @param writer el objeto donde escribir.
        **/
        virtual void toxmlEvaluable(XmlWriter * writer) const = 0;

        /**
        * Dado un identificador devuelve la key asociada.
        */
        virtual pkey compGetTermId(const char * name) const = 0;

        /**
        * Comprueba si el comparador tiene un término con
        * el identificador pasado como argumento.
        */
        virtual bool compHasTerm(int id) const = 0;

        /**
        * Realiza el renombrado de variables.
        */
        virtual void compRenameVars(Unifier * u, VUndo * undo) = 0;

        /**
        * Realiza la evaluación de un objeto evaluable con el fin de hacer una
        * comparación o una asignación.
        * En caso de error durante la evaluación el primer elemento del par
        * devuelto tendrá valor INT_MAX
        * @param state El estado actual de planificación.
        * @param contex El contexto de planificación.
        * @return un pkey con el resultado de la evaluación.
        */
        virtual pkey eval(const State * state, const Unifier * context) const = 0;

        /**
        * Realiza la evaluación de un objeto evaluable con el fin de hacer una
        * comparación o una asignación.
        * Esta evaluación es especial para dar tratamiento a los time points.
        * En caso de error durante la evaluación el primer elemento del par
        * devuelto tendrá valor INT_MAX
        * @param state El estado actual de planificación.
        * @param contex El contexto de planificación.
        * @param tp Es un parámetro de salida. Contendrá un time point si
        * durante la evaluación se encuentra una referencia a dicho elemento.
        * (espera inicializado a (-1,0))
        * @param pol Es un parámetro de salida. Si es true el tp no va afectado
        * por un signo negativo, false en otro caso. (espera inicializado a true)
        * @return un pkey con el resultado de la evaluación.
        */
        virtual pkey evaltp(const State * state, const Unifier * context, pkey * tp, bool * pol) const = 0;

        /**
        * Convierte la descripción textual del objeto
        * en un string.
        * @return Un string con la descripción del objeto.
        */
        virtual const char * toStringEvaluable(void) const {static string s; ostringstream os; printEvaluable(&os,0); s = os.str(); return s.c_str();};

        /**
        * Función para facilitar la identificación de las
        * clases hijas.
        */
        virtual bool isFluentNumber(void) const {return false;};

        /**
        * Función para facilitar la identificación de las
        * clases hijas.
        */
        virtual bool isType(const Type *t) const = 0;

        /**
        * Función para facilitar la identificación de las
        * clases hijas.
        */
        virtual bool isFluentLiteral(void) const {return false;};
};

#endif

