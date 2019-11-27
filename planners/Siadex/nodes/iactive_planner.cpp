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
 * Created by oscar oscar@decsai.ugr.es: lun 29 ago, 2005  09:34
 * Last modified: o.garcia vie 31 oct, 2008  01:49
 * ********************************************************************************** */

#include "constants.hh"
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <pthread.h>
#include <getopt.h>
#include "debugger.hh"
#include "termTable.hh"
#include "pythonWrapper.hh"
#include "papi.hh"
#include "problem.hh"
#include "controlrules.hh"
#include "selector.hh"
#include "replan.hh"
#include "plan.hh"

using namespace std;

/** Definición de variables globales */
extern int idCounter;
// variable que activa desactiva el modo de depuración del parser
extern int yydebug;
// flujo donde se imprimirán los mensajes de error
extern ostream * errflow;
// Objeto que hace de interfaz con el parser
extern PAPI * parser_api;

extern void check_key(void);

void sintaxis(string progName)
{
    *errflow << "Syntax: " << progName << " [options] --domain_file (-d) <domain.pddl> --problem_file (-p) <problem.pddl>" << endl << endl;
    *errflow << "Options:" << endl;
    *errflow << "\t--help (-h):\tShows this screen." << endl;
    *errflow << "\t--debug (-g):\tRuns the planner on debug mode." << endl;
    *errflow << "\t--verbose (-v[<level>] i.e: -v1):\tSets on the verbose mode (1,2 o 3) (default 2)." << endl;
    *errflow << "\t--output_file (-o) {filename}:\tWrites resulting plan in a plain text file." << endl;
    *errflow << "\t--xml_file (-x) {filename}:\tWrites resulting plan in xml format." << endl;
    *errflow << "\t--expansions_limit <number> :\tMaximun number of allowed expansions." << endl;
    *errflow << "\t--depth_limit <number> :\tMaximun depth during expansions." << endl;
    *errflow << "\t--time_limit <number> :\tMaximun time of execution, in seconds." << endl;
    *errflow << "\t--seed (-s) <number> :\tRandom seed." << endl;
    *errflow << endl << parser_api->ver();
    exit(EXIT_FAILURE);
}

/**
 * Función main del programa SIADEX.
 * Se inicializan los distintos objetos y se realiza una llamada al planificador.
 **/
int main(int argc, char *argv[]){
    // inicialización del flujo donde se pondrán los mensajes de error
    errflow = &cerr;
    // el fichero de dominio
    string domainf="";
    // el fichero de problema
    string problemf="";
    // por defecto se activa la comprobación de errores de dominio rápida
    bool fast = true;
    // nombre del fichero donde se escribirá la salida del planificador en texto plano
    string fout="";
    // nombre del fichero donde se escribirá el plan resultante en formato xml
    string xml_out="";
    // nivel de mensajes que sacará el planificador por pantalla
    int verbosity = 0;
    // Modulo que usaremos para tomar las decisiones en los puntos de decision
    Selector select;
    // limites en expansion profundiad y tiempo para parar el planificador
    int elimit = 0;
    int dlimit = 0;
    int tlimit = 0;
    // El objeto que calcula el plan resultante
    Plan * plan=0;
    // Esta variable pone al parser en modo de depuración
    //yydebug=1;
    int seed = -1;

    // ----------------------------------------------------
    // Captura de los parámetros desde la línea de órdenes.
    // ----------------------------------------------------

    // La opción que se está leyendo desde la línea de órdenes
    int siguiente_opcion;

    // Una cadena que lista las opciones cortas válidas 
    const char* const op_cortas = "hv::gd:p:o:x:" ;

    // El indice a la opcion
    int option_index;

    // Una estructura de varios arrays describiendo las opciones en formato largo
    const struct option op_largas[] =
    {
        {"help",	    no_argument,	    0,   'h'},
        {"verbose",	    optional_argument,	    0,   'v'},
        {"debug",	    no_argument,	    0,   'g'},
        {"domain_file",	    required_argument,	    0,   'd'},
        {"problem_file",    required_argument,	    0,   'p'},
        {"out_file",	    required_argument,	    0,   'o'},
        {"xml_file",	    required_argument,	    0,   'x'},
        {"seed",	    required_argument,	    0,   's'},
        {"expansions_limit",	required_argument,	0,   '1'},
        {"time_limit",	    required_argument,	    0,   '2'},
        {"depth_limit",	    required_argument,	    0,   '3'},
        {0,		    0,			    0,   0  }
    };

    *errflow << endl;

    while (1){
        /* Llamamos a la función getopt */
        siguiente_opcion = getopt_long (argc, argv, op_cortas, op_largas, &option_index);

        if (siguiente_opcion == -1)
            break; /* No hay más opciones. Rompemos el bucle */

        switch (siguiente_opcion)
        {
            case 'h' : /* -h o --help */
                sintaxis(argv[0]);
                break;

            case 'v' : /* -v o --verbose */
                if(optarg){
                    verbosity = atoi(optarg);
                }
                else{
                    verbosity = 2;
                }
                if(verbosity < 0 || verbosity > 3){
                    *errflow << "Invalid verbosity level (" << optarg << "), setting to default." << endl;
                    verbosity = 2 ;
                }
                break;

            case 'g' : /* -g o --debug */
                // se activa el modo de depuración
                FLAG_DEBUG = true;
                break;

            case 'd' : /* -d o --domain_file */
                // capturamos el fichero de dominio
                domainf=optarg;
                break;

            case 'p' : /* -p o --problem_file */
                // capturamos el fichero de problema 
                problemf=optarg;
                break;

            case 'o' : /* -p o --outfile */
                // capturamos el fichero de salida 
                fout=optarg;
                break;

            case 'x' : /* -x o --xml_file */
                // capturamos el fichero de salida xml 
                xml_out=optarg;
                break;

            case '1' : /* --expansions_limit */
                if(optarg)
                    elimit=atoi(optarg);
                break;

            case '2' : /* --time_limit */
                if(optarg)
                    tlimit=atoi(optarg);
                break;

            case '3' : /* --depth_limit */
                if(optarg)
                    dlimit=atoi(optarg);
                break;

            case 's' : /* -s o --seed */
                if(optarg){
                    seed = atoi(optarg);
                }
                break;
            case '?' : /* opción no valida */
                *errflow << "Type `" << argv[0] << " --help' to get the list of available options." << endl;
                exit(EXIT_FAILURE);
                break;

            default : /* Algo más? No esperado. Abortamos */
                *errflow << "Unexpected argument: -" << (unsigned char) siguiente_opcion << endl;
                *errflow << "Type `" << argv[0] << " --help' to get the list of available options." << endl;
                exit(1);
        }
    } 

    // Cualquier otra cosa que quede en la línea de órdenes es un error
    if (optind < argc){
        printf ("non-option ARGV-elements: ");
        while (optind < argc)
            printf ("%s ", argv[optind++]);
        putchar ('\n');
        abort();
    }

    if(seed != -1) {
        srand((unsigned int)seed);
    }
    else {
        srand((unsigned int)time(0));
    }

    // Comprobamos que tanto el fichero de dominio como el de problema
    // estén definidos
    if(domainf.length() == 0){
        *errflow << "Error: Undefined domain file option --domain_file." << endl;
        *errflow << "Type `" << argv[0] << " --help' to get the list of available options." << endl;
        exit(EXIT_FAILURE);
    }

    if(problemf.length() == 0 ){
        *errflow << "Error: Undefined problem file option --problem_file." << endl;
        *errflow << "Type `" << argv[0] << " --help' to get the list of available options." << endl;
        exit(EXIT_FAILURE);
    }


    // ----------------------------------------------------
    // Lanzar el proceso de planificación.
    // ----------------------------------------------------

    // este índice mantiene un contador de identificadores que van siendo asignados a
    // variables, literales, funciones y constantes.
    idCounter = 0;

    // controla si se produjeron errores durante el proceso de planificación
    bool errors = false;
    try{
        parser_api = new PAPI();
        // parsear el fichero de dominio y de problema
        parser_api->parse(domainf.c_str(),problemf.c_str(),fast);
        if(parser_api->errors)
            errors = true;
        if(FLAG_DEBUG){
            // inicializar el depurador integrado
            debugger = new Debugger();
            if(verbosity == 0)
                verbosity = 2;
        }

        if(!errors){
            // si no se produjeron errores.
            // Se inicializa el algoritmo de planificación
            plan = new Plan(parser_api->domain,parser_api->problem);

            if(FLAG_DEBUG){
                // Se establece el depurador como objeto que toma el control en los puntos de decisión
                plan->setSelector(debugger);
            }
            else {
                // Reglas de decisión por defecto 
                plan->setSelector(&select);
            }

            // Flags para cortar el proceso de planificación y para establecer el nivel de detalle
            // de los mensajes por pantalla.
            plan->FLAG_EXPANSIONS_LIMIT = elimit;
            plan->FLAG_DEPTH_LIMIT = dlimit;
            plan->FLAG_TLIMIT = tlimit;
            plan->FLAG_VERBOSE = verbosity;

            check_key();
            plan->solve();

            if(!fout.empty()){
                // si se estableció como salida un fichero de texto se imprime allí
                ofstream * tmp = openwfile(fout.c_str());
                plan->printPlan(tmp);
                delete tmp;
                tmp = 0;
            }
            else{
                // en otro caso se imprime por pantalla
                plan->printPlan(&cout); 
            }

            if(!xml_out.empty()){
                // si se pidió que se generara un xml con el resultado del plan se hace ahora.
                ofstream * tmp = openwfile(xml_out.c_str());
                plan->toxml(tmp,true,false,true);
                delete tmp;
                tmp = 0;
            }
        }

    }
    catch(exception &e){
        cerr << "Exception caught!: " << e.what() << endl;
    }
    catch(...) {
        cerr << "Exception caught!: ??" << endl;
    }


    if(!errors){
        plan->printStatistics(errflow);
    }


    delete parser_api;

    //myinfo=mallinfo();
    //cout << "Memory allocated (bytes): " << myinfo.hblkhd << " Memory chunks occupied: " << myinfo.uordblks << endl;
    exit(EXIT_SUCCESS);    

}
