if $cursor[1] == 0 or $type == "variable_name" or ($type == "word" and $texts[0] == "function_definition") then
  .properties + (.patternProperties | to_entries[] | {(.key | gsub("[$^]"; "") | gsub("[(][^)]*[)]"; "")): .value})
else
  {}
end | to_entries[] |
if .key | (if $complete then startswith($text) else . == $text end) then
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
