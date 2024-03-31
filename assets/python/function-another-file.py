import importlib.util

function_file_path = '/path-of-file'
input_value = 'input content'
spec = importlib.util.spec_from_file_location("function_file", function_file_path)
function_file = importlib.util.module_from_spec(spec)
spec.loader.exec_module(function_file)

output_value = function_file.function_name(input_value)
print("Output value:", output_value)