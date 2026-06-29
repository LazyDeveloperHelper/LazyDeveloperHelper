<h1 align="center">💫 Lazy Developer Helper</h1>
<p align="center">
  <img src="./images/neovim_logotype/neovim-logotype.png" alt="Neovim Logo" width="200" /><br>
  <b>Image from: <a href="https://github.com/vyfor/cord.nvim">vyfor/cord.nvim</a></b>
</p>

<p align="center">
  Automation tools for lazy developers.<br/>
  <i>Less routine, more coding!</i>
</p>

<p align="center">
  <a href="https://github.com/LazyDeveloperHelper/LazyDeveloperHelper/stargazers">
    <img src="https://img.shields.io/github/stars/LazyDeveloperHelper/LazyDeveloperHelper?style=for-the-badge&logo=neovim&logoColor=8281f3&color=8281f3&labelColor=242529" alt="GitHub Stars"/>
  </a>
  <a href="https://neovim.io/">
    <img src="https://img.shields.io/badge/Neovim-%3E%3D%200.11.5-ffffff?style=for-the-badge&logo=neovim&color=8281f3&labelColor=242529&logoColor=8281f3" alt="Neovim">
  </a>
  <a href="https://github.com/LazyDeveloperHelper/LazyDeveloperHelper/network/members">
    <img src="https://img.shields.io/github/forks/LazyDeveloperHelper/LazyDeveloperHelper?style=for-the-badge&color=8281f3&labelColor=242529" alt="Forks">
  </a><br>
  <img src="https://img.shields.io/github/license/LazyDeveloperHelper/LazyDeveloperHelper?style=for-the-badge&color=8281f3&labelColor=242529" alt="License" />
  <img src="https://img.shields.io/github/last-commit/LazyDeveloperHelper/LazyDeveloperHelper?style=for-the-badge&color=8281f3&labelColor=242529" alt="Last Commit" />
  <a href="https://discord.gg/QnthFV3Zgp">
    <img src="https://img.shields.io/badge/Discord-Join-8281f3?style=for-the-badge&logo=discord&logoColor=white&labelColor=242529" alt="Discord" />
  </a>
</p>

<p align="center">
  <strong>Supported Languages:</strong><br/>
  <img src="https://img.shields.io/badge/Lua-2C2D72?style=for-the-badge&logo=lua&logoColor=white" alt="Lua" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust" />
  <img src="https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white" alt="Ruby" />
  <img src="https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=black" alt="C" />
  <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Golang" />
  <img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white" alt="Dart" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
</p>

<p align="center">
  <strong>Supported Package Managers:</strong><br/>
  <img src="https://img.shields.io/badge/pip-3776AB?style=for-the-badge&logo=pypi&logoColor=white" alt="pip" />
  <img src="https://img.shields.io/badge/poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white" alt="Poetry" />
  <img src="https://img.shields.io/badge/Cargo-DEA584?style=for-the-badge&logo=rust&logoColor=black" alt="Cargo" />
  <img src="https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white" alt="npm" />
  <img src="https://img.shields.io/badge/Gem-990000?style=for-the-badge&logo=rubygems&logoColor=white" alt="RubyGems" />
  <img src="https://img.shields.io/badge/Luarocks-2C2D72?style=for-the-badge&logo=lua&logoColor=white" alt="Luarocks" />
  <img src="https://img.shields.io/badge/Conan-66C2A5?style=for-the-badge&logo=conan&logoColor=white" alt="Conan" />
  <img src="https://img.shields.io/badge/NuGet-512BD4?style=for-the-badge&logo=nuget&logoColor=white" alt="NuGet" />
  <img src="https://img.shields.io/badge/Gradle-02303A?style=for-the-badge&logo=gradle&logoColor=white" alt="Gradle" />
  <img src="https://img.shields.io/badge/go%20install-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="go install" />
  <img src="https://img.shields.io/badge/dart-0175C2?style=for-the-badge&logo=dart&logoColor=white" alt="Dart CLI" />
</p>

---

## Contents

<!-- toc -->

- [Video example](#video-example)
- [Introduction](#introduction)
- [Features](#features)
- [Available Commands](#available-commands)
- [Roadmap](#roadmap)
- [Available in](#available-in)
- [Installation Methods](#installation-methods)
	* [Install using Packer](#install-using-packer)
	* [Install using Lazy](#install-using-lazy)
- [Usage](#usage)
- [How to Support Me](#how-to-support-me)
- [Plugin History](#plugin-history)

<!-- tocstop -->

## Video example

> [!IMPORTANT]
> GitHub can't handle this file directly, and I don't want to drop quality (well.. sometimes xD) or FPS — so here's the link:

<a href="https://youtu.be/pH86IEqpqAk" target="_blank">
  <img src="https://img.youtube.com/vi/pH86IEqpqAk/0.jpg" alt="Example video" />
</a>

## Introduction

_Have you ever found yourself adding multiple dependencies to your code before installing them?_ **Do you hate switching between your editor and terminal just to install libs?** 🤔

**LazyDeveloperHelper solves this problem!** It's a Neovim plugin that lets you manage dependencies for:

- _Python_ — via `pip` / `poetry`
- _Rust_ — via `Cargo`
- _Kotlin / Groovy_ — via `Gradle` + Maven Central
- _JavaScript_ — via `npm`
- _C++_ — via `NuGet` / `Conan` / `vcpkg` (`vim.ui.select` to pick between them)
- _C_ — via `Conan`
- _Ruby_ — via `gem`
- _Lua_ — via `luarocks`
- _Golang_ — via `go install`
- _Dart_ — via Dart CLI

...all directly from your editor. No terminal switching required.

Join the community on [Discord](https://discord.gg/QnthFV3Zgp)!

## Features

- ✨ Install packages for Python, Lua, JavaScript, Ruby, Rust, Kotlin, Go, Dart, C/C++ — without leaving Neovim
- ✨ Install from dependency files (`requirements.txt`, `Cargo.toml`) via `:LazyDevInstallRequirements`
- ✨ Quiet mode (`-q` / `--quiet`) to suppress output when you don't need the noise
- ✨ `vim.notify()` integration — tells you what's happening (or what broke)
- ✨ Compatible with modern Neovim configurations (>= 0.11.5)

## Available Commands

| Command | Description |
|---|---|
| `:LazyDevInstall {lib}` | Install a package for the current filetype |
| `:LazyDevInstall {lib} -q` | Install quietly (suppresses output, for few package managers)) |
| `:LazyDevInstallRequirements` | Install all deps from the corresponding file (Python, Rust) |
| `:LazyDevDonation` | Support the plugin if you want to |
| `:HellPip` | Help command, but make it ✨ styled ✨ |
| `:IsWorking` | Check that the plugin is loaded correctly |

## Roadmap

Want to see what's planned for 2026?
[Go to Roadmap.sh](https://roadmap.sh/r/lazydeveloperhelper-roadmap-for-2026-year)

## Available in

- [vim.org](https://www.vim.org/scripts/script.php?script_id=6156) — script ID 6156, rated 30/12, 2382+ downloads
- [dotfyle.com](https://dotfyle.com/plugins/Silletr/LazyDevHelper)
- [Awesome-Neovim](https://github.com/rockerBOO/awesome-neovim?tab=readme-ov-file#dependency-management)
- [Neovim Craft](https://neovimcraft.com/plugin/Silletr/LazyDeveloperHelper)
- [Store.nvim](https://store.nvim)
- [Dev.to](https://dev.to/silletr)
- [X.com](https://x.com/silletr)

[TrendShift.io](https://trendshift.io/repositories/23615)
## Installation Methods

### Install using Packer

```lua
use {
  'LazyDeveloperHelper/LazyDeveloperHelper',
  config = function()
    require("LazyDeveloperHelper").setup()
  end
}
```

Then run: `:PackerSync`

### Install using Lazy

```lua
return {
  "LazyDeveloperHelper/LazyDeveloperHelper",
  config = function()
    require("LazyDeveloperHelper").setup()
  end
}
```

Then run: `:Lazy sync`

## Usage

Command example:

![Command example](https://github.com/LazyDeveloperHelper/LazyDeveloperHelper/blob/ee3d4c47e690170a6ca3c28e523bdb035909ea6a/images/examples/command_example.png)

---

Example output:

![Installation Output](https://github.com/LazyDeveloperHelper/LazyDeveloperHelper/blob/d129a416c1f6a1273fdc077dff73bbd948757d6c/images/examples/output_example.png)

## How to Support Me

**If you want to support me — run `:LazyDevDonation` and pick a method that works for you.**

The plugin will **always stay free**. No paywalls, no locked features. Donations are purely optional and entirely up to you — but they do help keep the updates coming. Thanks to everyone who does! 🙏

## Plugin History

[Want to know the full story? Read the plugin history!](./PLUGIN_HISTORY.md)

![Repobeats analytics](https://repobeats.axiom.co/api/embed/91c0a59ebb003b31f4184cc769db134500a0fde8.svg "Repobeats analytics image")
