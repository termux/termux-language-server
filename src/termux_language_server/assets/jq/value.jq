$nodes[0].type as $type |
# https://github.com/termux/termux-packages/wiki/Auto-updating-packages#auto-update-steps-refrence
if $type == "word" and $nodes[1].type == "command_name" then
  (
    if .propertyNames == null
    then
      {}
    else
      .propertyNames.not.anyOf[] |
        if .const | test("^[a-z_]+$") then
          {key: .const, value: {description: .description}}
        else
          empty
        end
    end
  )
else
  (
    if $cursor[1] == 0 or $type == "variable_name" or ($type == "word" and $nodes[1].type == "function_definition") then
      .properties + (
          if .patternProperties == null
          then
            {}
          else
            (.patternProperties | to_entries[] | {(.key | gsub("[$^]"; "") | gsub("[(][^)]*[)]"; "")): .value})
          end
        )
    else
      {}
    end | to_entries[]
  )
end |
if .key | ($nodes[0].text as $text | if $complete then startswith($text) else . == $text end) then
  {
    label: .key,
    insert_text: .key,
    kind: (
      if $type == "variable_name" then
        $enums.CompletionItemKind.Variable
      elif $type == "word" then
        $enums.CompletionItemKind.Function
      else
        $enums.CompletionItemKind.Constant
      end
    ),
    documentation: {kind: "markdown", value: .value.description}
  }
else
  empty
end
