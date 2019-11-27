/*  ***************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

/* **************************************************************
 * Created by oscar o.garcia@iactive.es: jue 01 sep, 2005  10:04
 * Last modified: o.garcia lun 15 sep, 2008  12:01
 * ************************************************************** */

#ifndef COMPOUNDTASK_H
#define COMPOUNDTASK_H

#include "constants.hh"
#include "task.hh"
#include "variablesymbol.hh"
#include "constants.hh"
#include "goal.hh"

class Method;
typedef vector<Method *>::const_iterator methodcit;
typedef vector<Method *>::const_iterator methodit;
typedef vector<Method *>::const_reverse_iterator methodcrit;

class CompoundTask: public Task
{
    public: 

	CompoundTask(int id, int mid);

	CompoundTask(int id, int mid, const KeyList * v);

	/**
	 * El constructor de copia. Crea una copia exacta de la tarea compuesta
	 * pasada como argumento.
	 * /param t la tarea a copiar.
	 */
	CompoundTask(const CompoundTask * t);

	virtual ~CompoundTask(void);

	/**
	  @brief Añade un nuevo método a la tarea.
	  @description Añade a la tarea el método al que apunta el puntero m
	  @param m Puntero al método a añadir.
	  */
	void addMethod(Method * m);

	/**
	 * @brief Devuelve un iterador apuntando al primer método de la tarea.
	 */
	methodcit getBeginMethod(void) const {return methods.begin();}

	/**
	 * @brief Devuelve un iterador apuntando al elemento después del último método
	 */
	methodcit getEndMethod(void) const {return methods.end();};

	/**
	 * @brief Devuelve un iterador apuntando al primer método de la tarea.
	 */
	methodit beginMethod(void) {return methods.begin();}

	/**
	 * @brief Devuelve un iterador apuntando al elemento después del último método
	 */
	methodit endMethod(void) {return methods.end();};

	/**
	 * @brief Devuelve un iterador apuntando al primer método de la tarea.
	 */
	methodcrit getBeginRMethod(void) const {return methods.rbegin();}

	/**
	 * @brief Devuelve un iterador apuntando al elemento después del último método
	 */
	methodcrit getEndRMethod(void) const {return methods.rend();};

	/**
	  @brief Devuelve el número de métodos de la tarea.
	  */
	int getNumOfMethods(void) const {return methods.size();}

	/**
	 * @brief Realiza una copia exacta de este objeto.
	 * @description La memoria debe ser liberada por la función llamadora con delete.
	 */
	virtual Expression * clone(void) const;

	/**
	  @brief Imprime el contenido del objeto por la salida estandard.
	  @param os un flujo de salida, por defecto la salida estandard.
	  */
	virtual void print(ostream * os, int indent=0) const;

	virtual void vcprint(ostream * os, int indent=0) const {print(os,indent);};

	/**
	 * Esta función escribe la información sobre la tarea compuesta
	 * como un documento xml.
	 * @param writer El objeto donde volcaremos el xml.
	 **/
	virtual void toxml(XmlWriter * writer) const {toxml(writer,true);};

	virtual void toxml(XmlWriter * writer, bool complete) const;

	virtual void vctoxml(XmlWriter * w) const {toxml(w);};

	virtual void printHead(ostream * os) const;

	void prettyPrint(ostream * os) const;

	virtual bool isCompoundTask(void) const {return true;};

	virtual pkey getTermId(const char * name) const;

	virtual bool hasTerm(int id) const;

	virtual void renameVars(Unifier * u, VUndo * undo);

	virtual bool isReachable(ostream * err) const;

	virtual bool provides(const Literal * l) const;

	/**
	 * Establece el flag de poda para los métodos.
	 * Ver first.
	 * /param v el nuevo valor.
	 */
	inline void setFirst(bool v = true) {first = v;};

        /**
         * Selecciona los métodos a expandir de forma aleatoria en 
         * lugar de por orden
         **/
	inline void setRandom(bool v = true) {random = v;};

	/**
	 * Comprueba el flag de poda
	 */
	inline bool isFirst(void) const {return first;};

	/**
	 * Comprueba el flag de random en la selección de métodos 
	 */
	inline bool isRandom(void) const {return random;};


	inline void setTPoints(unsigned int first, unsigned int second) {tpoints.first = first; tpoints.second = second;};

	inline TPoints getTPoints(void) const {return tpoints;};


    protected:
	/** Los métodos que contiene la tarea compuesta */
	vector<Method *> methods;
	/** Este flag sirve para podar el resto de métodos cuando las
	 * precondiciones de un método se han cumplido con éxito. */
	bool first;
        /**
         * Modo ramdom en la selección de métodos
         **/
        bool random;

	TPoints tpoints;
};

#endif
