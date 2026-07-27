(variable_assignment
  name: (variable_name) @_name
  value: (array
    (word) @package.PKGBUILD)
  (#any-of? @_name "depends" "makedepends" "optdepends" "conflicts" "provides" "replaces"))

(variable_assignment
  name: (variable_name) @_name
  value: (array
    (raw_string) @package.PKGBUILD)
  (#any-of? @_name "depends" "makedepends" "optdepends" "conflicts" "provides" "replaces"))

(variable_assignment
  name: (variable_name) @_name
  value: (array
    (string
      (string_content) @package.PKGBUILD))
  (#any-of? @_name "depends" "makedepends" "optdepends" "conflicts" "provides" "replaces"))

(variable_assignment
  name: (variable_name) @_name
  value: (string
    (string_content) @package._ebuild)
  (#any-of? @_name "DEPEND" "RDEPEND" "BDEPEND" "IDEPEND" "PDEPEND"))
