(variable_assignment
  name: (variable_name) @--name
  value: (word) @-name)

(variable_assignment
  name: (variable_name) @--name
  value: (raw_string) @-name.--shlex)

(variable_assignment
  name: (variable_name) @--name
  value: (string) @-name.--shlex)

(variable_assignment
  name: (variable_name) @--name
  value: (concatenation) @-name.--shlex)

(variable_assignment
  name: (variable_name) @--name
  value: (array
    (word) @-name.--))

(variable_assignment
  name: (variable_name) @--name
  value: (array
    (raw_string) @-name.--.--shlex))

(variable_assignment
  name: (variable_name) @--name
  value: (array
    (string) @-name.--.--shlex))

(variable_assignment
  name: (variable_name) @--name
  value: (array
    (concatenation) @-name.--.--shlex))

(function_definition
  name: (word) @--function
  (#set! -function.--integer 0))
