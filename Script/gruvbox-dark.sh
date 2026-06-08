#bin/bash
# Gruvbox-dark Theme Swapper

cp -r ~/dotfiles-swapper/Gruvbox-dark/config/dunst ~/.config
cp -r ~/dotfiles-swapper/Gruvbox-dark/config/vesktop/themes  ~/.config/vesktop
cp -r ~/dotfiles-swapper/Gruvbox-dark/config/alacritty/. ~/.config/alacritty
cp -r ~/dotfiles-swapper/Gruvbox-dark/config/waybar  ~/.config
cp -r ~/dotfiles-swapper/Gruvbox-dark/gtk/. ~/.themes
cp -r ~/dotfiles-swapper/Gruvbox-dark/icons/. ~/.icons
cp -r ~/dotfiles-swapper/Gruvbox-dark/config/spicetify/Themes/. ~/.config/spicetify/Themes
cp -r ~/dotfiles-swapper/Gruvbox-dark/Wallpapers ~/
sudo cp -r ~/dotfiles-swapper/Gruvbox-dark/config/rofi/. /usr/share/rofi/themes
cp -r ~/dotfiles-swapper/Gruvbox-dark/config/hypr/. ~/.config/hypr
gsettings set org.gnome.desktop.interface icon-theme "oomox-Gruvbox-Dark"
gsettings set org.gnome.desktop.interface gtk-theme "Gruvbox-Dark-Gruvbox"
spicetify config current_theme text
spicetify config color_scheme gruvboxhard
spicetify apply
killall dunst && dunst &
killall waybar && waybar &
killall hyprpaper && hyprpaper &
