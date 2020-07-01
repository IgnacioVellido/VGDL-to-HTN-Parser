/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

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
#line 204 "yacc/parser.yy" /* yacc.c:1909  */

        void * otype;
        const void * cotype;
        const char * type_string;
        double type_number;
        pair<int,float> * termtype;
        int type_int;

#line 213 "src/parser.hpp" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_SRC_PARSER_HPP_INCLUDED  */
