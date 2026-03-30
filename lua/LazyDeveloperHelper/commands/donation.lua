M = {}

function M.register()
    vim.api.nvim_create_user_command("LazyDevDonation", function()
        vim.ui.select({
            {
                label = "📦 USDT (TRC-20)",
                value = "TRC20",
            },
            {
                label = "🐍 Monobank (USD/Other → UAH, by QR)",
                value = "https://send.monobank.ua/jar/23KvyLvxaj",
            },
        }, {
            prompt = "Select donation method:",
            format_item = function(item)
                return item.label
            end,
        }, function(choice)
            if not choice then
                vim.notify("❌ Selection cancelled", vim.log.levels.WARN)
                return
            end

            if choice.value == "TRC20" then
                vim.notify("Address copied to clipboard!", vim.log.levels.INFO)
                vim.fn.setreg("+", "TRY3MuM5rzyzGoLxXr9wFeMs38o8AyMDUj")
                vim.notify(
                    "Address to TRC-20: TRY3MuM5rzyzGoLxXr9wFeMs38o8AyMDUj\n(ONLY TRC-20 (TRON), srry no other networks)",
                    vim.log.levels.INFO
                )
            elseif type(choice.value) == "string" and choice.value:match("^https?://") then
                vim.fn.jobstart({ "xdg-open", choice.value })
                vim.notify("Opening Monobank link...", vim.log.levels.INFO)
            else
                vim.notify("❌ Unknown choice", vim.log.levels.WARN)
            end
        end)
    end, {})
end

return M
