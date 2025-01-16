#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def flatten(items):
    for x in items:
        if isinstance(x, list):
            yield from flatten(x)
        else:
            yield x

def flatten_stack(items):
    stack = [ iter(items) ]
    while stack:
        try:
            item = next(stack[-1])
            if isinstance(item, list):
                stack.append(iter(item))
            else:
                yield item
        except StopIteration:
            stack.pop()


linear_list = ['a', 'b', 'c', 'd']
nested2 = ['a', [1, 2], 'c', 'd']
nested_list = [1, 2,
               ['a',
                ['a1', 'a2',
                 ['a2_1', 'a2_2', 'a2_3'], 'a3'],
                'b', 'c'],
               123.8, 256.2]

if __name__ == '__main__':
    print('*** nested2')
    for x in flatten(nested2):
        print(x, end=' ')
    print()
    print('*** nested_list')
    for x in flatten(nested_list):
        print(x, end=' ')
    print()
    print('*** flatten_stack')
    for x in flatten_stack(nested_list):
        print(x, end=' ')
    print()

    
