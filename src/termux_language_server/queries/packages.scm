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
      (string_content) @package.PKGBUILD) @_string)
  (#not-match? @_string "[$]")
  (#any-of? @_name "depends" "makedepends" "optdepends" "conflicts" "provides" "replaces"))

(variable_assignment
  name: (variable_name) @_name
  value: (string
    (string_content) @package._ebuild)
  (#match? @package._ebuild "/")
  (#any-of? @_name "DEPEND" "RDEPEND" "BDEPEND" "IDEPEND" "PDEPEND"))

; TODO: should we match command_name by lua_gen_cond_dep?
; DEPEND="${LUA_DEPS}
; 	$(lua_gen_cond_dep "
; 		dev-lua/lpeg[${LUA_USEDEP}]
; 		dev-lua/mpack[${LUA_USEDEP}]
; 	")
; "
(variable_assignment
  name: (variable_name) @_name
  value: (string
    (command_substitution
      (command
        argument: (string
          (string_content) @package._ebuild))))
  (#match? @package._ebuild "/")
  (#any-of? @_name "DEPEND" "RDEPEND" "BDEPEND" "IDEPEND" "PDEPEND"))
