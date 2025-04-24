-- example.lua
-- Basic function
function add(a, b)
    return a + b
end

-- Local variable declaration
local x = 10
local y = "hello"

-- Conditional statement
if x > 5 then
    print(y)
else
    print("x is too small")
end

-- Table example
local my_table = {
    name = "Lua",
    version = 5.4,
    features = {"tables", "coroutines", "metatables"}
}

-- Loop example
for i = 1, 5 do
    print("Count:", i)
end

-- Function with table parameter
function print_table(t)
    for k, v in pairs(t) do
        print(k, "=", v)
    end
end

-- Test different Lua features
local t = {1, 2, 3, key="value"}
local function closure(x)
    return function(y) return x + y end
end

print("Tokens:", json.dumps(tokenizer.tokens[:5], indent=2))

print_table(my_table)