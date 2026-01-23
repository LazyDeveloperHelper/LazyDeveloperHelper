local M = {}

function M.register()
    vim.api.nvim_create_user_command("LazyDevInstall", function(opts)
        local fargs = vim.deepcopy(opts.fargs)
        local flag = false
        local lang = vim.api.nvim_buf_get_option(0, "filetype")

        -- Parse flags
        for i = #fargs, 1, -1 do
            if fargs[i] == "--quiet" or fargs[i] == "-q" then
                flag = true
                table.remove(fargs, i)
                break
            end
        end
        local args = fargs
        if #args == 0 then
            vim.notify("❌ You must specify at least one library!", vim.log.levels.ERROR)
            return
        end

        vim.notify("Detected filetype: " .. lang, vim.log.levels.INFO)

        local installers = {
            python = "pip_install.py",
            lua = "luarocks_install.py",
            rust = "cargo_install.py",
            javascript = "npm_install.py",
            ruby = "ruby_gem_install.py",
            kotlin = "java_installer/gradle_install.py",
            go = "go_installer/go_installer.py",
        }

        if lang == "c" or lang == "cpp" then
            vim.ui.select({
                { label = "📦 vcpkg (C/C++)", value = "c_installers/vcpkg_install.py" },
                { label = "🐍 Conan (C/C++)", value = "c_installers/conan_install.py" },
                { label = "🔧 NuGet (C#)", value = "c_installers/nuget_install.py" },
            }, {
                prompt = "Select C/C++ package manager:",
                format_item = function(item) -- Fixed: table:0x bug (was on local tests)
                    return item.label
                end,
            }, function(choice)
                if choice and choice.value then
                    execute_installs(choice.value, args, flag, "cpp")
                else
                    vim.notify("❌ Selection cancelled", vim.log.levels.WARN)
                end
            end)
            return
        end

        local script_name = installers[lang]
        if not script_name then
            vim.notify("❌ No installer for: " .. lang, vim.log.levels.WARN)
            return
        end

        execute_installs(script_name, args, flag, lang)
    end, { nargs = "+" })

    function execute_installs(script_name, args, flag, lang)
        local function get_plugin_python_path()
            local runtime_paths = vim.api.nvim_list_runtime_paths()
            for _, path in ipairs(runtime_paths) do
                if path:match("LazyDeveloperHelper") then
                    return path .. "/lua/LazyDeveloperHelper/python/"
                end
            end
            vim.notify("❌ LazyDeveloperHelper path not found!", vim.log.levels.ERROR)
            return nil
        end

        local python_dir = get_plugin_python_path()
        if not python_dir then
            return
        end

        local script_path = python_dir .. script_name
        local current_dir = vim.fn.expand("%:p:h")

        local function execute_install(lib)
            vim.notify("📦 Installing: " .. lib, vim.log.levels.INFO)

            local cmd_args = { script_path, lib }
            if flag then
                table.insert(cmd_args, lang == "python" and "--quiet" or "-q")
            end

            vim.system(cmd_args, {
                cwd = current_dir,
                stdout = function(err, data)
                    if data then
                        vim.schedule(function()
                            vim.api.nvim_echo({ { data, "Normal" } }, false, {})
                        end)
                    end
                end,
                stderr = function(err, data)
                    if data then
                        vim.schedule(function()
                            vim.api.nvim_echo({ { data, "ErrorMsg" } }, false, {})
                        end)
                    end
                end,
            }, function(obj)
                vim.schedule(function()
                    if obj.code == 0 then
                        vim.notify("✅ Installed: " .. lib, vim.log.levels.INFO)
                    else
                        vim.notify("❌ Failed: " .. lib .. " (code " .. obj.code .. ")", vim.log.levels.ERROR)
                    end
                end)
            end)
        end
        for _, lib in ipairs(args) do
            execute_install(lib)
        end
    end
end

return M
