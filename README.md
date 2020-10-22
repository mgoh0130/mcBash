# mcBash
PLEASE EMAIL ME AT michelle.goh@yale.edu IF YOU WOULD LIKE TO SEE MY CODE FOR THIS

/bin/bash (the Bourne Again SHell) performs variable expansion on
the command line.  For example, if the value of the environment variable HWK is
the string "/c/cs323/Hwk3", then the command

  % $HWK/test.mcBash

is expanded to

  % /c/cs323/Hwk3/test.mcBash

More generally, bash performs a large set of variable expansions, including

  Syntax        Action
  ~~~~~~        ~~~~~~
  $NAME         Replace by the value of the environment variable NAME, or by
		the empty string if NAME is not defined.

  ${NAME}       Replace by the value of the environment variable NAME, or by
		the empty string if NAME is not defined.

  ${NAME-WORD}  Replace by the value of NAME, or by the expansion of WORD if
		NAME is not defined.

  ${NAME=WORD}  Replace by the value of the environment variable NAME, or by
		the expansion of WORD if NAME is not defined (in which case
		NAME is immediately assigned the expansion of WORD).

  $0, ..., $9   Replace $D (where D is a decimal digit) by the D-th command
		line argument to mcBash, or by the empty string if there is no
		D-th argument.

  ${N}          Replace by the N-th argument to mcBash, or by the empty string
		if there is no N-th argument.

  $*            Replace by a list of all arguments to mcBash (not including
		$0), separated by single space characters.

where

  * NAME is a maximal sequence of one or more alphanumeric or _ characters that
    begins with an alphabetic or _ character;

  * WORD is any sequence of characters that ends with the first } not escaped
    by a backslash and not part of one of the expansions above; and

  * N is a nonempty sequence of decimal digits.

The expansion of WORD takes place before the substitution so that the search
for substrings to expand proceeds from left to right and continues at the end
of the replacement string after each substitution.

The escape character \ removes any special meaning that is associated with the
following non-null, non-newline character.  This can be used to include $, {,
}, \, and whitespace (but not newlines) in a command.  The \ is not removed.

Collectively these expansions turn one stage in the front-end of bash into a
macroprocessor with a somewhat unusual syntax (e.g., when compared with that of
the C preprocessor /bin/cpp or /bin/m4).

Your task is to implement this stage in Perl or Python or Ruby; i.e., to write
a bash-like macroprocessor "mcBash" that
* prompts for and reads lines from the standard input,
* performs the variable expansions described above, and
* writes the expanded command to the standard output.

Examples:

  % /c/cs323/Hwk3/mcBash
  (1)$ OSTYPE = $OSTYPE
  >> OSTYPE = linux
  (2)$ ${OSTYPE-Linux}
  >> linux
  (3)$ ${NONEXISTENT}
  >>
  (4)$ ${NONEXISTENT=VALUE}
  >> VALUE
  (5)$ ${NONEXISTENT}
  >> VALUE
  (6)$ $0
  >> /c/cs323/Hwk3/mcBash
  (7)$ \$OSTYPE
  >> \$OSTYPE
  (8)$ ${ANOTHER=$OSTYPE}
  >> linux
  (9)$ $ANOTHER
  >> linux
   
