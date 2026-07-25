$nodes[0].type as $type |
if $cursor[1] == 0 or $type == "variable_name" or ($type == "word" and $nodes[1].text == "function_definition") then
  .properties + (.patternProperties | to_entries[] | {(.key | gsub("[$^]"; "") | gsub("[(][^)]*[)]"; "")): .value})
else
  {}
end | to_entries[] |
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
