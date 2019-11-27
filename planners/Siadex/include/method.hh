/* ****************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

#ifndef METHOD_H
#define METHOD_H
#include "literal.hh"
#include "goal.hh"
#include "tasknetwork.hh"
#include "compoundtask.hh"
#include "unifiable.hh"

class Method : public Unifiable, public ParameterContainer
{
    public:

	/**
	  @brief Constructor. Asocia el método a la tarea compuesta t. Los parámetros de
	  la tarea t se asignan también al método, no se clonan, son los mismos.
	  @param t La tarea compuesta a la que pertenece el método.
	  @param tasknetwork (opcional defecto nulo). La red de tareas del método. La
	  red de tareas se pasa por referencia. Esto quiere decir que este objeto se hace
	  cargo del puntero a todos los efectos de gestión de memoria.
	  @see setTaskNetwork
	  */
	Method(int mid, const CompoundTask *t, TaskNetwork * tasknetwork=0);

	/**
	 * Constructor de copia
	 */
	Method(const CompoundTask *t, const Method * other);

	/**
	  @brief Destructor
	  */
	virtual ~Method(void);

	/**
	  @brief Añade una nueva precondición al método.
	  @description g Se añade por referencia al objeto, esto quiere decir que una vez
	  pasado este objeto, el puntero no debería ser alterado ni liberado.
	  @param g La precondición a añadir.
	  @author oscar
	  */
	inline void setPrecondition(Goal * g) {precondition = g;};

	inline Goal * getPrecondition(void) {return precondition;};

	/**
	  @brief Devuelve un puntero a la red de tareas del método
	  */
	inline TaskNetwork * getTaskNetwork(void) const {return tasknetwork;};

	/**
	  @brief Edita la red de tareas del método
	  @param tn: La nueva red de tareas del método
	  Precondición: El método no puede tener ninguna red de tareas previamente asignada.
	  @author oscar
	*/
	inline void setTaskNetwork(TaskNetwork *tn) {tasknetwork = tn;};

	/**
	  @brief Imprime en el flujo una cadena descriptiva con el contenido del método.
	  Si el flujo es null (por defecto) se imprime en la salida estándar
	  */
	void print(ostream * os, int indent=0) const;

	virtual void vcprint(ostream * os, int indent=0) const {print(os,indent);};

	void toxml(ostream * os) const;

	void toxml(XmlWriter * writer) const;

	virtual void vctoxml(XmlWriter * w) const {toxml(w);};

	/**
	  @brief Realiza la clonación de un método.
	  Es extraño llamar a este método. Debería llamarse al clone de la clase
	  Tarea compuesta.
	  */
	Method * clone(const CompoundTask * ct) const;

	virtual pkey getTermId(const char * name) const;

	virtual bool hasTerm(int id) const;

	virtual void renameVars(Unifier * u, VUndo * undo);

	virtual const char * getName(void) const;

	virtual void setName(const char * n);

	inline int getMetaId(void) const {return metaid;};

	inline void setMetaId(int i) {metaid = i;};

	virtual bool isReachable(ostream * err) const;

	virtual bool provides(const Literal * l) const;

    protected:
	const CompoundTask *compoundtask;
	Goal * precondition;
	TaskNetwork *tasknetwork;
	int metaid;
	/** Esto realiza un mapeado entre las variables del método
	 * y las variables usadas como parámetro en la tarea compuesta
	 * contenedora. El método y la tarea compuesta contenedora
	 * tienen contextos distintos
	 */
	vector<pair<int,int> > mapping;
};

#endif
