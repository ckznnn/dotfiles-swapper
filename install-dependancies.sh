#!/bin/bash

pacman_deps=(
	waybar
	dunst
	spotify-launcher	
	alacritty
	hyprpaper
	rofi
)

aur_deps=(
	vesktop
	spicetify-cli
)


sudo pacman -S --noconfirm --needed "${pacman_deps[@]}"
yay -S --noconfirm --needed "${aur_deps[@]}"
