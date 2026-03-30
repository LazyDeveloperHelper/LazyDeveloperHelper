local M = {}

local general = require("LazyDeveloperHelper.commands.general")
local install = require("LazyDeveloperHelper.commands.install")
local requirements = require("LazyDeveloperHelper.commands.install_requirements")
local donations = require("LazyDeveloperHelper.commands.donation")

function M.setup()
    general.register()
    install.register()
    requirements.register()
    donations.register()
end

return M
