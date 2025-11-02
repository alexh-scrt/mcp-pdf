# Oh My Zsh Customization Quick Guide

## Installation (run on your local machine)
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## Key Files & Directories

- `~/.zshrc` - Main configuration file (edit this!)
- `~/.oh-my-zsh/` - Oh My Zsh installation
- `~/.oh-my-zsh/themes/` - Built-in themes
- `~/.oh-my-zsh/plugins/` - Built-in plugins
- `~/.oh-my-zsh/custom/` - Your custom themes/plugins

## Quick Customization Steps

### 1. Change Theme
Edit `~/.zshrc`:
```bash
ZSH_THEME="agnoster"  # or any theme name
```

Popular themes:
- `robbyrussell` - Default, minimal
- `agnoster` - Powerline style (needs fonts)
- `af-magic` - Shows git info nicely
- `bira` - Two-line, clean
- `bureau` - Detailed, shows git and time

### 2. Add Plugins
Edit the plugins line in `~/.zshrc`:
```bash
plugins=(
  git
  python
  golang
  rust
  docker
  kubectl
  sudo
  extract
)
```

### 3. Add Custom Aliases
Add to the bottom of `~/.zshrc`:
```bash
alias py='python3'
alias gst='git status'
alias ll='ls -lah'
```

### 4. Apply Changes
```bash
source ~/.zshrc
# or just restart your terminal
```

## Essential Plugins for Your Work

### Python Development
```bash
plugins=(
  python          # Python aliases
  pip             # Pip completion
  virtualenv      # Virtualenv support
  poetry          # Poetry completion
)
```

### Go Development
```bash
plugins=(
  golang          # Go completion and aliases
)
```

### Rust Development
```bash
plugins=(
  rust            # Rust completion and aliases
  cargo           # Cargo completion
)
```

### General Development
```bash
plugins=(
  git             # Git aliases (gst, gco, etc.)
  docker          # Docker completion
  vscode          # VS Code integration
  sudo            # ESC ESC to add sudo
  extract         # Smart extract for any archive
  command-not-found # Suggests packages
  colored-man-pages # Pretty man pages
)
```

## Must-Have External Plugins

### 1. zsh-autosuggestions
```bash
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```
Add to plugins: `zsh-autosuggestions`

### 2. zsh-syntax-highlighting
```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```
Add to plugins: `zsh-syntax-highlighting`

### 3. fzf (fuzzy finder)
```bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

## Best Themes for Developers

### Powerlevel10k (Most Popular)
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```
Set in `.zshrc`: `ZSH_THEME="powerlevel10k/powerlevel10k"`
Run: `p10k configure` to customize

### Spaceship (Modern)
```bash
git clone https://github.com/spaceship-prompt/spaceship-prompt.git \
  "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" \
  "$ZSH_CUSTOM/themes/spaceship.zsh-theme"
```
Set in `.zshrc`: `ZSH_THEME="spaceship"`

## Useful Git Aliases (from git plugin)

- `gst` = `git status`
- `ga` = `git add`
- `gc` = `git commit`
- `gco` = `git checkout`
- `gp` = `git push`
- `gl` = `git pull`
- `gd` = `git diff`
- `glog` = `git log --oneline --decorate --graph`
- `gcb` = `git checkout -b` (new branch)

## Custom Functions Example

Add to `~/.zshrc`:
```bash
# Create and enter directory
mkcd() {
  mkdir -p "$1" && cd "$1"
}

# Activate Python venv
va() {
  if [ -d "venv" ]; then
    source venv/bin/activate
  elif [ -d ".venv" ]; then
    source .venv/bin/activate
  fi
}

# Git commit with message
gcm() {
  git commit -m "$*"
}
```

## Troubleshooting

### Plugins not working?
```bash
# Make sure you sourced the config
source ~/.zshrc

# Check plugin exists
ls ~/.oh-my-zsh/plugins/ | grep plugin-name
```

### Theme looks broken?
```bash
# Some themes need special fonts (Powerline/Nerd Fonts)
# Install from: https://github.com/ryanoasis/nerd-fonts

# Or use a simple theme
ZSH_THEME="robbyrussell"
```

### Slow startup?
```bash
# Disable plugins you don't use
# Comment out in ~/.zshrc:
plugins=(
  git
  # docker  # commented out
)
```

## Update Oh My Zsh
```bash
omz update
```

## Get Help
```bash
# List all commands
omz --help

# List all plugins
ls ~/.oh-my-zsh/plugins/

# List all themes
ls ~/.oh-my-zsh/themes/
```