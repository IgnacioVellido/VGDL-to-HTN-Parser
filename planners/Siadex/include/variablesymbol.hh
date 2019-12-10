/* ****************************************************************************
 * Copyright (C) 2008, IActive Intelligent Solutions S.L. http://www.iactive.es
 * ***************************************************************************/

#ifndef VARIABLESYMBOL_HH
#define VARIABLESYMBOL_HH

using namespace std;

#include "constants.hh"
#include <string>
#include "term.hh"
#include "constantsymbol.hh"
#include "undoChangeValue.hh"
#include "undoChangeType.hh"

/**
 * Símbolo de variable. 
 * Las variables son símbolos que se deciden en tiempo de planificación
 * tras realizar una unificación.
 */
class VariableSymbol: public Term, public TypeChangeable {
    public:
        /**
          @brief Constructor
          @param s1: Nombre del simbolo.
          */
        VariableSymbol(int id, int mid) :Term(id) {metaid = mid;};

        VariableSymbol(int id, int mid, const vctype * v) :Term(id,v) {metaid = mid;};

        VariableSymbol(const VariableSymbol * other) :Term(other) {metaid = other->getMetaId();};

        VariableSymbol(void) :Term() {metaid=-1;};

        virtual const char * getName(void) const;

        virtual void setName(const char * n);

        virtual ~VariableSymbol() {for_each(references.begin(),references.end(),Delete<UndoChangeValue>());};

        virtual bool isVariable(void) const {return true;};

        /**
          @brief Devuelve un duplicado de la variable
          */
        virtual Term * clone(void) const;

        /**
          @brief Imprime la descripción de la variable en un flujo por defecto el estándar 
          */
        virtual void print(ostream * os, int indent=0) const;

        virtual void toxml(XmlWriter * writer) const;

        inline void addReference(UndoChangeValue * ref) {references.push_back(ref);};

        inline bool hasReference(const ValueChangeable * ptr) {return references.end() != find_if(references.begin(),references.end(),bind2nd(mem_fun(&UndoChangeValue::hasTarget),ptr));}

        inline bool hasReference2(UndoChangeValue * ptr) {return references.end() != find(references.begin(),references.end(),ptr);}

        inline void removeReference(const ValueChangeable * ptr) {references.erase(remove_if(references.begin(),references.end(),bind2nd(mem_fun(&UndoChangeValue::hasTarget),ptr)),references.end());};

        void printReferences(ostream * os) const {
            referencescit i, e;
            e = references.end();
            for(i = references.begin(); i != e; i++) {
                (*i)->print(os);
                *os << " ";
            }
        }

        /**
          Dejo la estructura abierta por comodidad, ¡¡ Cuidado con lo que haces !!
         **/
        VReferences references;

        inline int getMetaId(void) const {return metaid;};

        inline void setMetaId(int i) {metaid = i;};

        virtual vctype * getTypeRef(void) {return &types;};

    protected:
        int metaid;

};

#endif
