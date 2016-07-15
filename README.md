Generatie JSDoc Function Documentation
======================================

This plugin provides a means of automatically generating a JavaScript function documentation block in the JSDoc style. While in insert mode and on the line immediately preceding a JS function, use a key command (customizable) to generate the documentation block. The function signiture will be analized and used to generate the documentation.

Dependencies
============

# UltiSnips

The UltiSnips plugin is used to create tab stops that can be cycled through just like a regular UltiSnips snippet. Some of the tab stops will be filled in with appropriate values, such as data type or parameter name, if they can be determined from the function signeture. In cases where this is not possible, simply overwrite the default value as needed using UltiSnips functionality.

# Python

The script that is use to generate the resulting documentation block is written in python so you must have python available somewhere on your path in order for this plugin to work.

Customization
=============

You must provide a insert mode key map to enable to command:

`let g:generateJSDocFuncDocKeyMap = '<C-F>'`
