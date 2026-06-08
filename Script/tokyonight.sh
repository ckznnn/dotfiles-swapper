#bin/bash
# TokyoNight Theme Swapper

cp -r ~/dotfiles-swapper/ToykoNight/config/dunst ~/.config
cp -r ~/dotfiles-swapper/ToykoNight/config/vesktop/themes  ~/.config/vesktop
cp -r ~/dotfiles-swapper/ToykoNight/config/alacritty/. ~/.config/alacritty
cp -r ~/dotfiles-swapper/ToykoNight/config/waybar  ~/.config
cp -r ~/dotfiles-swapper/ToykoNight/gtk/. ~/.themes
cp -r ~/dotfiles-swapper/ToykoNight/icons/. ~/.icons
cp -r ~/dotfiles-swapper/ToykoNight/config/spicetify/Themes/. ~/.config/spicetify/Themes
cp -r ~/dotfiles-swapper/ToykoNight/Wallpapers ~/
sudo cp -r ~/dotfiles-swapper/ToykoNight/config/rofi/. /usr/share/rofi/themes
cp -r ~/dotfiles-swapper/ToykoNight/config/hypr/. ~/.config/hypr
gsettings set org.gnome.desktop.interface icon-theme "Tokyonight-Dark"
gsettings set org.gnome.desktop.interface gtk-theme "Tokyonight-Dark"
spicetify config current_theme text
spicetify config color_scheme tokyonight
spicetify apply
killall dunst && dunst &
killall waybar && waybar &
killall hyprpaper && hyprpaper &
