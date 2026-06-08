#bin/bash
# TokyoNight Theme Swapper

cp -r ~/dotfiles/ToykoNight/.config/dunst ~/.config
cp -r ~/dotfiles/ToykoNight/.config/vesktop/themes  ~/.config/vesktop
cp -r ~/dotfiles/ToykoNight/.config/alacritty/. ~/.config/alacritty
cp -r ~/dotfiles/ToykoNight/.config/waybar  ~/.config
cp -r ~/dotfiles/ToykoNight/gtk/. ~/.themes
cp -r ~/dotfiles/ToykoNight/icons/. ~/.icons
cp -r ~/dotfiles/ToykoNight/.config/spicetify/Themes/. ~/.config/spicetify/Themes
cp -r ~/dotfiles/ToykoNight/Wallpapers ~/
sudo cp -r ~/dotfiles/ToykoNight/.config/rofi/. /usr/share/rofi/themes
cp -r ~/dotfiles/ToykoNight/.config/hypr/. ~/.config/hypr
gsettings set org.gnome.desktop.interface icon-theme "Tokyonight-Dark"
gsettings set org.gnome.desktop.interface gtk-theme "Tokyonight-Dark"
spicetify config current_theme text
spicetify config color_scheme tokyonight
spicetify apply
killall dunst && dunst &
killall waybar && waybar &
killall hyprpaper && hyprpaper &
