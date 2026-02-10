1. Add auto-detecting of file-type (.lua, .py, etc.)
   - [x] Check it from vim.bo.filetype
   - [x] Save to "file_type" variable
   - [x] If filetype is python = call plugin/pip_install.py, or if lua - call `luarocks install {package_name}`
2. [x] Replace `prints` to vim.notify for better UI and just visual enjoyment

---

1. Add supporting:
   - [x] **Lua** (`luarocks install ...`)
   - [x] **Rust** (`cargo add ...`)
   - [x] _Node.js_ (`npm install ...`)

---

1. - [x] **Optimize code**

---

New point (20.10.2025, 10:47):

1. - [x] **Create a option for installing requirements from files (Applyable for Cargo, Python)** by adding new command. End result - `:LazyDevInstallRequirements` (Done in 21.10.2025)
2. - [ ] Add an optional donation (only optional, i don`t push) on 2000 download in vim.org and in 10 stars in GitHub.

---

New points (24.10.2025, 10:08):

- [x] **Create a some.. Big update as for python installing libs** (_not python/requirements_installers/_\_req_install, but some file in python/ dir\*) (i mean - Ruby-gems installer)

---

New point (01.11.2025, 13:25):

- [x] **Add a flag -silent into** `:LazyDevInstall` **for quiet installing** (Done: 50% (in 07.11 - added rust and pip packages, remain - npm, luarocks))
      (UPD 18:44 (6:44 PM): Done both remained languages, all working)

---

28.11.2025, 10:23:

- [x] Add C++, C# support
- [x] Add Java support (by gradle + MavenCentral)
- [x] Add Go Support (08.02.2026 - idk when tf i did it, but for now - queue of this project to develop)

---

10.02.2026, 8:50:

- [ ] Add Dart support
