'''
Make simple python cli menus!
'''


# [ Imports ]
# [ -Python ]
# import as _name so that they do not show up as part of the module
import sys as _sys
import argparse as _argparse
import os.path as _path
import pkg_resources as _pkg_resources
try:
    # just importing readline means that 'input' will use it.
    # this is unpythonic, but I did not write the builtins.
    import readline as _readline
except ImportError:
    # No readline.
    # Arrow support will be disabled
    # Tab-completion will be disabled
    _readline = None


# [ GLOBALS ]
# _NO_ARG is a default.  If an arg is _NO_ARG, the function receiving it
# knows the user has not passed anything in, even None.  This allows the
# default argument to be dynamic, rather than static at parse time.
_NO_ARG=object()
_VERSION=_pkg_resources.get_distribution("pimento").version


# [ Private API ]
def _get_standard_tc_matches(text, full_text, options):
    '''
    get the standard tab completions.
    These are the options which could complete the full_text.
    '''
    final_matches = [o for o in options if o.startswith(full_text)]
    return final_matches


def _get_fuzzy_tc_matches(text, full_text, options):
    '''
    Get the options that match the full text, then from each option
    return only the individual words which have not yet been matched
    which also match the text being tab-completed.
    '''
    print("text: {}, full: {}, options: {}".format(text, full_text, options))
    # get the options which match the full text
    matching_options = _get_fuzzy_matches(full_text, options)
    # need to only return the individual words which:
    # - match the 'text'
    # - are not exclusively matched by other input in full_text
    # - when matched, still allows all other input in full_text to be matched
    # get the input tokens
    input_tokens = full_text.split()
    # remove one instance of the text to be matched
    initial_tokens = input_tokens.remove(text)
    # track the final matches:
    final_matches = []
    # find matches per option
    for option in options:
        option_tokens = option.split()
        # get tokens which match the text
        matches = [t for t in option_tokens if text in t]
        # get input tokens which match one of the matches
        input_tokens_which_match = [t for t in input_tokens for m in matches if t in m]
        # if any input token ONLY matches a match, remove that match
        for token in input_tokens_which_match:
            token_matches = [t for t in option_tokens if token in t]
            if len(token_matches) == 1:
                match = token_matches[0]
                if match in matches:
                    matches.remove(match)
        # for the remaining matches, if the input tokens can be fuzzily matched without
        # the match, it's ok to return it.
        for match in matches:
            # copy option tokens
            option_tokens_minus_match = option_tokens[:]
            # remove the match
            option_tokens_minus_match.remove(match)
            option_minus_match = ' '.join(option_tokens_minus_match)
            if _get_fuzzy_matches(' '.join(input_tokens), [option_minus_match]):
                if match not in final_matches:
                    final_matches.append(match)
    return final_matches


def _tab_complete_init(items, post_prompt, insensitive, fuzzy, stream):
    '''Create and use a tab-completer object'''
    # using some sort of nested-scope construct is
    # required because readline doesn't pass the necessary args to
    # its callback functions
    def _get_matches(text, state):
        '''
        Get a valid match, given:
            text - the portion of text currently trying to complete
            state - the index 0..inf which is an index into the list
            of valid matches.
        Put another way, given the text, this function is supposed
        to return matches_for(text)[state], where 'matches_for' returns
        the matches for the text from the options.
        '''
        # a copy of all the valid options
        options = [o for o in items]
        # the full user-entered text
        full_text = _readline.get_line_buffer()
        # insensitivity
        if insensitive:
            options = [o.lower() for o in options]
            text = text.lower()
            full_text = full_text.lower()
        # matches
        matches = []
        try:
            # get matches
            if fuzzy:
                # space-delimited - match words
                _readline.set_completer_delims(' ')
                matches = _get_fuzzy_tc_matches(text, full_text, options)
            else:
                # not delimited - match the whole text
                _readline.set_completer_delims('')
                matches = _get_standard_tc_matches(text, full_text, options)
            # re-sensitization not necessary - this completes what's on
            # the command prompt.  If the search is insensitive, then
            # a lower-case entry will match as well as an original-case
            # entry.
        except Exception:
            # try/catch is for debugging only.  The readline
            # lib swallows exceptions and just doesn't print anything
            import traceback as _traceback
            print(_traceback.format_exc())
            raise
        return matches[state]

    def _completion_display(substitution, matches, length):
        '''
        Display the matches for the substitution, which is the
        text being completed.
        '''
        try:
            response = substitution
            stream.write("\n[!] \"{response}\" matches multiple options:\n".format(
                response=response
            ))
            if fuzzy:
                if insensitive:
                    ordered_matches = [o for o in items if substitution in o.lower()]
                else:
                    ordered_matches = [o for o in items if substitution in o]
            else:
                if insensitive:
                    ordered_matches = [o for o in items if o.lower().startswith(substitution)]
                else:
                    ordered_matches = [o for o in items if o.startswith(substitution)]
            for match in ordered_matches:
                stream.write("[!]   {}\n".format(match))
            stream.write("[!] Please specify your choice further.\n")
            # the full user-entered text
            full_text = _readline.get_line_buffer()
            stream.write(post_prompt + full_text)
            stream.flush()
        except Exception:
            # try/catch is for debugging only.  The readline
            # lib swallows exceptions and just doesn't print anything
            #import traceback as _traceback
            #print(_traceback.format_exc())
            raise

    # activate tab completion
    # got libedit bit from:
    # https://stackoverflow.com/a/7116997
    # -----------------------------------
    if "libedit" in _readline.__doc__:
        # tabcompletion init for libedit
        _readline.parse_and_bind("bind ^I rl_complete")
    else:
        # tabcompletion init for actual readline
        _readline.parse_and_bind("tab: complete")
    # -----------------------------------
    # set the function that will actually provide the valid completions
    _readline.set_completer(_get_matches)
    # set the function that will display the valid completions
    _readline.set_completion_display_matches_hook(_completion_display)
    #_readline.set_completer_delims('')


def _prompt(pre_prompt, items, post_prompt, default, indexed, stream):
    '''
    Prompt once.
    If you want the default displayed, put a format {} into the
    post_prompt string (like 'select one [{}]: ')
    '''
    # try to sub in the default if provided
    if default is not None:
        if '{}' in pre_prompt:
            pre_prompt = pre_prompt.format(default)
        if '{}' in post_prompt:
            post_prompt = post_prompt.format(default)
    # build the item strings
    item_format = "{indent}{item}"
    if indexed:
        item_format = "{indent}[{index}] {item}"
    item_text_list = []
    indent = '  '
    for index, item in enumerate(items):
        item_text = ''
        components = {
            'indent': indent,
            'item': item
        }
        if indexed:
            components['index'] = index
        item_text = item_format.format(**components)
        item_text_list.append(item_text)
    # build full menu
    menu_parts = [pre_prompt] + item_text_list
    full_menu = '\n'.join(menu_parts) + '\n'
    stream.write(full_menu)
    stream.flush()
    # Get user response
    # - py 2/3 compatibility
    get_input = input
    try:
        get_input = raw_input
    except NameError:
        pass
    # - actuall get input
    response = get_input(post_prompt)
    return response


def _fuzzily_matches(response, candidate):
    '''return True if response fuzzily matches candidate'''
    r_words = response.split()
    c_words = candidate.split()
    # match whole words first
    for word in r_words:
        if word in c_words:
            r_words.remove(word)
            c_words.remove(word)
    # match partial words, fewest matches first
    match_pairs = []
    for partial in sorted(r_words, key=lambda p: len(p), reverse=True):
        matches = [w for w in c_words if partial in w]
        match_pairs.append((partial, matches))
    # if all items can be uniquly matched, the match is passed
    while len(match_pairs):
        min_pair = min(match_pairs, key=lambda x:len(x[1]))
        # this is the partial and matches with the shortest match list
        # if there are ever no matches for something, the match is failed
        if len(min_pair[1]) == 0:
            return False
        # choose the match with the fewest matches to remaining partials.
        # that way we leave more options for more partials, for the best
        # chance of a full match
        partials_left = [p[0] for p in match_pairs]
        min_option = min(min_pair[1], key=lambda x:len([p for p in partials_left if x in p]))
        # remove the current pair - we've matched it now
        match_pairs.remove(min_pair)
        # remove the matched option from all pairs' options so it won't be matched again
        for pair in match_pairs:
            pair_options = pair[1]
            if min_option in pair_options:
                pair_options.remove(min_option)
    # if all the items in the response were matched, this is match
    return True


def _get_fuzzy_matches(response, items):
    '''returns the list of items which fuzzily match the response'''
    return [i for i in items if _fuzzily_matches(response, i)]


def _exact_fuzzy_match(response, match, insensitive):
    '''
    Return True if the response matches fuzzily exactly.
    Insensitivity is taken into account.
    '''
    if insensitive:
        response = response.lower()
        match = match.lower()
    r_words = response.split()
    m_words = match.split()
    # match whole words first
    for word in r_words:
        if word in m_words:
            r_words.remove(word)
            m_words.remove(word)
    # no partial matches allowed
    # if all the items in the response were matched,
    # and all the items in the match were matched,
    # then this is an exact fuzzy match
    return len(r_words) == 0 and len(m_words) == 0


def _exact_match(response, matches, insensitive, fuzzy):
    '''
    returns an exact match, if it exists, given parameters
    for the match
    '''
    for match in matches:
        if response == match:
            return match
        elif insensitive and response.lower() == match.lower():
            return match
        elif fuzzy and _exact_fuzzy_match(response, match, insensitive):
            return match
    else:
        return None


def _check_response(response, items, default, indexed, stream, insensitive, fuzzy):
    '''Check the response against the items'''
    # Set selection
    selection = None
    # if indexed, check for index
    if indexed:
        if response.isdigit():
            index_response = int(response)
            if index_response < len(items):
                selection = items[index_response]
    # if not matched by an index, match by text
    if selection is None:
        # insensivitize, if necessary
        original_items = items[:]
        original_response = response
        if insensitive:
            response = response.lower()
            items = [i.lower() for i in items]
        # Check for text matches
        if fuzzy:
            matches = _get_fuzzy_matches(response, items)
        # if insensitive, lowercase the comparison
        else:
            matches = [i for i in items if i.startswith(response)]
        # re-sensivitize if necessary
        if insensitive:
            matches = [
                i for i in original_items
                if i.lower() in matches
            ]
            response = original_response
        num_matches = len(matches)
        # Empty response, no default
        if response == '' and default is None:
            stream.write("[!] an empty response is not valid.\n")
        elif response == '':
            selection = default
        # Bad response
        elif num_matches == 0:
            stream.write("[!] \"{response}\" does not match any of the valid choices.\n".format(
                response=response
            ))
        # One match
        elif num_matches == 1:
            selection = matches[0]
        # Multiple matches
        else:
            # look for an exact match
            selection = _exact_match(response, matches, insensitive, fuzzy)
            # Multiple matches left
            if selection is None:
                stream.write("[!] \"{response}\" matches multiple choices:\n".format(
                    response=response
                ))
                for match in matches:
                    stream.write("[!]   {}\n".format(match))
                stream.write("[!] Please specify your choice further.\n")
    return selection


def _check_prompts(pre_prompt, post_prompt):
    '''Check that the prompts are strings'''
    if not isinstance(pre_prompt, str):
        raise TypeError("The pre_prompt was not a string!")
    if post_prompt is not _NO_ARG and not isinstance(post_prompt, str):
        raise TypeError("The post_prompt was given and was not a string!")


def _check_items(items):
    '''
    Check:
     - that the list of items is iterable and finite.
     - that the list is not empty
    '''
    num_items = 0
    # Check that the list is iterable and finite
    try:
        num_items = len(items)
    except:
        raise TypeError("The item list ({}) is not a finite iterable (has no length)".format(items))
    # Check that the list has items
    if num_items == 0:
        raise ValueError("The item list is empty.")


def _check_default_index(items, default_index):
    '''Check that the default is in the list, and not empty'''
    num_items = len(items)
    if default_index is not None and not isinstance(default_index, int):
        raise TypeError("The default index ({}) is not an integer".format(default_index))
    if default_index is not None and default_index >= num_items:
        raise ValueError("The default index ({}) >= length of the list ({})".format(default_index, num_items))
    if default_index is not None and default_index < 0:
        raise ValueError("The default index ({}) < 0.".format(default_index))
    if default_index is not None and not items[default_index]:
        raise ValueError("The default index ({}) points to an empty item.".format(default_index))


def _check_stream(stream):
    '''Check that the stream is a file'''
    if not isinstance(stream, type(_sys.stderr)):
        raise TypeError("The stream given ({}) is not a file object.".format(stream))


def _cli():
    '''CLI interface'''
    parser = _argparse.ArgumentParser(
        description='''
            Present the user with a simple CLI menu, and return the option chosen.
            The menu is presented via stderr.
            The output is printed to stdout for piping.
            '''.format(_VERSION),
        epilog='''
            The default for the post prompt is "Enter an option to continue: ".
            If --default-index is specified, the default option value will be printed
                in the post prompt as well.
        '''
    )
    parser.add_argument(
        'option',
        help='The option(s) to present to the user.',
        nargs='*'
    )
    parser.add_argument(
        '--version', '-v',
        help='Print the version and then exit',
        action='store_true'
    )
    parser.add_argument(
        '--pre', '-p',
        help='The pre-prompt/title/introduction to the menu. [%(default)s]',
        default='Options:',
        metavar='TEXT'
    )
    parser.add_argument(
        '--post', '-P',
        help='The prompt presented to the user after the menu items.',
        default=_NO_ARG,
        metavar='TEXT'
    )
    parser.add_argument(
        '--default-index', '-d',
        help='The index of the item to use as the default',
        type=int,
        metavar='INT'
    )
    parser.add_argument(
        '--indexed', '-i',
        help='Print indices with the options, and allow the user to use them to choose.',
        action='store_true'
    )
    parser.add_argument(
        '--insensitive', '-I',
        help=(
            'Perform insensitive matching.  Also drops any items that case-insensitively match'
            + ' prior items.'
        ),
        action='store_true'
    )
    parser.add_argument(
        '--fuzzy', '-f',
        help='search for the individual words in the user input anywhere in the item strings.',
        action='store_true'
    )
    parser.add_argument(
        '--stdout',
        help='Use stdout for interactive output (instead of the default: stderr).',
        action='store_true'
    )
    # parse options
    args = parser.parse_args()
    # argparse nargs is awkward.  Translate to be a proper plural.
    options = args.option
    # set the stream
    stream = _sys.stdout if args.stdout else _sys.stderr
    # if version, print version and exit
    if args.version:
        stream.write('Pimento - v{}\n'.format(_VERSION))
        exit(0)
    # read more options from stdin if there are are any
    # but only if we're on a 'nix system with tty's
    tty = '/dev/tty'
    if not _sys.stdin.isatty() and _path.exists(tty):
        if _sys.version_info.major == 3:
            stream.write('[!] python3 input bug - tab completion not available\n')
            stream.write('[!] python3 input bug - arrow support not available\n')
            stream.write('[!] only known workaround is to not pipe in.\n')
        options += [l.rstrip() for l in _sys.stdin]
        # switch to the main tty
        # this solution (to being interactive after reading from pipe)
        # comes from: https://stackoverflow.com/questions/6312819/pipes-and-prompts-in-python-cli-scripts
        _sys.stdin = open(tty)
    # show the menu
    try:
        result = menu(
            options,
            pre_prompt=args.pre,
            post_prompt=args.post,
            default_index=args.default_index,
            indexed=args.indexed,
            insensitive=args.insensitive,
            fuzzy=args.fuzzy,
            stream=stream
        )
        # print the result (to stdout)
        _sys.stdout.write(result + '\n')
    except KeyboardInterrupt:
        _sys.stderr.write("\nCTRL-C detected. Exiting.\n")
        _sys.stderr.flush()
    except Exception as e:
        _sys.stdout.write("ERROR: {}\n".format(e))
        exit(1)


def _dedup(items, insensitive):
    '''
    Deduplicate an item list, and preserve order.

    For case-insensitive lists, drop items if they case-insensitively match
    a prior item.
    '''
    deduped = []
    if insensitive:
        i_deduped = []
        for item in items:
            lowered = item.lower()
            if lowered not in i_deduped:
                deduped.append(item)
                i_deduped.append(lowered)
    else:
        for item in items:
            if item not in deduped:
                deduped.append(item)
    return deduped


# [ Public API ]
def menu(items, pre_prompt="Options:", post_prompt=_NO_ARG, default_index=None, indexed=False,
         stream=_sys.stderr, insensitive=False, fuzzy=False, quiet=False):
    '''
    Prompt with a menu.

    Arguments:
        pre_prompt -  Text to print before the option list.
        items -  The items to print as options.
        post_prompt -  Text to print after the option list.
        default_index -  The index of the item which should be default, if any.
        indexed -  Boolean.  True if the options should be indexed.
        stream -  the stream to use to prompt the user.  Defaults to stderr so that stdout
            can be reserved for program output rather than interactive menu output.
        insensitive -  allow insensitive matching.  Also drops items which case-insensitively match
          prior items.
        fuzzy -  search for the individual words in the user input anywhere in the item strings.

    Specifying a default index:
        The default index must index into the items.  In other words, `items[default_index]`
        must exist.  It is encouraged, but not required, that you show the user that there is
        a default, and what it is, via string interpolation in either of the prompts:
            "prompt [{}]" as the prompt string will print "prompt [default]" if "default" were
            the value of the item at the default index.

    The default post-prompt:
        The default post prompt is different depending on whether or not you provide a default_index.
        If you don't, the prompt is just "Enter an option to continue: ".
        If you do, the prompt adds the default value: "Enter an option to continue [{}]: "

    Return:
        result -  The full text of the unambiguously selected item.
    '''
    # arg checking
    _check_prompts(pre_prompt, post_prompt)
    _check_items(items)
    _check_default_index(items, default_index)
    _check_stream(stream)
    # arg mapping
    # - Fill in post-prompt dynamically if no arg
    actual_post_prompt = post_prompt
    if post_prompt is _NO_ARG:
        if default_index is None:
            actual_post_prompt = "Enter an option to continue: "
        else:
            actual_post_prompt = "Enter an option to continue [{}]: "
    # - convert items to rstripped strings
    items = [str(i).rstrip() for i in items]
    # - set the default argument
    default = None
    if default_index is not None:
        default = items[default_index]
    # - deduplicate items
    items = _dedup(items, insensitive)
    # - remove empty options
    items = [i for i in items if i]
    # - re-check the items
    _check_items(items)
    # other state init
    acceptable_response_given = False
    if _readline is None:
        stream.write('[!] readline library not present - tab completion not available\n')
        stream.write('[!] readline library not present - arrow support not available\n')
    elif not stream.isatty():
        stream.write('[!] output stream is not interactive - tab completion not available\n')
        stream.write('[!] output stream is not interactive - arrow support not available\n')
    elif _sys.version_info.major == 3 and stream is not _sys.stdout:
        stream.write('[!] python3 input bug (issue24402) - tab completion not available\n')
        stream.write('[!] python3 input bug (issue24402) - arrow support not available\n')
        stream.write('[!] set sys.stdout as the stream to work around\n')
    else:
        _tab_complete_init(items, actual_post_prompt, insensitive, fuzzy, stream)
    # Set both stdout and stderr to the stream selected.
    # - in py2, raw_input uses sys.stdout
    # - in py3, input uses a lower-level stdout stream which is not redirectable.
    #   - there is an open bug for this, scheduled to be resolved in py3.6 (https://bugs.python.org/issue24402)
    # [raw_]input uses readline to do fancy things like tab completion, and also like reprinting the user
    # text on the cli when you type.  If we don't redirect the output streams, [raw_]input will always use
    # the default (stdout) even though most of the time we want stderr for interactive prompts.  we could just
    # print the prompt ourselves (and not let [raw_]input do so), but only when we control reprinting (which
    # we don't always for tab completion), and even then, if the user backspaces into the prompt, [raw_]input
    # would reprint the line itself, erasing the prompt it doesn't know about.  (see issue #70)
    try:
        _old_stdout = _sys.stdout
        _old_stderr = _sys.stderr
        # only overwrite the stream if we need to, due to the python3 issue
        if stream is _sys.stdout:
            pass
        else:
            _sys.stdout = stream
        # Prompt Loop
        # - wait until an acceptable response has been given
        while not acceptable_response_given:
            selection = None
            # Prompt and get response
            response = _prompt(pre_prompt, items, actual_post_prompt, default, indexed, stream)
            # validate response
            selection = _check_response(response, items, default, indexed, stream, insensitive, fuzzy)
            # NOTE: acceptable response logic is purposely verbose to be clear about the semantics.
            if selection is not None:
                acceptable_response_given = True
    finally:
        _sys.stdout = _old_stdout
        _sys.stderr = _old_stderr
    return selection
