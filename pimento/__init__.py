'''
Make simple python cli menus!
'''


# [ Imports ]
# [ -Python ]
# import as _name so that they do not show up as part of the module
import sys as _sys
import argparse as _argparse
import os.path as _path
try:
    # just importing readline means that 'input' will use it.
    # this is unpythonic, but I did not write the builtins.
    import readline as _readline
except ImportError:
    # No readline.
    # Arrow support will be disabled
    # Tab-completion will be disabled
    pass


# [ GLOBALS ]
# _NO_ARG is a default.  If an arg is _NO_ARG, the function receiving it
# knows the user has not passed anything in, even None.  This allows the
# default argument to be dynamic, rather than static at parse time.
_NO_ARG=object()


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
    # get the options which match the full text
    matching_options = _get_fuzzy_matches(full_text, options)
    # only return the unmatched words which match the text
    # being tab-completed
    final_matches = []
    entered_words = full_text.split(' ')
    # get the words from each option which have not been
    # previously matched, and which match the text being
    # completed.
    for option in matching_options:
        already_matched = entered_words[:]
        already_matched.remove(text)
        option_words = option.split()
        # strip out full-word matches
        for word in already_matched:
            if word in option_words:
                option_words.remove(word)
                already_matched.remove(word)
            # else it was a partial, too
        # strip out partial-word matches
        for partial in sorted(
            already_matched,
            key=lambda p: len(p),
            reverse=True
        ):
            for word in option_words:
                if partial in word:
                    option_words.remove(word)
                    already_matched.remove(partial)
                    assert len(already_matched) == 0, "{} not found in {}: _get_fuzzy_matches made a mistake".format(
                        already_matched, option
                    )
        # get unique words left which match the text
        for word in option_words:
            if text in word and word not in final_matches:
                final_matches.append(word)
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
            #import traceback as _traceback
            #print(_traceback.format_exc())
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
            if insensitive:
                ordered_matches = [o for o in items if substitution in o.lower()]
            else:
                ordered_matches = [o for o in items if substitution in o]
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
    # match partial words, longest first
    for partial in sorted(r_words, key=lambda p: len(p), reverse=True):
        for word in c_words:
            if partial in word:
                r_words.remove(partial)
                c_words.remove(word)
    # if all the items in the response were matched, this is match
    return len(r_words) == 0


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


def _check_response(response, items, default, indexed, stream, insensitive, search, fuzzy):
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
        elif search:
            matches = [i for i in items if response in i]
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
            ''',
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
    # parse options
    args, unknown = parser.parse_known_args()
    # set deprecated search option
    args.search = '--search' in unknown or '-s' in unknown
    # argparse nargs is awkward.  Translate to be a proper plural.
    options = args.option
    # read more options from stdin if there are are any
    # but only if we're on a 'nix system with tty's
    tty = '/dev/tty'
    if not _sys.stdin.isatty() and _path.exists(tty):
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
            search=args.search,
            fuzzy=args.fuzzy
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
         stream=_sys.stderr, insensitive=False, search=False,
         fuzzy=False):
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
        search -  [deprecated] search for the user input anwhere in the item strings, not just at the beginning.
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
    # deprecated use: pre_promt first, items second
    if isinstance(items, str) and not isinstance(pre_prompt, str):
        swap = items
        items = pre_prompt
        pre_prompt = swap
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
    _tab_complete_init(items, actual_post_prompt, insensitive, fuzzy, stream)
    # Prompt Loop
    # - wait until an acceptable response has been given
    while not acceptable_response_given:
        selection = None
        # Prompt and get response
        response = _prompt(pre_prompt, items, actual_post_prompt, default, indexed, stream)
        # validate response
        selection = _check_response(response, items, default, indexed, stream, insensitive, search, fuzzy)
        # NOTE: acceptable response logic is purposely verbose to be clear about the semantics.
        if selection is not None:
            acceptable_response_given = True
    return selection
