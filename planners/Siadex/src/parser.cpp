/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* Copy the first part of user declarations.  */
#line 5 "yacc/parser.yy" /* yacc.c:339  */

    using namespace std;

    #include "constants.hh"
    #include <string>
    #include <iostream>
    #include <stdio.h>
    #include <stdlib.h>
    #include <assert.h>
    #include <vector>
    #include <sys/resource.h>
    #include <math.h>
    #include <malloc.h>
    #include <ctype.h>
    #include "MyLexer.hh"
    #include "domain.hh"
    #include "problem.hh"
    #include "type.hh"
    #include "andGoal.hh"
    #include "papi.hh"
    #include "function.hh"
    #include "pyDefFunction.hh"
    #include "comparationGoal.hh"
    #include "fluentNumber.hh"
    #include "fluentOperator.hh"
    #include "fluentVar.hh"
    #include "forallgoal.hh"
    #include "existsgoal.hh"
    #include "foralleffect.hh"
    #include "cutgoal.hh"
    #include "sortgoal.hh"
    #include "undoARLiteralState.hh"
    #include "fluentEffect.hh"
    #include "wheneffect.hh"
    #include "fluentLiteral.hh"
    #include "literalgoal.hh"
    #include "orGoal.hh"
    #include "boundGoal.hh"
    #include "implyGoal.hh"
    #include "fluentConstant.hh"
    #include "timeInterval.hh"
    #include "printGoal.hh"
    #include "debugger.hh"
    #include "timeLineLitEffect.hh"
    #include "plan.hh"
    #include "textTag.hh"

    #define yytrue true
    #define yyfalse false
    #define DEBUG 0
    #define YYDEBUG 1
    #define YYMAXDEPTH INT_MAX

#ifdef PYTHON_FOUND
    #define PYTHON_FLAG 1
#else
    #define PYTHON_FLAG 0
#endif

// variables globales
// estas variables sirven para ir almacenando los valores
// que vamos capturando
ParameterContainer * container=0;
LDictionary * context=0;
LDictionary * oldContext=0;
vector<ContainerGoal *> gcontainer;
vector<ContainerEffect *> econtainer;
CompoundTask * cbuilding=0;
// Espera encontrar un n�mero
bool isNumber = false;
// Espera encontrar un at
bool AtExpected=false;
// determina si la acci�n que estamos parseando es o no durativa
bool isDurative = false;

// variable para construir los mensajes de error
char parerr[256];
// imprimir o no errores de tipos
bool errtypes=true;

int contador=0;

// Usar este objeto como interfaz con el debugger
extern Debugger * debugger;
// esperar o no tokens del debugger
bool inDebugContext= false;

// flags del parser
// evitar o no la mayor�a de los chequeos
bool fast_parsing = false;

inline int yylex(void)
{
    return lexer->yylex();
};

inline void yyerror(const char *s)
{
    lexer->LexerError(s);
};

inline void yywarning(const char *s)
{
    lexer->LexerWarning(s);
};

struct SearchLineInfo
{
    string fileName;
    int lineNumber;

    SearchLineInfo(const Type * t)
    {
        if(t->getFileId() != -1) {
        fileName = parser_api->files[t->getFileId()];
        lineNumber = t->getLineNumber();
        }
        else{
        fileName = "";
        lineNumber = 0;
        }
    }

    SearchLineInfo(const ConstantSymbol * c)
    {
        fileName = parser_api->files[c->getFileId()];
        lineNumber = c->getLineNumber();
    }

    SearchLineInfo(int mid) {
        Meta * m = parser_api->domain->metainfo[mid];
        fileName = parser_api->files[m->fileid];
        lineNumber = m->linenumber;
    }
};

// este operador verifica que no se dan definiciones
// de tipos redundantes
struct TestTypeTree {
    void operator()(Type * t) const {
        vector<Type *>::const_iterator i,e,j;
        e = t->getParentsEnd();
        if(t->getNumberOfParents() > 0)
        for(i = t->getParentsBegin(); i != e; i++){
                if((*i)->isSubTypeOf(t)){
                SearchLineInfo sli((*i));
                snprintf(parerr,256,"Ambiguous declaration type `%s' is subtype of `%s' near %d [%s].",(*i)->getName(),t->getName(),sli.lineNumber,sli.fileName.c_str());
                yyerror(parerr);
                }
                else{
                for(j = t->getParentsBegin(); j != e; j++)
                        if(i != j && (*i)->isSubTypeOf((*j))){
                        SearchLineInfo sli((*j));
                        snprintf(parerr,256,"Ambiguous declaration type `%s' is subtype of `%s' near %d [%s].",(*i)->getName(),(*j)->getName(),sli.lineNumber,sli.fileName.c_str());
                        yywarning(parerr);
                        }
                }
        }
    };

   void operator()(vector<Type *> * vt) const {
        vector<Type *>::const_iterator i,e,j;
        e = vt->end();
        for(i = vt->begin(); i != e; i++){
        for(j = vt->begin(); j != e; j++)
        if(i != j && (*i)->isSubTypeOf((*j))){
                SearchLineInfo sli((*j));
                snprintf(parerr,256,"Ambiguous declaration type `%s' is subtype of `%s' near %d [%s].",(*i)->getName(),(*j)->getName(),sli.lineNumber,sli.fileName.c_str());
                yywarning(parerr);
        }
        }
   };
};


// este operador verifica que un tipo est� correctamente
// definido
struct TestType {
   void operator()(Type * t) const {
       // Se trata del tipo number
       if(t->getId() == 0)
        return;

       SearchLineInfo sli(t);
       if(!sli.lineNumber) {
        snprintf(parerr,256,"Trying to use an undefined type `%s'.",t->getName());
        yyerror(parerr);
       }
       else{
        TestTypeTree()(t);
       }
   };
};


#line 262 "src/parser.cpp" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 1
#endif

/* In a future release of Bison, this section will be replaced
   by #include "parser.hpp".  */
#ifndef YY_YY_SRC_PARSER_HPP_INCLUDED
# define YY_YY_SRC_PARSER_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    LEFTPAR = 258,
    RIGHTPAR = 259,
    PDDL_DEFINE = 260,
    PDDL_DOMAIN = 261,
    PDDL_DOMAINREF = 262,
    PDDL_PROBLEM = 263,
    PDDL_CONSTANTS = 264,
    PDDL_NAME = 265,
    PDDL_VAR = 266,
    PYTHON_CODE = 267,
    PDDL_NUMBER = 268,
    PDDL_DNUMBER = 269,
    PDDL_REQUIREMENTS = 270,
    PDDL_TYPES = 271,
    PDDL_HYPHEN = 272,
    PDDL_EITHER = 273,
    PDDL_STRIPS = 274,
    PDDL_TYPING = 275,
    PDDL_NEGATIVE_PRECONDITIONS = 276,
    PDDL_DISJUNTIVE_PRECONDITIONS = 277,
    PDDL_EQUALITY = 278,
    PDDL_EXISTENTIAL_PRECONDITIONS = 279,
    PDDL_UNIVERSAL_PRECONDITIONS = 280,
    PDDL_QUANTIFIED_PRECONDITIONS = 281,
    PDDL_CONDITIONAL_EFFECTS = 282,
    PDDL_FLUENTS = 283,
    PDDL_ADL = 284,
    PDDL_DURATIVE_ACTIONS = 285,
    PDDL_DERIVED_PREDICATES = 286,
    PDDL_TIMED_INITIAL_LITERALS = 287,
    PDDL_PREDICATES = 288,
    PDDL_FUNCTIONS = 289,
    PDDL_ACTION = 290,
    PDDL_PARAMETERS = 291,
    PDDL_NOT = 292,
    PDDL_PRECONDITION = 293,
    PDDL_IMPLY = 294,
    PDDL_AND = 295,
    PDDL_OR = 296,
    PDDL_EXISTS = 297,
    PDDL_FORALL = 298,
    PLUS = 299,
    DIVIDE = 300,
    MULTIPLY = 301,
    POW = 302,
    ABS = 303,
    SQRT = 304,
    GREATHER = 305,
    LESS = 306,
    EQUAL = 307,
    DISTINCT = 308,
    GREATHER_EQUAL = 309,
    LESS_EQUAL = 310,
    PDDL_EFFECT = 311,
    PDDL_ASSIGN = 312,
    PDDL_SCALE_UP = 313,
    PDDL_SCALE_DOWN = 314,
    PDDL_INCREASE = 315,
    PDDL_DECREASE = 316,
    PDDL_WHEN = 317,
    PDDL_GOAL = 318,
    PDDL_AT = 319,
    PDDL_ATSTART = 320,
    PDDL_ATEND = 321,
    PDDL_BETWEEN = 322,
    PDDL_OBJECT = 323,
    PDDL_INIT = 324,
    PDDL_OVERALL = 325,
    PDDL_DURATIONVAR = 326,
    STARTVAR = 327,
    ENDVAR = 328,
    PDDL_DERIVED = 329,
    PDDL_CONDITION = 330,
    PDDL_DURATION = 331,
    PDDL_DURATIVE_ACTION = 332,
    HTN_EXPANSION = 333,
    META_TAGS = 334,
    META = 335,
    TAG = 336,
    HTN_TASK = 337,
    HTN_TASKS = 338,
    HTN_ACHIEVE = 339,
    HTN_METHOD = 340,
    HTN_TASKSGOAL = 341,
    HTN_INLINE = 342,
    HTN_INLINECUT = 343,
    HTN_TEXT = 344,
    LEFTBRAC = 345,
    RIGHTBRAC = 346,
    EXCLAMATION = 347,
    RANDOM = 348,
    SORTBY = 349,
    ASC = 350,
    DESC = 351,
    PDDL_BIND = 352,
    MAINTAIN = 353,
    PPRINT = 354,
    PDDL_AND_EVERY = 355,
    CUSTOMIZATION = 356,
    TIMEUNIT = 357,
    TIMESTART = 358,
    TIMEFORMAT = 359,
    TIMEHORIZON = 360,
    RELTIMEHORIZON = 361,
    THOURS = 362,
    TMINUTES = 363,
    TSECONDS = 364,
    TDAYS = 365,
    TMONTHS = 366,
    TYEARS = 367,
    PYTHON_INIT = 368,
    DBG_DEBUG = 369,
    DBG_QUIT = 370,
    DBG_BREAKPOINT = 371,
    DBG_WATCH = 372,
    DBG_CONTINUE = 373,
    DBG_HELP = 374,
    DBG_PATH = 375,
    DBG_PRINT = 376,
    DBG_DISPLAY = 377,
    DBG_DESCRIBE = 378,
    DBG_UNDISPLAY = 379,
    DBG_STATE = 380,
    DBG_AGENDA = 381,
    DBG_PLAN = 382,
    DBG_NEXT = 383,
    DBG_NEXP = 384,
    DBG_SET = 385,
    DBG_VIEWER = 386,
    DBG_DOTPATH = 387,
    DBG_TMPDIR = 388,
    DBG_PLOT = 389,
    DBG_CAUSAL = 390,
    DBG_MEM = 391,
    DBG_SELECT = 392,
    DBG_VERBOSE = 393,
    DBG_ON = 394,
    DBG_OFF = 395,
    DBG_OPTIONS = 396,
    DBG_TERMTABLE = 397,
    DBG_PREDICATES = 398,
    DBG_TASKS = 399,
    DBG_ENABLE = 400,
    DBG_DISABLE = 401,
    DBG_EVAL = 402,
    DBG_VERBOSITY = 403,
    DBG_APPLY = 404
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 208 "yacc/parser.yy" /* yacc.c:355  */

        void * otype;
        const void * cotype;
        const char * type_string;
        double type_number;
        pair<int,float> * termtype;
        int type_int;

#line 461 "src/parser.cpp" /* yacc.c:355  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_SRC_PARSER_HPP_INCLUDED  */

/* Copy the second part of user declarations.  */

#line 478 "src/parser.cpp" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  9
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   954

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  150
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  195
/* YYNRULES -- Number of rules.  */
#define YYNRULES  434
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  774

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   404

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124,
     125,   126,   127,   128,   129,   130,   131,   132,   133,   134,
     135,   136,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   440,   440,   441,   442,   445,   452,   457,   458,   461,
     462,   465,   466,   469,   470,   473,   474,   477,   478,   481,
     482,   485,   515,   518,   530,   533,   545,   555,   558,   561,
     562,   563,   566,   568,   570,   572,   574,   576,   578,   580,
     582,   584,   586,   588,   590,   592,   594,   596,   601,   607,
     624,   629,   630,   654,   654,   654,   685,   689,   690,   693,
     710,   731,   755,   759,   765,   771,   785,   802,   831,   837,
     845,   848,   849,   853,   852,   903,   907,   906,   965,   972,
     972,   975,   976,   991,  1019,  1029,  1031,  1035,  1034,  1104,
    1110,  1115,  1116,  1130,  1131,  1134,  1135,  1136,  1144,  1145,
    1150,  1176,  1148,  1205,  1203,  1257,  1264,  1269,  1276,  1282,
    1288,  1294,  1300,  1307,  1311,  1317,  1323,  1329,  1335,  1341,
    1347,  1353,  1359,  1365,  1373,  1379,  1387,  1388,  1392,  1397,
    1402,  1408,  1409,  1415,  1417,  1418,  1412,  1472,  1476,  1483,
    1486,  1495,  1494,  1523,  1525,  1527,  1532,  1531,  1561,  1560,
    1592,  1591,  1623,  1627,  1652,  1658,  1666,  1670,  1676,  1702,
    1718,  1741,  1754,  1777,  1793,  1794,  1798,  1800,  1807,  1813,
    1806,  1833,  1832,  1847,  1853,  1860,  1859,  1871,  1875,  1882,
    1888,  1881,  1897,  1903,  1896,  1911,  1927,  1937,  1943,  1936,
    1960,  1968,  1959,  1984,  1986,  1990,  2007,  2010,  2014,  2020,
    2021,  2024,  2032,  2033,  2043,  2045,  2055,  2054,  2118,  2117,
    2181,  2182,  2185,  2211,  2221,  2256,  2267,  2269,  2272,  2276,
    2280,  2284,  2290,  2328,  2340,  2346,  2352,  2358,  2364,  2370,
    2378,  2384,  2402,  2427,  2431,  2447,  2470,  2471,  2475,  2477,
    2479,  2483,  2488,  2493,  2498,  2569,  2568,  2687,  2686,  2749,
    2750,  2754,  2757,  2756,  2767,  2771,  2797,  2805,  2795,  2821,
    2831,  2833,  2837,  2838,  2847,  2857,  2864,  2868,  2869,  2879,
    2878,  2889,  2893,  2897,  2901,  2905,  2909,  2915,  2916,  2919,
    2920,  2923,  2924,  2927,  2928,  2931,  2931,  2945,  2948,  2952,
    2957,  2969,  2969,  2991,  3013,  3023,  3028,  3029,  3032,  3034,
    3070,  3072,  3081,  3080,  3143,  3170,  3185,  3141,  3206,  3212,
    3220,  3227,  3232,  3238,  3244,  3251,  3261,  3265,  3269,  3273,
    3273,  3273,  3286,  3285,  3297,  3312,  3330,  3330,  3330,  3334,
    3340,  3344,  3345,  3349,  3350,  3351,  3352,  3353,  3354,  3355,
    3356,  3357,  3358,  3362,  3366,  3371,  3375,  3379,  3385,  3395,
    3401,  3406,  3419,  3432,  3437,  3443,  3449,  3459,  3472,  3479,
    3486,  3493,  3500,  3509,  3514,  3523,  3527,  3527,  3527,  3535,
    3539,  3543,  3547,  3551,  3555,  3561,  3567,  3567,  3567,  3577,
    3583,  3589,  3593,  3597,  3605,  3609,  3614,  3621,  3625,  3629,
    3633,  3637,  3641,  3645,  3649,  3656,  3660,  3660,  3660,  3666,
    3670,  3674,  3678,  3678,  3678,  3696,  3699,  3704,  3704,  3704,
    3712,  3712,  3712,  3721,  3721,  3721,  3734,  3733,  3815,  3818,
    3819,  3822,  3823,  3826,  3830,  3834,  3838,  3842,  3851,  3862,
    3866,  3870,  3874,  3878,  3882
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 1
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "LEFTPAR", "RIGHTPAR", "PDDL_DEFINE",
  "PDDL_DOMAIN", "PDDL_DOMAINREF", "PDDL_PROBLEM", "PDDL_CONSTANTS",
  "PDDL_NAME", "PDDL_VAR", "PYTHON_CODE", "PDDL_NUMBER", "PDDL_DNUMBER",
  "PDDL_REQUIREMENTS", "PDDL_TYPES", "PDDL_HYPHEN", "PDDL_EITHER",
  "PDDL_STRIPS", "PDDL_TYPING", "PDDL_NEGATIVE_PRECONDITIONS",
  "PDDL_DISJUNTIVE_PRECONDITIONS", "PDDL_EQUALITY",
  "PDDL_EXISTENTIAL_PRECONDITIONS", "PDDL_UNIVERSAL_PRECONDITIONS",
  "PDDL_QUANTIFIED_PRECONDITIONS", "PDDL_CONDITIONAL_EFFECTS",
  "PDDL_FLUENTS", "PDDL_ADL", "PDDL_DURATIVE_ACTIONS",
  "PDDL_DERIVED_PREDICATES", "PDDL_TIMED_INITIAL_LITERALS",
  "PDDL_PREDICATES", "PDDL_FUNCTIONS", "PDDL_ACTION", "PDDL_PARAMETERS",
  "PDDL_NOT", "PDDL_PRECONDITION", "PDDL_IMPLY", "PDDL_AND", "PDDL_OR",
  "PDDL_EXISTS", "PDDL_FORALL", "PLUS", "DIVIDE", "MULTIPLY", "POW", "ABS",
  "SQRT", "GREATHER", "LESS", "EQUAL", "DISTINCT", "GREATHER_EQUAL",
  "LESS_EQUAL", "PDDL_EFFECT", "PDDL_ASSIGN", "PDDL_SCALE_UP",
  "PDDL_SCALE_DOWN", "PDDL_INCREASE", "PDDL_DECREASE", "PDDL_WHEN",
  "PDDL_GOAL", "PDDL_AT", "PDDL_ATSTART", "PDDL_ATEND", "PDDL_BETWEEN",
  "PDDL_OBJECT", "PDDL_INIT", "PDDL_OVERALL", "PDDL_DURATIONVAR",
  "STARTVAR", "ENDVAR", "PDDL_DERIVED", "PDDL_CONDITION", "PDDL_DURATION",
  "PDDL_DURATIVE_ACTION", "HTN_EXPANSION", "META_TAGS", "META", "TAG",
  "HTN_TASK", "HTN_TASKS", "HTN_ACHIEVE", "HTN_METHOD", "HTN_TASKSGOAL",
  "HTN_INLINE", "HTN_INLINECUT", "HTN_TEXT", "LEFTBRAC", "RIGHTBRAC",
  "EXCLAMATION", "RANDOM", "SORTBY", "ASC", "DESC", "PDDL_BIND",
  "MAINTAIN", "PPRINT", "PDDL_AND_EVERY", "CUSTOMIZATION", "TIMEUNIT",
  "TIMESTART", "TIMEFORMAT", "TIMEHORIZON", "RELTIMEHORIZON", "THOURS",
  "TMINUTES", "TSECONDS", "TDAYS", "TMONTHS", "TYEARS", "PYTHON_INIT",
  "DBG_DEBUG", "DBG_QUIT", "DBG_BREAKPOINT", "DBG_WATCH", "DBG_CONTINUE",
  "DBG_HELP", "DBG_PATH", "DBG_PRINT", "DBG_DISPLAY", "DBG_DESCRIBE",
  "DBG_UNDISPLAY", "DBG_STATE", "DBG_AGENDA", "DBG_PLAN", "DBG_NEXT",
  "DBG_NEXP", "DBG_SET", "DBG_VIEWER", "DBG_DOTPATH", "DBG_TMPDIR",
  "DBG_PLOT", "DBG_CAUSAL", "DBG_MEM", "DBG_SELECT", "DBG_VERBOSE",
  "DBG_ON", "DBG_OFF", "DBG_OPTIONS", "DBG_TERMTABLE", "DBG_PREDICATES",
  "DBG_TASKS", "DBG_ENABLE", "DBG_DISABLE", "DBG_EVAL", "DBG_VERBOSITY",
  "DBG_APPLY", "$accept", "pddl_root", "problem_definition",
  "domain_definition", "domain_definition_2", "domain_definition_31",
  "domain_definition_32", "domain_definition_3", "domain_definition_4",
  "domain_definition_5", "domain_definition_6", "domain_definition_7",
  "domainName", "problemName", "domainRef", "require_def",
  "require_key_list", "require_key", "term_name", "types_def",
  "constants_def", "typed_list", "$@1", "$@2", "constant_list",
  "constant_def_list", "type", "type_def_list", "type_ref",
  "type_ref_list", "predicates_def", "atomic_formula_skeleton_list",
  "atomic_formula_skeleton", "$@3", "derived_formula_skeleton", "$@4",
  "variable_typed_list", "$@5", "var_typel", "functions_def",
  "function_typed_list", "function_def", "$@6", "opt_type", "code",
  "structure_def_list", "structure_def", "action_def", "@7", "$@8",
  "htn_task_def", "$@9", "duration_constraints", "sdur_constraint",
  "simple_duration_constraint", "sduration_constraint_list",
  "methods_def_body", "method_list", "method_body", "$@10", "$@11", "@12",
  "meta_list", "tag_list", "tag_element", "@13", "task_def", "inlinetask",
  "@14", "@15", "atomic_task_formula", "$@16", "task_network", "task_list",
  "task_element", "preconditions_def", "goal_def", "@17", "$@18", "@19",
  "@20", "simple_goal_def", "@21", "$@22", "@23", "$@24", "@25", "$@26",
  "@27", "$@28", "timed_goal", "order", "v_list", "v_crit",
  "goal_def_list", "atomic_formula_term_effect", "literal_effect", "$@29",
  "atomic_formula_term_goal", "$@30", "term_list", "term", "number", "var",
  "variable", "f_comp", "binary_comp", "fluent_exp", "silly_exp",
  "unary_op", "binary_op", "f_head", "$@31", "f_head_ref", "$@32",
  "effect_def", "effect", "$@33", "timed_effect", "c_effect", "@34",
  "$@35", "c_effect_list", "p_effect", "p_effect_list", "cond_effect",
  "$@36", "assign_op", "problemBody", "problemBody21", "problemBody22",
  "problemBody2", "problemBody3", "$@37", "object_declaration", "init",
  "init_el", "$@38", "optional_repetition", "init_el_list", "goal",
  "literal_name", "atomic_formula_name", "$@39", "durative_action_def",
  "@40", "$@41", "$@42", "sdur_constraint_list", "pduration_constraints",
  "time_specifier", "time_point", "number_time_point", "$@43", "$@44",
  "derived_def", "$@45", "derived_body", "debug_sentence", "$@46", "$@47",
  "command", "help", "print", "$@48", "$@49", "display", "$@50", "$@51",
  "plot", "undisplay", "set", "breakpoint", "$@52", "$@53", "$@54", "$@55",
  "met_name", "eval", "$@56", "$@57", "apply", "$@58", "$@59", "describe",
  "$@60", "$@61", "simple_formula_term_goal", "$@62", "customization_def",
  "customization_body", "customization_list", "customization_element",
  "python_init", "time_unit", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377,   378,   379,   380,   381,   382,   383,   384,
     385,   386,   387,   388,   389,   390,   391,   392,   393,   394,
     395,   396,   397,   398,   399,   400,   401,   402,   403,   404
};
# endif

#define YYPACT_NINF -628

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-628)))

#define YYTABLE_NINF -403

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
      22,  -628,    37,    62,  -628,  -628,  -628,   -29,   311,  -628,
     675,  -628,   368,   195,   569,  -628,    42,  -628,  -628,   710,
     596,    21,  -628,    81,  -628,  -628,   -74,   -72,  -628,    95,
      10,   114,   141,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,   152,   152,   166,   159,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,   231,   357,
     431,   442,   471,   182,   484,  -628,  -628,  -628,  -628,   552,
     599,  -628,   206,   216,  -628,   227,   244,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
     227,  -628,  -628,  -628,  -628,  -628,   227,   227,  -628,   198,
     236,   239,   248,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
     244,   302,  -628,  -628,   327,   349,   325,   663,    83,   676,
    -628,   152,  -628,   152,   152,   318,   345,   169,  -628,   356,
    -628,   672,  -628,    -1,  -628,   320,  -628,  -628,  -628,  -628,
      31,  -628,   295,  -628,   152,    11,   395,   397,  -628,  -628,
    -628,  -628,   402,  -628,   417,   428,   152,   453,   374,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,   362,   372,   415,
     463,  -628,   486,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,   511,    65,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
     597,  -628,  -628,   515,   128,  -628,   152,   524,   604,   254,
    -628,   677,  -628,  -628,   506,   546,   318,  -628,  -628,   561,
     565,   325,  -628,   -30,  -628,  -628,   530,  -628,   603,   -15,
    -628,   200,  -628,  -628,  -628,  -628,  -628,   244,   244,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,   314,  -628,   244,  -628,   207,    29,  -628,   495,   609,
    -628,  -628,   606,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,   664,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,   244,   671,  -628,   695,   701,  -628,  -628,  -628,   251,
    -628,   692,   597,  -628,  -628,  -628,  -628,  -628,  -628,   152,
    -628,  -628,   694,  -628,   152,   185,   709,   696,   698,   531,
    -628,  -628,  -628,  -628,   727,   384,   -26,  -628,  -628,  -628,
     731,   244,  -628,  -628,   733,   749,   715,   759,   207,  -628,
    -628,  -628,  -628,  -628,  -628,   719,   771,  -628,   772,  -628,
     740,  -628,  -628,  -628,  -628,  -628,   495,  -628,   773,  -628,
      36,   774,  -628,   750,   776,   152,   777,  -628,   152,   495,
     473,   778,  -628,   762,  -628,   325,  -628,  -628,  -628,   251,
    -628,  -628,   780,  -628,  -628,  -628,  -628,   792,   797,   430,
     787,   717,   788,   793,  -628,   400,  -628,  -628,  -628,  -628,
     244,   728,   408,  -628,   806,   244,   244,  -628,  -628,   314,
    -628,  -628,   207,   359,   495,  -628,   575,  -628,   583,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,   495,   495,   810,
    -628,   495,  -628,   466,  -628,   517,  -628,   811,  -628,   600,
     812,  -628,   152,  -628,  -628,   813,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,   814,   815,
     819,   825,   826,   832,   833,   498,  -628,  -628,   837,   834,
     760,  -628,  -628,  -628,  -628,   828,  -628,  -628,   838,   842,
     843,   844,  -628,   244,  -628,  -628,  -628,  -628,   845,  -628,
    -628,  -628,   495,   495,  -628,  -628,   399,  -628,  -628,   846,
    -628,  -628,  -628,  -628,  -628,    57,    83,  -628,   490,   847,
     848,   849,   850,   854,  -628,  -628,  -628,  -628,  -628,   152,
     856,   152,   498,   821,  -628,   859,  -628,  -628,   226,   251,
    -628,  -628,  -628,  -628,   860,  -628,   628,  -628,   861,   862,
    -628,  -628,  -628,  -628,  -628,   251,  -628,   851,   728,  -628,
     728,   728,  -628,  -628,   863,   498,   639,    40,   865,   496,
     202,   272,   272,   867,  -628,  -628,  -628,   868,  -628,  -628,
     244,   244,  -628,  -628,  -628,  -628,   302,   500,  -628,   251,
     345,  -628,  -628,   870,  -628,  -628,   763,  -628,  -628,   790,
    -628,  -628,   316,  -628,   244,  -628,  -628,  -628,   303,  -628,
    -628,    45,  -628,   303,   130,   303,   173,   197,  -628,  -628,
     871,   872,   873,  -628,  -628,  -628,  -628,   836,   802,   124,
     875,   877,  -628,   647,   498,   859,   874,  -628,   878,   237,
     118,   378,   510,   519,   879,   244,   244,  -628,   211,   150,
    -628,  -628,   223,  -628,   242,  -628,  -628,  -628,  -628,   244,
     829,   883,   152,    26,    15,  -628,   803,  -628,  -628,  -628,
     885,  -628,   331,  -628,   627,   495,   495,   495,   495,   495,
     495,   495,   495,   495,   495,   495,   495,   495,   495,   495,
    -628,   302,   302,   655,  -628,  -628,  -628,  -628,   302,   886,
     693,  -628,  -628,  -628,   877,   641,   877,   699,  -628,   798,
     591,  -628,  -628,   887,   888,   889,   890,   891,   892,   893,
     894,   895,   896,   897,   898,   899,   900,   901,   902,   903,
    -628,  -628,  -628,  -628,   905,   839,   840,   841,   852,   853,
     807,   728,   705,  -628,   711,  -628,   909,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,   470,  -628,   713,   244,  -628,  -628,
    -628,  -628,  -628,  -628,   858,  -628,   302,   836,   911,   835,
    -628,   226,   912,  -628
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint16 yydefact[] =
{
       0,   329,     0,     0,     3,     2,     4,     0,     0,     1,
       0,    24,     0,     0,     0,   330,   395,   396,   332,   348,
     366,   376,   413,     0,   342,   343,     0,     0,   344,     0,
       0,     0,     0,   407,   410,   327,   331,   333,   334,   336,
     335,   337,   338,   340,   341,   339,     0,     0,    99,     0,
       6,     8,    10,    12,    14,    16,    18,    20,     0,     0,
       0,     0,     0,     0,     0,    95,    98,    96,    97,     0,
       0,    27,     0,     0,   399,     0,     0,   350,   362,   361,
     349,   351,   352,   358,   353,   354,   355,   357,   356,   359,
     360,   363,   364,   365,   369,   370,   371,   372,   374,   373,
       0,   382,   375,   379,   380,   383,     0,     0,   386,   387,
     391,   389,   393,   384,   385,   345,   346,   347,   400,   401,
       0,     0,   328,    48,     0,     0,    57,     0,     0,     0,
      85,     0,   322,     0,     0,   419,    91,     0,     7,     0,
      13,     0,    15,     0,    17,     0,    19,    21,    99,    94,
       0,     9,     0,    11,     0,     0,     0,     0,   278,   280,
     282,   284,     0,   285,     0,     0,     0,   405,   319,   397,
     177,   178,   194,   193,   367,   377,   414,     0,     0,     0,
       0,   408,   319,   266,   204,   411,   261,   254,   260,    23,
      25,    60,     0,    58,    32,    33,    34,    35,    36,    37,
      38,    39,    40,    41,    42,    43,    44,    45,    47,    46,
       0,    56,    65,     0,    52,    75,     0,     0,     0,     0,
     100,     0,   304,   103,     0,     0,   420,   421,    92,     0,
       0,    57,   296,     0,   277,     5,     0,   283,     0,     0,
     279,     0,   281,   416,   406,   403,   166,     0,     0,   179,
     182,   187,   190,   224,   225,   226,   229,   227,   228,   316,
     317,   319,   314,     0,   168,     0,   175,   208,     0,     0,
     313,   318,     0,   398,   368,   378,   415,   388,   392,   390,
     394,   409,   251,     0,   252,   256,   272,   273,   274,   275,
     276,     0,     0,   206,     0,     0,   412,    50,    61,     0,
      31,     0,     0,    49,    66,    53,    73,    70,    72,     0,
      84,    86,     0,    78,     0,    91,     0,     0,     0,     0,
     418,   422,   428,    26,     0,     0,     0,   286,   210,   404,
       0,     0,   202,   202,     0,     0,     0,     0,     0,   218,
     219,   220,   221,   222,   171,     0,     0,   210,     0,   210,
       0,   216,   217,   235,   230,   234,     0,   233,     0,   320,
       0,     0,   262,     0,     0,     0,     0,   210,     0,     0,
       0,     0,    64,     0,    67,    57,    63,    28,    30,     0,
      79,    87,     0,    76,   325,   324,   323,     0,     0,     0,
       0,     0,     0,     0,   287,   291,   288,   297,   289,   300,
       0,   137,     0,   185,     0,   180,   183,    79,    79,   319,
     167,   169,   199,   196,     0,   174,     0,   173,     0,   238,
     241,   243,   242,   244,   239,   240,   247,     0,     0,     0,
     195,     0,   265,     0,    79,     0,   271,     0,   205,     0,
       0,   255,     0,    59,    54,     0,    81,    79,    79,    79,
      79,    79,   429,   430,   431,   432,   434,   433,     0,     0,
       0,     0,     0,     0,     0,     0,   302,   319,     0,     0,
       0,   417,   212,   211,   215,   213,   186,   203,     0,     0,
       0,     0,   315,     0,   200,   197,   198,   201,     0,   176,
     209,   210,   236,     0,   223,   321,   319,   253,   263,     0,
     269,   259,   207,   264,    68,     0,     0,    74,    80,     0,
       0,     0,     0,     0,   423,   427,   424,   425,   426,     0,
       0,     0,     0,     0,   210,     0,   298,   139,     0,     0,
     181,   184,   188,   191,     0,   172,     0,   237,     0,     0,
     257,   267,    62,    69,    55,     0,    82,    89,   137,    77,
     137,   137,   301,   245,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,   156,   145,   143,     0,   152,   214,
       0,     0,   170,   248,   232,   231,     0,     0,    83,     0,
      91,   101,   305,     0,   210,   290,   295,   303,   292,     0,
     138,   140,     0,   153,     0,   146,   148,   150,     0,   113,
     105,     0,   155,     0,     0,     0,     0,     0,   157,   299,
       0,     0,     0,   270,   268,    90,    88,   164,     0,     0,
       0,   126,   131,     0,     0,     0,     0,   107,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   210,     0,     0,
     161,   154,     0,   159,     0,   163,   189,   192,   258,     0,
     249,     0,     0,     0,     0,   104,     0,   132,   246,   294,
       0,   141,     0,   124,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     144,     0,     0,     0,   160,   158,   162,   165,     0,     0,
       0,   310,   306,   133,     0,     0,     0,     0,   293,     0,
       0,   106,   125,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     151,   250,   102,   312,     0,     0,     0,     0,     0,     0,
       0,   137,     0,   127,     0,   130,     0,   112,   118,   123,
     111,   117,   122,   108,   114,   119,   110,   116,   121,   109,
     115,   120,   147,   149,     0,   308,     0,     0,   134,   129,
     128,   142,   311,   309,     0,   135,     0,   164,     0,     0,
     307,     0,     0,   136
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -628,  -628,  -628,  -628,  -628,   864,   857,   855,   869,   876,
     866,   880,  -628,  -628,  -628,   881,   607,   794,   -43,  -628,
    -628,   411,  -628,  -628,  -218,  -628,  -368,  -628,  -374,  -628,
    -628,   702,  -628,  -628,  -628,  -628,   317,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -313,   882,  -628,  -628,  -628,  -628,
    -628,  -628,  -510,  -627,  -592,  -628,  -628,  -471,  -591,  -628,
    -628,  -628,  -536,  -628,  -628,  -628,   366,  -628,  -628,  -628,
    -628,  -628,   148,  -114,  -512,   163,   -76,  -628,  -628,  -628,
    -628,   -99,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,   520,  -628,   598,   650,   642,  -628,  -628,  -628,
    -340,  -628,  -396,  -628,  -260,  -628,  -628,  -328,  -628,  -628,
    -628,  -628,  -628,   643,  -628,  -628,  -566,  -628,  -628,   502,
    -628,  -628,  -628,  -294,  -628,  -628,  -628,  -628,  -628,   782,
     775,   779,   781,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -508,   477,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -160,   474,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,  -628,
    -628,  -628,  -628,  -628,  -628,  -628,  -628,   131,  -628,   -42,
    -628,  -628,   721,   -54,  -628
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     3,     4,     5,    50,    51,    52,    53,    54,    55,
      56,    57,    13,    14,    73,    58,   301,   302,   353,    59,
      60,   213,   379,   506,   192,   193,   375,   214,   376,   505,
      61,   217,   218,   380,   315,   449,   445,   446,   508,    62,
     219,   311,   447,   580,   229,    63,    64,    65,   312,   617,
      66,   318,   598,   599,   600,   664,   620,   621,   622,   731,
     765,   767,   470,   559,   591,   699,   564,   565,   635,   636,
     566,   637,   567,   601,   602,   650,   477,   338,   483,   414,
     347,   170,   332,   478,   333,   479,   334,   570,   335,   571,
     171,   487,   411,   412,   405,   183,   184,   367,   172,   349,
     402,   473,   354,   343,   355,   173,   268,   356,   538,   427,
     428,   522,   584,   357,   491,   689,   185,   362,   186,   187,
     363,   576,   433,   188,   577,   437,   541,   294,   157,   158,
     159,   160,   161,   238,   162,   163,   397,   467,   625,   325,
     327,   398,   399,   524,    67,   317,   618,   730,   756,   692,
     269,   295,   271,   272,   431,    68,   221,   316,     6,     7,
     122,    35,    36,    37,   100,   274,    38,   106,   275,    39,
      40,    41,    42,    76,   273,    75,   329,   245,    43,   120,
     281,    44,   121,   296,    45,   107,   276,   167,   328,    69,
     225,   226,   227,    70,   458
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
     169,   371,   384,   124,   125,   344,   474,   416,   270,   418,
     612,   444,   581,   324,   582,   583,   568,   558,   656,   165,
     474,  -381,   474,     1,   691,     2,   127,   439,   429,   656,
     657,   164,   345,   130,   131,   101,   663,   400,   231,   232,
     126,   440,     8,   474,   181,  -402,   123,   128,   638,   640,
     123,   603,   605,   231,   232,   113,    74,   109,   110,   111,
     401,   542,     9,   114,   129,   130,   131,   123,   504,   523,
     436,   135,   702,   132,   112,   298,   133,   463,   413,   231,
     232,   134,   299,   136,   211,    10,   488,   -51,   220,   641,
     222,   223,   641,   212,   641,   108,   561,   755,   136,   492,
     493,   336,   165,   495,   657,   132,   657,   696,   133,   115,
     165,   230,   135,   134,   164,   718,   719,   660,   346,   694,
     603,   592,   721,   243,   136,   267,   554,   641,   118,   763,
     641,   543,   641,   638,   292,   562,  -326,   563,   304,   293,
     474,   657,   475,   657,   136,   305,   102,   103,   104,   116,
     117,   536,   413,   638,   684,   119,   475,   443,   475,   586,
     474,   569,   123,   105,   537,   539,   -22,   348,   126,   561,
     358,   330,   331,   306,   127,   128,   638,   578,   126,   475,
     643,   561,   695,   697,   556,   128,   147,   337,   168,   668,
     669,   670,   129,   130,   131,   758,    48,   228,    49,   -93,
     768,   561,   129,   130,   131,   592,   593,   123,   562,   652,
     563,   615,   123,   154,   592,   364,   653,   654,   339,   155,
     562,   123,   563,   732,   561,   734,   638,   474,   659,   560,
     166,   174,    48,   132,   137,   -93,   133,   175,   176,   385,
     562,   134,   563,   132,   623,   638,   133,   168,   546,   482,
     177,   134,   372,   561,   373,   404,   374,   309,   310,   568,
     135,   123,   561,   562,   645,   563,   381,   616,   231,   232,
     135,   383,   136,   685,   561,   592,   475,   561,   340,   341,
     342,   594,   136,   614,   595,   596,   594,   474,   178,   595,
     596,   179,   562,   561,   563,   594,   475,   683,   595,   596,
     180,   562,   267,   563,   126,   182,   638,   426,   665,   666,
     667,   128,    11,   562,    12,   563,   562,   293,   563,   592,
     627,   224,   293,   561,   468,   426,   123,   293,   129,   130,
     131,   189,   562,   686,   563,   191,   374,   703,   704,   705,
     706,   707,   708,   709,   710,   711,   712,   713,   714,   715,
     716,   717,   466,   190,   561,   131,   628,   228,    48,   472,
     139,   -93,   562,   475,   563,   126,   629,   630,   631,   132,
     632,   633,   133,   472,    46,   472,    47,   134,   246,   259,
     260,   629,   700,   631,   123,   632,   633,   395,   396,   129,
     130,   131,   293,   562,   132,   563,   472,   133,   233,   374,
     594,   235,   134,   595,   596,   236,   562,   534,   563,   123,
     123,   247,   471,   248,   249,   250,   251,   252,   123,   339,
     239,   351,   352,   475,   253,   254,   255,   256,   257,   258,
     132,   241,    48,   133,   141,   -93,   283,   463,   134,   259,
     260,   261,   285,    48,   262,   143,   -93,   604,   606,   671,
     672,   673,   464,   293,   485,   486,   286,   287,   288,   289,
     290,   291,   374,   244,   259,   260,   263,   465,   264,   496,
     497,   265,    48,   266,   145,   -93,   466,   280,   553,   340,
     341,   342,   277,   123,   639,   148,   374,   145,   -93,   642,
     282,   644,   278,   472,   610,   611,   123,   292,   350,   589,
     590,   339,   374,   370,   613,   123,   339,   545,   351,   352,
     283,   351,   352,   472,   466,   297,   604,   597,   634,   303,
     725,   726,   727,   283,   728,   729,   284,   123,   307,   285,
     286,   287,   288,   289,   290,   279,   374,   452,   453,   454,
     455,   456,   457,   286,   287,   288,   289,   290,   291,   597,
     320,   259,   260,    48,   283,   150,   -93,   500,   319,   681,
     682,   340,   341,   342,   597,   322,   340,   341,   342,   323,
      71,   292,    72,   687,   286,   287,   288,   289,   290,   489,
     472,   674,   675,   676,   292,   123,   339,   490,   351,   352,
     677,   678,   679,   123,   339,   597,   351,   352,   300,   232,
      48,   -29,   152,   -93,   502,   215,   326,   216,   -71,   693,
     123,   339,   345,   351,   352,   292,   194,   195,   196,   197,
     198,   199,   200,   201,   202,   203,   204,   205,   206,   207,
     662,   701,   573,   389,   390,   391,   392,   393,   123,   339,
     472,   351,   352,   587,   656,   733,   340,   341,   342,   123,
     339,   658,   351,   352,   340,   341,   342,   123,   339,   720,
     351,   352,   668,   669,   670,   123,   339,   360,   351,   352,
     359,   340,   341,   342,   365,   208,   209,   215,   313,   216,
     314,   764,   194,   195,   196,   197,   198,   199,   200,   201,
     202,   203,   204,   205,   206,   207,   377,   723,   368,   340,
     341,   342,   656,   735,   370,   129,   130,   131,   656,   759,
     340,   341,   342,   386,   656,   760,   754,   762,   340,   341,
     342,    93,    94,    95,   480,   481,   340,   341,   342,   123,
     382,   394,   387,   724,   388,   403,   407,    96,    97,    98,
      99,   208,   209,   725,   726,   727,   132,   728,   729,   133,
     123,   499,   408,   434,   134,   409,   247,   419,   248,   249,
     250,   251,   252,   410,   509,   510,   511,   512,   513,   253,
     254,   255,   256,   257,   258,   415,   417,   430,   432,   435,
     442,   438,   441,   448,   420,   421,   422,   423,   424,   425,
      15,    16,    17,    18,    19,   450,    20,    21,    22,    23,
     451,   459,   461,    24,    25,    26,   460,   462,   469,    27,
     476,    28,    29,    30,   494,   501,   503,   507,   514,   515,
      31,    32,    33,   516,    34,    77,    78,    79,    80,   517,
     518,    81,    82,    83,    84,   519,   521,   527,    85,    86,
      87,   526,   530,   528,    88,   529,   531,   532,   533,   535,
     540,   547,   548,   549,   550,    89,    90,    91,   551,    92,
     552,   555,   557,   624,   572,   574,   575,   585,   579,   588,
     607,   626,   609,   619,   649,   646,   647,   648,   651,   655,
     656,   662,   757,   680,   661,   688,   690,   736,   652,   698,
     722,   737,   738,   739,   740,   741,   742,   743,   744,   745,
     746,   747,   748,   749,   750,   751,   752,   753,   754,   378,
     665,   668,   671,   761,   766,   770,   773,   544,   771,   772,
     308,   210,   138,   674,   677,   153,   151,   144,   140,   608,
     769,   406,   484,   361,   366,   498,   142,   369,   234,   240,
     520,   525,   146,   237,   242,     0,   149,   321,     0,     0,
       0,     0,     0,     0,   156
};

static const yytype_int16 yycheck[] =
{
      76,   295,   315,    46,    47,   265,   402,   347,   168,   349,
     576,   379,   548,   231,   550,   551,   528,   525,     3,    73,
     416,     0,   418,     1,   651,     3,    15,   367,   356,     3,
     621,    73,     3,    34,    35,    14,   628,    63,    68,    69,
       9,   369,     5,   439,   120,     3,    10,    16,     3,     4,
      10,   561,   562,    68,    69,   127,    14,   131,   132,   133,
      86,     4,     0,   135,    33,    34,    35,    10,   442,   465,
     364,   101,   664,    74,   148,    10,    77,    37,   338,    68,
      69,    82,    17,   113,     1,   114,   414,     4,   131,   601,
     133,   134,   604,    10,   606,    14,    51,   724,   113,   427,
     428,   261,   156,   431,   695,    74,   697,    92,    77,    14,
     164,   154,   101,    82,   156,   681,   682,   625,    89,    93,
     630,     3,   688,   166,   113,   168,   522,   639,    14,   756,
     642,   505,   644,     3,    98,    90,   114,    92,    10,   182,
     536,   732,   402,   734,   113,    17,   125,   126,   127,   139,
     140,   491,   412,     3,     4,    14,   416,   375,   418,   555,
     556,   529,    10,   142,   492,   493,     0,   266,     9,    51,
     269,   247,   248,   216,    15,    16,     3,   545,     9,   439,
      50,    51,   653,   654,   524,    16,     4,   263,     3,    71,
      72,    73,    33,    34,    35,   731,     1,    12,     3,     4,
     766,    51,    33,    34,    35,     3,     4,    10,    90,    85,
      92,   579,    10,     7,     3,   291,    92,    93,    11,     3,
      90,    10,    92,   694,    51,   696,     3,   623,   624,     3,
       3,   100,     1,    74,     3,     4,    77,   106,   107,   315,
      90,    82,    92,    74,   584,     3,    77,     3,   508,   409,
      52,    82,     1,    51,     3,   331,   299,     3,     4,   771,
     101,    10,    51,    90,    91,    92,   309,   580,    68,    69,
     101,   314,   113,    50,    51,     3,   536,    51,    71,    72,
      73,    84,   113,   577,    87,    88,    84,   683,    52,    87,
      88,    52,    90,    51,    92,    84,   556,   637,    87,    88,
      52,    90,   345,    92,     9,     3,     3,   350,    71,    72,
      73,    16,     1,    90,     3,    92,    90,   360,    92,     3,
       4,     3,   365,    51,   400,   368,    10,   370,    33,    34,
      35,     4,    90,    91,    92,    10,   379,   665,   666,   667,
     668,   669,   670,   671,   672,   673,   674,   675,   676,   677,
     678,   679,   395,     4,    51,    35,    40,    12,     1,   402,
       3,     4,    90,   623,    92,     9,    50,    51,    52,    74,
      54,    55,    77,   416,     6,   418,     8,    82,     4,    65,
      66,    50,    51,    52,    10,    54,    55,     3,     4,    33,
      34,    35,   435,    90,    74,    92,   439,    77,     3,   442,
      84,     4,    82,    87,    88,     3,    90,   483,    92,    10,
      10,    37,     4,    39,    40,    41,    42,    43,    10,    11,
       3,    13,    14,   683,    50,    51,    52,    53,    54,    55,
      74,     3,     1,    77,     3,     4,    37,    37,    82,    65,
      66,    67,    43,     1,    70,     3,     4,   561,   562,    71,
      72,    73,    52,   496,    95,    96,    57,    58,    59,    60,
      61,    62,   505,    10,    65,    66,    92,    67,    94,     3,
       4,    97,     1,    99,     3,     4,   519,    14,   521,    71,
      72,    73,   120,    10,   598,     1,   529,     3,     4,   603,
       4,   605,   120,   536,   570,   571,    10,    98,     3,     3,
       4,    11,   545,     3,     4,    10,    11,    17,    13,    14,
      37,    13,    14,   556,   557,     4,   630,   560,   594,     4,
      50,    51,    52,    37,    54,    55,    40,    10,     4,    43,
      57,    58,    59,    60,    61,   120,   579,   107,   108,   109,
     110,   111,   112,    57,    58,    59,    60,    61,    62,   592,
       4,    65,    66,     1,    37,     3,     4,    40,    52,   635,
     636,    71,    72,    73,   607,     4,    71,    72,    73,     4,
       1,    98,     3,   649,    57,    58,    59,    60,    61,     4,
     623,    71,    72,    73,    98,    10,    11,     4,    13,    14,
      71,    72,    73,    10,    11,   638,    13,    14,     1,    69,
       1,     4,     3,     4,     4,     1,     3,     3,     4,   652,
      10,    11,     3,    13,    14,    98,    19,    20,    21,    22,
      23,    24,    25,    26,    27,    28,    29,    30,    31,    32,
       3,     4,     4,   102,   103,   104,   105,   106,    10,    11,
     683,    13,    14,     4,     3,     4,    71,    72,    73,    10,
      11,     4,    13,    14,    71,    72,    73,    10,    11,     4,
      13,    14,    71,    72,    73,    10,    11,     3,    13,    14,
      64,    71,    72,    73,     3,    78,    79,     1,     1,     3,
       3,   757,    19,    20,    21,    22,    23,    24,    25,    26,
      27,    28,    29,    30,    31,    32,     4,     4,     3,    71,
      72,    73,     3,     4,     3,    33,    34,    35,     3,     4,
      71,    72,    73,     4,     3,     4,     3,     4,    71,    72,
      73,   125,   126,   127,   407,   408,    71,    72,    73,    10,
      36,     4,    36,    40,    36,     4,     3,   141,   142,   143,
     144,    78,    79,    50,    51,    52,    74,    54,    55,    77,
      10,   434,     3,     3,    82,    40,    37,    17,    39,    40,
      41,    42,    43,     4,   447,   448,   449,   450,   451,    50,
      51,    52,    53,    54,    55,     4,     4,     4,     4,     3,
      18,     4,     4,     3,    44,    45,    46,    47,    48,    49,
     115,   116,   117,   118,   119,     3,   121,   122,   123,   124,
       3,    14,    14,   128,   129,   130,    89,    14,    80,   134,
       4,   136,   137,   138,     4,     4,     4,     4,     4,     4,
     145,   146,   147,     4,   149,   115,   116,   117,   118,     4,
       4,   121,   122,   123,   124,     3,     3,     3,   128,   129,
     130,     4,     4,    83,   134,    17,     4,     4,     4,     4,
       4,     4,     4,     4,     4,   145,   146,   147,     4,   149,
       4,    40,     3,   100,     4,     4,     4,     4,    17,     4,
       3,    81,     4,     3,    38,     4,     4,     4,    76,     4,
       3,     3,    75,     4,    10,    56,     3,    89,    85,     4,
       4,     4,     4,     4,     4,     4,     4,     4,     4,     4,
       4,     4,     4,     4,     4,     4,     4,     4,     3,   302,
      71,    71,    71,     4,    56,     4,     4,   506,    83,   771,
     218,   127,    58,    71,    71,    70,    69,    61,    59,   563,
     767,   333,   412,   283,   292,   433,    60,   294,   156,   164,
     463,   467,    62,   162,   165,    -1,    64,   226,    -1,    -1,
      -1,    -1,    -1,    -1,    73
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint16 yystos[] =
{
       0,     1,     3,   151,   152,   153,   308,   309,     5,     0,
     114,     1,     3,   162,   163,   115,   116,   117,   118,   119,
     121,   122,   123,   124,   128,   129,   130,   134,   136,   137,
     138,   145,   146,   147,   149,   311,   312,   313,   316,   319,
     320,   321,   322,   328,   331,   334,     6,     8,     1,     3,
     154,   155,   156,   157,   158,   159,   160,   161,   165,   169,
     170,   180,   189,   195,   196,   197,   200,   294,   305,   339,
     343,     1,     3,   164,    14,   325,   323,   115,   116,   117,
     118,   121,   122,   123,   124,   128,   129,   130,   134,   145,
     146,   147,   149,   125,   126,   127,   141,   142,   143,   144,
     314,    14,   125,   126,   127,   142,   317,   335,    14,   131,
     132,   133,   148,   127,   135,    14,   139,   140,    14,    14,
     329,   332,   310,    10,   168,   168,     9,    15,    16,    33,
      34,    35,    74,    77,    82,   101,   113,     3,   155,     3,
     158,     3,   159,     3,   160,     3,   161,     4,     1,   195,
       3,   156,     3,   157,     7,     3,   165,   278,   279,   280,
     281,   282,   284,   285,   339,   343,     3,   337,     3,   226,
     231,   240,   248,   255,   337,   337,   337,    52,    52,    52,
      52,   226,     3,   245,   246,   266,   268,   269,   273,     4,
       4,    10,   174,   175,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    78,    79,
     167,     1,    10,   171,   177,     1,     3,   181,   182,   190,
     168,   306,   168,   168,     3,   340,   341,   342,    12,   194,
     168,    68,    69,     3,   279,     4,     3,   282,   283,     3,
     280,     3,   281,   168,    10,   327,     4,    37,    39,    40,
      41,    42,    43,    50,    51,    52,    53,    54,    55,    65,
      66,    67,    70,    92,    94,    97,    99,   168,   256,   300,
     301,   302,   303,   324,   315,   318,   336,   120,   120,   120,
      14,   330,     4,    37,    40,    43,    57,    58,    59,    60,
      61,    62,    98,   168,   277,   301,   333,     4,    10,    17,
       1,   166,   167,     4,    10,    17,   168,     4,   181,     3,
       4,   191,   198,     1,     3,   184,   307,   295,   201,    52,
       4,   342,     4,     4,   174,   289,     3,   290,   338,   326,
     226,   226,   232,   234,   236,   238,   301,   226,   227,    11,
      71,    72,    73,   253,   254,     3,    89,   230,   231,   249,
       3,    13,    14,   168,   252,   254,   257,   263,   231,    64,
       3,   245,   267,   270,   226,     3,   246,   247,     3,   263,
       3,   273,     1,     3,   168,   176,   178,     4,   166,   172,
     183,   168,    36,   168,   194,   226,     4,    36,    36,   102,
     103,   104,   105,   106,     4,     3,     4,   286,   291,   292,
      63,    86,   250,     4,   226,   244,   244,     3,     3,    40,
       4,   242,   243,   254,   229,     4,   250,     4,   250,    17,
      44,    45,    46,    47,    48,    49,   168,   259,   260,   257,
       4,   304,     4,   272,     3,     3,   273,   275,     4,   250,
     257,     4,    18,   174,   176,   186,   187,   192,     3,   185,
       3,     3,   107,   108,   109,   110,   111,   112,   344,    14,
      89,    14,    14,    37,    52,    67,   168,   287,   226,    80,
     212,     4,   168,   251,   252,   254,     4,   226,   233,   235,
     186,   186,   301,   228,   242,    95,    96,   241,   257,     4,
       4,   264,   257,   257,     4,   257,     3,     4,   269,   186,
      40,     4,     4,     4,   178,   179,   173,     4,   188,   186,
     186,   186,   186,   186,     4,     4,     4,     4,     4,     3,
     292,     3,   261,   252,   293,   302,     4,     3,    83,    17,
       4,     4,     4,     4,   226,     4,   250,   257,   258,   257,
       4,   276,     4,   178,   171,    17,   254,     4,     4,     4,
       4,     4,     4,   168,   252,    40,   250,     3,   291,   213,
       3,    51,    90,    92,   216,   217,   220,   222,   224,   176,
     237,   239,     4,     4,     4,     4,   271,   274,   176,    17,
     193,   212,   212,   212,   262,     4,   252,     4,     4,     3,
       4,   214,     3,     4,    84,    87,    88,   168,   202,   203,
     204,   223,   224,   202,   223,   202,   223,     3,   216,     4,
     226,   226,   266,     4,   273,   176,   194,   199,   296,     3,
     206,   207,   208,   250,   100,   288,    81,     4,    40,    50,
      51,    52,    54,    55,   226,   218,   219,   221,     3,   223,
       4,   224,   223,    50,   223,    91,     4,     4,     4,    38,
     225,    76,    85,    92,    93,     4,     3,   208,     4,   252,
     291,    10,     3,   204,   205,    71,    72,    73,    71,    72,
      73,    71,    72,    73,    71,    72,    73,    71,    72,    73,
       4,   226,   226,   250,     4,    50,    91,   226,    56,   265,
       3,   203,   299,   168,    93,   207,    92,   207,     4,   215,
      51,     4,   204,   257,   257,   257,   257,   257,   257,   257,
     257,   257,   257,   257,   257,   257,   257,   257,   266,   266,
       4,   266,     4,     4,    40,    50,    51,    52,    54,    55,
     297,   209,   207,     4,   207,     4,    89,     4,     4,     4,
       4,     4,     4,     4,     4,     4,     4,     4,     4,     4,
       4,     4,     4,     4,     3,   203,   298,    75,   212,     4,
       4,     4,     4,   203,   226,   210,    56,   211,   266,   225,
       4,    83,   222,     4
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint16 yyr1[] =
{
       0,   150,   151,   151,   151,   152,   153,   154,   154,   155,
     155,   156,   156,   157,   157,   158,   158,   159,   159,   160,
     160,   161,   161,   162,   162,   163,   164,   164,   165,   166,
     166,   166,   167,   167,   167,   167,   167,   167,   167,   167,
     167,   167,   167,   167,   167,   167,   167,   167,   168,   169,
     170,   171,   171,   172,   173,   171,   171,   174,   174,   174,
     175,   175,   176,   176,   176,   177,   177,   178,   179,   179,
     180,   181,   181,   183,   182,   182,   185,   184,   184,   187,
     186,   188,   188,   188,   189,   190,   190,   192,   191,   193,
     193,   194,   194,   195,   195,   196,   196,   196,   196,   196,
     198,   199,   197,   201,   200,   202,   202,   202,   203,   203,
     203,   203,   203,   204,   204,   204,   204,   204,   204,   204,
     204,   204,   204,   204,   205,   205,   206,   206,   206,   206,
     206,   207,   207,   209,   210,   211,   208,   212,   212,   213,
     213,   215,   214,   216,   216,   216,   218,   217,   219,   217,
     221,   220,   222,   222,   223,   223,   224,   224,   224,   224,
     224,   224,   224,   224,   225,   225,   226,   226,   227,   228,
     226,   229,   226,   226,   226,   230,   226,   226,   226,   232,
     233,   231,   234,   235,   231,   231,   231,   236,   237,   231,
     238,   239,   231,   231,   231,   240,   241,   241,   241,   242,
     242,   243,   244,   244,   245,   245,   247,   246,   249,   248,
     250,   250,   251,   251,   251,   251,   252,   252,   253,   253,
     253,   253,   254,   255,   256,   256,   256,   256,   256,   256,
     257,   257,   257,   257,   257,   257,   258,   258,   259,   259,
     259,   260,   260,   260,   260,   262,   261,   264,   263,   265,
     265,   266,   267,   266,   266,   268,   270,   271,   269,   269,
     269,   269,   272,   272,   273,   273,   273,   274,   274,   276,
     275,   275,   277,   277,   277,   277,   277,   278,   278,   279,
     279,   280,   280,   281,   281,   283,   282,   284,   285,   286,
     286,   287,   286,   286,   288,   288,   289,   289,   290,   290,
     291,   291,   293,   292,   295,   296,   297,   294,   298,   298,
     299,   299,   299,   300,   300,   300,   301,   301,   301,   303,
     304,   302,   306,   305,   307,   307,   309,   310,   308,   308,
     311,   311,   311,   311,   311,   311,   311,   311,   311,   311,
     311,   311,   311,   311,   311,   311,   311,   311,   312,   312,
     312,   312,   312,   312,   312,   312,   312,   312,   312,   312,
     312,   312,   312,   312,   312,   313,   314,   315,   313,   313,
     313,   313,   313,   313,   313,   316,   317,   318,   316,   316,
     316,   316,   316,   316,   319,   319,   320,   321,   321,   321,
     321,   321,   321,   321,   321,   322,   323,   324,   322,   322,
     322,   322,   325,   326,   322,   327,   327,   329,   330,   328,
     332,   333,   331,   335,   336,   334,   338,   337,   339,   340,
     340,   341,   341,   342,   342,   342,   342,   342,   343,   344,
     344,   344,   344,   344,   344
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     1,     1,     6,     4,     2,     1,     2,
       1,     2,     1,     2,     1,     2,     1,     2,     1,     2,
       1,     2,     1,     4,     1,     4,     4,     1,     5,     0,
       2,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     4,
       4,     0,     1,     0,     0,     6,     1,     0,     1,     4,
       1,     2,     4,     1,     1,     1,     2,     1,     1,     2,
       4,     1,     2,     0,     5,     1,     0,     5,     1,     0,
       2,     0,     2,     3,     4,     0,     2,     0,     7,     0,
       2,     0,     1,     0,     2,     1,     1,     1,     1,     1,
       0,     0,    13,     0,    11,     1,     4,     2,     5,     5,
       5,     5,     5,     1,     5,     5,     5,     5,     5,     5,
       5,     5,     5,     5,     1,     2,     1,     4,     5,     5,
       4,     1,     2,     0,     0,     0,    11,     0,     4,     0,
       2,     0,     6,     1,     4,     1,     0,     6,     0,     6,
       0,     5,     1,     2,     2,     1,     1,     2,     4,     3,
       4,     3,     4,     3,     0,     2,     2,     4,     0,     0,
       7,     0,     6,     4,     4,     0,     5,     1,     1,     0,
       0,     6,     0,     0,     6,     4,     5,     0,     0,     9,
       0,     0,     9,     1,     1,     4,     0,     1,     1,     1,
       2,     2,     0,     2,     1,     4,     0,     5,     0,     5,
       0,     2,     1,     1,     3,     1,     1,     1,     1,     1,
       1,     1,     1,     5,     1,     1,     1,     1,     1,     1,
       1,     5,     5,     1,     1,     1,     0,     1,     1,     1,
       1,     1,     1,     1,     1,     0,     5,     0,     5,     0,
       2,     2,     0,     5,     1,     4,     0,     0,     9,     5,
       1,     1,     0,     2,     5,     4,     1,     0,     2,     0,
       5,     1,     1,     1,     1,     1,     1,     2,     1,     2,
       1,     2,     1,     2,     1,     0,     3,     4,     4,     1,
       5,     0,     5,     8,     2,     0,     0,     2,     4,     6,
       1,     4,     0,     5,     0,     0,     0,    18,     1,     2,
       1,     4,     2,     1,     1,     4,     1,     1,     1,     0,
       0,     4,     0,     5,     2,     2,     0,     0,     4,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     2,     2,     2,     1,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     0,     0,     4,     2,
       2,     2,     2,     2,     2,     2,     0,     0,     4,     2,
       2,     1,     2,     2,     2,     2,     2,     2,     4,     2,
       4,     2,     4,     2,     4,     1,     0,     0,     4,     2,
       2,     2,     0,     0,     5,     0,     1,     0,     0,     4,
       0,     0,     4,     0,     0,     4,     0,     5,     4,     0,
       1,     1,     2,     5,     5,     5,     5,     5,     4,     1,
       1,     1,     1,     1,     1
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, int yyrule)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                                              );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
{
  YYUSE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yystacksize);

        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 8:
#line 459 "yacc/parser.yy" /* yacc.c:1646  */
    {parser_api->domain->addRequirement("strips");}
#line 2231 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 21:
#line 486 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                // tras la declaraci�n de acciones
                                // comprobar que las tareas definidad en la
                                // red de tareas realmente est�n definidas
                                tasktablecit i,e =parser_api->domain->getEndTask();
                                methodcit j, em;
                                bool errors=false;
                                bool changes = true;
                                while(changes){
                                        changes = false;
                                        for(i=parser_api->domain->getBeginTask(); i!= e; i++){
                                        errors = false;
                                        if((*i).second->isCompoundTask()){
                                                em = ((CompoundTask *)(*i).second)->getEndMethod();
                                                for(j=((CompoundTask *)(*i).second)->getBeginMethod();j!= em; j++) {
                                                if(!(*j)->getTaskNetwork()->isWellDefined(errflow,&changes))
                                                {
                                                        errors = true;
                                                };
                                                }
                                        }
                                        if(errors) {
                                                SearchLineInfo sli((*i).second->getMetaId());
                                                snprintf(parerr,256,"In the task network of task `%s' defined near %d [%s].",(*i).second->getName(),sli.lineNumber,sli.fileName.c_str());
                                                yyerror(parerr);
                                        }
                                        }
                                }
                                }
#line 2265 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 23:
#line 519 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    if(parser_api->domain->loaded)
                                    {
                                        snprintf(parerr,256,"There is a domain [%s] already loaded.",parser_api->domain->getName());
                                        yyerror(parerr);
                                        YYABORT;
                                    }
                                    parser_api->domain->setDomainName(((string *)(yyvsp[-1].otype))->c_str());
                                parser_api->domain->loaded=true;
                                    delete (string *)(yyvsp[-1].otype);
                                }
#line 2281 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 25:
#line 534 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    if(!parser_api->domain || !parser_api->problem)
                                    {
                                        yyerror("No domain loaded.");
                                        YYABORT;
                                    }
                                    parser_api->problem->setProblemName(((string *)(yyvsp[-1].otype))->c_str());
                                    delete (string *)(yyvsp[-1].otype);
                                }
#line 2295 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 26:
#line 546 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    if(strcmp(parser_api->domain->getName(),((string *)(yyvsp[-1].otype))->c_str()))
                                    {
                                        snprintf(parerr,256,"The problem requires the domain [%s] and the domain loaded is [%s].",((string *)(yyvsp[-1].otype))->c_str(),parser_api->domain->getName());
                                        yyerror(parerr);
                                        YYABORT;
                                    }
                                    delete (string *)(yyvsp[-1].otype);
                                }
#line 2309 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 32:
#line 567 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":strips");}
#line 2315 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 33:
#line 569 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":typing");}
#line 2321 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 34:
#line 571 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":negative-preconditions");}
#line 2327 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 35:
#line 573 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":disjuntive-preconditions");}
#line 2333 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 36:
#line 575 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":equality");}
#line 2339 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 37:
#line 577 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":existential-preconditions");}
#line 2345 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 38:
#line 579 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":universal-preconditions");}
#line 2351 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 39:
#line 581 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":quantified-preconditions");}
#line 2357 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 40:
#line 583 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":conditional-effects");}
#line 2363 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 41:
#line 585 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":fluents");}
#line 2369 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 42:
#line 587 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":adl");}
#line 2375 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 43:
#line 589 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":durative-actions");}
#line 2381 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 44:
#line 591 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":derived-predicates");}
#line 2387 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 45:
#line 593 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":timed-initial-literals");}
#line 2393 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 46:
#line 595 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":metatags");}
#line 2399 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 47:
#line 597 "yacc/parser.yy" /* yacc.c:1646  */
    { parser_api->domain->addRequirement(":htn-expansion");}
#line 2405 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 48:
#line 602 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new string((yyvsp[0].type_string));
                                }
#line 2413 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 49:
#line 608 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    if(!parser_api->domain->errtyping && !parser_api->domain->hasRequirement(":typing"))
                                    {
                                        parser_api->domain->errtyping = true;
                                        yyerror("Using a clause that requires `:typing' and is not declared in requirements clause");
                                    }
                                // verificamos que los tipos han sido definidos correctamente
                                if(!fast_parsing){
                                        typetablecit b = parser_api->domain->getBeginType();
                                        typetablecit e = parser_api->domain->getEndType();
                                        for_each(b,e,TestType());
                                }
                                parser_api->domain->buildTypeRelations();
                                }
#line 2432 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 51:
#line 629 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) = 0;}
#line 2438 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 52:
#line 631 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<Type *> * ptrTypes = (vector<Type *> *) (yyvsp[0].otype);
                                vector<Type *>::iterator i,e;
                                const Type * tmp;
                                e = ptrTypes->end();
                                for(i=ptrTypes->begin(); i != e; i++){
                                        if((tmp=parser_api->domain->addType((*i))) != *i){
                                        SearchLineInfo sli(tmp);
                                        if(sli.lineNumber){
                                        snprintf(parerr,256,"The type `%s' is already defined. (previous definition near %d [%s].",tmp->getName(),sli.lineNumber,sli.fileName.c_str());
                                        yywarning(parerr);
                                        delete (*i);
                                        (*i) = 0;
                                        }
                                        else {
                                        Type * n = parser_api->domain->getModificableType(tmp->getId());
                                        n->setFileId(parser_api->fileid);
                                        n->setLineNumber(lexer->getLineNumber());
                                        }
                                        }
                                }
                                delete ptrTypes;
                                }
#line 2466 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 53:
#line 654 "yacc/parser.yy" /* yacc.c:1646  */
    {errtypes=false;}
#line 2472 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 54:
#line 654 "yacc/parser.yy" /* yacc.c:1646  */
    {errtypes=true;}
#line 2478 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 55:
#line 655 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<Type *> * ptrTypes = (vector<Type *> *) (yyvsp[-5].otype);
                                vector<Type *> * ptrParents = (vector<Type *> *) (yyvsp[-2].otype);
                                vector<Type *>::iterator i,e;
                                const Type * tmp;
                                e = ptrTypes->end();
                                for(i=ptrTypes->begin(); i != e; i++){
                                        if((tmp=parser_api->domain->addType((*i))) != *i){
                                        SearchLineInfo sli(tmp);
                                        if(sli.lineNumber){
                                        snprintf(parerr,256,"The type `%s' is already defined. (previous definition near %d [%s].",tmp->getName(),sli.lineNumber,sli.fileName.c_str());
                                        yywarning(parerr);
                                        delete (*i);
                                        (*i) = 0;
                                        }
                                        else {
                                        Type * n = parser_api->domain->getModificableType(tmp->getId());
                                        n->setFileId(parser_api->fileid);
                                        n->setLineNumber(lexer->getLineNumber());
                                        }
                                        }
                                        if(ptrParents) {
                                        Type * n = parser_api->domain->getModificableType((tmp)->getName());
                                        n->addSuperTypes(ptrParents);
                                        }
                                }
                                if(ptrParents)
                                        delete ptrParents;
                                delete ptrTypes;
                                }
#line 2513 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 56:
#line 686 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=0;}
#line 2519 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 58:
#line 691 "yacc/parser.yy" /* yacc.c:1646  */
    {delete (vector<ConstantSymbol *> *) (yyvsp[0].otype);}
#line 2525 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 59:
#line 694 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<ConstantSymbol *> * ptr = (vector<ConstantSymbol *> *) (yyvsp[-3].otype);
                                vector<Type *> * types = (vector<Type *> *) (yyvsp[-1].otype);
                                if(types){
                                        // Definimos el tipo para cada una de las constantes
                                        for_each(ptr->begin(),ptr->end(),bind2nd(mem_fun1_t<void,Term,const vector<Type *> *>(&Term::addTypes),types));
                                        // Para cada tipo a�adimos referencias inversas a las constantes
                                        // Esto sirve para por ejemplo en un forall obtener todas las constantes
                                        // de un tipo dado.
                                        for_each(types->begin(),types->end(),bind2nd(mem_fun1_t<void,Type,const vector<ConstantSymbol *> *>(&Type::addRefsBy),ptr));
                                        delete types;
                                }
                                delete ptr;
                                }
#line 2544 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 60:
#line 711 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<ConstantSymbol *> * ptr = new vector<ConstantSymbol *>;
                                  ConstantSymbol * n = new ConstantSymbol((yyvsp[0].type_string));
                                  // comprobamos que la constante no se encuentre ya definida
                                  ConstantSymbol * f = parser_api->termtable->getConstantFromName(n->getName());
                                  if(f != 0){
                                    // Comprobar que los tipos sean iguales a la hora de generar un
                                    // error o bien un warning
                                    SearchLineInfo sli(f);
                                    snprintf(parerr,256,"Redefinition of the constant `%s'. (previous definition before or in line %d [%s]).",n->getName(),sli.lineNumber,sli.fileName.c_str());
                                    yywarning(parerr);
                                    delete n;
                                  }
                                  else{
                                      ptr->push_back(n);
                                      parser_api->termtable->addConstant(n);
                                      n->setFileId(parser_api->fileid);
                                      n->setLineNumber(lexer->getLineNumber());
                                  }
                                  (yyval.otype)=ptr;
                                }
#line 2569 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 61:
#line 732 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<ConstantSymbol *> * ptr = (vector<ConstantSymbol *> *) (yyvsp[-1].otype);
                                  ConstantSymbol * n = new ConstantSymbol((yyvsp[0].type_string));
                                  // comprobamos que la constante no se encuentre ya definida
                                  ConstantSymbol * f = parser_api->termtable->getConstantFromName(n->getName());
                                  if(f != 0){
                                      // Comprobar que los tipos sean iguales a la hora de generar un
                                      // error o bien un warning
                                      SearchLineInfo sli(f);
                                      snprintf(parerr,256,"Redefinition of the constant `%s'. (previous definition before or in line %d [%s]).",n->getName(),sli.lineNumber,sli.fileName.c_str());
                                      yywarning(parerr);
                                      delete n;
                                 }
                                 else{
                                        ptr->push_back(n);
                                        parser_api->termtable->addConstant(n);
                                        n->setFileId(parser_api->fileid);
                                        n->setLineNumber(lexer->getLineNumber());
                                }
                                  (yyval.otype)=ptr;
                                }
#line 2594 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 62:
#line 756 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = (yyvsp[-1].otype);
                                }
#line 2602 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 63:
#line 760 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<Type *> * ptr = new vector<Type *> ;
                                if((yyvsp[0].otype))
                                ptr->push_back((Type *)(yyvsp[0].otype));
                                  (yyval.otype)=ptr;
                                }
#line 2612 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 64:
#line 766 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<Type *> * ptr = new vector<Type *> ;
                                  (yyval.otype)=ptr;
                                }
#line 2620 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 65:
#line 772 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<Type *> * ptr = new vector<Type *>;
                                if(strcasecmp((yyvsp[0].type_string),"object")==0){
                                snprintf(parerr,256,"`object' is a built-in type and can't be redefined.");
                                yyerror(parerr);
                                }
                                else {
                                Type * t = new Type((yyvsp[0].type_string));
                                t->setFileId(parser_api->fileid);
                                t->setLineNumber(lexer->getLineNumber());
                                ptr->push_back(t);
                                }
                                  (yyval.otype)=ptr;
                                }
#line 2638 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 66:
#line 786 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<Type *> * ptr = (vector<Type *> *) (yyvsp[-1].otype);
                                if(strcasecmp((yyvsp[0].type_string),"object")==0){
                                snprintf(parerr,256,"`object' is a built-in type and can't be redefined.");
                                yyerror(parerr);
                                }
                                else {
                                Type * t = new Type((yyvsp[0].type_string));
                                t->setFileId(parser_api->fileid);
                                t->setLineNumber(lexer->getLineNumber());
                                ptr->push_back(t);
                                }
                                  (yyval.otype)=ptr;
                                }
#line 2656 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 67:
#line 803 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                // buscamos la referencia al tipo en el dominio
                                string * s = (string *) (yyvsp[0].otype);
                                if(strcasecmp(s->c_str(),"object") == 0) {
                                delete s;
                                (yyval.otype) = 0;
                                }
                                else {
                                Type * t = parser_api->domain->getModificableType(s->c_str());
                                const Type * nt;
                                if(!t){
                                        // cuando ocurre esto el tipo se crea de todas las maneras
                                        // pero posiblemente se trate de un error que deber�n gestionar
                                        // las reglas padre. Observar que en caso de que se cree como
                                        // nuevo el tipo no tendr� ni fichero ni l�nea asociados.
                                        nt = parser_api->domain->addType(s->c_str());
                                        t = parser_api->domain->getModificableType(nt->getId());
                                        if(errtypes){
                                                snprintf(parerr,256,"Undeclared type `%s'.",s->c_str());
                                                yyerror(parerr);
                                        }
                                }
                                delete s;
                                    (yyval.otype)=t;
                                }
                                }
#line 2687 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 68:
#line 832 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<const Type *> * ptr = new vector<const Type *> ;
                                if((yyvsp[0].otype))
                                    ptr->push_back((const Type *)(yyvsp[0].otype));
                                  (yyval.otype)=ptr;
                                }
#line 2697 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 69:
#line 838 "yacc/parser.yy" /* yacc.c:1646  */
    { vector<const Type *> * ptr = (vector<const Type *> *) (yyvsp[-1].otype);
                                  if((yyvsp[0].otype))
                                ptr->push_back((const Type *)(yyvsp[0].otype));
                                  (yyval.otype)=ptr;
                                }
#line 2707 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 73:
#line 853 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  string * nameLit = (string *) (yyvsp[0].otype);
                                  LiteralEffect * lit=0;
                                  Meta * mt=0;
                                  // buscamos si el literal ya est� definido en el diccionario de
                                  // nombres de literales
                                  ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),(const char *) nameLit->c_str());
                                  if(posit != (parser_api->domain->ldictionary).end()) {
                                      lit = new LiteralEffect(posit->second,parser_api->domain->metainfo.size());
                                      mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                      parser_api->domain->metainfo.push_back(mt);
                                  }
                                  else {
                                      lit = new LiteralEffect(idCounter++,parser_api->domain->metainfo.size());
                                      mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                      parser_api->domain->metainfo.push_back(mt);
                                      (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                  }
                                  container = lit;
                                  delete nameLit;
                                }
#line 2733 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 74:
#line 875 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  LiteralEffect * lit= (LiteralEffect *) container;
                                  container = 0;
                                  delete context;
                                  context=0;
                                  // buscar predicados duplicados
                                  int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                  bool duplicated=false;
                                  literaltablecit ite;
                                  for(ite = r.first; ite != r.second && !duplicated; ite++) {
                                      if(lit->sizep() == (*ite).second->sizep()) {
                                              // tenemos dos definiciones de predicado con el mismo nombre
                                              // y n�mero de argumentos ��No se como distinguirlos!!
                                              duplicated = true;
                                      }
                                  }

                                  if(!duplicated) {
                                      parser_api->domain->addLiteral(lit);
                                  }
                                  else {
                                      SearchLineInfo sli(lit->getMetaId());
                                      snprintf(parerr,256,"Conflicting predicate definition `%s' previous definition %d [%s].",lit->getName(),sli.lineNumber,sli.fileName.c_str());
                                      yyerror(parerr);
                                      delete lit;
                                  }
                                }
#line 2766 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 76:
#line 907 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  string * nameLit = (string *) (yyvsp[0].otype);
                                  Axiom * lit=0;
                                  Meta * mt=0;
                                  // buscamos si el literal ya est� definido en el diccionario de
                                  // nombres de literales
                                  ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),(const char *) nameLit->c_str());
                                  if(posit != (parser_api->domain->ldictionary).end()) {
                                      lit = new Axiom(posit->second,parser_api->domain->metainfo.size());
                                      mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                      parser_api->domain->metainfo.push_back(mt);
                                  }
                                  else {
                                      lit = new Axiom(idCounter++,parser_api->domain->metainfo.size());
                                      mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                      parser_api->domain->metainfo.push_back(mt);
                                      (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                  }
                                  container = lit;
                                  delete nameLit;
                                }
#line 2792 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 77:
#line 929 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  Axiom * lit= (Axiom *) container;
                                  container = 0;
                                  // comprobaciones de correctitud
                                  // busco en el dominio los literales con el nombre capturado
                                  // y el n�mero de argumentos adecuado
                                  // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                  int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                  bool unificacion=false;
                                  vector<Literal *> candidates;
                                  vector<Literal *>::const_iterator j;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++) {
                                      candidates.push_back((*i).second);
                                      Unifier u;
                                      if(unify3(lit->getParameters(),(*i).second->getParameters(),&u)){
                                          u.applyTypeSubstitutions(0);
                                          unificacion=true;
                                       }
                                  }
                                  if(!unificacion){
                                          snprintf(parerr,256,"(1) No matching predicate for `%s'.",lit->toString());
                                          yyerror(parerr);
                                          if(candidates.size() > 0) {
                                          *errflow << "Possible candidates:" << endl;
                                            for(j=candidates.begin();j!=candidates.end();j++) {
                                          SearchLineInfo sli((*j)->getMetaId());
                                               *errflow << "\t[" << sli.fileName << "]:" << sli.lineNumber;
                                          (*j)->printL(errflow,1);
                                          *errflow << endl;
                                            }
                                          }
                                  }
                                  parser_api->domain->addAxiom(lit);
                                  (yyval.otype) = lit;
                                }
#line 2833 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 78:
#line 966 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  (yyval.otype) =0;
                                }
#line 2841 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 79:
#line 972 "yacc/parser.yy" /* yacc.c:1646  */
    {contador = 0;}
#line 2847 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 82:
#line 977 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  // si tenemos un contenedor donde meter la variable
                                  // la a�adimos
                                  if(!container)
                                      *errflow << "(mensaje recordatorio) (-- Aqui deber�a haber un container --)" << endl;
                                  if(container){
                                      if(container->searchTermId((yyvsp[0].termtype)->first) != container->parametersEnd()){
                                          // es raro que se tenga una variable repetida
                                          snprintf(parerr,256,"Duplicated variable: `%s'.",parser_api->termtable->getVariable(*(yyvsp[0].termtype))->getName());
                                          yywarning(parerr);
                                      }
                                      container->addParameter(*(yyvsp[0].termtype));
                                  }
                                }
#line 2866 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 83:
#line 992 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  if(!container)
                                      *errflow << "(mensaje recordatorio) (-- Aqui deber�a haber un container --)" << endl;
                                  if(container && (yyvsp[0].otype)) {
                                      // recorremos hacia atr�s todas las variables insertadas anteriormente,
                                      // hasta encontrar la primera que no tiene tipo asignado.
                                      // A partir de este asignamos type
                                      vector<Type *> * vt = (vector<Type *> *)(yyvsp[0].otype);
                                      if(!vt->empty()) {
                                          TestTypeTree()(vt);
                                          KeyList * kl = container->getModificableParameters();
                                          KeyList::iterator i,e;
                                          e = kl->end();
                                          for(i=kl->begin() + contador;i!=e;i++) {
                                                  parser_api->termtable->getVariable(*i)->addTypes2(vt);
                                          }
                                      }
                                      delete vt;
                                      contador = container->getModificableParameters()->size();
                                  }
                                  else if(!(yyvsp[0].otype)) {
                                      snprintf(parerr,256,"Type expected after `-'.");
                                      yywarning(parerr);
                                  }
                                }
#line 2896 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 84:
#line 1020 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    if(!parser_api->domain->errfluents && !parser_api->domain->hasRequirement(":fluents"))
                                    {
                                        parser_api->domain->errfluents = true;
                                        yyerror("Using a clause that requires `:fluents' and is not declared in requirements clause");
                                    }
                                }
#line 2908 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 87:
#line 1035 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                PyDefFunction * lit=0;
                                Meta * mt=0;
                                // buscamos si el literal ya est� definido en el diccionario de
                                // nombres de literales
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),(const char *) nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                lit = new PyDefFunction(posit->second,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                lit = new PyDefFunction(idCounter++,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                context = new LDictionary;
                                }
#line 2936 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 88:
#line 1059 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PyDefFunction * lit= (PyDefFunction *) container;
                                container = 0;
                                delete context;
                                context=0;
                                // buscar predicados duplicados
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool duplicated=false;
                                literaltablecit ite;
                                for(ite = r.first; ite != r.second && !duplicated; ite++)
                                {
                                if(lit->sizep() == (*ite).second->sizep())
                                        // tenemos dos definiciones de predicado con el mismo nombre
                                        // y n�mero de argumentos ��No se como distinguirlos!!
                                        duplicated = true;
                                }

                                if(!duplicated){
                                parser_api->domain->addLiteral(lit);
                                }
                                else {
                                SearchLineInfo sli(lit->getMetaId());
                                snprintf(parerr,256,"Conflicting function definition `%s' previous definition %d [%s].",lit->getName(),sli.lineNumber,sli.fileName.c_str());
                                yyerror(parerr);
                                delete lit;
                                }
                                if((yyvsp[0].type_string)){
                                if(!lit->setCode((yyvsp[0].type_string))){
                                snprintf(parerr,256,"Error in Python script code. Function: %s.",lit->getName());
                                yyerror(parerr);
                                }
                                }
                                vector<Type *> * types = (vector<Type *> *) (yyvsp[-1].otype);
                                if(types){
                                        // en pddl estandard se supone que el tipo es un n�mero
                                        // pero lo dejamos abierto para la extensi�n. De momento
                                        // se ignora el tipo en las funciones.
                                        lit->addTypes(types);
                                        delete types;
                                }
                                }
#line 2983 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 89:
#line 1104 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Type * number = parser_api->domain->getModificableType("number");
                                vector<Type *> * vt = new vector<Type *>;
                                vt->push_back(number);
                                (yyval.otype)=vt;
                                }
#line 2994 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 90:
#line 1111 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=(yyvsp[0].otype);}
#line 3000 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 91:
#line 1115 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.type_string) = 0;}
#line 3006 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 92:
#line 1117 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    static string code = "";
                                code = (yyvsp[0].type_string);
                                    if(PYTHON_FLAG) {
                                        (yyval.type_string) = code.c_str();
                                    }
                                    else {
                                        yyerror("Parser compiled without Python support. Install python and recompile.");
                                        (yyval.type_string) = 0;
                                    }
                                 }
#line 3022 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 97:
#line 1137 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  if(!parser_api->domain->errder && !parser_api->domain->hasRequirement(":derived-predicates"))
                                  {
                                        parser_api->domain->errhtn = true;
                                        yyerror("Using a clause that requires `:derived-predicates' and is not declared in requirements clause");
                                  }
                                }
#line 3034 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 100:
#line 1150 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                context = new LDictionary;
                                string * name = (string *) (yyvsp[0].otype);
                                PrimitiveTask * priTask=0;
                                Meta * mt = 0;
                                // buscamos en el diccionario si la acci�n ya tiene un identificador
                                // asociado, en cuyo caso lo reutilizamos
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),name->c_str());
                                      if(posit != (parser_api->domain->ldictionary).end()) {
                                        priTask = new PrimitiveTask(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                      else
                                      {
                                        priTask = new PrimitiveTask(idCounter++,parser_api->domain->metainfo.size());
                                        mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                          (parser_api->domain->ldictionary).insert(make_pair(priTask->getName(),priTask->getId()));
                                      }
                                container = priTask;
                                delete name;
                                (yyval.otype) = priTask;
                                }
#line 3063 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 101:
#line 1176 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                        // si hay alg�n tag
                                        if((yyvsp[0].otype)){
                                        TagVector * tv = (TagVector *) (yyvsp[0].otype);
                                        tagv_ite tb, te = tv->end();
                                        int mid = ((PrimitiveTask *) container)->getMetaId();
                                        for(tb = tv->begin();tb!=te;tb++){
                                        parser_api->domain->metainfo[mid]->addTag(*tb);
                                        }
                                        tv->clear();
                                        delete tv;
                                        }
                                        container = 0;
                                }
#line 3082 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 102:
#line 1193 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PrimitiveTask * priTask= (PrimitiveTask *) (yyvsp[-9].otype);
                                priTask->setPrecondition((Goal *) (yyvsp[-2].otype));
                                priTask->setEffect((Effect *) (yyvsp[-1].otype));
                                parser_api->domain->addTask(priTask);
                                delete context;
                                context = 0;
                                }
#line 3095 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 103:
#line 1205 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                context = new LDictionary;
                                string * name = (string *) (yyvsp[0].otype);
                                CompoundTask * compTask=0;
                                Meta * mt=0;
                                // buscamos en el diccionario si la acci�n ya tiene un identificador
                                // asociado, en cuyo caso lo reutilizamos
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),name->c_str());
                                      if(posit != (parser_api->domain->ldictionary).end()) {
                                        compTask = new CompoundTask(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                      else
                                      {
                                        compTask = new CompoundTask(idCounter++,parser_api->domain->metainfo.size());
                                        mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                          (parser_api->domain->ldictionary).insert(make_pair(compTask->getName(),compTask->getId()));
                                      }
                                container = compTask;
                                delete name;
                                cbuilding = compTask;
                                }
#line 3124 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 104:
#line 1233 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if((yyvsp[-2].otype)){
                                        TagVector * tv = (TagVector *) (yyvsp[-2].otype);
                                        tagv_ite tb, te = tv->end();
                                        int mid = ((CompoundTask *) container)->getMetaId();
                                        for(tb = tv->begin();tb!=te;tb++)
                                        parser_api->domain->metainfo[mid]->addTag(*tb);
                                        tv->clear();
                                        delete tv;
                                }
                                if(!parser_api->domain->errhtn && !parser_api->domain->hasRequirement(":htn-expansion"))
                                {
                                        parser_api->domain->errhtn = true;
                                        yyerror("Using a clause that requires `:htn-expansion' and is not declared in requirements clause");
                                }
                                CompoundTask * compTask= cbuilding;
                                parser_api->domain->addTask(compTask);
                                delete context;
                                context = 0;
                                cbuilding=0;
                                }
#line 3150 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 105:
#line 1258 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TCTR> * v = new vector<TCTR>;
                                TCTR * ele = (TCTR *) (yyvsp[0].otype);
                                v->push_back(*ele);
                                (yyval.otype)= v;
                                }
#line 3161 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 106:
#line 1265 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TCTR> * v = (vector<TCTR> *) (yyvsp[-1].otype);
                                (yyval.otype)= v;
                                }
#line 3170 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 107:
#line 1270 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TCTR> * v = new vector<TCTR>;
                                (yyval.otype)= v;
                                }
#line 3179 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 108:
#line 1277 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    static TCTR p;
                                    p = make_pair(EQ_DUR,(Evaluable *)(yyvsp[-1].otype));
                                    (yyval.otype) = &p;
                                }
#line 3189 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 109:
#line 1283 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    static TCTR p;
                                    p = make_pair(LEQ_DUR,(Evaluable *)(yyvsp[-1].otype));
                                    (yyval.otype) = &p;
                                }
#line 3199 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 110:
#line 1289 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    static TCTR p;
                                    p = make_pair(GEQ_DUR,(Evaluable *)(yyvsp[-1].otype));
                                    (yyval.otype) = &p;
                                }
#line 3209 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 111:
#line 1295 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    static TCTR p;
                                    p = make_pair(LESS_DUR,(Evaluable *)(yyvsp[-1].otype));
                                    (yyval.otype) = &p;
                                }
#line 3219 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 112:
#line 1301 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    static TCTR p;
                                    p = make_pair(GRE_DUR,(Evaluable *)(yyvsp[-1].otype));
                                    (yyval.otype) = &p;
                                }
#line 3229 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 113:
#line 1308 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    (yyval.otype) = (yyvsp[0].otype);
                                }
#line 3237 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 114:
#line 1312 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(EQ_START,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3247 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 115:
#line 1318 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(LEQ_START,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3257 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 116:
#line 1324 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(GEQ_START,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3267 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 117:
#line 1330 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(LESS_START,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3277 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 118:
#line 1336 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(GRE_START,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3287 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 119:
#line 1342 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(EQ_END,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3297 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 120:
#line 1348 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(LEQ_END,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3307 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 121:
#line 1354 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(GEQ_END,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3317 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 122:
#line 1360 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(LESS_END,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3327 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 123:
#line 1366 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                static TCTR p;
                                p = make_pair(GRE_END,(Evaluable *)(yyvsp[-1].otype));
                                (yyval.otype) = &p;
                                }
#line 3337 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 124:
#line 1374 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<pair<int,Evaluable *> > * v = new vector<pair<int,Evaluable *> >;
                                v->push_back(*((pair<int,Evaluable *> *) (yyvsp[0].otype)));
                                (yyval.otype)= v;
                                }
#line 3347 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 125:
#line 1380 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<pair<int,Evaluable *> > * v = (vector<pair<int,Evaluable *> > *) (yyvsp[-1].otype);
                                v->push_back(*((pair<int,Evaluable *> *) (yyvsp[0].otype)));
                                (yyval.otype)= v;
                                }
#line 3357 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 127:
#line 1389 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cbuilding->setFirst();
                                }
#line 3365 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 128:
#line 1393 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cbuilding->setFirst();
                                cbuilding->setRandom();
                                }
#line 3374 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 129:
#line 1398 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cbuilding->setFirst();
                                cbuilding->setRandom();
                                }
#line 3383 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 130:
#line 1403 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cbuilding->setRandom();
                                }
#line 3391 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 133:
#line 1415 "yacc/parser.yy" /* yacc.c:1646  */
    {container=cbuilding;}
#line 3397 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 134:
#line 1417 "yacc/parser.yy" /* yacc.c:1646  */
    {container=0;}
#line 3403 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 135:
#line 1418 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * name = (string *) (yyvsp[-3].otype);
                                // comprobar que el m�todo no se haya definido con anterioridad
                                methodcit i,e = cbuilding->getEndMethod();
                                bool definido=false;
                                for(i=cbuilding->getBeginMethod();i!=e && !definido;i++)
                                        if(!strcasecmp((*i)->getName(),name->c_str())){
                                        definido = true;
                                        break;
                                        }
                                if(definido){
                                        SearchLineInfo sli((*i)->getMetaId());
                                        snprintf(parerr,256,"The method `%s' is already defined for this task in or before %d [%s].",(*i)->getName(),sli.lineNumber,sli.fileName.c_str());
                                        yywarning(parerr);
                                }
                                Method * method=0;
                                      method = new Method(parser_api->domain->metainfo.size(),cbuilding);
                                Meta * mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                if((yyvsp[-1].otype)){
                                        TagVector * tv = (TagVector *) (yyvsp[-1].otype);
                                        tagv_ite tb, te = tv->end();
                                        int mid = method->getMetaId();
                                        for(tb = tv->begin();tb!=te;tb++)
                                        parser_api->domain->metainfo[mid]->addTag(*tb);
                                        tv->clear();
                                        delete tv;
                                }
                                delete name;

                                // forzamos a que cada m�todo tenga su propio contexto
                                oldContext = context;
                                context = new LDictionary();
                                // A�adimos al contexto las variables que tengo
                                keylistcit j, k = method->parametersEnd();
                                for(j=method->parametersBegin();j!=k;j++)
                                        context->insert(make_pair(parser_api->termtable->getVariable((*j))->getName(),(*j).first));
                                (yyval.otype) = method;
                                }
#line 3447 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 136:
#line 1460 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Method * method = (Method *) (yyvsp[-4].otype);
                                method->setPrecondition((Goal *) (yyvsp[-3].otype));
                                method->setTaskNetwork((TaskNetwork *) (yyvsp[-1].otype));
                                cbuilding->addMethod(method);
                                delete context;
                                context = oldContext;
                                oldContext = 0;
                                }
#line 3461 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 137:
#line 1472 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = 0;
                                }
#line 3469 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 138:
#line 1477 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = (yyvsp[-1].otype);
                                }
#line 3477 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 139:
#line 1483 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new TagVector();
                                }
#line 3485 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 140:
#line 1487 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                TagVector * tv = (TagVector *) (yyvsp[-1].otype);
                                tv->push_back((Tag *)(yyvsp[0].otype));
                                (yyval.otype) = tv;
                                }
#line 3495 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 141:
#line 1495 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                const char * name = (const char *) (yyvsp[0].type_string);
                                TextTag * mt = new TextTag(name);
                                (yyval.otype) = mt;
                                }
#line 3505 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 142:
#line 1501 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                TextTag * mt = (TextTag *) (yyvsp[-2].otype);
                                    string text = (const char *) (yyvsp[-1].type_string);

                                // Fijar el valor
                                if(container){
                                        string value = processTextTag(text, container);
                                        mt->setValue(value.c_str());
                                }
                                else{
                                        mt->setValue(text.c_str());
                                }

                                    (yyval.otype) = mt;
                                    if(!parser_api->domain->errmetatags && !parser_api->domain->hasRequirement(":metatags"))
                                    {
                                        parser_api->domain->errmetatags = true;
                                        yyerror("Using a clause that requires `:metatags' and is not declared in requirements clause");
                                    }
                                }
#line 3530 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 143:
#line 1524 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=(yyvsp[0].otype);}
#line 3536 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 144:
#line 1526 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=0; *errflow << "No implementado achieve" << endl;}
#line 3542 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 145:
#line 1528 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) =(yyvsp[0].otype);}
#line 3548 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 146:
#line 1532 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PrimitiveTask * priTask=0;
                                Meta * mt = 0;
                                // buscamos en el diccionario si la acci�n ya tiene un identificador
                                // asociado, en cuyo caso lo reutilizamos
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),":inline");
                                      if(posit != (parser_api->domain->ldictionary).end()) {
                                        priTask = new PrimitiveTask(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(":inline",lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                      else
                                      {
                                        priTask = new PrimitiveTask(idCounter++,parser_api->domain->metainfo.size());
                                        mt = new Meta(":inline",lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                          (parser_api->domain->ldictionary).insert(make_pair(priTask->getName(),priTask->getId()));
                                      }
                                priTask->setInline();
                                (yyval.otype) = priTask;
                                }
#line 3574 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 147:
#line 1554 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                        PrimitiveTask * priTask= (PrimitiveTask *) (yyvsp[-3].otype);
                                        priTask->setPrecondition((Goal *) (yyvsp[-2].otype));
                                        priTask->setEffect((Effect *) (yyvsp[-1].otype));
                                        (yyval.otype) = priTask;
                                }
#line 3585 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 148:
#line 1561 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PrimitiveTask * priTask=0;
                                Meta * mt = 0;
                                // buscamos en el diccionario si la acci�n ya tiene un identificador
                                // asociado, en cuyo caso lo reutilizamos
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),":!inline");
                                      if(posit != (parser_api->domain->ldictionary).end()) {
                                        priTask = new PrimitiveTask(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(":!inline",lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                      else
                                      {
                                        priTask = new PrimitiveTask(idCounter++,parser_api->domain->metainfo.size());
                                        mt = new Meta(":!inline",lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                          (parser_api->domain->ldictionary).insert(make_pair(priTask->getName(),priTask->getId()));
                                      }
                                priTask->setInline(2);
                                (yyval.otype) = priTask;
                                }
#line 3611 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 149:
#line 1583 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                        PrimitiveTask * priTask= (PrimitiveTask *) (yyvsp[-3].otype);
                                        priTask->setPrecondition((Goal *) (yyvsp[-2].otype));
                                        priTask->setEffect((Effect *) (yyvsp[-1].otype));
                                        (yyval.otype) = priTask;
                                }
#line 3622 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 150:
#line 1592 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * name = (string *) (yyvsp[0].otype);
                                TaskHeader * th=0;
                                MetaTH * mt = 0;
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),name->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                th = new TaskHeader(posit->second,parser_api->domain->metainfo.size());
                                mt = new MetaTH(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back((Meta *)mt);
                                }
                                else
                                {
                                th = new TaskHeader(idCounter++,parser_api->domain->metainfo.size());
                                mt = new MetaTH(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back((Meta *)mt);
                                (parser_api->domain->ldictionary).insert(make_pair(th->getName(), th->getId()));
                                }
                                container = th;
                                delete name;
                                contador=0;
                                }
#line 3648 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 151:
#line 1614 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                // se deja para una comprobaci�n posterior el ver
                                // si el th se corresponde con alguna tarea del dominio
                                TaskHeader * th= (TaskHeader *) container;
                                container = 0;
                                (yyval.otype) = th;
                                }
#line 3660 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 152:
#line 1624 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = (yyvsp[0].otype);
                                }
#line 3668 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 153:
#line 1628 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                // esto es una noop
                                Meta * mt = 0;
                                PrimitiveTask * priTask;
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),":!inline");
                                    if(posit != (parser_api->domain->ldictionary).end()) {
                                        priTask = new PrimitiveTask(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(":inline",lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                    else
                                    {
                                        priTask = new PrimitiveTask(idCounter++,parser_api->domain->metainfo.size());
                                        mt = new Meta(":inline",lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                          (parser_api->domain->ldictionary).insert(make_pair(priTask->getName(),priTask->getId()));
                                    }
                                priTask->setInline();
                                TaskNetwork * tn = new TaskNetwork(priTask);
                                (yyval.otype) = tn;
                                }
#line 3694 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 154:
#line 1653 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);
                                vt->push_back((TaskNetwork *) (yyvsp[0].otype));
                                (yyval.otype) = vt;
                                }
#line 3704 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 155:
#line 1659 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TaskNetwork *> * vt = new vector<TaskNetwork *>;
                                vt->push_back((TaskNetwork *) (yyvsp[0].otype));
                                (yyval.otype) = vt;
                                }
#line 3714 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 156:
#line 1667 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new TaskNetwork((Task *) (yyvsp[0].otype));
                                }
#line 3722 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 157:
#line 1671 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                TaskNetwork * tn = new TaskNetwork((Task *) (yyvsp[0].otype));
                                tn->setInmediate(0,true);
                                (yyval.otype) = tn;
                                }
#line 3732 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 158:
#line 1677 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TCTR> * v = (vector<TCTR> *) (yyvsp[-2].otype);
                                vector<TCTR>::iterator iv, ev = v->end();
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);

                                TaskNetwork * tn = vt->front();
                                vector<TaskNetwork *>::iterator i, e = vt->end();
                                for(i = vt->begin() + 1; i != e; i++) {
                                        tn->merge(*i);
                                        delete (*i);
                                }
                                delete vt;

                                if(v){
                                        for(iv = v->begin();iv!=ev;iv++){
                                        tn->addTConstraint((*iv));
                                        }
                                        delete v;
                                }

                                intvit j, je = tn->getSuccEnd(0);
                                for(j=tn->getSuccBegin(0);j!=je;j++)
                                        tn->setBTTask((*j)-1);
                                (yyval.otype) = tn;
                                }
#line 3762 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 159:
#line 1703 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);

                                TaskNetwork * tn = vt->front();
                                vector<TaskNetwork *>::iterator i, e = vt->end();
                                for(i = vt->begin() + 1; i != e; i++) {
                                        tn->merge(*i);
                                        delete (*i);
                                }
                                delete vt;
                                intvit j, je = tn->getSuccEnd(0);
                                for(j=tn->getSuccBegin(0);j!=je;j++)
                                        tn->setBTTask((*j)-1);
                                (yyval.otype) = tn;
                                }
#line 3782 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 160:
#line 1719 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TCTR> * v = (vector<TCTR> *) (yyvsp[-2].otype);
                                vector<TCTR>::iterator iv, ev = v->end();
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);

                                TaskNetwork * tn = vt->front();
                                vector<TaskNetwork *>::iterator i, e = vt->end();
                                for(i = vt->begin() + 1; i != e; i++) {
                                        tn->join(*i);
                                        delete (*i);
                                }
                                delete vt;

                                if(v){
                                        for(iv = v->begin();iv!=ev;iv++){
                                        tn->addTConstraint((*iv));
                                        }
                                        delete v;
                                }

                                (yyval.otype) = tn;
                                }
#line 3809 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 161:
#line 1742 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);

                                TaskNetwork * tn = vt->front();
                                vector<TaskNetwork *>::iterator i, e = vt->end();
                                for(i = vt->begin() + 1; i != e; i++) {
                                        tn->join(*i);
                                        delete (*i);
                                }
                                delete vt;
                                (yyval.otype) = tn;
                                }
#line 3826 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 162:
#line 1755 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TCTR> * v = (vector<TCTR> *) (yyvsp[-2].otype);
                                vector<TCTR>::iterator iv, ev = v->end();
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);

                                TaskNetwork * tn = vt->front();
                                vector<TaskNetwork *>::iterator i, e = vt->end();
                                for(i = vt->begin() + 1; i != e; i++) {
                                        tn->merge(*i);
                                        delete (*i);
                                }
                                delete vt;

                                if(v){
                                        for(iv = v->begin();iv!=ev;iv++){
                                        tn->addTConstraint((*iv));
                                        }
                                        delete v;
                                }

                                (yyval.otype) = tn;
                                }
#line 3853 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 163:
#line 1778 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<TaskNetwork *> * vt = (vector<TaskNetwork *> *) (yyvsp[-1].otype);

                                TaskNetwork * tn = vt->front();
                                vector<TaskNetwork *>::iterator i, e = vt->end();
                                for(i = vt->begin() + 1; i != e; i++) {
                                        tn->merge(*i);
                                        delete (*i);
                                }
                                delete vt;
                                (yyval.otype) = tn;
                                }
#line 3870 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 164:
#line 1793 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = 0;}
#line 3876 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 165:
#line 1795 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = (yyvsp[0].otype);}
#line 3882 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 166:
#line 1799 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = 0;}
#line 3888 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 167:
#line 1801 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                CutGoal * cg = new CutGoal();
                                cg->setGoal((Goal *)(yyvsp[-1].otype));
                                (yyval.otype) = cg;
                                }
#line 3898 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 168:
#line 1807 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                SortGoal * sg = new SortGoal();
                                container = sg;
                                (yyval.otype) = sg;
                                }
#line 3908 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 169:
#line 1813 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                container = 0;
                                }
#line 3916 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 170:
#line 1817 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                SortGoal * sg = (SortGoal *) (yyvsp[-4].otype);
                                Goal * g = (Goal *) (yyvsp[-1].otype);
                                sg->setGoal(g);
                                // Buscamos que la variable por la que queremos ordenar al menos
                                // aparezca en la precondicion.
                                keylistcit i, e = sg->endp();
                                for(i=sg->beginp();i!=e;i++){
                                        if(!g->hasTerm((*i).first)) {
                                        snprintf(parerr,256,"The variable you are trying to sort by (%s), doesn't appear in goal!.",parser_api->termtable->getVariable((*i))->getName());
                                        yyerror(parerr);
                                        }
                                }
                                (yyval.otype) = sg;
                                }
#line 3936 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 171:
#line 1833 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new FluentVar((pkey *)(yyvsp[0].termtype));
                                }
#line 3944 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 172:
#line 1837 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentVar * fv = (FluentVar *) (yyvsp[-2].otype);
                                BoundGoal * bg = new BoundGoal(fv,(Evaluable *)(yyvsp[-1].otype));
                                    if(!parser_api->domain->errfluents && !parser_api->domain->hasRequirement(":fluents"))
                                    {
                                        parser_api->domain->errfluents = true;
                                        yyerror("Using a clause that requires `:fluents' and is not declared in requirements clause");
                                    }
                                (yyval.otype) = bg;
                                }
#line 3959 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 173:
#line 1848 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PrintGoal * pg = new PrintGoal();
                                pg->setGoal((Goal *) (yyvsp[-1].otype));
                                (yyval.otype) = pg;
                                }
#line 3969 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 174:
#line 1854 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PrintGoal * pg = new PrintGoal();
                                pg->setStr((yyvsp[-1].type_string));
                                (yyval.otype) = pg;
                                }
#line 3979 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 175:
#line 1860 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                PrintGoal * pg = new PrintGoal();
                                container = pg;
                                (yyval.otype) = pg;
                                contador = 0;
                                }
#line 3990 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 176:
#line 1867 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                container = 0;
                                (yyval.otype) = (yyvsp[-2].otype);
                                }
#line 3999 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 177:
#line 1872 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = (yyvsp[0].otype);
                                }
#line 4007 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 178:
#line 1876 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = (yyvsp[0].otype);
                                }
#line 4015 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 179:
#line 1882 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                AndGoal * ag = new AndGoal();
                                gcontainer.push_back(ag);
                                (yyval.otype) = ag;
                                }
#line 4025 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 180:
#line 1888 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                gcontainer.pop_back();
                                }
#line 4033 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 181:
#line 1892 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                AndGoal * ag = (AndGoal *) (yyvsp[-3].otype);
                                (yyval.otype) = ag;
                                }
#line 4042 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 182:
#line 1897 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                OrGoal * ag = new OrGoal();
                                gcontainer.push_back(ag);
                                (yyval.otype) = ag;
                                }
#line 4052 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 183:
#line 1903 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                gcontainer.pop_back();
                                }
#line 4060 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 184:
#line 1907 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                OrGoal * ag = (OrGoal *) (yyvsp[-3].otype);
                                (yyval.otype) = ag;
                                }
#line 4069 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 185:
#line 1912 "yacc/parser.yy" /* yacc.c:1646  */
    { Goal * g = (Goal *) (yyvsp[-1].otype);
                                if(g){
                                if(g->getPolarity())
                                g->setPolarity(false);
                                else
                                g->setPolarity(true);
                                }
                                /* negative-preconditions */
                                if(!parser_api->domain->errnegative && !parser_api->domain->hasRequirement(":negative-preconditions"))
                                {
                                        parser_api->domain->errnegative = true;
                                yyerror("Using a clause that requires `:negative-preconditions' and is not declared in requirements clause");
                                }
                                (yyval.otype) = g;
                                }
#line 4089 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 186:
#line 1928 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new ImplyGoal((Goal *) (yyvsp[-2].otype), (Goal *) (yyvsp[-1].otype));
                                    if(!parser_api->domain->errdisjuntive && !parser_api->domain->hasRequirement(":disjuntive-preconditions"))
                                    {
                                        parser_api->domain->errdisjuntive = true;
                                        yyerror("Using a clause that requires `:disjuntive-preconditions' and is not declared in requirements clause");
                                    }
                                }
#line 4102 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 187:
#line 1937 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ExistsGoal * fag = new ExistsGoal();
                                container = fag;
                                (yyval.otype) = fag;
                                }
#line 4112 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 188:
#line 1943 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                container = 0;
                                }
#line 4120 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 189:
#line 1947 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ExistsGoal * fag = (ExistsGoal *) (yyvsp[-6].otype);
                                Goal * g = (Goal *) (yyvsp[-1].otype);
                                fag->setGoal(g);
                                /* universal-preconditions */
                                    if(!parser_api->domain->errexistential && !parser_api->domain->hasRequirement(":existential-preconditions"))
                                    {
                                        parser_api->domain->errexistential = true;
                                        yyerror("Using a clause that requires `:existential-preconditions' and is not declared in requirements clause");
                                    }
                                (yyval.otype) = fag;
                                }
#line 4137 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 190:
#line 1960 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                // creamos el forall, y lo ponemos como
                                // el elemento que va a contener a las variables
                                ForallGoal * fag = new ForallGoal();
                                container = fag;
                                (yyval.otype) = fag;
                                }
#line 4149 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 191:
#line 1968 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                container = 0;
                                }
#line 4157 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 192:
#line 1972 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ForallGoal * fag = (ForallGoal *) (yyvsp[-6].otype);
                                Goal * g = (Goal *) (yyvsp[-1].otype);
                                fag->setGoal(g);
                                /* universal-preconditions */
                                    if(!parser_api->domain->erruniversal && !parser_api->domain->hasRequirement(":universal-preconditions"))
                                    {
                                        parser_api->domain->erruniversal = true;
                                        yyerror("Using a clause that requires `:universal-preconditions' and is not declared in requirements clause");
                                    }
                                (yyval.otype) = fag;
                                }
#line 4174 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 193:
#line 1985 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = (yyvsp[0].otype);}
#line 4180 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 194:
#line 1987 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = (LiteralGoal *) (yyvsp[0].otype);}
#line 4186 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 195:
#line 1991 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Goal * g = (Goal *) (yyvsp[-1].otype);
                                TimeInterval * ti = (TimeInterval *) (yyvsp[-2].otype);
                                g->setTime(ti);
                                    if(!parser_api->domain->errdurative && !parser_api->domain->hasRequirement(":durative-actions"))
                                    {
                                        parser_api->domain->errdurative = true;
                                        yyerror("Using a clause that requires `:durative-actions' and is not declared in requirements clause");
                                    }
                                    if(!isDurative) {
                                        yyerror("Using a durative goal inside a non durative action.");
                                    }
                                (yyval.otype) = g;
                                }
#line 4205 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 196:
#line 2007 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = DEFAULT_CRITERIA;
                                }
#line 4213 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 197:
#line 2011 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = SASC;
                                }
#line 4221 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 198:
#line 2015 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = SDESC;
                                }
#line 4229 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 201:
#line 2025 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                pkey ret = *(yyvsp[-1].termtype);
                                SortGoal * sg = (SortGoal *) container;
                                sg->addCriteria((SortType)(yyvsp[0].type_int));
                                sg->addParameter(ret);
                                }
#line 4240 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 203:
#line 2034 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if((yyvsp[0].otype)){
                                ContainerGoal * lc = (ContainerGoal *) gcontainer.back();
                                lc->addGoalByRef((Goal *) (yyvsp[0].otype));

                                }
                                }
#line 4252 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 204:
#line 2044 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = (LiteralEffect *) (yyvsp[0].otype);}
#line 4258 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 205:
#line 2046 "yacc/parser.yy" /* yacc.c:1646  */
    { LiteralEffect * lit = (LiteralEffect *) (yyvsp[-1].otype);
                                lit->setMaintain(true);
                                (yyval.otype) = lit;
                                }
#line 4267 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 206:
#line 2055 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                LiteralEffect * lit=0;
                                Meta * mt=0;
                                // buscamos si el literal ya est� definido en el diccionario de
                                // nombres de literales (deber�a estarlo)
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                lit = new LiteralEffect(posit->second,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                lit = new LiteralEffect(idCounter++,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                contador = 0;
                                }
#line 4295 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 207:
#line 2079 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralEffect * lit= (LiteralEffect *) container;
                                container = 0;
                                // comprobaciones de correctitud
                                // busco en el dominio los literales con el nombre capturado
                                  // y el n�mero de argumentos adecuado
                                  // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool unificacion=false;
                                vector<Literal *> candidates;
                                vector<Literal *>::const_iterator j;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++)
                                  {
                                candidates.push_back((*i).second);
                                     Unifier u;
                                     if(unify3(lit->getParameters(),(*i).second->getParameters(),&u)){
                                        u.applyTypeSubstitutions(0);
                                        unificacion=true;
                                     }
                                  }
                                if(!unificacion){
                                        snprintf(parerr,256,"(2) No matching predicate for `%s'.",lit->toString());
                                        yyerror(parerr);
                                        if(candidates.size() > 0) {
                                        *errflow << "Possible candidates:" << endl;
                                          for(j=candidates.begin();j!=candidates.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                             *errflow << "\t[" << sli.fileName << "]:" << sli.lineNumber;
                                        (*j)->printL(errflow,1);
                                        *errflow << endl;
                                          }
                                        }
                                }
                                (yyval.otype) = lit;
                                }
#line 4336 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 208:
#line 2118 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                LiteralGoal * lit=0;
                                Meta * mt = 0;
                                // buscamos si el literal ya est� definido en el diccionario de
                                // nombres de literales (deber�a estarlo)
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                lit = new LiteralGoal(posit->second,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                lit = new LiteralGoal(idCounter++,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                contador = 0;
                                }
#line 4364 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 209:
#line 2142 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralGoal * lit= (LiteralGoal *) container;
                                container = 0;
                                // comprobaciones de correctitud
                                // busco en el dominio los literales con el nombre capturado
                                  // y el n�mero de argumentos adecuado
                                  // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool unificacion=false;
                                vector<Literal *> candidates;
                                vector<Literal *>::const_iterator j;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++)
                                  {
                                candidates.push_back((*i).second);
                                     Unifier u;
                                     if(unify3(lit->getParameters(),(*i).second->getParameters(),&u)){
                                        u.applyTypeSubstitutions(0);
                                        unificacion=true;
                                     }
                                  }
                                if(!unificacion){
                                        snprintf(parerr,256,"(3) No matching predicate for `%s'.",lit->toString());
                                        yyerror(parerr);
                                        if(candidates.size() > 0) {
                                        *errflow << "Possible candidates:" << endl;
                                          for(j=candidates.begin();j!=candidates.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                             *errflow << "\t[" << sli.fileName << "]:" << sli.lineNumber;
                                        (*j)->printL(errflow,1);
                                        *errflow << endl;
                                          }
                                        }
                                }
                                (yyval.otype) = lit;
                                }
#line 4405 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 212:
#line 2186 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * c = (string *) (yyvsp[0].otype);
                                if(!container)
                                *errflow << "(mensaje recordatorio) (-- Aqui deber�a haber un container --)" << endl;
                                if(container){
                                // la constante deber�a haberse definido con anterioridad, en otro caso
                                // se trata de un error
                                ldictionaryit posit = (parser_api->domain->cdictionary).find(c->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                        // devolver el pkey de la constante
                                        container->addParameter(make_pair((*posit).second, 0));
                                        contador = container->getModificableParameters()->size()+1;
                                }
                                else {
                                     snprintf(parerr,256,"Undefined constant `%s'.",c->c_str());
                                     yyerror(parerr);
                                     ConstantSymbol * n = new ConstantSymbol(c->c_str(),-1);
                                     n->setLineNumber(lexer->getLineNumber());
                                     n->setFileId(parser_api->fileid);
                                     container->addParameter(parser_api->termtable->addConstant(n));
                                     contador = container->getModificableParameters()->size()+1;
                                }
                                }
                                delete c;
                                }
#line 4435 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 213:
#line 2212 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if(!container)
                                *errflow << "(mensaje recordatorio) (-- Aqui deber�a haber un container --)" << endl;
                                if(container){
                                container->addParameter(*(yyvsp[0].termtype));
                                if(container->getModificableParameters()->empty())
                                        contador = 0;
                                }
                                }
#line 4449 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 214:
#line 2222 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if(!container)
                                *errflow << "(mensaje recordatorio) (-- Aqui deber�a haber un container --)" << endl;
                                if(container && (yyvsp[0].otype)){
                                // recorremos hacia atr�s todas las variables insertadas anteriormente,
                                // hasta encontrar la primera que no tiene tipo asignado.
                                // A partir de este asignamos type
                                if(container->getModificableParameters()->empty())
                                        contador = 0;
                                container->addParameter(*(yyvsp[-2].termtype));
                                vector<Type *> * vt = (vector<Type *> *)(yyvsp[0].otype);
                                if(!vt->empty()) {
                                TestTypeTree()(vt);
                                KeyList * kl = container->getModificableParameters();
                                KeyList::iterator i,e;
                                e = kl->end();
                                for(i=kl->begin() + contador;i!=e;i++)
                                {
                                        if(parser_api->termtable->isVariable(*i)){
                                        if(!parser_api->termtable->getVariable(*i)->specializeTypes(vt)){
                                                snprintf(parerr,256,"Unable to specialize the type(s) for variable `%s'.",parser_api->termtable->getVariable(*i)->getName());
                                                yyerror(parerr);
                                        }
                                        }
                                }
                                }
                                delete vt;
                                contador = container->getModificableParameters()->size();
                                }
                                else if(!(yyvsp[0].otype)) {
                                        snprintf(parerr,256,"Type expected after `-'.");
                                        yywarning(parerr);
                                }
                                }
#line 4488 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 215:
#line 2257 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if(!container)
                                *errflow << "(mensaje recordatorio) (-- Aqui deber�a haber un container --)" << endl;
                                if(container){
                                container->addParameter(make_pair(-1,(yyvsp[0].type_number)));
                                contador = container->getModificableParameters()->size() +1;
                                }
                                }
#line 4501 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 216:
#line 2268 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.type_number)=(yyvsp[0].type_number);}
#line 4507 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 217:
#line 2270 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.type_number)=(yyvsp[0].type_number);}
#line 4513 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 218:
#line 2273 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_string) = (yyvsp[0].type_string);
                                }
#line 4521 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 219:
#line 2277 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_string) =(yyvsp[0].type_string);
                                }
#line 4529 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 220:
#line 2281 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_string) = (yyvsp[0].type_string);
                                }
#line 4537 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 221:
#line 2285 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_string) = (yyvsp[0].type_string);
                                }
#line 4545 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 222:
#line 2291 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                  // miramos si la variable se define en un contexto en concreto
                                  // para dar el mismo identificador, por ejemplo en el literal
                                  // (l ?x ?y ?x) en el contexto del literal las dos variables ?x
                                  // que aparecen tienen el mismo identificador. Esto sirve para
                                  // que cuando cambie el valor de una de las ?x se cambien todas.
                                  static pkey id;
                                  id.first=-1;
                                  id.second=0;

                                  if(context){
                                      ldictionaryit posit = context->find((yyvsp[0].type_string));

                                      if(posit==context->end()){
                                          // no se encontr� ninguna variable igual en el contexto
                                          // se crea una nueva
                                          VariableSymbol * v = new VariableSymbol(-1,parser_api->domain->metainfo.size());
                                          Meta * mt = new Meta((yyvsp[0].type_string),lexer->getLineNumber(),parser_api->fileid);
                                          id = parser_api->termtable->addVariable(v);
                                          parser_api->domain->metainfo.push_back(mt);
                                          context->insert(make_pair(parser_api->termtable->getVariable(id)->getName(),id.first));
                                      }
                                      else {
                                          id.first=(*posit).second;
                                      }
                                  }
                                  else {
                                       VariableSymbol * v = new VariableSymbol(-1,parser_api->domain->metainfo.size());
                                       Meta * mt = new Meta((yyvsp[0].type_string),lexer->getLineNumber(),parser_api->fileid);
                                       id = parser_api->termtable->addVariable(v);
                                       parser_api->domain->metainfo.push_back(mt);
                                  }
                                  // devolvemos la variable
                                  (yyval.termtype) = &id;
                                }
#line 4585 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 223:
#line 2329 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg = (ComparationGoal *) (yyvsp[-3].otype);
                                Evaluable * first, * second;
                                first = (Evaluable *) (yyvsp[-2].otype);
                                second = (Evaluable *) (yyvsp[-1].otype);
                                cg->setFirst(first);
                                cg->setSecond(second);
                                (yyval.otype) = cg;
                                }
#line 4599 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 224:
#line 2341 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg =  new ComparationGoal();
                                cg->setComparator(CGREATHER);
                                (yyval.otype) = cg;
                                }
#line 4609 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 225:
#line 2347 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg =  new ComparationGoal();
                                cg->setComparator(CLESS);
                                (yyval.otype) = cg;
                                }
#line 4619 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 226:
#line 2353 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg =  new ComparationGoal();
                                cg->setComparator(CEQUAL);
                                (yyval.otype) = cg;
                                }
#line 4629 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 227:
#line 2359 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg =  new ComparationGoal();
                                cg->setComparator(CGREATHER_EQUAL);
                                (yyval.otype) = cg;
                                }
#line 4639 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 228:
#line 2365 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg =  new ComparationGoal();
                                cg->setComparator(CLESS_EQUAL);
                                (yyval.otype) = cg;
                                }
#line 4649 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 229:
#line 2371 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ComparationGoal * cg =  new ComparationGoal();
                                cg->setComparator(CDISTINCT);
                                (yyval.otype) = cg;
                                }
#line 4659 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 230:
#line 2379 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentNumber * f = new FluentNumber((yyvsp[0].type_number));
                                isNumber = true;
                                (yyval.otype) = f;
                                }
#line 4669 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 231:
#line 2385 "yacc/parser.yy" /* yacc.c:1646  */
    { FluentOperator * fo = (FluentOperator *) (yyvsp[-3].otype);
                                Evaluable * first, * second;
                                first = (Evaluable *) (yyvsp[-2].otype);
                                second = (Evaluable *) (yyvsp[-1].otype);
                                const Type * number = parser_api->domain->getType("number");
                                if(!first->isType(number)) {
                                snprintf(parerr,256,"Operand `%s' is not of number type.",first->toStringEvaluable());
                                yyerror(parerr);
                                }
                                if(!second->isType(number)) {
                                snprintf(parerr,256,"Operand `%s' is not of number type.",second->toStringEvaluable());
                                yyerror(parerr);
                                }
                                fo->setFirst(first);
                                fo->setSecond(second);
                                (yyval.otype) = fo;
                                }
#line 4691 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 232:
#line 2403 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentOperator * fo = new FluentOperator((Operation)(yyvsp[-3].type_int));
                                Evaluable * first, * second;
                                first = (Evaluable *) (yyvsp[-2].otype);
                                second = (Evaluable *) (yyvsp[-1].otype);
                                const Type * number = parser_api->domain->getType("number");
                                if(!first->isType(number)) {
                                        snprintf(parerr,256,"Operand `%s' is not of number type.",first->toStringEvaluable());
                                        yyerror(parerr);
                                }
                                if(second)
                                        if(!second->isType(number)) {
                                        snprintf(parerr,256,"Operand `%s' is not of number type.",second->toStringEvaluable());
                                        yyerror(parerr);
                                        }
                                fo->setFirst(first);
                                if(second)
                                        fo->setSecond(second);
                                if(second && (yyvsp[-3].type_int) != OSUBSTRACT) {
                                        snprintf(parerr,256,"Using two arguments in a operator that only needs one: %s.",fo->toStringEvaluable());
                                        yyerror(parerr);
                                }
                                (yyval.otype) = fo;
                                }
#line 4720 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 233:
#line 2428 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = (FluentLiteral *) (yyvsp[0].otype);
                                }
#line 4728 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 234:
#line 2432 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentVar * v = new FluentVar((yyvsp[0].termtype));
                                // comprobar que la variable sea de tipo number
                                if(!v->isType(parser_api->domain->getType("number"))){
                                        // Dar warning si es objeto.
                                        if(v->isObjectType()) {
                                        parser_api->termtable->getVariable(v->getId())->specializeTypes(parser_api->domain->getModificableType("number"));
                                        snprintf(parerr,256,"Seting type of `%s' to number.",parser_api->termtable->getVariable(v->getId())->getName());
                                        yywarning(parerr);
                                        }
                                        else
                                        parser_api->termtable->getVariable(v->getId())->specializeTypes(parser_api->domain->getModificableType("number"));
                                }
                                (yyval.otype) = v;
                                }
#line 4748 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 235:
#line 2448 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * c = (string *) (yyvsp[0].otype);
                                FluentConstant * f;
                                ldictionaryit posit = (parser_api->domain->cdictionary).find(c->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                        // devolver el pkey de la constante
                                        f = new FluentConstant(make_pair((*posit).second, 0));
                                }
                                else {
                                    snprintf(parerr,256,"Undefined constant `%s'.",c->c_str());
                                    yyerror(parerr);
                                    ConstantSymbol * n = new ConstantSymbol(c->c_str(),-1);
                                    n->setLineNumber(lexer->getLineNumber());
                                    n->setFileId(parser_api->fileid);
                                    f = new FluentConstant(parser_api->termtable->addConstant(n));
                                }
                                delete c;
                                (yyval.otype) = f;
                                }
#line 4772 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 236:
#line 2470 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=0;}
#line 4778 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 237:
#line 2472 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=(yyvsp[0].otype);}
#line 4784 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 238:
#line 2476 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.type_int)=(int)OSUBSTRACT;}
#line 4790 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 239:
#line 2478 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.type_int)=(int)UABS;}
#line 4796 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 240:
#line 2480 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.type_int)=(int)USQRT;}
#line 4802 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 241:
#line 2484 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentOperator * fo = new FluentOperator(OADD);
                                (yyval.otype) = fo;
                                }
#line 4811 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 242:
#line 2489 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentOperator * fo = new FluentOperator(OTIMES);
                                (yyval.otype) = fo;
                                }
#line 4820 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 243:
#line 2494 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentOperator * fo = new FluentOperator(ODIVIDE);
                                (yyval.otype) = fo;
                                }
#line 4829 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 244:
#line 2499 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentOperator * fo = new FluentOperator(OPOW);
                                (yyval.otype) = fo;
                                }
#line 4838 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 245:
#line 2569 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                Function * lit=0;
                                Meta * mt = 0;
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),(const char *) nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                        lit = new Function(posit->second,parser_api->domain->metainfo.size(),false,0);
                                        mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                lit = new Function(idCounter++,parser_api->domain->metainfo.size(),false,0);
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                contador=0;
                                }
#line 4864 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 246:
#line 2591 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Function * lit= (Function *) container;
                                container = 0;
                                // comprobaciones de correctitud
                                // busco en el dominio los literales con el nombre capturado
                                  // y el n�mero de argumentos adecuado
                                  // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool unificacion=false;
                                vector<Literal *> candidates;
                                vector<Literal *>::const_iterator j;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++)
                                  {
                                candidates.push_back((*i).second);
                                     Unifier u;
                                     if(unify3(lit->getParameters(),(*i).second->getParameters(),&u)){
                                        u.applyTypeSubstitutions(0);
                                        //if(((Function *)(*i).second)->isPython()){
                                        //    lit->setPython();
                                        //    lit->setCode(((Function *)(*i).second)->getCode());
                                        //}
                                        unificacion=true;
                                     }
                                  }
                                if(!unificacion){
                                        snprintf(parerr,256,"(5) No matching predicate for `%s'.",lit->toString());
                                        yyerror(parerr);
                                        if(candidates.size() > 0) {
                                        *errflow << "Possible candidates:" << endl;
                                          for(j=candidates.begin();j!=candidates.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                             *errflow << "\t[" << sli.fileName << "]:" << sli.lineNumber;
                                        (*j)->printL(errflow,1);
                                        *errflow << endl;
                                          }
                                        }
                                }
                                (yyval.otype) = lit;
                                }
#line 4909 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 247:
#line 2687 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                FluentLiteral * lit=0;
                                Meta * mt = 0;
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),(const char *) nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                        lit = new FluentLiteral(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                lit = new FluentLiteral(idCounter++,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                contador = 0;
                                }
#line 4935 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 248:
#line 2709 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentLiteral * lit= (FluentLiteral *) container;
                                container = 0;
                                // comprobaciones de correctitud
                                // busco en el dominio los literales con el nombre capturado
                                // y el n�mero de argumentos adecuado
                                // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool unificacion=false;
                                vector<Literal *> candidates;
                                vector<Literal *>::const_iterator j;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++)
                                  {
                                candidates.push_back((*i).second);
                                     Unifier u;
                                     if(unify3(lit->getParameters(),(*i).second->getParameters(),&u)){
                                        u.applyTypeSubstitutions(0);
                                        unificacion=true;
                                     }
                                  }
                                if(!unificacion){
                                        snprintf(parerr,256,"(7) No matching predicate for `%s'.",lit->toString());
                                        yyerror(parerr);
                                        if(candidates.size() > 0) {
                                        *errflow << "Possible candidates:" << endl;
                                          for(j=candidates.begin();j!=candidates.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                             *errflow << "\t[" << sli.fileName << "]:" << sli.lineNumber;
                                        (*j)->printL(errflow,1);
                                        *errflow << endl;
                                          }
                                        }
                                }
                                (yyval.otype) = lit;
                                }
#line 4976 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 249:
#line 2749 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) = 0;}
#line 4982 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 250:
#line 2751 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) =(yyvsp[0].otype);}
#line 4988 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 251:
#line 2755 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=0;}
#line 4994 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 252:
#line 2757 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                AndEffect * ae = new AndEffect();
                                econtainer.push_back(ae);
                                }
#line 5003 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 253:
#line 2762 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                AndEffect * ae = (AndEffect *) econtainer.back();
                                econtainer.pop_back();
                                (yyval.otype) = ae;
                                }
#line 5013 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 254:
#line 2768 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype)= (yyvsp[0].otype);}
#line 5019 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 255:
#line 2772 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Effect * e = (Effect *) (yyvsp[-1].otype);
                                Evaluable * ti = (Evaluable *) (yyvsp[-2].otype);
                                if(e->isLiteralEffect()){
                                        LiteralEffect * le = ((LiteralEffect *)e);
                                        le->setTime(ti);
                                }
                                else{
                                        ((FluentEffect *)e)->setTime(ti);
                                }
                                    if(!parser_api->domain->errdurative && !parser_api->domain->hasRequirement(":durative-actions"))
                                    {
                                        parser_api->domain->errdurative = true;
                                        yyerror("Using a clause that requires `:durative-actions' and is not declared in requirements clause");
                                    }
                                    if(!isDurative)
                                    {
                                        yyerror("Using a durative effect inside a non durative action.");
                                    }
                                (yyval.otype) = e;
                                }
#line 5045 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 256:
#line 2797 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                // creamos el forall, y lo ponemos como
                                // el elemento que va a contener a las variables
                                ForallEffect * fae = new ForallEffect();
                                container = fae;
                                (yyval.otype) = fae;
                                }
#line 5057 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 257:
#line 2805 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                container = 0;
                                }
#line 5065 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 258:
#line 2810 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                ForallEffect * fae = (ForallEffect *) (yyvsp[-6].otype);
                                Effect * e = (Effect *) (yyvsp[-1].otype);
                                fae->setEffect(e);
                                    if(!parser_api->domain->errconditionals && !parser_api->domain->hasRequirement(":conditional-effects"))
                                    {
                                        parser_api->domain->errconditionals = true;
                                        yyerror("Using a clause that requires `:conditional-effects' and is not declared in requirements clause");
                                    }
                                (yyval.otype) = fae;
                                }
#line 5081 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 259:
#line 2822 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                WhenEffect * we = new WhenEffect((Goal *)(yyvsp[-2].otype),(Effect *)(yyvsp[-1].otype));
                                    if(!parser_api->domain->errconditionals && !parser_api->domain->hasRequirement(":conditional-effects"))
                                    {
                                        parser_api->domain->errconditionals = true;
                                        yyerror("Using a clause that requires `:conditional-effects' and is not declared in requirements clause");
                                    }
                                (yyval.otype) = we;
                                }
#line 5095 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 260:
#line 2832 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) = (yyvsp[0].otype);}
#line 5101 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 261:
#line 2834 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype)= (yyvsp[0].otype);}
#line 5107 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 263:
#line 2839 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if((yyvsp[0].otype)){
                                ContainerEffect * lc = (ContainerEffect *) econtainer.back();
                                lc->addEffectByRef((Effect *) (yyvsp[0].otype));
                                }
                                }
#line 5118 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 264:
#line 2848 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                FluentEffect * fe = new FluentEffect((FOperation)(yyvsp[-3].type_int),(FluentLiteral *)(yyvsp[-2].otype),(Evaluable *)(yyvsp[-1].otype));
                                    if(!parser_api->domain->errfluents && !parser_api->domain->hasRequirement(":fluents"))
                                    {
                                        parser_api->domain->errfluents = true;
                                        yyerror("Using a clause that requires `:fluents' and is not declared in requirements clause");
                                    }
                                (yyval.otype) = fe;
                                }
#line 5132 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 265:
#line 2858 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralEffect * le = (LiteralEffect *) (yyvsp[-1].otype);
                                if(le->getPolarity())
                                        le->setPolarity(false);
                                (yyval.otype)=le;
                                }
#line 5143 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 266:
#line 2865 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype)=(yyvsp[0].otype);}
#line 5149 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 268:
#line 2870 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if((yyvsp[0].otype)){
                                ContainerEffect * lc = (ContainerEffect *) econtainer.back();
                                lc->addEffectByRef((Effect *) (yyvsp[0].otype));
                                }
                                }
#line 5160 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 269:
#line 2879 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                AndEffect * ae = new AndEffect();
                                econtainer.push_back(ae);
                                }
#line 5169 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 270:
#line 2884 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                AndEffect * ae = (AndEffect *) econtainer.back();
                                econtainer.pop_back();
                                (yyval.otype) = ae;
                                }
#line 5179 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 271:
#line 2890 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) = (yyvsp[0].otype);}
#line 5185 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 272:
#line 2894 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = (int) FASSIGN;
                                }
#line 5193 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 273:
#line 2898 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = (int) FSCALEUP;
                                }
#line 5201 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 274:
#line 2902 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = (int) FSCALEDOWN;
                                }
#line 5209 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 275:
#line 2906 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = (int) FINCREASE;
                                }
#line 5217 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 276:
#line 2910 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_int) = (int) FDECREASE;
                                }
#line 5225 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 285:
#line 2931 "yacc/parser.yy" /* yacc.c:1646  */
    {context = new LDictionary;}
#line 5231 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 286:
#line 2931 "yacc/parser.yy" /* yacc.c:1646  */
    {delete context; context=0;}
#line 5237 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 289:
#line 2953 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                parser_api->problem->addToInitialState((LiteralEffect *)(yyvsp[0].otype));
                                //parser_api->problem->getInitialContext()->stateChanges.push_back(new UndoARLiteralState((Literal *)$1,true));
                                }
#line 5246 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 290:
#line 2958 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Function * f = (Function *) (yyvsp[-2].otype);
                                f->setValue((yyvsp[-1].type_number));
                                parser_api->problem->addToInitialState(f);
                                //parser_api->problem->getInitialContext()->stateChanges.push_back(new UndoARLiteralState(f,true));
                                if(!parser_api->domain->errfluents && !parser_api->domain->hasRequirement(":fluents"))
                                    {
                                        parser_api->domain->errfluents = true;
                                        yyerror("Using a clause that requires `:fluents' and is not declared in requirements clause");
                                    }
                                }
#line 5262 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 291:
#line 2969 "yacc/parser.yy" /* yacc.c:1646  */
    {isNumber = false;}
#line 5268 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 292:
#line 2970 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                /* Comprobar que la expresi�n dada por el time specifier
                                * es un n�mero */
                                Evaluable * n = (Evaluable *) (yyvsp[-2].otype);
                                LiteralEffect * l = (LiteralEffect *) (yyvsp[-1].otype);
                                if(!isNumber){
                                        snprintf(parerr,256,"Expecting a number in time initialization: `%s'",l->getName());
                                        yyerror(parerr);
                                }
                                else {
                                        l->setTime(n);
                                }
                                    /*requires timed-initial-literals */
                                if(!parser_api->domain->errdurative && !parser_api->domain->hasRequirement(":durative-actions"))
                                {
                                        parser_api->domain->errdurative = true;
                                        yyerror("Using a clause that requires `:timed-initial-literals' and is not declared in requirements clause");
                                }
                                parser_api->problem->addToInitialState(l);
                                //parser_api->problem->getInitialContext()->stateChanges.push_back(new UndoARLiteralState(l,true));
                                }
#line 5294 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 293:
#line 2996 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralEffect * l = (LiteralEffect *) (yyvsp[-1].otype);
                                TimeLineLiteralEffect * tl = new TimeLineLiteralEffect(l->getId(),l->getMetaId(),l->getParameters(),l->getPolarity());
                                delete l;
                                if(!parser_api->domain->errdurative && !parser_api->domain->hasRequirement(":durative-actions"))
                                {
                                        parser_api->domain->errdurative = true;
                                        yyerror("Using a clause that requires `:timed-initial-literals' and is not declared in requirements clause");
                                }
                                tl->setInterval((int)(yyvsp[-5].type_number),(int)(yyvsp[-3].type_number));
                                tl->setGap((int)(yyvsp[-2].type_number));
                                parser_api->problem->addToInitialState(tl);
                                //parser_api->problem->getInitialContext()->stateChanges.push_back(new UndoARLiteralState(tl,true));
                                (yyval.otype) = 0;
                                }
#line 5314 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 294:
#line 3014 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if((yyvsp[0].type_number) < 0){
                                        yyerror("Expecting a positive number.");
                                        (yyval.type_number) = 0;
                                }
                                else
                                        (yyval.type_number) = (yyvsp[0].type_number);
                                }
#line 5327 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 295:
#line 3023 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = 0;
                                }
#line 5335 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 298:
#line 3033 "yacc/parser.yy" /* yacc.c:1646  */
    { *errflow << "Los goal 'planos' de pddl no est�n soportados." << endl;}
#line 5341 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 299:
#line 3039 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                parser_api->problem->setInitialGoal((TaskNetwork *)(yyvsp[-1].otype));
                                   if(!parser_api->domain->errhtn && !parser_api->domain->hasRequirement(":htn-expansion"))
                                   {
                                        parser_api->domain->errhtn = true;
                                        yyerror("Using a clause that requires `:htn-expansion' that is not declared in requirements clause");
                                   }
                                if((yyvsp[-3].otype)){
                                TagVector * tv = (TagVector *) (yyvsp[-3].otype);
                                tagv_ite tb, te = tv->end();
                                for(tb = tv->begin();tb!=te;tb++)
                                        parser_api->problem->meta.addTag((*tb));
                                tv->clear();
                                delete tv;
                                }

                                // verificar que todos los objetivos expuestos en
                                // la red de tareas son alcanzables.
                                bool changes=true;
                                while(changes){
                                changes = false;
                                if(!((TaskNetwork *) (yyvsp[-1].otype))->isWellDefined(errflow,&changes))
                                {
                                        snprintf(parerr,256,"In the task network of goal specification.");
                                        yyerror(parerr);
                                }
                                }

                                }
#line 5375 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 300:
#line 3071 "yacc/parser.yy" /* yacc.c:1646  */
    {(yyval.otype) = (LiteralEffect *) (yyvsp[0].otype);}
#line 5381 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 301:
#line 3073 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralEffect * lit = (LiteralEffect *) (yyvsp[-1].otype);
                                lit->setPolarity(false);
                                (yyval.otype) = lit;
                                }
#line 5391 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 302:
#line 3081 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                LiteralEffect * lit=0;
                                Meta * mt = 0;
                                // buscamos si el literal ya est� definido en el diccionario de
                                // nombres de literales (deber�a estarlo)
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                lit = new LiteralEffect(posit->second,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                lit = new LiteralEffect(idCounter++,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                contador = 0;
                                }
#line 5419 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 303:
#line 3105 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralEffect * lit= (LiteralEffect *) container;
                                container = 0;
                                // comprobaciones de correctitud
                                // busco en el dominio los literales con el nombre capturado
                                  // y el n�mero de argumentos adecuado
                                  // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool unificacion=false;
                                vector<Literal *> candidates;
                                vector<Literal *>::const_iterator j;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++)
                                  {
                                candidates.push_back((*i).second);
                                     if(unify(lit->getParameters(),(*i).second->getParameters())){
                                        unificacion=true;
                                     }
                                  }
                                if(!unificacion){
                                        snprintf(parerr,256,"(8) No matching predicate for `%s'.",lit->toString());
                                        yyerror(parerr);
                                        if(candidates.size() > 0) {
                                        *errflow << "Possible candidates:" << endl;
                                          for(j=candidates.begin();j!=candidates.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                             *errflow << "\t[" << sli.fileName << "]:" << sli.lineNumber;
                                        (*j)->printL(errflow,1);
                                        *errflow << endl;
                                          }
                                        }
                                }
                                (yyval.otype) = lit;
                                }
#line 5458 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 304:
#line 3143 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                context = new LDictionary;
                                string * name = (string *) (yyvsp[0].otype);
                                PrimitiveTask * priTask=0;
                                Meta * mt = 0;
                                isDurative = true;
                                // buscamos en el diccionario si la acci�n ya tiene un identificador
                                // asociado, en cuyo caso lo reutilizamos
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),name->c_str());
                                      if(posit != (parser_api->domain->ldictionary).end()) {
                                        priTask = new PrimitiveTask(posit->second,parser_api->domain->metainfo.size());
                                        mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                }
                                      else
                                      {
                                        priTask = new PrimitiveTask(idCounter++,parser_api->domain->metainfo.size());
                                        mt = new Meta(name->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                        parser_api->domain->metainfo.push_back(mt);
                                          (parser_api->domain->ldictionary).insert(make_pair(priTask->getName(),priTask->getId()));
                                      }
                                container = priTask;
                                delete name;
                                (yyval.otype) = priTask;
                                }
#line 5488 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 305:
#line 3170 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                    container = 0;
                                    // si hay alg�n tag
                                    if((yyvsp[0].otype)){
                                        TagVector * tv = (TagVector *) (yyvsp[0].otype);
                                        tagv_ite tb, te = tv->end();
                                        int mid = ((PrimitiveTask *) (yyvsp[-5].otype))->getMetaId();
                                        for(tb = tv->begin();tb!=te;tb++){
                                                parser_api->domain->metainfo[mid]->addTag(*tb);
                                        }
                                        tv->clear();
                                        delete tv;
                                    }
                                }
#line 5507 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 306:
#line 3185 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                 if((yyvsp[0].otype)){
                                     ((PrimitiveTask *) (yyvsp[-8].otype))->setTConstraints((vector<TCTR> *) (yyvsp[0].otype));
                                 }
                                }
#line 5517 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 307:
#line 3193 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                 isDurative = false;
                                 PrimitiveTask * priTask= (PrimitiveTask *) (yyvsp[-14].otype);
                                 priTask->setPrecondition((Goal *) (yyvsp[-3].otype));
                                 priTask->setEffect((Effect *) (yyvsp[-1].otype));
                                 parser_api->domain->addTask(priTask);
                                 delete context;
                                 context = 0;
                                 if(!parser_api->domain->errdurative && !parser_api->domain->hasRequirement(":durative-actions")){
                                     parser_api->domain->errdurative = true;
                                     yyerror("Using a clause that requires `:durative-actions' and is not declared in requirements clause");
                                 }
                                }
#line 5535 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 308:
#line 3207 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<pair<int,Evaluable *> > * v = new vector<pair<int,Evaluable *> >;
                                v->push_back(*((pair<int,Evaluable *> *) (yyvsp[0].otype)));
                                (yyval.otype)= v;
                                }
#line 5545 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 309:
#line 3213 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                vector<pair<int,Evaluable *> > * v = (vector<pair<int,Evaluable *> > *) (yyvsp[-1].otype);
                                v->push_back(*((pair<int,Evaluable *> *) (yyvsp[0].otype)));
                                (yyval.otype)= v;
                                }
#line 5555 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 310:
#line 3221 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                 vector<TCTR> * v = new vector<TCTR>;
                                 TCTR * ele = (TCTR *) (yyvsp[0].otype);
                                 v->push_back(*ele);
                                 (yyval.otype)= v;
                                }
#line 5566 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 311:
#line 3228 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                 vector<TCTR> * v = (vector<TCTR> *) (yyvsp[-1].otype);
                                 (yyval.otype)= v;
                                }
#line 5575 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 312:
#line 3233 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                 vector<TCTR> * v = new vector<TCTR>;
                                 (yyval.otype)= v;
                                }
#line 5584 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 313:
#line 3239 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                TimeInterval * ti = new TimeInterval();
                                ti->setStart((Evaluable *)(yyvsp[0].otype));
                                (yyval.otype) = ti;
                                }
#line 5594 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 314:
#line 3245 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                TimeInterval * ti = new TimeInterval();
                                ti->setStart((double)ATSTART);
                                ti->setEnd((double)ATEND);
                                (yyval.otype) = ti;
                                }
#line 5605 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 315:
#line 3252 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                TimeInterval * ti = new TimeInterval();
                                ti->setStart((Evaluable *)(yyvsp[-2].otype));
                                ti->setEnd((Evaluable *)(yyvsp[0].otype));
                                (yyval.otype) = ti;
                                isNumber = false;
                                }
#line 5617 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 316:
#line 3262 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new FluentNumber((double)ATSTART);
                                }
#line 5625 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 317:
#line 3266 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new FluentNumber((double)ATEND);
                                }
#line 5633 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 318:
#line 3270 "yacc/parser.yy" /* yacc.c:1646  */
    { (yyval.otype) = (yyvsp[0].otype);}
#line 5639 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 319:
#line 3273 "yacc/parser.yy" /* yacc.c:1646  */
    {AtExpected = true;}
#line 5645 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 320:
#line 3273 "yacc/parser.yy" /* yacc.c:1646  */
    {AtExpected = false;}
#line 5651 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 321:
#line 3274 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                Evaluable * c = (Evaluable *) (yyvsp[0].otype);
                                const Type * number = parser_api->domain->getType("number");
                                if(!c->isType(number)) {
                                snprintf(parerr,256,"Expression `%s' is not numeric.",c->toStringEvaluable());
                                yyerror(parerr);
                                }
                                (yyval.otype) = c;
                                }
#line 5665 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 322:
#line 3286 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                context = new LDictionary;
                                }
#line 5673 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 323:
#line 3290 "yacc/parser.yy" /* yacc.c:1646  */
    {

                                delete context;
                                context = 0;
                                }
#line 5683 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 324:
#line 3298 "yacc/parser.yy" /* yacc.c:1646  */
    {

                                if((yyvsp[-1].otype))
                                {
                                        Axiom * a = (Axiom *) (yyvsp[-1].otype);
                                        if((yyvsp[0].otype))
                                        a->setGoal((Goal *)(yyvsp[0].otype));
                                }
                                else
                                {
                                        if((yyvsp[0].otype))
                                        delete (Goal *) (yyvsp[0].otype);
                                }
                                }
#line 5702 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 325:
#line 3313 "yacc/parser.yy" /* yacc.c:1646  */
    {

                                if((yyvsp[-1].otype))
                                {
                                        Axiom * a = (Axiom *) (yyvsp[-1].otype);
                                        if((yyvsp[0].type_string)){
                                        if(!a->setCode((yyvsp[0].type_string))){
                                                snprintf(parerr,256,"Error in Python script code. Axiom: %s.",a->getName());
                                                yyerror(parerr);
                                        }
                                        }
                                }
                                }
#line 5720 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 326:
#line 3330 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true;}
#line 5726 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 327:
#line 3330 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;}
#line 5732 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 328:
#line 3331 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                YYACCEPT;
                        }
#line 5740 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 329:
#line 3335 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                YYABORT;
                        }
#line 5748 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 330:
#line 3341 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                exit(EXIT_SUCCESS);
                            }
#line 5756 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 332:
#line 3346 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->cont = true;
                            }
#line 5764 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 342:
#line 3359 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->next = true;
                            }
#line 5772 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 343:
#line 3363 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->nexp = true;
                            }
#line 5780 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 344:
#line 3367 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                struct mallinfo myinfo=mallinfo();
                                cerr << "Memory allocated (bytes): " << myinfo.hblkhd << " Memory chunks occupied: " << myinfo.uordblks << endl;
                            }
#line 5789 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 345:
#line 3372 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->select((int)(yyvsp[0].type_number));
                            }
#line 5797 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 346:
#line 3376 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                current_plan->FLAG_VERBOSE = 1;
                            }
#line 5805 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 347:
#line 3380 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                current_plan->FLAG_VERBOSE = 0;
                            }
#line 5813 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 348:
#line 3386 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Type `help <command>' to obtain detailed information about a command." << endl;
                                cerr << "Avaliable commands:" <<endl;
                                cerr << "print          display        quit           plot"<<endl;
                                cerr << "continue       undisplay      next           set" <<endl;
                                cerr << "describe       break          disable        enable"<<endl;
                                cerr << "nexp           eval           watch          apply"<<endl;
                                cerr << "<enter> executes the last command." << endl;
                            }
#line 5827 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 349:
#line 3396 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `continue'. Shortcut: `c'" << endl << endl;
                                cerr << "Description: Continues the execution until a breakpoint or the end of the program is reached." << endl;
                                cerr << "See also: `next'" << endl;
                            }
#line 5837 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 350:
#line 3402 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `quit' or `exit'" << endl << endl;
                                cerr << "Description: Terminates the program execution." << endl;
                            }
#line 5846 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 351:
#line 3407 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `print'. Shortcut: `p'" << endl << endl;
                                cerr << "Description: Prints information about the planning context." << endl;
                                cerr << "\t`print state':\tPrints the current state." << endl;
                                cerr << "\t`print agenda':\tPrints the current agenda." << endl;
                                cerr << "\t`print plan':\tPrints the ongoing plan." << endl;
                                cerr << "\t`print options':\tPrints the options you can peform on next step." << endl;
                                cerr << "\t`print termtable':\tPrints the internal term table." << endl;
                                cerr << "\t`print tasks':\tPrints all the tasks defined in the domain." << endl;
                                cerr << "\t`print predicates':\tPrints all the avaliable predicates defined in the domain." << endl;
                                cerr << "\t`print <predicate-expression>':\tPrints all the predicates in the current state, or the tasks in current plan, that match the given expression." << endl;
                            }
#line 5863 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 352:
#line 3420 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `display'. Shortcut `d'." << endl << endl;
                                cerr << "Description: Display information about the current planning context every step until is undisplayed." << endl;
                                cerr << "\t`display':\tShows information about the current displays." << endl;
                                cerr << "\t`display <number>':\tActivates the display of given number." << endl;
                                cerr << "\t`display state':\tDisplays the current state." << endl;
                                cerr << "\t`display agenda':\tDisplays the current agenda." << endl;
                                cerr << "\t`display plan':\tDisplays the ongoing plan." << endl;
                                cerr << "\t`display termtable':\tDisplays the internal term table." << endl;
                                cerr << "\t`display <predicate-expression>':\tDisplays all the predicates in the current state, or the tasks in current plan, that match the given expression." << endl;
                                cerr << "See also: `print', `undisplay'" << endl;
                            }
#line 5880 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 353:
#line 3433 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `undisplay <number>'." << endl << endl;
                                cerr << "Description: Deactivates the display of given number." << endl;
                        }
#line 5889 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 354:
#line 3438 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `next'. ShortCut: `n'" << endl << endl;
                                cerr << "Description: Advance one more step." << endl;
                                cerr << "See also: `continue'" << endl;
                        }
#line 5899 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 355:
#line 3444 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `nexp' (next expansion). ShortCut: `ne'" << endl << endl;
                                cerr << "Description: Advance until a new task is chosen." << endl;
                                cerr << "See also: `continue', `next'" << endl;
                        }
#line 5909 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 356:
#line 3450 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `plot'." << endl << endl;
                                cerr << "Description: Graphically shows information about the current plan." << endl;
                                cerr << "You need to have installed the 'dot' program avaliable at http://www.graphviz.org." << endl;
                                cerr << "You also need to correct set up some environment variables." << endl;
                                cerr << "\t`plot plan':\tShows the current plan graph." << endl;
                                cerr << "\t`plot causal':\tShows the graph of the causal link structure in the plan." << endl;
                                cerr << "See also: `set'" << endl;
                        }
#line 5923 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 357:
#line 3460 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `set'." << endl << endl;
                                cerr << "Description: Sets some environment variables." << endl;
                                cerr << "\t`set <variable>':\tShows the current value of the given variable." << endl;
                                cerr << "\t`set <variable> = <value>':\tSets a new value for the given variable." << endl;
                                cerr << "\tAvaliable variables:" << endl;
                                cerr << "\t\t`verbosity: Level of verbosity (0=nothing,1=shy,2=normal(default),3=promiscuous)." << endl;
                                cerr << "\t\t`viewer: Path to a program able to display png format images." << endl;
                                cerr << "\t\t`tmpdir: Directory to store temporary information." << endl;
                                cerr << "\t\t`dotpath: Path to the dot program." << endl;
                                cerr << "See also: `plot'" << endl;
                        }
#line 5940 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 358:
#line 3473 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `describe'." << endl << endl;
                                cerr << "Description: Shows detailed information about a structure defined in the domain." << endl;
                                cerr << "\t`describe <predicate-expression>':\tPrint the description in the domain relative to the predicate expression. It can be a predicate or a task." << endl;
                                cerr << "See also: `print', `display'" << endl;
                            }
#line 5951 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 359:
#line 3480 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `enable <number>'." << endl << endl;
                                cerr << "Description: Reactivates a previously disabled breakpoint or watch." << endl;
                                cerr << "<number> is de id of the breakpoint or watch to enable." << endl;
                                cerr << "See also: `break', `watch', `disable'." << endl;
                            }
#line 5962 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 360:
#line 3487 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `disable <number>'." << endl << endl;
                                cerr << "Description: Deactivates a breakpoint or watch." << endl;
                                cerr << "<number> is de id of the breakpoint or watch to disable." << endl;
                                cerr << "See also: `break', `watch', `enable'." << endl;
                            }
#line 5973 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 361:
#line 3494 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `watch <precondition>'. Shortcut `s'" << endl << endl;
                                cerr << "Description: Defines a condition where the debugger will stop." << endl;
                                cerr << "If ithe watch is enabled, the debugger will stop every time the condition produce one or more valid unifications." << endl;
                                cerr << "See also: `break', `disable', `enable'." << endl;
                            }
#line 5984 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 362:
#line 3501 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `break'. Shortcut `b'" << endl << endl;
                                cerr << "Description: Manages the stablished breakpoints." << endl;
                                cerr << "\t`break':\tLists all defined breakpoints." << endl;
                                cerr << "\t`break <number>':\tPrints breakpoint whith given id." << endl;
                                cerr << "\t`break <predicate>':\tDefines a new breakpoint. <predcate> can be a task definition or a simple predicate." << endl;
                                cerr << "See also: `watch', `disable', `enable'." << endl;
                            }
#line 5997 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 363:
#line 3510 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `eval <precondition>'." << endl << endl;
                                cerr << "Description: Evaluates the given expression and prints the produced unifications." << endl;
                            }
#line 6006 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 364:
#line 3515 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << "Command: `apply <effect>'." << endl << endl;
                                cerr << "Description: Applies the given effect." << endl;
                                cerr << "Be cautious with this command is dangerous." << endl;
                                cerr << "See also: `eval'." << endl;
                            }
#line 6017 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 365:
#line 3524 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printState();
                            }
#line 6025 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 366:
#line 3527 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context=new LDictionary();}
#line 6031 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 367:
#line 3527 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true; delete context; context=0;}
#line 6037 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 368:
#line 3528 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralGoal * lg = (LiteralGoal *) (yyvsp[-1].otype);
                                if((yyvsp[-1].otype)){
                                debugger->printLiteral(lg);
                                delete lg;
                                }
                            }
#line 6049 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 369:
#line 3536 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printAgenda();
                            }
#line 6057 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 370:
#line 3540 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printPlan();
                            }
#line 6065 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 371:
#line 3544 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printOptions();
                            }
#line 6073 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 372:
#line 3548 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printTermtable();
                            }
#line 6081 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 373:
#line 3552 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printTasks();
                        }
#line 6089 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 374:
#line 3556 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printPredicates();
                        }
#line 6097 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 375:
#line 3562 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                de->name = "state";
                                debugger->displaySymbol(de);
                            }
#line 6107 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 376:
#line 3567 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context= new LDictionary();}
#line 6113 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 377:
#line 3567 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true; delete context; context=0;}
#line 6119 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 378:
#line 3568 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                if((yyvsp[-1].otype)){
                                de->goal = (LiteralGoal *) (yyvsp[-1].otype);
                                debugger->displaySymbol(de);
                                }
                                else
                                delete de;
                            }
#line 6133 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 379:
#line 3578 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                de->name = "agenda";
                                debugger->displaySymbol(de);
                            }
#line 6143 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 380:
#line 3584 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                de->name = "plan";
                                debugger->displaySymbol(de);
                            }
#line 6153 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 381:
#line 3590 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printDisplays();
                            }
#line 6161 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 382:
#line 3594 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->display((int)(yyvsp[0].type_number));
                            }
#line 6169 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 383:
#line 3598 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                de->name = "termtable";
                                debugger->displaySymbol(de);
                            }
#line 6179 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 384:
#line 3606 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->plotPlan();
                            }
#line 6187 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 385:
#line 3610 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->plotCausal();
                            }
#line 6195 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 386:
#line 3615 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->undisplay((int)(yyvsp[0].type_number));
                            }
#line 6203 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 387:
#line 3622 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << debugger->viewerCommand << endl;
                            }
#line 6211 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 388:
#line 3626 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->viewerCommand = (yyvsp[0].type_string);
                            }
#line 6219 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 389:
#line 3630 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << debugger->tmpdir << endl;
                            }
#line 6227 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 390:
#line 3634 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->tmpdir = (yyvsp[0].type_string);
                            }
#line 6235 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 391:
#line 3638 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << debugger->dotPath << endl;
                            }
#line 6243 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 392:
#line 3642 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->dotPath = (yyvsp[0].type_string);
                            }
#line 6251 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 393:
#line 3646 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                cerr << current_plan->FLAG_VERBOSE << endl;
                        }
#line 6259 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 394:
#line 3650 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if((yyvsp[0].type_number) >= 0 && (yyvsp[0].type_number) <= 3)
                                current_plan->FLAG_VERBOSE = (int) (yyvsp[0].type_number);
                        }
#line 6268 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 395:
#line 3657 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printBreakpoints();
                            }
#line 6276 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 396:
#line 3660 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context= new LDictionary();}
#line 6282 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 397:
#line 3660 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true;delete context; context=0;}
#line 6288 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 398:
#line 3661 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                de->goal = (Goal *) (yyvsp[-1].otype);
                                debugger->setBreakpoint(de);
                            }
#line 6298 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 399:
#line 3667 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->printBreakpoint((int)(yyvsp[0].type_number));
                            }
#line 6306 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 400:
#line 3671 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->enableBreakpoint((int) (yyvsp[0].type_number));
                        }
#line 6314 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 401:
#line 3675 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->disableBreakpoint((int) (yyvsp[0].type_number));
                        }
#line 6322 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 402:
#line 3678 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context= new LDictionary();}
#line 6328 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 403:
#line 3678 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true; delete context; context=0;}
#line 6334 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 404:
#line 3679 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                DisplayElement * de = new DisplayElement();
                                de->goal = (Goal *) (yyvsp[-2].otype);
                                if((yyvsp[-2].otype)){
                                if((yyvsp[-1].otype)){
                                        de->name = *((string *) (yyvsp[-1].otype));
                                        delete (string *) (yyvsp[-1].otype);
                                }
                                debugger->setBreakpoint(de);
                                }
                                else{
                                delete de;
                                }
                        }
#line 6353 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 405:
#line 3696 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = 0;
                        }
#line 6361 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 406:
#line 3700 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.otype) = new string((yyvsp[0].type_string));
                        }
#line 6369 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 407:
#line 3704 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context= new LDictionary();}
#line 6375 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 408:
#line 3704 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true;delete context; context=0;}
#line 6381 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 409:
#line 3705 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->eval((Goal *) (yyvsp[-1].otype));
                                if((yyvsp[-1].otype))
                                delete (Goal *) (yyvsp[-1].otype);
                            }
#line 6391 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 410:
#line 3712 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context= new LDictionary();}
#line 6397 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 411:
#line 3712 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true;delete context; context=0;}
#line 6403 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 412:
#line 3713 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                debugger->apply((Effect *) (yyvsp[-1].otype));
                                if((yyvsp[-1].otype))
                                delete (Effect *) (yyvsp[-1].otype);
                            }
#line 6413 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 413:
#line 3721 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=false;context = new LDictionary();}
#line 6419 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 414:
#line 3721 "yacc/parser.yy" /* yacc.c:1646  */
    {inDebugContext=true; delete context; context=0;}
#line 6425 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 415:
#line 3722 "yacc/parser.yy" /* yacc.c:1646  */
    {

                                DisplayElement * de = new DisplayElement();
                                de->goal = (LiteralGoal *) (yyvsp[-1].otype);
                                if((yyvsp[-1].otype)){
                                debugger->describeSymbol(de);
                                }
                                delete de;
                            }
#line 6439 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 416:
#line 3734 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                string * nameLit = (string *) (yyvsp[0].otype);
                                LiteralGoal * lit=0;
                                Meta * mt = 0;
                                // buscamos si el literal ya est� definido en el diccionario de
                                // nombres de literales (deber�a estarlo)
                                ldictionaryit posit = SearchDictionary(&(parser_api->domain->ldictionary),nameLit->c_str());
                                if(posit != (parser_api->domain->ldictionary).end()) {
                                lit = new LiteralGoal(posit->second,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                }
                                else
                                {
                                snprintf(parerr,256,"Undefined name: `%s'.",nameLit->c_str());
                                yyerror(parerr);
                                lit = new LiteralGoal(idCounter,parser_api->domain->metainfo.size());
                                mt = new Meta(nameLit->c_str(),lexer->getLineNumber(),parser_api->fileid);
                                parser_api->domain->metainfo.push_back(mt);
                                (parser_api->domain->ldictionary).insert(make_pair(lit->getName(), lit->getId()));
                                }
                                container = lit;
                                delete nameLit;
                                contador = 0;
                                }
#line 6469 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 417:
#line 3760 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                LiteralGoal * lit= (LiteralGoal *) container;
                                container = 0;
                                // comprobaciones de correctitud
                                // busco en el dominio los literales con el nombre capturado
                                  // y el n�mero de argumentos adecuado
                                  // Esto sirve para poner los tipos seg�n est�n definidos en la tabla de literales.
                                int id = SearchDictionary(&(parser_api->domain->ldictionary),lit->getName())->second;
                                  LiteralTableRange r = parser_api->domain->getLiteralRange(id);
                                bool unificacion=false;
                                vector<Literal *> candidates;
                                  for(literaltablecit i = r.first; i != r.second && !unificacion; i++)
                                  {
                                candidates.push_back((*i).second);
                                     if(unify((*i).second->getParameters(),lit->getParameters())){
                                        unificacion=true;
                                     }
                                  }
                                  TaskTableRange tr = parser_api->domain->getTaskRange(id);
                                vector<Task *> candidates2;
                                  for(tasktablecit k = tr.first; k != tr.second && !unificacion; k++)
                                  {
                                candidates2.push_back((*k).second);
                                     if(unify((*k).second->getParameters(),lit->getParameters())){
                                        unificacion=true;
                                     }
                                  }
                                if(!unificacion){
                                snprintf(parerr,256,"No matching predicate or action for: `%s'.",lit->toString());
                                yyerror(parerr);
                                if(candidates.size() > 0) {
                                        *errflow << "Possible candidate predicates:" << endl;
                                        vector<Literal *>::const_iterator j;
                                        for(j=candidates.begin();j!=candidates.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                        (*j)->printL(errflow,0);
                                        *errflow << endl;
                                        }
                                }
                                if(candidates2.size() > 0) {
                                        *errflow << "Possible candidate tasks:" << endl;
                                        vector<Task *>::const_iterator j;
                                        for(j=candidates2.begin();j!=candidates2.end();j++) {
                                        SearchLineInfo sli((*j)->getMetaId());
                                        (*j)->printHead(errflow);
                                        *errflow << endl;
                                        }
                                }
                                delete lit;
                                lit = 0;
                                }
                                (yyval.otype) = lit;
                                }
#line 6527 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 423:
#line 3827 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                parser_api->setFlagTUnit((TimeUnit) (yyvsp[-1].type_number));
                                }
#line 6535 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 424:
#line 3831 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                parser_api->setTFormat((yyvsp[-1].type_string));
                                }
#line 6543 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 425:
#line 3835 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                parser_api->setMTHorizon((int) rint((yyvsp[-1].type_number)));
                                }
#line 6551 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 426:
#line 3839 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                parser_api->setRTHorizon((int) rint((yyvsp[-1].type_number)));
                                }
#line 6559 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 427:
#line 3843 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                if(parser_api->getTStart() != 0){
                                        snprintf(parerr,256,":time-start redefinition.");
                                        yyerror(parerr);
                                }
                                parser_api->setTStart((time_t) (yyvsp[-1].type_number));
                                }
#line 6571 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 428:
#line 3852 "yacc/parser.yy" /* yacc.c:1646  */
    {
#ifdef PYTHON_FOUND
                                if(parser_api->wpython.loadStr((yyvsp[-1].type_string))){
                                        yyerror("While parsing :pyinit.");
                                }
#else
                                yyerror("Parser compiled without Python support. Install python and recompile.");
#endif
                                }
#line 6585 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 429:
#line 3863 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = TU_HOURS;
                                }
#line 6593 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 430:
#line 3867 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = TU_MINUTES;
                                }
#line 6601 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 431:
#line 3871 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = TU_SECONDS;
                                }
#line 6609 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 432:
#line 3875 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = TU_DAYS;
                                }
#line 6617 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 433:
#line 3879 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = TU_YEARS;
                                }
#line 6625 "src/parser.cpp" /* yacc.c:1646  */
    break;

  case 434:
#line 3883 "yacc/parser.yy" /* yacc.c:1646  */
    {
                                (yyval.type_number) = TU_MONTHS;
                                }
#line 6633 "src/parser.cpp" /* yacc.c:1646  */
    break;


#line 6637 "src/parser.cpp" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 3887 "yacc/parser.yy" /* yacc.c:1906  */

