#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Secret Labs' Regular Expression Engine123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# re-compatible interface for the sre matching engine123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Copyright (c) 1998-2001 by Secret Labs AB.  All rights reserved.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# This version of the SRE library can be redistributed under CNRI's123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Python 1.6 license.  For any other use, please contact Secret Labs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# AB (info@pythonware.com).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Portions of this engine have been developed in cooperation with123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# CNRI.  Hewlett-Packard provided funding for 1.6 integration and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# other compatibility work.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFr"""Support for regular expressions (RE).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThis module provides regular expression matching operations similar to123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFthose found in Perl.  It supports both 8-bit and Unicode strings; both123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFthe pattern and the strings being processed can contain null bytes and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcharacters outside the US ASCII range.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFRegular expressions can contain both special and ordinary characters.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFMost ordinary characters, like "A", "a", or "0", are the simplest123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFregular expressions; they simply match themselves.  You can123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFconcatenate ordinary characters, so last matches the string 'last'.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThe special characters are:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "."      Matches any character except a newline.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "^"      Matches the start of the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "$"      Matches the end of the string or just before the newline at123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF             the end of the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "*"      Matches 0 or more (greedy) repetitions of the preceding RE.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF             Greedy means that it will match as many repetitions as possible.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "+"      Matches 1 or more (greedy) repetitions of the preceding RE.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "?"      Matches 0 or 1 (greedy) of the preceding RE.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    *?,+?,?? Non-greedy versions of the previous three special characters.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    {m,n}    Matches from m to n repetitions of the preceding RE.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    {m,n}?   Non-greedy version of the above.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "\\"     Either escapes special characters or signals a special sequence.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    []       Indicates a set of characters.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF             A "^" as the first character indicates a complementing set.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "|"      A|B, creates an RE that will match either A or B.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (...)    Matches the RE inside the parentheses.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF             The contents can be retrieved or matched later in the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?iLmsux) Set the I, L, M, S, U, or X flag for the RE (see below).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?:...)  Non-grouping version of regular parentheses.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?P<name>...) The substring matched by the group is accessible by name.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?P=name)     Matches the text matched earlier by the group named name.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?#...)  A comment; ignored.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?=...)  Matches if ... matches next, but doesn't consume the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?!...)  Matches if ... doesn't match next.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?<=...) Matches if preceded by ... (must be fixed length).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?<!...) Matches if not preceded by ... (must be fixed length).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (?(id/name)yes|no) Matches yes pattern if the group with id/name matched,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       the (optional) no pattern otherwise.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThe special sequences consist of "\\" and a character from the list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFbelow.  If the ordinary character is not on the list, then the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFresulting RE will match the second character.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \number  Matches the contents of the group of the same number.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \A       Matches only at the start of the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \Z       Matches only at the end of the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \b       Matches the empty string, but only at the start or end of a word.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \B       Matches the empty string, but not at the start or end of a word.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \d       Matches any decimal digit; equivalent to the set [0-9].123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \D       Matches any non-digit character; equivalent to the set [^0-9].123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \s       Matches any whitespace character; equivalent to [ \t\n\r\f\v].123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \S       Matches any non-whitespace character; equiv. to [^ \t\n\r\f\v].123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \w       Matches any alphanumeric character; equivalent to [a-zA-Z0-9_].123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF             With LOCALE, it will match the set [0-9_] plus characters defined123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF             as letters for the current locale.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \W       Matches the complement of \w.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    \\       Matches a literal backslash.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThis module exports the following functions:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match    Match a regular expression pattern to the beginning of a string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    search   Search a string for the presence of a pattern.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sub      Substitute occurrences of a pattern found in a string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    subn     Same as sub, but also return the number of substitutions made.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    split    Split a string by the occurrences of a pattern.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    findall  Find all occurrences of a pattern in a string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    finditer Return an iterator yielding a match object for each match.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    compile  Compile a pattern into a RegexObject.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    purge    Clear the regular expression cache.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    escape   Backslash all non-alphanumerics in a string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFSome of the functions in this module takes flags as optional parameters:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    I  IGNORECASE  Perform case-insensitive matching.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    L  LOCALE      Make \w, \W, \b, \B, dependent on the current locale.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    M  MULTILINE   "^" matches the beginning of lines (after a newline)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                   as well as the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                   "$" matches the end of lines (before a newline) as well123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                   as the end of the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    S  DOTALL      "." matches any character at all, including the newline.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    X  VERBOSE     Ignore whitespace and comments for nicer looking RE's.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    U  UNICODE     Make \w, \W, \b, \B, dependent on the Unicode locale.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThis module also defines an exception 'error'.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sre_compile123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sre_parse123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtry:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    import _locale123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFexcept ImportError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _locale = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# public symbols123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF__all__ = [ "match", "search", "sub", "subn", "split", "findall",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "compile", "purge", "template", "escape", "I", "L", "M", "S", "X",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "U", "IGNORECASE", "LOCALE", "MULTILINE", "DOTALL", "VERBOSE",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "UNICODE", "error" ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF__version__ = "2.2.1"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# flags123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFI = IGNORECASE = sre_compile.SRE_FLAG_IGNORECASE # ignore case123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFL = LOCALE = sre_compile.SRE_FLAG_LOCALE # assume current 8-bit locale123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFU = UNICODE = sre_compile.SRE_FLAG_UNICODE # assume unicode locale123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFM = MULTILINE = sre_compile.SRE_FLAG_MULTILINE # make anchors look for newline123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFS = DOTALL = sre_compile.SRE_FLAG_DOTALL # make dot match newline123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFX = VERBOSE = sre_compile.SRE_FLAG_VERBOSE # ignore whitespace and comments123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# sre extensions (experimental, don't rely on these)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFT = TEMPLATE = sre_compile.SRE_FLAG_TEMPLATE # disable backtracking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFDEBUG = sre_compile.SRE_FLAG_DEBUG # dump pattern after compilation123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# sre exception123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFerror = sre_compile.error123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# --------------------------------------------------------------------123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# public interface123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef match(pattern, string, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Try to apply the pattern at the start of the string, returning123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    a match object, or None if no match was found."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags).match(string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef search(pattern, string, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Scan through string looking for a match to the pattern, returning123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    a match object, or None if no match was found."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags).search(string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef sub(pattern, repl, string, count=0, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Return the string obtained by replacing the leftmost123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    non-overlapping occurrences of the pattern in string by the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    replacement repl.  repl can be either a string or a callable;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if a string, backslash escapes in it are processed.  If it is123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    a callable, it's passed the match object and must return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    a replacement string to be used."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags).sub(repl, string, count)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef subn(pattern, repl, string, count=0, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Return a 2-tuple containing (new_string, number).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    new_string is the string obtained by replacing the leftmost123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    non-overlapping occurrences of the pattern in the source123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    string by the replacement repl.  number is the number of123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    substitutions that were made. repl can be either a string or a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    callable; if a string, backslash escapes in it are processed.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    If it is a callable, it's passed the match object and must123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return a replacement string to be used."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags).subn(repl, string, count)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef split(pattern, string, maxsplit=0, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Split the source string by the occurrences of the pattern,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    returning a list containing the resulting substrings."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags).split(string, maxsplit)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef findall(pattern, string, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Return a list of all non-overlapping matches in the string.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    If one or more groups are present in the pattern, return a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    list of groups; this will be a list of tuples if the pattern123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    has more than one group.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Empty matches are included in the result."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags).findall(string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif sys.hexversion >= 0x02020000:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    __all__.append("finditer")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def finditer(pattern, string, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Return an iterator over all non-overlapping matches in the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        string.  For each match, the iterator returns a match object.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Empty matches are included in the result."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return _compile(pattern, flags).finditer(string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef compile(pattern, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Compile a regular expression pattern, returning a pattern object."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef purge():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Clear the regular expression cache"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _cache.clear()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _cache_repl.clear()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef template(pattern, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Compile a template pattern, returning a pattern object"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile(pattern, flags|T)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF_alphanum = frozenset(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef escape(pattern):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Escape all non-alphanumeric characters in pattern."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    s = list(pattern)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    alphanum = _alphanum123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i, c in enumerate(pattern):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if c not in alphanum:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if c == "\000":123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                s[i] = "\\000"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                s[i] = "\\" + c123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return pattern[:0].join(s)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# --------------------------------------------------------------------123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# internals123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF_cache = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF_cache_repl = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF_pattern_type = type(sre_compile.compile("", 0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF_MAXCACHE = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _compile(*key):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # internal: compile pattern123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pattern, flags = key123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    bypass_cache = flags & DEBUG123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not bypass_cache:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cachekey = (type(key[0]),) + key123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            p, loc = _cache[cachekey]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if loc is None or loc == _locale.setlocale(_locale.LC_CTYPE):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except KeyError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if isinstance(pattern, _pattern_type):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if flags:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise ValueError('Cannot process flags argument with a compiled pattern')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return pattern123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not sre_compile.isstring(pattern):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise TypeError, "first argument must be string or compiled pattern"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        p = sre_compile.compile(pattern, flags)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except error, v:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise error, v # invalid expression123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not bypass_cache:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(_cache) >= _MAXCACHE:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            _cache.clear()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if p.flags & LOCALE:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if not _locale:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            loc = _locale.setlocale(_locale.LC_CTYPE)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            loc = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _cache[cachekey] = p, loc123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _compile_repl(*key):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # internal: compile replacement pattern123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    p = _cache_repl.get(key)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if p is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    repl, pattern = key123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        p = sre_parse.parse_template(repl, pattern)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except error, v:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise error, v # invalid expression123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(_cache_repl) >= _MAXCACHE:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _cache_repl.clear()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _cache_repl[key] = p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _expand(pattern, match, template):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # internal: match.expand implementation hook123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    template = sre_parse.parse_template(template, pattern)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return sre_parse.expand_template(template, match)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _subx(pattern, template):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # internal: pattern.sub/subn implementation helper123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    template = _compile_repl(template, pattern)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not template[0] and len(template[1]) == 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # literal replacement123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return template[1][0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def filter(match, template=template):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return sre_parse.expand_template(template, match)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return filter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# register myself for pickling123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport copy_reg123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _pickle(p):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return _compile, (p.pattern, p.flags)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcopy_reg.pickle(_pattern_type, _pickle, _compile)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# --------------------------------------------------------------------123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# experimental stuff (see python-dev discussions for details)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass Scanner:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self, lexicon, flags=0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        from sre_constants import BRANCH, SUBPATTERN123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.lexicon = lexicon123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # combine phrases into a compound pattern123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        p = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s = sre_parse.Pattern()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s.flags = flags123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for phrase, action in lexicon:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            p.append(sre_parse.SubPattern(s, [123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                (SUBPATTERN, (len(p)+1, sre_parse.parse(phrase, flags))),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                ]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s.groups = len(p)+1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scanner = sre_compile.compile(p)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def scan(self, string):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        result = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        append = result.append123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        match = self.scanner.scanner(string).match123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        i = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        while 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            m = match()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if not m:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                break123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            j = m.end()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if i == j:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                break123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            action = self.lexicon[m.lastindex-1][1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if hasattr(action, '__call__'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.match = m123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                action = action(self, m.group())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if action is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                append(action)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            i = j123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return result, string[i:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF