
# Dotfiles Theme Switcher

A theme switcher i made for hyprland. It changes the GTK theme as well as themes for multiple applications.

currently only has the TokyoNight theme and the Gruvbox-Dark theme.


# Screenshots

## Gruvbox-Dark
![Gruvbox-Dark](https://github.com/ckznnn/dotfiles-swapper/blob/main/Gruvbox-Dark-Preview.png?raw=true)

## TokyoNight
![TokyoNight](https://github.com/ckznnn/dotfiles-swapper/blob/main/TokyoNIght-Preview.png?raw=true)


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
  nemo
```


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


# Usage

### Make sure to launch Vesktop and do spicetifty backup_apply before you use the script

### As well as adding hyprpaper and waybar to your auto start in your hyprland config

### Backup your hyprland.lua as the script replaces it




## Make Zen-Browser theme work

```bash
  about:config # Enter into search bar in zen
```
```bash
  toolkit.legacyUserProfileCustomizations.stylesheets # Search for this and toggle on
```

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
## After running select your theme in discord as well as selecting "master.rasi" theme within the rofi theme selector (You only need to do this on first activation)

## Demo

Pick number between 1-4 to activate the theme.

![demo](https://github.com/ckznnn/dotfiles-swapper/blob/main/Script-Preview.png?raw=true)


# DISCLAIMER
# Whilst testing this i ran into a an issue with dolphin i highly suggest swapping your file manager to nemo to avoid issues
