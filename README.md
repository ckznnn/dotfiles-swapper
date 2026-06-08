
# Dotfiles Theme Switcher

A theme switcher i made for hyprland. It changes the GTK theme as well as themes for multiple applications.


# Screenshots

## Gruvbox-Dark
![Gruvbox-Dark](https://github.com/ckznnn/dotfiles-swapper/blob/main/Gruvbox-Dark-Preview.png?raw=true)


## Installation

Clone the repo (Install to home ~/)

```bash
  git clone https://github.com/ckznnn/dotfiles-swapper.git
```
## Install Dependancies:

If you aren't on arch linux the install script wont work. Install these dependancies:
```bash
  waybar
  dunst
  spotify
  spicetify
  alacritty
  hyprpaper
  rofi
  vesktop
```

## Make sure to launch Vesktop and do spicetifty backup_apply before you use the script

## Using Install script for arch

change directory to repo

```bash
  cd dotfiles-swapper 
```
make script executable

```bash
 chmod +x install-dependancies.sh 
```
execute script


```bash
  ./install-dependancies.sh 
```
## Features

- Four different themes (Gruvbox-Dark, Gruvbox-Light, Everforest-dark and TokyoNight)
- Theming for different applications (Discord, Alacritty, Spotify, GTK, Icons, Notifications, Waybar, Rofi)
- Included Wallpapers as well as Wallpaper switcher.


## Usage

To use this project first make the script executable

```bash
  cd Script
```
```bash
  chmod +x gruvbox-dark.sh
  chmod +x tokyonight.sh
  chmod +x gruvbox-light.sh
  chmod +x everforest-dark.sh
```
Then make the master script executable

```bash
  cd ..
```
```bash
  chmod +x theme-switcher.sh
```
 
Finally execute the script

```bash
  ./theme-switcher.sh
```
## Demo

Pick number between 1-4 to activate the theme.

![demo](https://github.com/ckznnn/dotfiles-swapper/blob/main/Script-Preview.png?raw=true)

