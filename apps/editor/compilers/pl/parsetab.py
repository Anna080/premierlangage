# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'startCOMMENT ID OP_ASSIGN_FILE OP_ASSIGN_MULTI OP_ASSIGN_SINGLE OP_SANDBOX ' \
                'TEXT\n        start : instructions\n        \n        instructions : ' \
                'instructions assign_single\n                    | instructions assign_multi\n    ' \
                '                | instructions assign_file\n                    | instructions ' \
                'sandbox\n                    | empty\n        \n        assign_single : ID ' \
                'OP_ASSIGN_SINGLE\n                    | ID OP_ASSIGN_SINGLE TEXT\n        \n     ' \
                '   assign_multi : ID OP_ASSIGN_MULTI TEXT\n        \n        assign_file : ID ' \
                'OP_ASSIGN_FILE TEXT\n        \n        sandbox : OP_SANDBOX TEXT\n        empty :'

_lr_action_items = {
    'ID': ([0, 2, 3, 4, 5, 6, 7, 10, 13, 14, 15, 16, ],
           [-12, 8, -6, -2, -3, -4, -5, -7, -11, -8, -9, -10, ]), 'OP_SANDBOX': (
    [0, 2, 3, 4, 5, 6, 7, 10, 13, 14, 15, 16, ],
    [-12, 9, -6, -2, -3, -4, -5, -7, -11, -8, -9, -10, ]), '$end': (
    [0, 1, 2, 3, 4, 5, 6, 7, 10, 13, 14, 15, 16, ],
    [-12, 0, -1, -6, -2, -3, -4, -5, -7, -11, -8, -9, -10, ]), 'OP_ASSIGN_SINGLE': ([8, ], [10, ]),
    'OP_ASSIGN_MULTI': ([8, ], [11, ]), 'OP_ASSIGN_FILE': ([8, ], [12, ]),
    'TEXT': ([9, 10, 11, 12, ], [13, 14, 15, 16, ]),
}

_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':         ([0, ], [1, ]), 'instructions': ([0, ], [2, ]),
                  'empty':         ([0, ], [3, ]), 'assign_single': ([2, ], [4, ]),
                  'assign_multi':  ([2, ], [5, ]), 'assign_file': ([2, ], [6, ]),
                  'sandbox':       ([2, ], [7, ]),
}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
    ("S' -> start", "S'", 1, None, None, None),
    ('start -> instructions', 'start', 1, 'p_start', 'pl_parser.py', 232),
    ('instructions -> instructions assign_single', 'instructions', 2, 'p_instructions',
     'pl_parser.py', 237),
    ('instructions -> instructions assign_multi', 'instructions', 2, 'p_instructions',
     'pl_parser.py', 238),
    (
    'instructions -> instructions assign_file', 'instructions', 2, 'p_instructions', 'pl_parser.py',
    239),
    ('instructions -> instructions sandbox', 'instructions', 2, 'p_instructions', 'pl_parser.py',
     240),
    ('instructions -> empty', 'instructions', 1, 'p_instructions', 'pl_parser.py', 241),
    ('assign_single -> ID OP_ASSIGN_SINGLE', 'assign_single', 2, 'p_assign_single', 'pl_parser.py',
     253),
    ('assign_single -> ID OP_ASSIGN_SINGLE TEXT', 'assign_single', 3, 'p_assign_single',
     'pl_parser.py', 254),
    ('assign_multi -> ID OP_ASSIGN_MULTI TEXT', 'assign_multi', 3, 'p_assign_multi', 'pl_parser.py',
     267),
    ('assign_file -> ID OP_ASSIGN_FILE TEXT', 'assign_file', 3, 'p_assign_file', 'pl_parser.py',
     278),
    ('sandbox -> OP_SANDBOX TEXT', 'sandbox', 2, 'p_sandbox', 'pl_parser.py', 301),
    ('empty -> <empty>', 'empty', 0, 'p_empty', 'pl_parser.py', 329),
]
