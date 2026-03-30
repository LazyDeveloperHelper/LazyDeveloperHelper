local M = {}

function M.register()
    vim.api.nvim_create_user_command("IsWorking", function()
        print("Yep!")
        print("Command executed successfully")
    end, {})

    vim.api.nvim_create_user_command("HellPip", function()
        print("Need help? Thats for u: ")
        print("Commands: \n:IsWorking - for check plugin status\n")
        print(
            ":LazyDevInstall (if u wanna write -silent) {lib_names (can be multiply)} - \nwell.. main functional, maybe"
        )
    end, {})
end
return M
