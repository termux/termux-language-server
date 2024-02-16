(
 (variable_assignment
   name: (variable_name) @variable.name
   )
 (#match?
  @variable.name "^(mingw|msys2)_"
  )
 )
