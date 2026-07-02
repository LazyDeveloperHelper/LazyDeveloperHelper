local M = {}

function M.register()
    vim.api.nvim_create_user_command("LazyDevInstallRequirements", function()
        local lang = vim.api.nvim_buf_get_option(0, "filetype")
        local config_path = vim.fn.stdpath("config") .. "/lua/LazyDeveloperHelper/lua/LazyDeveloperHelper/python/"
        local installers = {
            python = "requirements_installers/pip_req_installer.py",
            rust = "requirements_installers/cargo_req_installer.py",
        }

        local script_name = installers[lang]
        if not script_name then
            vim.notify("❌ No installer configured for filetype: " .. lang, vim.log.levels.WARN)
            return
        end

        local script_path = config_path .. script_name
        local env_map = vim.fn.environ()
        local python_path = config_path
        if env_map.PYTHONPATH and env_map.PYTHONPATH ~= "" then
            python_path = python_path .. ":" .. env_map.PYTHONPATH
        end
        local env = { "PYTHONPATH=" .. python_path }
        for k, v in pairs(env_map) do
            if k ~= "PYTHONPATH" then
                table.insert(env, k .. "=" .. v)
            end
        end

        -- arguments is not important, Cargo.toml searching the python script
        local args = {}

        local stdout = vim.loop.new_pipe(false)
        local stderr = vim.loop.new_pipe(false)

        vim.notify("📦 Installing dependencies for " .. lang)

        local handle
        handle = vim.loop.spawn("python3", {
            args = { script_path, unpack(args) },
            stdio = { nil, stdout, stderr },
            env = env,
        }, function(code)
            stdout:read_stop()
            stderr:read_stop()
            stdout:close()
            stderr:close()
            handle:close()

            vim.schedule(function()
                if code == 0 then
                    vim.notify("✅ All dependencies installed successfully")
                else
                    vim.notify("❌ Dependencies installation failed (code: " .. code .. ")", vim.log.levels.ERROR)
                end
            end)
        end)

        stdout:read_start(function(err, data)
            if data then
                vim.schedule(function()
                    vim.notify(data, vim.log.levels.INFO)
                end)
            end
        end)

        stderr:read_start(function(err, data)
            if data then
                vim.schedule(function()
                    vim.notify(data, vim.log.levels.ERROR)
                end)
            end
        end)
    end, {})
end

return M
