(
 (variable_assignment
   name: (variable_name) @variable.name
   value: (array (word) @package)
   )
 (#match?
  @variable.name "^(depends|optdepends|makedepends|conflicts|provides)$"
  )
 )
