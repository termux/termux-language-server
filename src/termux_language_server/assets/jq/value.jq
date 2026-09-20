$nodes[0].type as $type |
if $cursor[1] == 0 or $type == "variable_name" or ($type == "word" and $nodes[1].type == "function_definition") then
  .properties + (
      if .patternProperties == null or .patternProperties == {}
      then
        {}
      else
        (.patternProperties | to_entries[] | {(.key | gsub("[$^]"; "") | gsub("[(][^)]*[)]"; "")): .value})
      end
    ) | to_entries[]
# https://github.com/termux/termux-packages/wiki/Auto-updating-packages#auto-update-steps-refrence
elif $type == "word" and $nodes[1].type == "command_name" and .propertyNames != null then
  (
    .propertyNames.not.anyOf[] |
      if .const | test("^[a-z_]+$") then
        {key: .const, value: {description: .description}}
      else
        empty
      end
  )
else
  empty
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
